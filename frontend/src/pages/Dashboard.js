import React, { useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [userId, setUserId] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !userId) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      const response = await axios.post('http://localhost:8000/api/trades/upload_csv/', formData);
      alert(`Uploaded ${response.data.count} trades. Hash: ${response.data.hash}`);
    } catch (error) {
      alert('Upload failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">Upload Trade History</h2>
      <form onSubmit={handleUpload} className="bg-gray-800 p-6 rounded-lg">
        <div className="mb-4">
          <label className="block mb-2">User ID</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full bg-gray-700 p-2 rounded text-white"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">CSV File</label>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full bg-gray-700 p-2 rounded text-white"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-bold"
        >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}

export default Dashboard;
