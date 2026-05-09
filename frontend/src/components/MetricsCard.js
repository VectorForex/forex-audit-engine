import React from 'react';

function MetricsCard({ title, value, unit = '', color = 'green' }) {
  const colorClass = {
    green: 'text-green-400',
    red: 'text-red-400',
    blue: 'text-blue-400',
    yellow: 'text-yellow-400',
  }[color];

  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <p className="text-gray-400 text-sm">{title}</p>
      <p className={`text-3xl font-bold ${colorClass}`}>
        {typeof value === 'number' ? value.toFixed(2) : value}{unit}
      </p>
    </div>
  );
}

export default MetricsCard;
