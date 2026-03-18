using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace IdeLogsApi.Models;

[Table("metrics")]
public class Metric
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; }

    [Required]
    [Column("metric_date")]
    public DateOnly MetricDate { get; set; }

    [Required]
    [Column("source")]
    [MaxLength(50)]
    public string Source { get; set; } = string.Empty;

    [Column("total_sessions")]
    public int TotalSessions { get; set; }

    [Column("total_events")]
    public int TotalEvents { get; set; }

    [Column("total_errors")]
    public int TotalErrors { get; set; }

    [Column("total_warnings")]
    public int TotalWarnings { get; set; }

    [Column("avg_session_duration")]
    public decimal? AvgSessionDuration { get; set; }

    [Column("unique_workspaces")]
    public int UniqueWorkspaces { get; set; }

    [Column("created_at")]
    public DateTime CreatedAt { get; set; }

    [Column("updated_at")]
    public DateTime UpdatedAt { get; set; }
}
