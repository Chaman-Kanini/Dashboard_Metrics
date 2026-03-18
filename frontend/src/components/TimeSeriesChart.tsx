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
      <h3 className="text-xl font-semibold text-gray-900 mb-4">Session Activity Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={mergedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" stroke="#6b7280" />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
              color: '#111827',
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="windsurfSessions"
            stroke="#00A8E4"
            name="Windsurf Sessions"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="vscodeSessions"
            stroke="#BDDA57"
            name="VS Code Sessions"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="windsurfErrors"
            stroke="#dc2626"
            name="Windsurf Errors"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          <Line
            type="monotone"
            dataKey="vscodeErrors"
            stroke="#ea580c"
            name="VS Code Errors"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
