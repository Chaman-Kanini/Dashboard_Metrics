from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker, Session
from models import Base, SessionModel, EventModel, MetricModel
from schemas import (
    DashboardSummary,
    SessionResponse,
    EventResponse,
    TimeSeriesData,
    HealthDistribution,
    Stats
)

load_dotenv()

app = FastAPI(title="IDE Logs Dashboard API", version="1.0.0")

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
origins = ["http://localhost:5173", "http://localhost:3000"] + allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "IDE Logs Dashboard API", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/dashboard/summary", response_model=List[DashboardSummary])
def get_summary():
    db = next(get_db())
    try:
        sessions = db.query(SessionModel).all()
        
        # Group by source
        summary_dict = {}
        for session in sessions:
            source = session.source
            if source not in summary_dict:
                summary_dict[source] = {
                    "sessions": [],
                    "total_sessions": 0,
                    "total_events": 0,
                    "total_errors": 0,
                    "total_warnings": 0,
                    "total_info": 0,
                    "healthy_sessions": 0,
                    "warning_sessions": 0,
                    "critical_sessions": 0,
                    "total_input_tokens": 0,
                    "total_output_tokens": 0,
                    "total_tokens": 0,
                    "unique_users": set(),
                    "unique_workspaces": set()
                }
            
            summary_dict[source]["sessions"].append(session)
            summary_dict[source]["total_sessions"] += 1
            summary_dict[source]["total_events"] += session.total_events or 0
            summary_dict[source]["total_errors"] += session.error_count or 0
            summary_dict[source]["total_warnings"] += session.warning_count or 0
            summary_dict[source]["total_info"] += session.info_count or 0
            summary_dict[source]["total_input_tokens"] += session.input_tokens or 0
            summary_dict[source]["total_output_tokens"] += session.output_tokens or 0
            summary_dict[source]["total_tokens"] += session.total_tokens or 0
            
            if session.health_status == "healthy":
                summary_dict[source]["healthy_sessions"] += 1
            elif session.health_status in ["warning", "minor_issues"]:
                summary_dict[source]["warning_sessions"] += 1
            elif session.health_status == "critical":
                summary_dict[source]["critical_sessions"] += 1
            
            if session.user_id:
                summary_dict[source]["unique_users"].add(session.user_id)
            
            if session.workspaces:
                for workspace in session.workspaces:
                    summary_dict[source]["unique_workspaces"].add(workspace)
        
        # Build response
        result = []
        for source, data in summary_dict.items():
            avg_duration = sum(s.session_duration_seconds or 0 for s in data["sessions"]) / len(data["sessions"]) if data["sessions"] else 0
            
            result.append(DashboardSummary(
                source=source,
                total_sessions=data["total_sessions"],
                total_events=data["total_events"],
                total_errors=data["total_errors"],
                total_warnings=data["total_warnings"],
                total_info=data["total_info"],
                avg_duration=avg_duration,
                unique_workspaces=len(data["unique_workspaces"]),
                healthy_sessions=data["healthy_sessions"],
                warning_sessions=data["warning_sessions"],
                critical_sessions=data["critical_sessions"],
                total_input_tokens=data["total_input_tokens"],
                total_output_tokens=data["total_output_tokens"],
                total_tokens=data["total_tokens"],
                unique_users=len(data["unique_users"])
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/dashboard/sessions", response_model=List[SessionResponse])
def get_recent_sessions(
    limit: int = Query(50, ge=1, le=200),
    source: Optional[str] = None
):
    db = next(get_db())
    try:
        query = db.query(SessionModel)
        
        if source:
            query = query.filter(SessionModel.source == source)
        
        sessions = query.order_by(SessionModel.timestamp.desc()).limit(limit).all()
        
        return [SessionResponse(
            id=str(s.id),
            session_id=s.session_id,
            source=s.source,
            timestamp=s.timestamp,
            total_events=s.total_events,
            error_count=s.error_count,
            warning_count=s.warning_count,
            health_status=s.health_status,
            session_duration_seconds=s.session_duration_seconds,
            workspaces=s.workspaces,
            extensions=s.extensions,
            user_id=s.user_id,
            input_tokens=s.input_tokens,
            output_tokens=s.output_tokens,
            total_tokens=s.total_tokens
        ) for s in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/dashboard/sessions/{session_id}/events", response_model=List[EventResponse])
def get_session_events(session_id: str):
    db = next(get_db())
    try:
        events = db.query(EventModel).filter(
            EventModel.session_id == session_id
        ).order_by(EventModel.timestamp).all()
        
        return [EventResponse(
            id=str(e.id),
            timestamp=e.timestamp,
            level=e.level,
            message=e.message,
            source_file=e.source_file
        ) for e in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/dashboard/timeseries", response_model=List[TimeSeriesData])
def get_timeseries(days: int = Query(7, ge=1, le=90)):
    db = next(get_db())
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        sessions = db.query(SessionModel).filter(
            SessionModel.timestamp >= start_date
        ).all()
        
        # Group by date and source
        timeseries_dict = {}
        for session in sessions:
            date_key = session.timestamp.date()
            source = session.source
            key = (date_key, source)
            
            if key not in timeseries_dict:
                timeseries_dict[key] = {
                    "session_count": 0,
                    "error_count": 0,
                    "warning_count": 0
                }
            
            timeseries_dict[key]["session_count"] += 1
            timeseries_dict[key]["error_count"] += session.error_count or 0
            timeseries_dict[key]["warning_count"] += session.warning_count or 0
        
        result = []
        for (date, source), data in timeseries_dict.items():
            result.append(TimeSeriesData(
                date=datetime.combine(date, datetime.min.time()),
                source=source,
                session_count=data["session_count"],
                error_count=data["error_count"],
                warning_count=data["warning_count"]
            ))
        
        return sorted(result, key=lambda x: x.date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/dashboard/health-distribution", response_model=List[HealthDistribution])
def get_health_distribution():
    db = next(get_db())
    try:
        sessions = db.query(SessionModel).all()
        
        # Group by source and health status
        distribution_dict = {}
        for session in sessions:
            source = session.source
            health_status = session.health_status or "unknown"
            key = (source, health_status)
            
            if key not in distribution_dict:
                distribution_dict[key] = 0
            
            distribution_dict[key] += 1
        
        result = []
        for (source, health_status), count in distribution_dict.items():
            result.append(HealthDistribution(
                source=source,
                health_status=health_status,
                count=count
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/dashboard/stats", response_model=Stats)
def get_stats():
    db = next(get_db())
    try:
        total_sessions = db.query(SessionModel).count()
        total_events = db.query(EventModel).count()
        
        # Recent errors (last 24 hours)
        recent_errors = db.query(EventModel).filter(
            EventModel.level == "error",
            EventModel.timestamp >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        # Last updated
        last_updated = db.query(func.max(SessionModel.updated_at)).scalar()
        
        return Stats(
            total_sessions=total_sessions,
            total_events=total_events,
            recent_errors=recent_errors,
            last_updated=last_updated
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
