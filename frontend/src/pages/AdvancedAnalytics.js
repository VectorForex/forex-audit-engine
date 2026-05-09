import React, { useState } from 'react';
import axios from 'axios';

function AdvancedAnalytics() {
  const [userId, setUserId] = useState('');
  const [advStats, setAdvStats] = useState(null);

  const fetchAdvancedStats = async () => {
    if (!userId) return;
    try {
      const response = await axios.get(
        `http://localhost:8000/api/analytics/advanced_stats/?user_id=${userId}`
      );
      setAdvStats(response.data);
    } catch (error) {
      console.error('Failed to fetch advanced stats:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">🔬 Advanced Analytics</h2>
      
      <div className="mb-6 flex gap-4">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="flex-1 bg-gray-800 p-2 rounded text-white"
        />
        <button
          onClick={fetchAdvancedStats}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-bold"
        >
          Analyze
        </button>
      </div>

      {advStats && (
        <>
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Sharpe Ratio</p>
              <p className="text-2xl font-bold text-blue-400">
                {advStats.sharpe_ratio.toFixed(2)}
              </p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Recovery Factor</p>
              <p className="text-2xl font-bold text-green-400">
                {advStats.recovery_factor.toFixed(2)}
              </p>
            </div>
          </div>

          <div className="bg-gray-800 p-6 rounded mb-8">
            <h3 className="text-xl font-bold mb-4">Time of Day Performance</h3>
            <div className="grid grid-cols-3 gap-4">
              {Object.entries(advStats.time_of_day).map(([session, data]) => (
                <div key={session} className="bg-gray-700 p-4 rounded">
                  <p className="font-semibold capitalize">{session}</p>
                  <p className="text-sm text-gray-400">Trades: {data.total}</p>
                  <p className="text-lg font-bold text-green-400">
                    {data.win_rate.toFixed(1)}%
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-800 p-6 rounded">
            <h3 className="text-xl font-bold mb-4">Best Performing Setups</h3>
            <div className="space-y-2">
              {advStats.best_setups.map((setup, idx) => (
                <div key={setup.setup} className="flex justify-between p-3 bg-gray-700 rounded">
                  <span className="font-semibold">#{idx + 1} {setup.setup}</span>
                  <span className="text-sm">
                    {setup.count} trades | WR: {setup.win_rate.toFixed(1)}% | Avg: ${setup.avg_win.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default AdvancedAnalytics;
