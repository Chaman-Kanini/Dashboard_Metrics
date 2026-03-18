# IDE Logs Dashboard

Comprehensive log aggregation and monitoring system for Windsurf and VS Code Copilot IDEs with PostgreSQL storage, Langfuse integration, and interactive React dashboard.

## 🌟 Features

- **Dual IDE Support**: Scrapes logs from both Windsurf and VS Code Copilot
- **Duplicate Detection**: SHA-256 hash-based deduplication prevents duplicate log entries
- **PostgreSQL Storage**: Robust database with optimized indexes and views
- **Langfuse Integration**: Automatic trace export for observability
- **Interactive Dashboard**: Real-time React dashboard with charts and metrics
- **RESTful API**: .NET 8 Web API backend with Swagger documentation
- **Supabase Ready**: Database schema compatible with Supabase migration
- 🔍 Extracts errors, warnings, and info events
- 📈 Sends structured traces to Langfuse
- 🏷️ Tracks workspaces and extensions used
- 💡 Calculates session health status
- ⚡ Processes multiple sessions in batch

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env` file is already configured with your Langfuse credentials:
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_BASE_URL`

## Usage

Simply run the script:

```bash
python windsurf_to_langfuse.py
```

The script will:
1. ✅ Scan all log sessions in `C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs`
2. ✅ Parse events from each session
3. ✅ Send structured traces to Langfuse
4. ✅ Display a summary of processed sessions

## What Gets Tracked

### Session Metrics
- **Session ID**: Unique identifier for each Windsurf session
- **Timestamp**: When the session started
- **Event Counts**: Total events, errors, warnings, info messages
- **Workspaces**: List of workspaces opened during the session
- **Extensions**: Extensions that were active

### Event Details
- **Errors**: Critical issues and exceptions (up to 50 per session)
- **Warnings**: Warning messages (up to 30 per session)
- **Session Duration**: How long the session lasted
- **Health Status**: Overall session health (healthy, minor_issues, warning, critical)

## Viewing Results

After running the script, view your metrics at:
**https://cloud.langfuse.com**

### In Langfuse Dashboard:

1. **Traces**: Each Windsurf session appears as a trace
2. **Spans**: Errors and warnings appear as spans within traces
3. **Metadata**: Session details, workspace info, and health status
4. **Tags**: All traces are tagged with `windsurf`, `ide`, `logs`

## Example Output

```
============================================================
Windsurf Logs to Langfuse Integration
============================================================

📂 Parsing logs from: C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs
📊 Found 10 log sessions

🔄 Processing session: 20260317T161759
   📝 Events: 76 (Errors: 12, Warnings: 5)
   ✅ Sent to Langfuse (Trace ID: abc123...)

🔄 Flushing events to Langfuse...

============================================================
📊 Summary
============================================================
✅ Successfully processed: 10 sessions

🌐 View your metrics at: https://cloud.langfuse.com
============================================================
```

## Customization

### Change Log Directory

Edit the `LOGS_DIR` variable in `windsurf_to_langfuse.py`:

```python
LOGS_DIR = r"C:\Your\Custom\Path\To\Logs"
```

### Adjust Event Limits

Modify the limits in the `send_session_trace` method:

```python
for idx, error in enumerate(session_data['errors'][:50]):  # Change 50 to your limit
```

## Troubleshooting

### Missing Environment Variables
```
❌ Error: Missing environment variables: LANGFUSE_SECRET_KEY
```
**Solution**: Ensure your `.env` file contains all required Langfuse credentials.

### No Log Sessions Found
```
⚠️  No log sessions found
```
**Solution**: Verify the `LOGS_DIR` path points to your Windsurf logs directory.

### Connection Errors
**Solution**: Check your internet connection and verify Langfuse credentials are correct.

## Notes

- The script processes logs from the standard Windsurf logs location
- Empty log sessions are automatically skipped
- Long messages are truncated to 500 characters for readability
- The script uses smart limits to avoid overwhelming Langfuse with too many events

## Support

For issues or questions, check:
- Langfuse Documentation: https://langfuse.com/docs
- Windsurf Logs Location: `%APPDATA%\Roaming\Windsurf\logs`
