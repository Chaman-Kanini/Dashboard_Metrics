-- PostgreSQL Database Schema for IDE Logs
-- Supports both Windsurf and VS Code Copilot logs
-- Designed to be Supabase-compatible

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sessions table: stores IDE session information
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('windsurf', 'vscode_copilot')),
    timestamp TIMESTAMPTZ NOT NULL,
    workspaces TEXT[],
    extensions TEXT[],
    total_events INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    warning_count INTEGER DEFAULT 0,
    info_count INTEGER DEFAULT 0,
    health_status VARCHAR(50),
    session_duration_seconds DECIMAL(10, 2),
    langfuse_trace_id VARCHAR(255),
    user_id VARCHAR(255),
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_session_source UNIQUE (session_id, source)
);

-- Events table: stores individual log events
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL,
    level VARCHAR(20) NOT NULL CHECK (level IN ('info', 'warning', 'error', 'debug')),
    message TEXT NOT NULL,
    source_file VARCHAR(255),
    event_hash VARCHAR(64) UNIQUE NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_event UNIQUE (event_hash)
);

-- Metrics table: aggregated metrics for dashboard
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_date DATE NOT NULL,
    source VARCHAR(50) NOT NULL,
    total_sessions INTEGER DEFAULT 0,
    total_events INTEGER DEFAULT 0,
    total_errors INTEGER DEFAULT 0,
    total_warnings INTEGER DEFAULT 0,
    avg_session_duration DECIMAL(10, 2),
    unique_workspaces INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_metric_date_source UNIQUE (metric_date, source)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_source ON sessions(source);
CREATE INDEX IF NOT EXISTS idx_sessions_timestamp ON sessions(timestamp);
CREATE INDEX IF NOT EXISTS idx_sessions_health_status ON sessions(health_status);
CREATE INDEX IF NOT EXISTS idx_events_session_id ON events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_level ON events(level);
CREATE INDEX IF NOT EXISTS idx_events_hash ON events(event_hash);
CREATE INDEX IF NOT EXISTS idx_metrics_date ON metrics(metric_date);
CREATE INDEX IF NOT EXISTS idx_metrics_source ON metrics(source);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_metrics_updated_at BEFORE UPDATE ON metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to aggregate daily metrics
CREATE OR REPLACE FUNCTION aggregate_daily_metrics()
RETURNS void AS $$
BEGIN
    INSERT INTO metrics (metric_date, source, total_sessions, total_events, total_errors, total_warnings, avg_session_duration, unique_workspaces)
    SELECT 
        DATE(timestamp) as metric_date,
        source,
        COUNT(DISTINCT id) as total_sessions,
        SUM(total_events) as total_events,
        SUM(error_count) as total_errors,
        SUM(warning_count) as total_warnings,
        AVG(session_duration_seconds) as avg_session_duration,
        COUNT(DISTINCT UNNEST(workspaces)) as unique_workspaces
    FROM sessions
    WHERE DATE(timestamp) = CURRENT_DATE - INTERVAL '1 day'
    GROUP BY DATE(timestamp), source
    ON CONFLICT (metric_date, source) 
    DO UPDATE SET
        total_sessions = EXCLUDED.total_sessions,
        total_events = EXCLUDED.total_events,
        total_errors = EXCLUDED.total_errors,
        total_warnings = EXCLUDED.total_warnings,
        avg_session_duration = EXCLUDED.avg_session_duration,
        unique_workspaces = EXCLUDED.unique_workspaces,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- View for dashboard summary
CREATE OR REPLACE VIEW dashboard_summary AS
SELECT 
    s.source,
    COUNT(DISTINCT s.id) as total_sessions,
    SUM(s.total_events) as total_events,
    SUM(s.error_count) as total_errors,
    SUM(s.warning_count) as total_warnings,
    SUM(s.info_count) as total_info,
    AVG(s.session_duration_seconds) as avg_duration,
    (SELECT COUNT(DISTINCT w) FROM sessions s2, UNNEST(s2.workspaces) w WHERE s2.source = s.source) as unique_workspaces,
    COUNT(CASE WHEN s.health_status = 'healthy' THEN 1 END) as healthy_sessions,
    COUNT(CASE WHEN s.health_status = 'warning' THEN 1 END) as warning_sessions,
    COUNT(CASE WHEN s.health_status = 'critical' THEN 1 END) as critical_sessions
FROM sessions s
GROUP BY s.source;

-- View for recent sessions
CREATE OR REPLACE VIEW recent_sessions AS
SELECT 
    s.id,
    s.session_id,
    s.source,
    s.timestamp,
    s.total_events,
    s.error_count,
    s.warning_count,
    s.health_status,
    s.session_duration_seconds,
    s.workspaces,
    s.extensions
FROM sessions s
ORDER BY s.timestamp DESC
LIMIT 100;
