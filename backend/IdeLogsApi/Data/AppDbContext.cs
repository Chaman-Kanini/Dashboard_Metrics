using Microsoft.EntityFrameworkCore;
using IdeLogsApi.Models;

namespace IdeLogsApi.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Session> Sessions { get; set; }
    public DbSet<Event> Events { get; set; }
    public DbSet<Metric> Metrics { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Session>(entity =>
        {
            entity.HasIndex(e => e.Source);
            entity.HasIndex(e => e.Timestamp);
            entity.HasIndex(e => e.HealthStatus);
            entity.HasIndex(e => new { e.SessionId, e.Source }).IsUnique();
        });

        modelBuilder.Entity<Event>(entity =>
        {
            entity.HasIndex(e => e.SessionId);
            entity.HasIndex(e => e.Timestamp);
            entity.HasIndex(e => e.Level);
            entity.HasIndex(e => e.EventHash).IsUnique();
        });

        modelBuilder.Entity<Metric>(entity =>
        {
            entity.HasIndex(e => e.MetricDate);
            entity.HasIndex(e => e.Source);
            entity.HasIndex(e => new { e.MetricDate, e.Source }).IsUnique();
        });
    }
}
