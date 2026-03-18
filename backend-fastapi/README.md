# FastAPI Backend for Dashboard Metrics

Python FastAPI backend for IDE Logs Dashboard.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update `.env` with your Supabase connection string

4. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

5. Access API docs: http://localhost:8000/docs

## Deployment to Render

This backend is configured for easy deployment to Render's free tier.

### Environment Variables Required:
- `DATABASE_URL`: Your Supabase connection string
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (your Vercel URL)

### Render will automatically:
- Detect Python runtime
- Install dependencies from requirements.txt
- Start the server with uvicorn

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/dashboard/summary` - Dashboard summary statistics
- `GET /api/dashboard/sessions` - Recent sessions (with optional filters)
- `GET /api/dashboard/sessions/{id}/events` - Events for a specific session
- `GET /api/dashboard/timeseries` - Time series data
- `GET /api/dashboard/health-distribution` - Health status distribution
- `GET /api/dashboard/stats` - Overall statistics
