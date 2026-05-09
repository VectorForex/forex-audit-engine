import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav className="bg-gray-800 border-b border-gray-700 p-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold text-blue-400">📊 Forex Ledger</h1>
        <div className="space-x-6">
          <Link to="/" className="hover:text-blue-400">Dashboard</Link>
          <Link to="/analytics" className="hover:text-blue-400">Analytics</Link>
          <Link to="/red-flags" className="hover:text-blue-400">Red Flags</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;
