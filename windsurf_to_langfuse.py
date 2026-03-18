"""
Windsurf Logs to Langfuse Integration Script
Parses Windsurf logs and sends metrics to Langfuse dashboard
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from langfuse import Langfuse
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values, Json

# Load environment variables
load_dotenv()

class LogParser:
    """Parse IDE log files and extract relevant metrics"""
    
    def __init__(self, logs_dir: str, source: str = 'windsurf'):
        self.logs_dir = Path(logs_dir)
        self.source = source
        self.log_pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(info|warning|error|debug)\] (.+)'
        )
        
    def get_log_sessions(self) -> List[Path]:
        """Get all log session directories"""
        sessions = []
        for item in self.logs_dir.iterdir():
            if item.is_dir() and re.match(r'\d{8}T\d{6}', item.name):
                sessions.append(item)
        return sorted(sessions)
    
    def parse_log_file(self, log_file: Path) -> List[Dict]:
        """Parse a single log file and extract events"""
        events = []
        
        if not log_file.exists() or log_file.stat().st_size == 0:
            return events
            
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    match = self.log_pattern.match(line.strip())
                    if match:
                        timestamp_str, level, message = match.groups()
                        events.append({
                            'timestamp': timestamp_str,
                            'level': level,
                            'message': message,
                            'source': log_file.name
                        })
        except Exception as e:
            print(f"Error parsing {log_file}: {e}")
            
        return events
    
    def parse_session(self, session_dir: Path) -> Dict:
        """Parse all logs in a session directory"""
        session_data = {
            'session_id': session_dir.name,
            'source': self.source,
            'timestamp': self._parse_session_timestamp(session_dir.name),
            'events': [],
            'errors': [],
            'warnings': [],
            'info': [],
            'workspaces': set(),
            'extensions': set(),
            'user_id': None,
            'input_tokens': 0,
            'output_tokens': 0,
            'total_tokens': 0
        }
        
        # Parse main logs
        for log_file in session_dir.glob('*.log'):
            events = self.parse_log_file(log_file)
            session_data['events'].extend(events)
            
        # Parse window logs
        window_dir = session_dir / 'window1'
        if window_dir.exists():
            for log_file in window_dir.glob('*.log'):
                events = self.parse_log_file(log_file)
                session_data['events'].extend(events)
        
        # Categorize events and extract metadata
        for event in session_data['events']:
            level = event['level']
            if level == 'error':
                session_data['errors'].append(event)
            elif level == 'warning':
                session_data['warnings'].append(event)
            elif level == 'info':
                session_data['info'].append(event)
            
            # Extract workspace info
            if 'workspaceUri' in event['message']:
                try:
                    workspace_match = re.search(r'"fsPath":"([^"]+)"', event['message'])
                    if workspace_match:
                        session_data['workspaces'].add(workspace_match.group(1))
                except:
                    pass
            
            # Extract extension info
            if 'Extension' in event['message']:
                ext_match = re.search(r"Extension '([^']+)'", event['message'])
                if ext_match:
                    session_data['extensions'].add(ext_match.group(1))
            
            # Extract token usage if present
            token_patterns = [
                (r'"?input_tokens?"?\s*:\s*(\d+)', 'input_tokens'),
                (r'"?output_tokens?"?\s*:\s*(\d+)', 'output_tokens'),
                (r'"?total_tokens?"?\s*:\s*(\d+)', 'total_tokens'),
            ]
            for pattern, field in token_patterns:
                match = re.search(pattern, event['message'], re.IGNORECASE)
                if match:
                    session_data[field] += int(match.group(1))
            
            # Extract user ID if present
            user_patterns = [
                r'"?user_?id"?\s*:\s*"([^"]+)"',
                r'"?userId"?\s*:\s*"([^"]+)"',
            ]
            for pattern in user_patterns:
                match = re.search(pattern, event['message'], re.IGNORECASE)
                if match and not session_data['user_id']:
                    session_data['user_id'] = match.group(1)
        
        session_data['workspaces'] = list(session_data['workspaces'])
        session_data['extensions'] = list(session_data['extensions'])
        
        # Extract user from workspace path if user_id not found
        if not session_data['user_id'] and session_data['workspaces']:
            for workspace in session_data['workspaces']:
                # Normalize path separators (handle escaped backslashes)
                normalized = workspace.replace('\\\\', '\\').replace('/', '\\')
                # Extract username from Windows path (C:\Users\Username\...)
                user_match = re.search(r'\\Users\\([^\\]+)\\', normalized, re.IGNORECASE)
                if user_match:
                    session_data['user_id'] = user_match.group(1)
                    break
        
        return session_data
    
    def _parse_session_timestamp(self, session_name: str) -> str:
        """Convert session name to ISO timestamp"""
        try:
            dt = datetime.strptime(session_name, '%Y%m%dT%H%M%S')
            return dt.isoformat()
        except:
            return session_name


class DatabaseManager:
    """Manage PostgreSQL database operations"""
    
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'ide_logs'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        self.conn.autocommit = False
    
    def _generate_event_hash(self, session_id: str, timestamp: str, message: str) -> str:
        """Generate unique hash for event to prevent duplicates"""
        content = f"{session_id}:{timestamp}:{message}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def session_exists(self, session_id: str, source: str) -> bool:
        """Check if session already exists in database"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS(SELECT 1 FROM sessions WHERE session_id = %s AND source = %s)",
                (session_id, source)
            )
            return cur.fetchone()[0]
    
    def insert_session(self, session_data: Dict, langfuse_trace_id: str = None) -> str:
        """Insert session into database, returns session UUID"""
        with self.conn.cursor() as cur:
            # Calculate session duration
            duration = self._calculate_duration_seconds(session_data['events'])
            
            cur.execute("""
                INSERT INTO sessions (
                    session_id, source, timestamp, workspaces, extensions,
                    total_events, error_count, warning_count, info_count,
                    health_status, session_duration_seconds, langfuse_trace_id,
                    user_id, input_tokens, output_tokens, total_tokens
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id, source) DO UPDATE SET
                    total_events = EXCLUDED.total_events,
                    error_count = EXCLUDED.error_count,
                    warning_count = EXCLUDED.warning_count,
                    info_count = EXCLUDED.info_count,
                    health_status = EXCLUDED.health_status,
                    session_duration_seconds = EXCLUDED.session_duration_seconds,
                    langfuse_trace_id = EXCLUDED.langfuse_trace_id,
                    user_id = EXCLUDED.user_id,
                    input_tokens = EXCLUDED.input_tokens,
                    output_tokens = EXCLUDED.output_tokens,
                    total_tokens = EXCLUDED.total_tokens,
                    updated_at = NOW()
                RETURNING id
            """, (
                session_data['session_id'],
                session_data['source'],
                session_data['timestamp'],
                session_data['workspaces'],
                session_data['extensions'],
                len(session_data['events']),
                len(session_data['errors']),
                len(session_data['warnings']),
                len(session_data['info']),
                self._calculate_health_status(session_data),
                duration,
                langfuse_trace_id,
                session_data.get('user_id'),
                session_data.get('input_tokens', 0),
                session_data.get('output_tokens', 0),
                session_data.get('total_tokens', 0)
            ))
            session_uuid = cur.fetchone()[0]
            self.conn.commit()
            return str(session_uuid)
    
    def insert_events(self, session_uuid: str, events: List[Dict]):
        """Insert events into database with duplicate detection"""
        if not events:
            return
        
        with self.conn.cursor() as cur:
            event_data = []
            for event in events:
                event_hash = self._generate_event_hash(
                    session_uuid,
                    event['timestamp'],
                    event['message']
                )
                event_data.append((
                    session_uuid,
                    event['timestamp'],
                    event['level'],
                    event['message'][:5000],
                    event.get('source', ''),
                    event_hash,
                    Json(event.get('metadata', {}))
                ))
            
            execute_values(
                cur,
                """
                INSERT INTO events (session_id, timestamp, level, message, source_file, event_hash, metadata)
                VALUES %s
                ON CONFLICT (event_hash) DO NOTHING
                """,
                event_data
            )
            self.conn.commit()
    
    def _calculate_duration_seconds(self, events: List[Dict]) -> float:
        """Calculate session duration in seconds"""
        if not events:
            return 0.0
        try:
            first = datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            last = datetime.strptime(events[-1]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            return (last - first).total_seconds()
        except:
            return 0.0
    
    def _calculate_health_status(self, session_data: Dict) -> str:
        """Calculate overall health status"""
        error_count = len(session_data['errors'])
        warning_count = len(session_data['warnings'])
        
        if error_count > 10:
            return 'critical'
        elif error_count > 5 or warning_count > 20:
            return 'warning'
        elif error_count > 0:
            return 'minor_issues'
        else:
            return 'healthy'
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class LangfuseIntegration:
    """Send parsed IDE logs to Langfuse"""
    
    def __init__(self):
        self.langfuse = Langfuse(
            secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
            public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
            host=os.getenv('LANGFUSE_BASE_URL')
        )
        
    def send_session_trace(self, session_data: Dict):
        """Send a session as a trace to Langfuse"""
        
        source = session_data.get('source', 'windsurf')
        # Create main trace for the session
        trace = self.langfuse.start_observation(
            name=f"{source}_session_{session_data['session_id']}",
            as_type="trace",
            input={
                "session_id": session_data['session_id'],
                "source": source,
                "timestamp": session_data['timestamp'],
                "workspaces": session_data['workspaces'],
                "extensions": session_data['extensions']
            },
            metadata={
                "total_events": len(session_data['events']),
                "error_count": len(session_data['errors']),
                "warning_count": len(session_data['warnings']),
                "info_count": len(session_data['info']),
                "tags": [source, "ide", "logs"]
            }
        )
        
        # Add error events as spans
        for idx, error in enumerate(session_data['errors'][:50]):  # Limit to 50 errors
            error_span = trace.start_observation(
                name=f"error_{idx}",
                as_type="span"
            )
            error_span.update(
                input={"message": error['message'][:500], "source": error['source']},
                metadata={"level": "error"},
                level="ERROR"
            )
            error_span.end()
        
        # Add warning events as spans
        for idx, warning in enumerate(session_data['warnings'][:30]):  # Limit to 30 warnings
            warning_span = trace.start_observation(
                name=f"warning_{idx}",
                as_type="span"
            )
            warning_span.update(
                input={"message": warning['message'][:500], "source": warning['source']},
                metadata={"level": "warning"},
                level="WARNING"
            )
            warning_span.end()
        
        # Add session summary as generation
        summary_gen = trace.start_observation(
            name="session_summary",
            as_type="generation"
        )
        summary_gen.update(
            model=f"{session_data.get('source', 'windsurf')}_ide",
            output={
                "session_duration": self._calculate_duration(session_data['events']),
                "unique_workspaces": len(session_data['workspaces']),
                "unique_extensions": len(session_data['extensions']),
                "health_status": self._calculate_health_status(session_data)
            }
        )
        summary_gen.end()
        
        # End the trace
        trace.end()
        
        return trace
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime"""
        try:
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        except:
            return datetime.now()
    
    def _calculate_duration(self, events: List[Dict]) -> str:
        """Calculate session duration from events"""
        if not events:
            return "0s"
        
        try:
            first = self._parse_timestamp(events[0]['timestamp'])
            last = self._parse_timestamp(events[-1]['timestamp'])
            duration = (last - first).total_seconds()
            return f"{duration:.1f}s"
        except:
            return "unknown"
    
    def _calculate_health_status(self, session_data: Dict) -> str:
        """Calculate overall health status"""
        error_count = len(session_data['errors'])
        warning_count = len(session_data['warnings'])
        
        if error_count > 10:
            return "critical"
        elif error_count > 5 or warning_count > 20:
            return "warning"
        elif error_count > 0:
            return "minor_issues"
        else:
            return "healthy"
    
    def flush(self):
        """Flush all pending events to Langfuse"""
        self.langfuse.flush()


def process_logs(logs_dir: str, source: str, db_manager: DatabaseManager, langfuse_integration: LangfuseIntegration):
    """Process logs from a specific directory"""
    parser = LogParser(logs_dir, source)
    sessions = parser.get_log_sessions()
    
    print(f"\n📂 Processing {source} logs from: {logs_dir}")
    print(f"📊 Found {len(sessions)} log sessions")
    
    if not sessions:
        print(f"   ⚠️  No log sessions found for {source}")
        return 0, 0, 0
    
    processed = 0
    skipped = 0
    failed = 0
    
    for session_dir in sessions:
        try:
            session_data = parser.parse_session(session_dir)
            
            if not session_data['events']:
                skipped += 1
                continue
            
            # Check if session already exists
            if db_manager.session_exists(session_data['session_id'], source):
                print(f"   ⏭️  Skipping {session_dir.name} (already in database)")
                skipped += 1
                continue
            
            print(f"\n🔄 Processing session: {session_dir.name}")
            print(f"   📝 Events: {len(session_data['events'])} "
                  f"(Errors: {len(session_data['errors'])}, "
                  f"Warnings: {len(session_data['warnings'])})")
            
            # Send to Langfuse
            trace = langfuse_integration.send_session_trace(session_data)
            trace_id = trace.id if hasattr(trace, 'id') else None
            print(f"   ✅ Sent to Langfuse (Trace ID: {trace_id})")
            
            # Insert into database
            session_uuid = db_manager.insert_session(session_data, trace_id)
            db_manager.insert_events(session_uuid, session_data['events'])
            print(f"   💾 Saved to database (Session UUID: {session_uuid})")
            
            processed += 1
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    return processed, skipped, failed


def main():
    """Main execution function"""
    
    # Configuration
    WINDSURF_LOGS_DIR = r"C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs"
    VSCODE_LOGS_DIR = r"C:\Users\ChamanPrakash\AppData\Roaming\Code\logs"
    
    print("=" * 70)
    print("IDE Logs to Langfuse & PostgreSQL Integration")
    print("=" * 70)
    
    # Verify environment variables
    required_vars = ['LANGFUSE_SECRET_KEY', 'LANGFUSE_PUBLIC_KEY', 'LANGFUSE_BASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\n❌ Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment")
        return
    
    # Initialize integrations
    db_manager = None
    langfuse_integration = None
    
    try:
        db_manager = DatabaseManager()
        print("✅ Connected to PostgreSQL database")
        
        langfuse_integration = LangfuseIntegration()
        print("✅ Connected to Langfuse")
        
        total_processed = 0
        total_skipped = 0
        total_failed = 0
        
        # Process Windsurf logs
        if os.path.exists(WINDSURF_LOGS_DIR):
            processed, skipped, failed = process_logs(
                WINDSURF_LOGS_DIR, 'windsurf', db_manager, langfuse_integration
            )
            total_processed += processed
            total_skipped += skipped
            total_failed += failed
        else:
            print(f"\n⚠️  Windsurf logs directory not found: {WINDSURF_LOGS_DIR}")
        
        # Process VS Code Copilot logs
        if os.path.exists(VSCODE_LOGS_DIR):
            processed, skipped, failed = process_logs(
                VSCODE_LOGS_DIR, 'vscode_copilot', db_manager, langfuse_integration
            )
            total_processed += processed
            total_skipped += skipped
            total_failed += failed
        else:
            print(f"\n⚠️  VS Code logs directory not found: {VSCODE_LOGS_DIR}")
        
        # Flush all events to Langfuse
        print("\n🔄 Flushing events to Langfuse...")
        langfuse_integration.flush()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Summary")
        print("=" * 70)
        print(f"✅ Successfully processed: {total_processed} sessions")
        print(f"⏭️  Skipped (duplicates/empty): {total_skipped} sessions")
        if total_failed > 0:
            print(f"❌ Failed: {total_failed} sessions")
        print(f"\n🌐 View your metrics at: {os.getenv('LANGFUSE_BASE_URL')}")
        print("💾 Data saved to PostgreSQL database")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db_manager:
            db_manager.close()
            print("\n🔌 Database connection closed")


if __name__ == "__main__":
    main()
