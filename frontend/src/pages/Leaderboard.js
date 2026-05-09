import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/analytics/leaderboard/');
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">🏆 Leaderboard</h2>
      
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-4 text-left">Rank</th>
              <th className="p-4 text-left">User</th>
              <th className="p-4 text-center">Win Rate</th>
              <th className="p-4 text-center">Profit Factor</th>
              <th className="p-4 text-center">Trades</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, idx) => (
              <tr key={entry.user_id} className="border-t border-gray-700 hover:bg-gray-700">
                <td className="p-4 font-bold text-yellow-400">#{idx + 1}</td>
                <td className="p-4">{entry.user_id}</td>
                <td className="p-4 text-center text-green-400">{entry.win_rate.toFixed(1)}%</td>
                <td className="p-4 text-center text-blue-400">{entry.profit_factor.toFixed(2)}</td>
                <td className="p-4 text-center">{entry.total_trades}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
