import React from 'react';

function HeatMap({ data }) {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
  const sessions = ['Asian', 'European', 'US'];

  const getColor = (value) => {
    if (value >= 60) return 'bg-green-600';
    if (value >= 50) return 'bg-green-400';
    if (value >= 40) return 'bg-yellow-400';
    return 'bg-red-500';
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h3 className="text-xl font-bold mb-4">Win Rate Heat Map</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-center">
          <thead>
            <tr>
              <th className="p-2">Session</th>
              {days.map(day => <th key={day} className="p-2">{day}</th>)}
            </tr>
          </thead>
          <tbody>
            {sessions.map(session => (
              <tr key={session}>
                <td className="p-2 font-bold">{session}</td>
                {days.map(day => {
                  const value = Math.random() * 100;
                  return (
                    <td key={`${session}-${day}`} className={`p-2 ${getColor(value)}`}>
                      {value.toFixed(0)}%
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HeatMap;
