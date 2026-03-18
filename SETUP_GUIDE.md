# Complete Setup and Testing Guide

This guide walks you through setting up and testing the entire IDE Logs Dashboard system.

## Step-by-Step Setup

### Step 1: Install Prerequisites

#### Windows
```powershell
# Install Python 3.8+
winget install Python.Python.3.11

# Install PostgreSQL
winget install PostgreSQL.PostgreSQL

# Install .NET 8 SDK
winget install Microsoft.DotNet.SDK.8

# Install Node.js
winget install OpenJS.NodeJS.LTS
```

#### macOS
```bash
brew install python postgresql@15 dotnet node
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip postgresql nodejs npm
wget https://dot.net/v1/dotnet-install.sh
bash dotnet-install.sh --channel 8.0
```

### Step 2: Database Setup

```bash
# Start PostgreSQL service
# Windows: Services → PostgreSQL → Start
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database and user
psql -U postgres
```

```sql
-- In PostgreSQL prompt
CREATE DATABASE ide_logs;
CREATE USER ide_logs_user WITH PASSWORD 'SecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE ide_logs TO ide_logs_user;
\c ide_logs
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ide_logs_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ide_logs_user;
\q
```

```bash
# Run schema
cd database
psql -U postgres -d ide_logs -f schema.sql
```

### Step 3: Python Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env .env.backup
```

Edit `.env`:
```env
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ide_logs
DB_USER=postgres
DB_PASSWORD=SecurePassword123!

# Langfuse Configuration
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

### Step 4: Backend API Setup

```bash
cd backend/IdeLogsApi

# Restore NuGet packages
dotnet restore

# Update appsettings.json with your database password
```

Edit `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=ide_logs;Username=postgres;Password=SecurePassword123!"
  }
}
```

```bash
# Build the project
dotnet build

# Run the API
dotnet run
```

The API should start on `http://localhost:5000`. Keep this terminal open.

### Step 5: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:5000/api
```

```bash
# Start development server
npm run dev
```

The frontend should start on `http://localhost:5173`. Keep this terminal open.

## Testing the Complete Workflow

### Test 1: Verify Database Connection

```bash
# From project root
python -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
print('✅ Database connection successful!')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM sessions')
count = cur.fetchone()[0]
print(f'📊 Current sessions in database: {count}')
conn.close()
"
```

Expected output:
```
✅ Database connection successful!
📊 Current sessions in database: 0
```

### Test 2: Run Log Scraper

```bash
# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the scraper
python windsurf_to_langfuse.py
```

Expected output:
```
======================================================================
IDE Logs to Langfuse & PostgreSQL Integration
======================================================================
✅ Connected to PostgreSQL database
✅ Connected to Langfuse

📂 Processing windsurf logs from: C:\Users\...\Windsurf\logs
📊 Found X log sessions

🔄 Processing session: 20240317T103045
   📝 Events: 150 (Errors: 2, Warnings: 5)
   ✅ Sent to Langfuse (Trace ID: ...)
   💾 Saved to database (Session UUID: ...)

📂 Processing vscode_copilot logs from: C:\Users\...\Code\logs
📊 Found Y log sessions
...

======================================================================
📊 Summary
======================================================================
✅ Successfully processed: X sessions
⏭️  Skipped (duplicates/empty): Y sessions
🌐 View your metrics at: https://cloud.langfuse.com
💾 Data saved to PostgreSQL database
======================================================================
```

### Test 3: Verify Backend API

Open a new terminal:

```bash
# Test stats endpoint
curl http://localhost:5000/api/dashboard/stats

# Test summary endpoint
curl http://localhost:5000/api/dashboard/summary

# Test sessions endpoint
curl http://localhost:5000/api/dashboard/sessions?limit=5
```

Or visit Swagger UI: `http://localhost:5000/swagger`

### Test 4: Verify Frontend Dashboard

1. Open browser to `http://localhost:5173`
2. You should see:
   - Summary cards with total sessions, events, errors
   - Source breakdown for Windsurf and VS Code
   - Time series chart showing activity
   - Health distribution pie chart
   - Sessions table with recent logs

3. Verify data is displaying:
   - Check if session counts match database
   - Verify charts are rendering
   - Click on a session row to test interactivity

### Test 5: Test Duplicate Detection

```bash
# Run the scraper again
python windsurf_to_langfuse.py
```

Expected output should show:
```
⏭️  Skipping <session_id> (already in database)
```

This confirms duplicate detection is working.

### Test 6: Verify Langfuse Integration

