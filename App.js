import React, { useState, useEffect } from 'react';
import axios from 'axios';
import socketIOClient from 'socket.io-client';

const ENDPOINT = "http://127.0.0.1:5000";

function App() {
  const [groups, setGroups] = useState([]);
  const [hostels, setHostels] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on("update", data => {
      setMessage(data.message);
    });

    return () => socket.disconnect();
  }, []);

  const handleGroupsUpload = async (e) => {
    const file = e.target.files[0];
    const data = new FormData();
    data.append('file', file);
    await axios.post(`${ENDPOINT}/upload-groups`, data);
  };

  const handleHostelsUpload = async (e) => {
    const file = e.target.files[0];
    const data = new FormData();
    data.append('file', file);
    await axios.post(`${ENDPOINT}/upload-hostels`, data);
  };

  return (
    <div className="App">
      <h1>Group Accommodation Allocation</h1>
      <input type="file" onChange={handleGroupsUpload} />
      <input type="file" onChange={handleHostelsUpload} />
      <p>{message}</p>
    </div>
  );
}

export default App;
