from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def allocate_rooms(groups_df, hostels_df):
    allocation = []
    hostels = hostels_df.groupby(['Hostel Name', 'Room Number', 'Gender']).apply(lambda x: x.to_dict('records')[0]).to_dict()

    for _, group in groups_df.iterrows():
        group_id = group['Group ID']
        members = group['Members']
        gender = group['Gender']
        
        if 'Boys' in gender and 'Girls' in gender:
            boys = int(gender.split()[0])
            girls = int(gender.split()[2])
            members_info = [('Boys', boys), ('Girls', girls)]
        else:
            members_info = [(gender, members)]

        for gender, members in members_info:
            for hostel_key, hostel in hostels.items():
                if hostel['Gender'] == gender and hostel['Capacity'] >= members:
                    allocation.append({
                        'Group ID': group_id,
                        'Hostel Name': hostel['Hostel Name'],
                        'Room Number': hostel['Room Number'],
                        'Members Allocated': members
                    })
                    hostel['Capacity'] -= members
                    break

    allocation_df = pd.DataFrame(allocation)
    allocation_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'allocation.csv'), index=False)
    return allocation_df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        groups_file = request.files['groups']
        hostels_file = request.files['hostels']

        if groups_file and hostels_file:
            groups_path = os.path.join(app.config['UPLOAD_FOLDER'], groups_file.filename)
            hostels_path = os.path.join(app.config['UPLOAD_FOLDER'], hostels_file.filename)
            groups_file.save(groups_path)
            hostels_file.save(hostels_path)

            groups_df = pd.read_csv(groups_path)
            hostels_df = pd.read_csv(hostels_path)

            allocation_df = allocate_rooms(groups_df, hostels_df)

            return render_template('index.html', tables=[allocation_df.to_html(classes='data')], titles=allocation_df.columns.values)
    
    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'allocation.csv'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
