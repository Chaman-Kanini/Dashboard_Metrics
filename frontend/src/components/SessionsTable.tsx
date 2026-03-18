import { format } from 'date-fns';
import { AlertCircle, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import type { Session } from '../types';
import { cn } from '../utils/cn';
import { formatSourceName } from '../utils/formatters';

interface SessionsTableProps {
  sessions: Session[];
  onSessionClick?: (session: Session) => void;
}

const healthStatusConfig = {
  healthy: { icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-100' },
  warning: { icon: AlertTriangle, color: 'text-yellow-600', bg: 'bg-yellow-100' },
  minor_issues: { icon: Info, color: 'text-orange-600', bg: 'bg-orange-100' },
  critical: { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-100' },
};

export function SessionsTable({ sessions, onSessionClick }: SessionsTableProps) {
  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">Recent Sessions</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs uppercase bg-gray-100 text-gray-700">
            <tr>
              <th className="px-6 py-3">Source</th>
              <th className="px-6 py-3">User</th>
              <th className="px-6 py-3">Session ID</th>
              <th className="px-6 py-3">Timestamp</th>
              <th className="px-6 py-3">Events</th>
              <th className="px-6 py-3">Errors</th>
              <th className="px-6 py-3">Warnings</th>
              <th className="px-6 py-3">Tokens</th>
              <th className="px-6 py-3">Health</th>
              <th className="px-6 py-3">Duration</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((session) => {
              const healthConfig = healthStatusConfig[session.healthStatus as keyof typeof healthStatusConfig] || healthStatusConfig.healthy;
              const HealthIcon = healthConfig.icon;

              return (
                <tr
                  key={session.id}
                  onClick={() => onSessionClick?.(session)}
                  className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4">
                    <span className={cn(
                      'px-2 py-1 rounded text-xs font-medium',
                      session.source === 'windsurf' ? 'bg-secondary-100 text-secondary-700' : 'bg-purple-100 text-purple-700'
                    )}>
                      {formatSourceName(session.source)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-700 text-sm">
                    {session.userId || 'N/A'}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs text-gray-700">
                    {session.sessionId ? `${session.sessionId.substring(0, 15)}...` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 text-gray-700">
                    {format(new Date(session.timestamp), 'MMM dd, HH:mm')}
                  </td>
                  <td className="px-6 py-4 text-gray-700">{session.totalEvents}</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'font-semibold',
                      session.errorCount > 0 ? 'text-red-600' : 'text-gray-400'
                    )}>
                      {session.errorCount}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'font-semibold',
                      session.warningCount > 0 ? 'text-yellow-600' : 'text-gray-400'
                    )}>
                      {session.warningCount}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'text-xs font-mono',
                      (session.totalTokens || 0) > 0 ? 'text-secondary-600' : 'text-gray-400'
                    )}>
                      {(session.totalTokens || 0) > 0 ? (session.totalTokens || 0).toLocaleString() : '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className={cn('flex items-center gap-2 px-2 py-1 rounded w-fit', healthConfig.bg)}>
                      <HealthIcon className={cn('w-4 h-4', healthConfig.color)} />
                      <span className={cn('text-xs font-medium capitalize', healthConfig.color)}>
                        {session.healthStatus?.replace('_', ' ')}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-700">
                    {session.sessionDurationSeconds && session.sessionDurationSeconds > 0
                      ? `${session.sessionDurationSeconds.toFixed(1)}s`
                      : 'N/A'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
