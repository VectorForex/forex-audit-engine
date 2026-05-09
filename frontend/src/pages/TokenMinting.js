import React, { useState } from 'react';
import axios from 'axios';

function TokenMinting() {
  const [userId, setUserId] = useState('');
  const [threshold, setThreshold] = useState(55);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMintToken = async () => {
    if (!userId) return;
    
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:8000/api/tokens/mint_token/',
        {
          user_id: userId,
          win_rate_threshold: threshold,
        }
      );
      setToken(response.data);
    } catch (error) {
      alert('Failed to mint token: ' + error.response?.data?.error || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-6">🎖️ Mint Performance Token</h2>
      
      <div className="bg-gray-800 p-6 rounded-lg space-y-4">
        <div>
          <label className="block mb-2">User ID</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full bg-gray-700 p-2 rounded text-white"
            placeholder="Enter your user ID"
          />
        </div>

        <div>
          <label className="block mb-2">Win Rate Threshold (%)</label>
          <input
            type="number"
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            className="w-full bg-gray-700 p-2 rounded text-white"
            min="0"
            max="100"
          />
        </div>

        <button
          onClick={handleMintToken}
          disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 px-6 py-3 rounded font-bold disabled:opacity-50"
        >
          {loading ? 'Minting...' : 'Mint Token'}
        </button>
      </div>

      {token && (
        <div className="bg-green-900 p-6 rounded-lg mt-8">
          <h3 className="text-xl font-bold mb-4">✅ Token Minted Successfully!</h3>
          <div className="space-y-2 text-sm">
            <p><strong>User ID:</strong> {token.user_id}</p>
            <p><strong>Win Rate Threshold:</strong> {token.win_rate_threshold}%</p>
            <p><strong>Stellar Address:</strong> {token.stellar_public_key}</p>
            <p><strong>Minted At:</strong> {new Date(token.minted_at).toLocaleString()}</p>
            {token.stellar_tx_hash && (
              <p><strong>TX Hash:</strong> {token.stellar_tx_hash.substring(0, 16)}...</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default TokenMinting;
