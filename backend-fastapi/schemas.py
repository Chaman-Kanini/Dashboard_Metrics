from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DashboardSummary(BaseModel):
    source: str
    total_sessions: int
    total_events: int
    total_errors: int
    total_warnings: int
    total_info: int
    avg_duration: Optional[float] = None
    unique_workspaces: int
    healthy_sessions: int
    warning_sessions: int
    critical_sessions: int
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    unique_users: int
    
    class Config:
        orm_mode = True

class SessionResponse(BaseModel):
    id: str
    session_id: str
    source: str
    timestamp: datetime
    total_events: int
    error_count: int
    warning_count: int
    health_status: Optional[str] = None
    session_duration_seconds: Optional[float] = None
    workspaces: Optional[List[str]] = None
    extensions: Optional[List[str]] = None
    user_id: Optional[str] = None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    
    class Config:
        orm_mode = True

class EventResponse(BaseModel):
    id: str
    timestamp: datetime
    level: str
    message: str
    source_file: Optional[str] = None
    
    class Config:
        orm_mode = True

class TimeSeriesData(BaseModel):
    date: datetime
    source: str
    session_count: int
    error_count: int
    warning_count: int
    
    class Config:
        orm_mode = True

class HealthDistribution(BaseModel):
    source: str
    health_status: str
    count: int
    
    class Config:
        orm_mode = True

class Stats(BaseModel):
    total_sessions: int
    total_events: int
    recent_errors: int
    last_updated: Optional[datetime] = None
    
    class Config:
        orm_mode = True
