import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import type { HealthDistribution } from '../types';

interface HealthDistributionChartProps {
  data: HealthDistribution[];
}

const COLORS = {
  healthy: '#10b981',
  warning: '#f59e0b',
  minor_issues: '#f97316',
  critical: '#ef4444',
  unknown: '#6b7280',
};

export function HealthDistributionChart({ data }: HealthDistributionChartProps) {
  const chartData = data.map(item => ({
    name: `${item.source} - ${item.healthStatus}`,
    value: item.count,
    healthStatus: item.healthStatus,
  }));

  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-white mb-4">Health Status Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.healthStatus as keyof typeof COLORS] || COLORS.unknown}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
            }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
