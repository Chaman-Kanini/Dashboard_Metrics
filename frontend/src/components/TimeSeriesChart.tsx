import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import type { TimeSeriesData } from '../types';

interface TimeSeriesChartProps {
  data: TimeSeriesData[];
}

export function TimeSeriesChart({ data }: TimeSeriesChartProps) {
  const formattedData = data.map(item => ({
    ...item,
    date: format(new Date(item.date), 'MMM dd'),
  }));

  const windsurfData = formattedData.filter(d => d.source === 'windsurf');
  const vscodeData = formattedData.filter(d => d.source === 'vscode_copilot');

  const mergedData = windsurfData.map((item, index) => ({
    date: item.date,
    windsurfSessions: item.sessionCount,
    windsurfErrors: item.errorCount,
    vscodeSessions: vscodeData[index]?.sessionCount || 0,
    vscodeErrors: vscodeData[index]?.errorCount || 0,
  }));

  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-white mb-4">Session Activity Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={mergedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="windsurfSessions"
            stroke="#0ea5e9"
            name="Windsurf Sessions"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="vscodeSessions"
            stroke="#8b5cf6"
            name="VS Code Sessions"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="windsurfErrors"
            stroke="#ef4444"
            name="Windsurf Errors"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          <Line
            type="monotone"
            dataKey="vscodeErrors"
            stroke="#f97316"
            name="VS Code Errors"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
