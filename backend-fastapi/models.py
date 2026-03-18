from sqlalchemy import Column, String, Integer, DateTime, ARRAY, Numeric, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class SessionModel(Base):
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    workspaces = Column(ARRAY(Text), nullable=True)
    extensions = Column(ARRAY(Text), nullable=True)
    total_events = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    health_status = Column(String(50), nullable=True)
    session_duration_seconds = Column(Numeric(10, 2), nullable=True)
    langfuse_trace_id = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    events = relationship("EventModel", back_populates="session")

class EventModel(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    source_file = Column(String(255), nullable=True)
    event_hash = Column(String(64), nullable=False, unique=True)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("SessionModel", back_populates="events")

class MetricModel(Base):
    __tablename__ = "metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_date = Column(DateTime, nullable=False)
    source = Column(String(50), nullable=False)
    total_sessions = Column(Integer, default=0)
    total_events = Column(Integer, default=0)
    total_errors = Column(Integer, default=0)
    total_warnings = Column(Integer, default=0)
    avg_session_duration = Column(Numeric(10, 2), nullable=True)
    unique_workspaces = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
