using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace IdeLogsApi.Models;

[Table("events")]
public class Event
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; }

    [Required]
    [Column("session_id")]
    public Guid SessionId { get; set; }

    [Required]
    [Column("timestamp")]
    public DateTime Timestamp { get; set; }

    [Required]
    [Column("level")]
    [MaxLength(20)]
    public string Level { get; set; } = string.Empty;

    [Required]
    [Column("message")]
    public string Message { get; set; } = string.Empty;

    [Column("source_file")]
    [MaxLength(255)]
    public string? SourceFile { get; set; }

    [Required]
    [Column("event_hash")]
    [MaxLength(64)]
    public string EventHash { get; set; } = string.Empty;

    [Column("metadata")]
    public string? Metadata { get; set; }

    [Column("created_at")]
    public DateTime CreatedAt { get; set; }

    [ForeignKey("SessionId")]
    public Session? Session { get; set; }
}
