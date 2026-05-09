import React, { useState } from 'react';
import axios from 'axios';

function RedFlags() {
  const [userId, setUserId] = useState('');
  const [flags, setFlags] = useState(null);

  const fetchRedFlags = async () => {
    if (!userId) return;
    try {
      const response = await axios.get(`http://localhost:8000/api/analytics/red_flags/?user_id=${userId}`);
      setFlags(response.data);
    } catch (error) {
      console.error('Failed to fetch red flags:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">🚩 Red Flags Detection</h2>
      
      <div className="mb-6 flex gap-4">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="flex-1 bg-gray-800 p-2 rounded text-white"
        />
        <button
          onClick={fetchRedFlags}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-bold"
        >
          Analyze
        </button>
      </div>

      {flags && (
        <div className="space-y-4">
          <div className="bg-red-900 p-4 rounded">
            <h3 className="font-bold mb-2">Revenge Trading</h3>
            <p>{flags.revenge_trading.length} instances detected</p>
          </div>
          <div className="bg-red-900 p-4 rounded">
            <h3 className="font-bold mb-2">High Drawdown</h3>
            <p>{flags.high_drawdown.length > 0 ? `Max: $${flags.high_drawdown[0]}` : 'None'}</p>
          </div>
          <div className="bg-yellow-900 p-4 rounded">
            <h3 className="font-bold mb-2">Session Analysis</h3>
            <p>Check analytics for session-specific win rates</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default RedFlags;
