import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const tradeAPI = {
  uploadCSV: (userId, file) => {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('file', file);
    return client.post('/trades/upload_csv/', formData);
  },
  calculatePnL: (userId) => client.post('/trades/calculate_pnl/', { user_id: userId }),
};

export const analyticsAPI = {
  getUserStats: (userId) => client.get(`/analytics/user_stats/?user_id=${userId}`),
  getSetupPerformance: (userId) => client.get(`/analytics/setup_performance/?user_id=${userId}`),
  getRedFlags: (userId) => client.get(`/analytics/red_flags/?user_id=${userId}`),
};

export default client;
