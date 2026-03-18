namespace IdeLogsApi.DTOs;

public class DashboardSummaryDto
{
    public string Source { get; set; } = string.Empty;
    public long TotalSessions { get; set; }
    public long TotalEvents { get; set; }
    public long TotalErrors { get; set; }
    public long TotalWarnings { get; set; }
    public long TotalInfo { get; set; }
    public decimal? AvgDuration { get; set; }
    public long UniqueWorkspaces { get; set; }
    public long HealthySessions { get; set; }
    public long WarningSessions { get; set; }
    public long CriticalSessions { get; set; }
    public long TotalInputTokens { get; set; }
    public long TotalOutputTokens { get; set; }
    public long TotalTokens { get; set; }
    public int UniqueUsers { get; set; }
}

public class SessionDto
{
    public Guid Id { get; set; }
    public string SessionId { get; set; } = string.Empty;
    public string Source { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; }
    public int TotalEvents { get; set; }
    public int ErrorCount { get; set; }
    public int WarningCount { get; set; }
    public string? HealthStatus { get; set; }
    public decimal? SessionDurationSeconds { get; set; }
    public string[]? Workspaces { get; set; }
    public string[]? Extensions { get; set; }
    public string? UserId { get; set; }
    public int InputTokens { get; set; }
    public int OutputTokens { get; set; }
    public int TotalTokens { get; set; }
}

public class EventDto
{
    public Guid Id { get; set; }
    public DateTime Timestamp { get; set; }
    public string Level { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string? SourceFile { get; set; }
}

public class TimeSeriesDataDto
{
    public DateTime Date { get; set; }
    public string Source { get; set; } = string.Empty;
    public int SessionCount { get; set; }
    public int ErrorCount { get; set; }
    public int WarningCount { get; set; }
}

public class HealthDistributionDto
{
    public string Source { get; set; } = string.Empty;
    public string HealthStatus { get; set; } = string.Empty;
    public int Count { get; set; }
}
