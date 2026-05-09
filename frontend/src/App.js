import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import AdvancedAnalytics from './pages/AdvancedAnalytics';
import RedFlags from './pages/RedFlags';
import Leaderboard from './pages/Leaderboard';
import TokenMinting from './pages/TokenMinting';
import Portfolio from './pages/Portfolio';
import Navigation from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white">
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/advanced" element={<AdvancedAnalytics />} />
          <Route path="/red-flags" element={<RedFlags />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/tokens" element={<TokenMinting />} />
          <Route path="/portfolio" element={<Portfolio />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
