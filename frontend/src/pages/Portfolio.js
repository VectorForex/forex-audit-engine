import React, { useState } from 'react';
import axios from 'axios';

function Portfolio() {
  const [userIds, setUserIds] = useState('');
  const [portfolio, setPortfolio] = useState(null);

  const handleAnalyze = async () => {
    const ids = userIds.split(',').map(id => id.trim()).filter(id => id);
    if (ids.length === 0) return;

    try {
      const response = await axios.post(
        'http://localhost:8000/api/portfolio/multi_account_stats/',
        { user_ids: ids }
      );
      setPortfolio(response.data);
    } catch (error) {
      console.error('Failed to fetch portfolio:', error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">💼 Portfolio Analysis</h2>
      
      <div className="mb-6">
        <label className="block mb-2">User IDs (comma-separated)</label>
        <div className="flex gap-4">
          <input
            type="text"
            value={userIds}
            onChange={(e) => setUserIds(e.target.value)}
            placeholder="user1, user2, user3"
            className="flex-1 bg-gray-800 p-2 rounded text-white"
          />
          <button
            onClick={handleAnalyze}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-bold"
          >
            Analyze
          </button>
        </div>
      </div>

      {portfolio && (
        <>
          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Total Trades</p>
              <p className="text-2xl font-bold">{portfolio.summary.total_trades}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Total PnL</p>
              <p className="text-2xl font-bold text-green-400">${portfolio.summary.total_pnl.toFixed(2)}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Portfolio Win Rate</p>
              <p className="text-2xl font-bold text-green-400">{portfolio.summary.win_rate.toFixed(1)}%</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-gray-400">Accounts</p>
              <p className="text-2xl font-bold">{portfolio.summary.accounts}</p>
            </div>
          </div>

          <div className="bg-gray-800 p-6 rounded mb-8">
            <h3 className="text-xl font-bold mb-4">Account Comparison</h3>
            <div className="space-y-2">
              {portfolio.comparison.map((acc, idx) => (
                <div key={acc.user_id} className="flex justify-between p-3 bg-gray-700 rounded">
                  <span className="font-semibold">#{idx + 1} {acc.user_id}</span>
                  <span className="text-sm">
                    Trades: {acc.total_trades} | WR: {acc.win_rate.toFixed(1)}% | PF: {acc.profit_factor.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-800 p-6 rounded">
            <h3 className="text-xl font-bold mb-4">Asset Allocation</h3>
            <div className="space-y-2">
              {Object.entries(portfolio.allocation).map(([asset, data]) => (
                <div key={asset} className="flex justify-between p-3 bg-gray-700 rounded">
                  <span className="font-semibold">{asset}</span>
                  <span className="text-sm">
                    Trades: {data.count} | PnL: ${data.pnl.toFixed(2)}
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

export default Portfolio;
