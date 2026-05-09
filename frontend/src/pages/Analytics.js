import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MetricsCard from '../components/MetricsCard';
import HeatMap from '../components/HeatMap';

function Analytics() {
  const [userId, setUserId] = useState('');
  const [stats, setStats] = useState(null);
  const [setupPerf, setSetupPerf] = useState(null);
  const [sessionData, setSessionData] = useState(null);

  const fetchAnalytics = async () => {
    if (!userId) return;
    try {
      const statsRes = await axios.get(`http://localhost:8000/api/analytics/user_stats/?user_id=${userId}`);
      const setupRes = await axios.get(`http://localhost:8000/api/analytics/setup_performance/?user_id=${userId}`);
      const sessionRes = await axios.get(`http://localhost:8000/api/trades/by_session/?user_id=${userId}`);
      setStats(statsRes.data);
      setSetupPerf(setupRes.data);
      setSessionData(sessionRes.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">📊 Analytics Dashboard</h2>
      
      <div className="mb-6 flex gap-4">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="flex-1 bg-gray-800 p-2 rounded text-white"
        />
        <button
          onClick={fetchAnalytics}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-bold"
        >
          Load Analytics
        </button>
      </div>

      {stats && (
        <>
          <div className="grid grid-cols-4 gap-4 mb-8">
            <MetricsCard title="Win Rate" value={stats.win_rate} unit="%" color="green" />
            <MetricsCard title="Profit Factor" value={stats.profit_factor} color="green" />
            <MetricsCard title="Expectancy" value={stats.expectancy} unit="$" color="blue" />
            <MetricsCard title="Max Drawdown" value={stats.max_drawdown} unit="$" color="red" />
          </div>

          <div className="grid grid-cols-2 gap-4 mb-8">
            <MetricsCard title="Consecutive Wins" value={stats.consecutive_wins} color="green" />
            <MetricsCard title="Consecutive Losses" value={stats.consecutive_losses} color="red" />
          </div>

          <HeatMap data={sessionData} />

          {setupPerf && (
            <div className="bg-gray-800 p-6 rounded mt-8">
              <h3 className="text-xl font-bold mb-4">Setup Performance</h3>
              <div className="space-y-2">
                {Object.entries(setupPerf).map(([setup, data]) => (
                  <div key={setup} className="flex justify-between p-3 bg-gray-700 rounded">
                    <span className="font-semibold">{setup}</span>
                    <span className="text-sm">
                      Trades: {data.count} | WR: {data.win_rate.toFixed(1)}% | PF: {data.profit_factor.toFixed(2)} | E: ${data.expectancy.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Analytics;
