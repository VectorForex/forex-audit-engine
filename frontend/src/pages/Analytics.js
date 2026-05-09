import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

function Analytics() {
  const [userId, setUserId] = useState('');
  const [stats, setStats] = useState(null);
  const [setupPerf, setSetupPerf] = useState(null);

  const fetchAnalytics = async () => {
    if (!userId) return;
    try {
      const statsRes = await axios.get(`http://localhost:8000/api/analytics/user_stats/?user_id=${userId}`);
      const setupRes = await axios.get(`http://localhost:8000/api/analytics/setup_performance/?user_id=${userId}`);
      setStats(statsRes.data);
      setSetupPerf(setupRes.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">Analytics</h2>
      
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
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400">Win Rate</p>
            <p className="text-2xl font-bold text-green-400">{stats.win_rate.toFixed(2)}%</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400">Profit Factor</p>
            <p className="text-2xl font-bold text-green-400">{stats.profit_factor.toFixed(2)}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400">Expectancy</p>
            <p className="text-2xl font-bold text-green-400">${stats.expectancy.toFixed(2)}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded">
            <p className="text-gray-400">Max Drawdown</p>
            <p className="text-2xl font-bold text-red-400">${stats.max_drawdown.toFixed(2)}</p>
          </div>
        </div>
      )}

      {setupPerf && (
        <div className="bg-gray-800 p-6 rounded">
          <h3 className="text-xl font-bold mb-4">Setup Performance</h3>
          <div className="space-y-2">
            {Object.entries(setupPerf).map(([setup, data]) => (
              <div key={setup} className="flex justify-between p-2 bg-gray-700 rounded">
                <span>{setup}</span>
                <span>WR: {data.win_rate.toFixed(1)}% | E: ${data.expectancy.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Analytics;
