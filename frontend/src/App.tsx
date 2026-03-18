import { useEffect, useState } from 'react';
import { Activity, AlertCircle, Database, TrendingUp } from 'lucide-react';
import { StatCard } from './components/StatCard';
import { TimeSeriesChart } from './components/TimeSeriesChart';
import { SessionsTable } from './components/SessionsTable';
import { KaniniLogo } from './components/KaniniLogo';
import { dashboardApi } from './services/api';
import { formatSourceName } from './utils/formatters';
import type { DashboardSummary, Session, TimeSeriesData, Stats } from './types';

function App() {
  const [summary, setSummary] = useState<DashboardSummary[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [timeSeries, setTimeSeries] = useState<TimeSeriesData[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [summaryData, sessionsData, timeSeriesData, statsData] = await Promise.all([
        dashboardApi.getSummary(),
        dashboardApi.getRecentSessions(20),
        dashboardApi.getTimeSeries(7),
        dashboardApi.getStats(),
      ]);

      setSummary(summaryData);
      setSessions(sessionsData);
      setTimeSeries(timeSeriesData);
      setStats(statsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const totalSummary = summary.reduce(
    (acc, curr) => ({
      totalSessions: acc.totalSessions + curr.totalSessions,
      totalEvents: acc.totalEvents + curr.totalEvents,
      totalErrors: acc.totalErrors + curr.totalErrors,
      totalWarnings: acc.totalWarnings + curr.totalWarnings,
    }),
    { totalSessions: 0, totalEvents: 0, totalErrors: 0, totalWarnings: 0 }
  );

  if (loading && !stats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-900 text-xl">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-red-600 text-xl">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex items-center gap-6">
          <KaniniLogo className="h-8 w-auto" />
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Usage Dashboard</h1>
            <p className="text-gray-600">
              Monitor multi platform AI usage logs in real-time
            </p>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Sessions"
            value={(totalSummary.totalSessions || 0).toLocaleString()}
            icon={Activity}
          />
          <StatCard
            title="Total Events"
            value={(totalSummary.totalEvents || 0).toLocaleString()}
            icon={Database}
          />
          <StatCard
            title="Total Errors"
            value={(totalSummary.totalErrors || 0).toLocaleString()}
            icon={AlertCircle}
            className="border-red-500/20"
          />
          <StatCard
            title="Recent Errors (24h)"
            value={(stats?.recentErrors || 0).toLocaleString()}
            icon={TrendingUp}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {summary.map((item) => (
            <div key={item.source} className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {formatSourceName(item.source)} Summary
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Sessions</p>
                  <p className="text-2xl font-bold text-gray-900">{item.totalSessions}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Events</p>
                  <p className="text-2xl font-bold text-gray-900">{item.totalEvents}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Errors</p>
                  <p className="text-2xl font-bold text-red-600">{item.totalErrors}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Warnings</p>
                  <p className="text-2xl font-bold text-yellow-600">{item.totalWarnings}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Tokens</p>
                  <p className="text-2xl font-bold text-secondary-600">
                    {(item.totalTokens || 0) > 0 ? (item.totalTokens || 0).toLocaleString() : '-'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Users</p>
                  <p className="text-2xl font-bold text-gray-900">{item.uniqueUsers || 0}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Avg Duration</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {item.avgDuration ? `${item.avgDuration.toFixed(1)}s` : 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Workspaces</p>
                  <p className="text-2xl font-bold text-gray-900">{item.uniqueWorkspaces}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mb-8">
          <TimeSeriesChart data={timeSeries} />
        </div>

        <SessionsTable sessions={sessions} />
      </div>
    </div>
  );
}

export default App;
