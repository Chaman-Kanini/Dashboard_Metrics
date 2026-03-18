import { useEffect, useState } from 'react';
import { Activity, AlertCircle, Database, TrendingUp } from 'lucide-react';
import { StatCard } from './components/StatCard';
import { TimeSeriesChart } from './components/TimeSeriesChart';
import { HealthDistributionChart } from './components/HealthDistributionChart';
import { SessionsTable } from './components/SessionsTable';
import { dashboardApi } from './services/api';
import type { DashboardSummary, Session, TimeSeriesData, HealthDistribution, Stats } from './types';

function App() {
  const [summary, setSummary] = useState<DashboardSummary[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [timeSeries, setTimeSeries] = useState<TimeSeriesData[]>([]);
  const [healthDistribution, setHealthDistribution] = useState<HealthDistribution[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [summaryData, sessionsData, timeSeriesData, healthData, statsData] = await Promise.all([
        dashboardApi.getSummary(),
        dashboardApi.getRecentSessions(20),
        dashboardApi.getTimeSeries(7),
        dashboardApi.getHealthDistribution(),
        dashboardApi.getStats(),
      ]);

      setSummary(summaryData);
      setSessions(sessionsData);
      setTimeSeries(timeSeriesData);
      setHealthDistribution(healthData);
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
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-red-400 text-xl">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">IDE Logs Dashboard</h1>
          <p className="text-slate-400">
            Monitor Windsurf and VS Code Copilot logs in real-time
          </p>
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
              <h3 className="text-xl font-semibold text-white mb-4 capitalize">
                {item.source.replace('_', ' ')} Summary
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-slate-400">Sessions</p>
                  <p className="text-2xl font-bold text-white">{item.totalSessions}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Events</p>
                  <p className="text-2xl font-bold text-white">{item.totalEvents}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Errors</p>
                  <p className="text-2xl font-bold text-red-400">{item.totalErrors}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Warnings</p>
                  <p className="text-2xl font-bold text-yellow-400">{item.totalWarnings}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Total Tokens</p>
                  <p className="text-2xl font-bold text-cyan-400">
                    {(item.totalTokens || 0) > 0 ? (item.totalTokens || 0).toLocaleString() : '-'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Users</p>
                  <p className="text-2xl font-bold text-white">{item.uniqueUsers || 0}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Avg Duration</p>
                  <p className="text-2xl font-bold text-white">
                    {item.avgDuration ? `${item.avgDuration.toFixed(1)}s` : 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Workspaces</p>
                  <p className="text-2xl font-bold text-white">{item.uniqueWorkspaces}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <TimeSeriesChart data={timeSeries} />
          <HealthDistributionChart data={healthDistribution} />
        </div>

        <SessionsTable sessions={sessions} />
      </div>
    </div>
  );
}

export default App;
