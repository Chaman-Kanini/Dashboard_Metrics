using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace IdeLogsApi.Models;

[Table("sessions")]
public class Session
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; }

    [Required]
    [Column("session_id")]
    [MaxLength(255)]
    public string SessionId { get; set; } = string.Empty;

    [Required]
    [Column("source")]
    [MaxLength(50)]
    public string Source { get; set; } = string.Empty;

    [Required]
    [Column("timestamp")]
    public DateTime Timestamp { get; set; }

    [Column("workspaces")]
    public string[]? Workspaces { get; set; }

    [Column("extensions")]
    public string[]? Extensions { get; set; }

    [Column("total_events")]
    public int TotalEvents { get; set; }

    [Column("error_count")]
    public int ErrorCount { get; set; }

    [Column("warning_count")]
    public int WarningCount { get; set; }

    [Column("info_count")]
    public int InfoCount { get; set; }

    [Column("health_status")]
    [MaxLength(50)]
    public string? HealthStatus { get; set; }

    [Column("session_duration_seconds")]
    public decimal? SessionDurationSeconds { get; set; }

    [Column("langfuse_trace_id")]
    [MaxLength(255)]
    public string? LangfuseTraceId { get; set; }

    [Column("user_id")]
    [MaxLength(255)]
    public string? UserId { get; set; }

    [Column("input_tokens")]
    public int InputTokens { get; set; }

    [Column("output_tokens")]
    public int OutputTokens { get; set; }

    [Column("total_tokens")]
    public int TotalTokens { get; set; }

    [Column("created_at")]
    public DateTime CreatedAt { get; set; }

    [Column("updated_at")]
    public DateTime UpdatedAt { get; set; }

    public ICollection<Event> Events { get; set; } = new List<Event>();
}