1. Go to your Langfuse dashboard: `https://cloud.langfuse.com`
2. You should see traces for each session
3. Traces should be named: `windsurf_session_<id>` or `vscode_copilot_session_<id>`
4. Each trace should contain:
   - Session metadata
   - Error spans
   - Warning spans
   - Session summary

## Production Deployment

### Database (Supabase)

1. Create Supabase project
2. Run `database/schema.sql` in SQL Editor
3. Get connection string from Settings → Database
4. Update `.env` and `appsettings.json` with Supabase credentials

### Backend (.NET API)

```bash
cd backend/IdeLogsApi

# Publish for production
dotnet publish -c Release -o ./publish

# Run published app
cd publish
dotnet IdeLogsApi.dll
```

Or deploy to:
- Azure App Service
- AWS Elastic Beanstalk
- Docker container

### Frontend (React)

```bash
cd frontend

# Build for production
npm run build

# Preview production build
npm run preview
```

Deploy `dist/` folder to:
- Vercel: `vercel deploy`
- Netlify: `netlify deploy --prod`
- AWS S3 + CloudFront
- Azure Static Web Apps

### Log Scraper (Scheduled)

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 30 minutes
4. Action: Start program → `run_windsurf_to_langfuse.bat`

**Linux/macOS Cron:**
```bash
crontab -e
# Add:
*/30 * * * * cd /path/to/project && /path/to/venv/bin/python windsurf_to_langfuse.py >> /var/log/ide_logs.log 2>&1
```

## Monitoring and Maintenance

### Database Maintenance

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('ide_logs'));

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Vacuum and analyze
VACUUM ANALYZE sessions;
VACUUM ANALYZE events;

-- Archive old data (optional)
DELETE FROM events WHERE created_at < NOW() - INTERVAL '90 days';
DELETE FROM sessions WHERE created_at < NOW() - INTERVAL '90 days';
```

### Log Rotation

```bash
# Keep last 30 days of logs
find /path/to/logs -name "*.log" -mtime +30 -delete
```

### Performance Tuning

```sql
-- Add indexes if needed
CREATE INDEX CONCURRENTLY idx_events_created_at ON events(created_at);
CREATE INDEX CONCURRENTLY idx_sessions_created_at ON sessions(created_at);

-- Update statistics
ANALYZE sessions;
ANALYZE events;
```

## Troubleshooting

### Issue: "psycopg2 module not found"
```bash
pip install psycopg2-binary
```

### Issue: "Port 5000 already in use"
Edit `backend/IdeLogsApi/Properties/launchSettings.json`:
```json
"applicationUrl": "http://localhost:5001"
```

### Issue: "CORS error in frontend"
Update `backend/IdeLogsApi/Program.cs`:
```csharp
policy.WithOrigins("http://localhost:5173", "http://localhost:3000", "https://yourdomain.com")
```

### Issue: "Database connection timeout"
Check PostgreSQL is running:
```bash
# Windows
services.msc → PostgreSQL

# macOS
brew services list

# Linux
sudo systemctl status postgresql
```

### Issue: "No logs found"
Verify log directories exist and contain session folders:
```bash
# Windows
dir "C:\Users\%USERNAME%\AppData\Roaming\Windsurf\logs"
dir "C:\Users\%USERNAME%\AppData\Roaming\Code\logs"

# macOS/Linux
ls ~/Library/Application\ Support/Windsurf/logs
ls ~/Library/Application\ Support/Code/logs
```

## Success Checklist

- [ ] PostgreSQL database created and schema applied
- [ ] Python dependencies installed
- [ ] .NET 8 backend running on port 5000
- [ ] React frontend running on port 5173
- [ ] Log scraper successfully processes logs
- [ ] Data appears in PostgreSQL database
- [ ] Traces appear in Langfuse dashboard
- [ ] Frontend dashboard displays data correctly
- [ ] No duplicate sessions when running scraper twice
- [ ] API endpoints return valid JSON
- [ ] Charts and graphs render properly

## Next Steps

1. **Schedule Regular Scraping**: Set up cron job or Task Scheduler
2. **Configure Alerts**: Set up monitoring for critical errors
3. **Backup Database**: Implement regular backup strategy
4. **Scale as Needed**: Monitor performance and optimize queries
5. **Customize Dashboard**: Add custom metrics or visualizations
6. **Integrate with CI/CD**: Automate deployments

## Support

For issues or questions:
1. Check logs: Python script output, API logs, browser console
2. Verify all services are running
3. Check database connectivity
4. Review environment variables
5. Consult troubleshooting section above
