import { format } from 'date-fns';
import { AlertCircle, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import type { Session } from '../types';
import { cn } from '../utils/cn';

interface SessionsTableProps {
  sessions: Session[];
  onSessionClick?: (session: Session) => void;
}

const healthStatusConfig = {
  healthy: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-400/10' },
  warning: { icon: AlertTriangle, color: 'text-yellow-400', bg: 'bg-yellow-400/10' },
  minor_issues: { icon: Info, color: 'text-orange-400', bg: 'bg-orange-400/10' },
  critical: { icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-400/10' },
};

export function SessionsTable({ sessions, onSessionClick }: SessionsTableProps) {
  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-white mb-4">Recent Sessions</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs uppercase bg-slate-700 text-slate-300">
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
                  className="border-b border-slate-700 hover:bg-slate-700/50 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4">
                    <span className={cn(
                      'px-2 py-1 rounded text-xs font-medium',
                      session.source === 'windsurf' ? 'bg-blue-400/10 text-blue-400' : 'bg-purple-400/10 text-purple-400'
                    )}>
                      {session.source}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-300 text-sm">
                    {session.userId || 'N/A'}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-300">
                    {session.sessionId ? `${session.sessionId.substring(0, 15)}...` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 text-slate-300">
                    {format(new Date(session.timestamp), 'MMM dd, HH:mm')}
                  </td>
                  <td className="px-6 py-4 text-slate-300">{session.totalEvents}</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'font-semibold',
                      session.errorCount > 0 ? 'text-red-400' : 'text-slate-500'
                    )}>
                      {session.errorCount}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'font-semibold',
                      session.warningCount > 0 ? 'text-yellow-400' : 'text-slate-500'
                    )}>
                      {session.warningCount}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      'text-xs font-mono',
                      (session.totalTokens || 0) > 0 ? 'text-cyan-400' : 'text-slate-500'
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
                  <td className="px-6 py-4 text-slate-300">
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
