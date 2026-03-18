# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ PostgreSQL installed and running
- ✅ Python 3.8+ installed
- ✅ .NET 8 SDK installed
- ✅ Node.js 18+ installed

## Step 1: Database Setup (5 minutes)

### Set PostgreSQL Password

First, you need to update your `.env` file with the correct PostgreSQL password:

```bash
# Open .env file and update DB_PASSWORD
DB_PASSWORD=your_actual_postgres_password
```

### Create Database

```bash
# Open PostgreSQL command line
psql -U postgres

# In psql prompt, run:
CREATE DATABASE ide_logs;
\c ide_logs
\i C:/Users/ChamanPrakash/Downloads/windsurf logs/database/schema.sql
\q
```

Or use pgAdmin:
1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Name: `ide_logs`
4. Open Query Tool
5. Copy-paste contents of `database/schema.sql`
6. Execute (F5)

## Step 2: Install Python Dependencies (2 minutes)

```bash
cd "C:\Users\ChamanPrakash\Downloads\windsurf logs"

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Test Database Connection

```bash
python -c "import psycopg2; from dotenv import load_dotenv; import os; load_dotenv(); conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD')); print('✅ Database connected!'); conn.close()"
```

If this fails, double-check your PostgreSQL password in `.env`.

## Step 4: Run Log Scraper (1 minute)

```bash
python windsurf_to_langfuse.py
```

Expected output:
- ✅ Connected to PostgreSQL database
- ✅ Connected to Langfuse
- Processing sessions from both Windsurf and VS Code logs
- Data saved to database

## Step 5: Start Backend API (2 minutes)

Open a new terminal:

```bash
cd "C:\Users\ChamanPrakash\Downloads\windsurf logs\backend\IdeLogsApi"

# Update appsettings.json with your PostgreSQL password first!

# Run the API
dotnet run
```

Wait for: `Now listening on: http://localhost:5000`

## Step 6: Start Frontend Dashboard (2 minutes)

Open another new terminal:

```bash
cd "C:\Users\ChamanPrakash\Downloads\windsurf logs\frontend"

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

Wait for: `Local: http://localhost:5173/`

## Step 7: View Dashboard

Open browser to: **http://localhost:5173**

You should see:
- Summary cards with session counts
- Interactive charts
- Sessions table with your IDE logs

## Troubleshooting

### "Password authentication failed"
- Update `DB_PASSWORD` in `.env` file
- Update `Password` in `backend/IdeLogsApi/appsettings.json`
- Restart PostgreSQL service

### "Cannot connect to API"
- Ensure backend is running: `dotnet run` in backend/IdeLogsApi folder
- Check port 5000 is not in use
- Verify CORS settings allow localhost:5173

### "No logs found"
- Check if Windsurf/VS Code have been used
- Verify log directories exist
- Run IDEs to generate new logs

### "Frontend shows no data"
- Ensure backend API is running
- Check browser console for errors
- Verify API URL in frontend/.env

## Next Steps

1. **Schedule automatic scraping**: Set up Task Scheduler to run `run_windsurf_to_langfuse.bat` every 30 minutes
2. **Customize dashboard**: Modify frontend components to add custom metrics
3. **Set up monitoring**: Configure alerts for critical errors
4. **Deploy to production**: Follow SETUP_GUIDE.md for deployment instructions

## Success Checklist

- [ ] PostgreSQL database created with schema
- [ ] Python script runs without errors
- [ ] Backend API responds on port 5000
- [ ] Frontend displays on port 5173
- [ ] Dashboard shows your IDE session data
- [ ] Langfuse dashboard shows traces
- [ ] No duplicate sessions when running scraper twice

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review SETUP_GUIDE.md for detailed troubleshooting
3. Verify all services are running
4. Check log files for detailed errors
