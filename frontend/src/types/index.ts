export interface DashboardSummary {
  source: string;
  totalSessions: number;
  totalEvents: number;
  totalErrors: number;
  totalWarnings: number;
  totalInfo: number;
  avgDuration: number | null;
  uniqueWorkspaces: number;
  healthySessions: number;
  warningSessions: number;
  criticalSessions: number;
  totalInputTokens: number;
  totalOutputTokens: number;
  totalTokens: number;
  uniqueUsers: number;
}

export interface Session {
  id: string;
  sessionId: string;
  source: string;
  timestamp: string;
  totalEvents: number;
  errorCount: number;
  warningCount: number;
  healthStatus: string | null;
  sessionDurationSeconds: number | null;
  workspaces: string[] | null;
  extensions: string[] | null;
  userId: string | null;
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}

export interface Event {
  id: string;
  timestamp: string;
  level: string;
  message: string;
  sourceFile: string | null;
}

export interface TimeSeriesData {
  date: string;
  source: string;
  sessionCount: number;
  errorCount: number;
  warningCount: number;
}

export interface HealthDistribution {
  source: string;
  healthStatus: string;
  count: number;
}

export interface Stats {
  totalSessions: number;
  totalEvents: number;
  recentErrors: number;
  lastUpdated: string | null;
}
