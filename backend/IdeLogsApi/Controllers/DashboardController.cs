using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using IdeLogsApi.Data;
using IdeLogsApi.DTOs;

namespace IdeLogsApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DashboardController : ControllerBase
{
    private readonly AppDbContext _context;
    private readonly ILogger<DashboardController> _logger;

    public DashboardController(AppDbContext context, ILogger<DashboardController> logger)
    {
        _context = context;
        _logger = logger;
    }

    [HttpGet("summary")]
    public async Task<ActionResult<IEnumerable<DashboardSummaryDto>>> GetSummary()
    {
        try
        {
            var sessions = await _context.Sessions.ToListAsync();
            
            var summary = sessions
                .GroupBy(s => s.Source)
                .Select(g => new DashboardSummaryDto
                {
                    Source = g.Key,
                    TotalSessions = g.Count(),
                    TotalEvents = g.Sum(s => s.TotalEvents),
                    TotalErrors = g.Sum(s => s.ErrorCount),
                    TotalWarnings = g.Sum(s => s.WarningCount),
                    TotalInfo = g.Sum(s => s.InfoCount),
                    AvgDuration = g.Average(s => s.SessionDurationSeconds),
                    UniqueWorkspaces = g.SelectMany(s => s.Workspaces ?? Array.Empty<string>()).Distinct().Count(),
                    HealthySessions = g.Count(s => s.HealthStatus == "healthy"),
                    WarningSessions = g.Count(s => s.HealthStatus == "warning" || s.HealthStatus == "minor_issues"),
                    CriticalSessions = g.Count(s => s.HealthStatus == "critical"),
                    TotalInputTokens = g.Sum(s => s.InputTokens),
                    TotalOutputTokens = g.Sum(s => s.OutputTokens),
                    TotalTokens = g.Sum(s => s.TotalTokens),
                    UniqueUsers = g.Select(s => s.UserId).Where(u => !string.IsNullOrEmpty(u)).Distinct().Count()
                })
                .ToList();

            return Ok(summary);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching dashboard summary");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("sessions")]
    public async Task<ActionResult<IEnumerable<SessionDto>>> GetRecentSessions(
        [FromQuery] int limit = 50,
        [FromQuery] string? source = null)
    {
        try
        {
            var query = _context.Sessions.AsQueryable();

            if (!string.IsNullOrEmpty(source))
            {
                query = query.Where(s => s.Source == source);
            }

            var sessions = await query
                .OrderByDescending(s => s.Timestamp)
                .Take(limit)
                .Select(s => new SessionDto
                {
                    Id = s.Id,
                    SessionId = s.SessionId,
                    Source = s.Source,
                    Timestamp = s.Timestamp,
                    TotalEvents = s.TotalEvents,
                    ErrorCount = s.ErrorCount,
                    WarningCount = s.WarningCount,
                    HealthStatus = s.HealthStatus,
                    SessionDurationSeconds = s.SessionDurationSeconds,
                    Workspaces = s.Workspaces,
                    Extensions = s.Extensions,
                    UserId = s.UserId,
                    InputTokens = s.InputTokens,
                    OutputTokens = s.OutputTokens,
                    TotalTokens = s.TotalTokens
                })
                .ToListAsync();

            return Ok(sessions);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching recent sessions");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("sessions/{id}/events")]
    public async Task<ActionResult<IEnumerable<EventDto>>> GetSessionEvents(Guid id)
    {
        try
        {
            var events = await _context.Events
                .Where(e => e.SessionId == id)
                .OrderBy(e => e.Timestamp)
                .Select(e => new EventDto
                {
                    Id = e.Id,
                    Timestamp = e.Timestamp,
                    Level = e.Level,
                    Message = e.Message,
                    SourceFile = e.SourceFile
                })
                .ToListAsync();

            return Ok(events);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching session events");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("timeseries")]
    public async Task<ActionResult<IEnumerable<TimeSeriesDataDto>>> GetTimeSeries(
        [FromQuery] int days = 7)
    {
        try
        {
            var startDate = DateTime.UtcNow.AddDays(-days);

            var timeSeries = await _context.Sessions
                .Where(s => s.Timestamp >= startDate)
                .GroupBy(s => new { Date = s.Timestamp.Date, s.Source })
                .Select(g => new TimeSeriesDataDto
                {
                    Date = g.Key.Date,
                    Source = g.Key.Source,
                    SessionCount = g.Count(),
                    ErrorCount = g.Sum(s => s.ErrorCount),
                    WarningCount = g.Sum(s => s.WarningCount)
                })
                .OrderBy(t => t.Date)
                .ToListAsync();

            return Ok(timeSeries);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching time series data");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("health-distribution")]
    public async Task<ActionResult<IEnumerable<HealthDistributionDto>>> GetHealthDistribution()
    {
        try
        {
            var distribution = await _context.Sessions
                .GroupBy(s => new { s.Source, s.HealthStatus })
                .Select(g => new HealthDistributionDto
                {
                    Source = g.Key.Source,
                    HealthStatus = g.Key.HealthStatus ?? "unknown",
                    Count = g.Count()
                })
                .ToListAsync();

            return Ok(distribution);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching health distribution");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("stats")]
    public async Task<ActionResult<object>> GetStats()
    {
        try
        {
            var totalSessions = await _context.Sessions.CountAsync();
            var totalEvents = await _context.Events.CountAsync();
            var recentErrors = await _context.Events
                .Where(e => e.Level == "error" && e.Timestamp >= DateTime.UtcNow.AddHours(-24))
                .CountAsync();

            return Ok(new
            {
                totalSessions,
                totalEvents,
                recentErrors,
                lastUpdated = await _context.Sessions.MaxAsync(s => (DateTime?)s.UpdatedAt)
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching stats");
            return StatusCode(500, "Internal server error");
        }
    }
}
