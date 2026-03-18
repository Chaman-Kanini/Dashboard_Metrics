#!/usr/bin/env python3
"""
System Test Script for IDE Logs Dashboard
Tests all components: Database, Python Scraper, Backend API, and Frontend
"""

import os
import sys
import time
import json
import psycopg2
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def test_database_connection():
    """Test PostgreSQL database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'ide_logs'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        print_success("Connected to PostgreSQL database")
        
        cur = conn.cursor()
        
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print_info(f"PostgreSQL version: {version.split(',')[0]}")
        
        cur.execute("SELECT COUNT(*) FROM sessions")
        session_count = cur.fetchone()[0]
        print_info(f"Total sessions in database: {session_count}")
        
        cur.execute("SELECT COUNT(*) FROM events")
        event_count = cur.fetchone()[0]
        print_info(f"Total events in database: {event_count}")
        
        cur.execute("""
            SELECT source, COUNT(*) 
            FROM sessions 
            GROUP BY source
        """)
        for row in cur.fetchall():
            print_info(f"  - {row[0]}: {row[1]} sessions")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return False

def test_database_schema():
    """Test database schema integrity"""
    print("\n" + "="*60)
    print("TEST 2: Database Schema")
    print("="*60)
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'ide_logs'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cur = conn.cursor()
        
        required_tables = ['sessions', 'events', 'metrics']
        for table in required_tables:
            cur.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                );
            """)
            exists = cur.fetchone()[0]
            if exists:
                print_success(f"Table '{table}' exists")
            else:
                print_error(f"Table '{table}' missing")
                return False
        
        cur.execute("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename IN ('sessions', 'events', 'metrics')
        """)
        indexes = [row[0] for row in cur.fetchall()]
        print_info(f"Found {len(indexes)} indexes")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Schema validation failed: {e}")
        return False

def test_backend_api():
    """Test .NET backend API"""
    print("\n" + "="*60)
    print("TEST 3: Backend API")
    print("="*60)
    
    api_url = "http://localhost:5000/api"
    
    try:
        response = requests.get(f"{api_url}/dashboard/stats", timeout=5)
        if response.status_code == 200:
            print_success("API is responding")
            data = response.json()
            print_info(f"Total sessions: {data.get('totalSessions', 0)}")
            print_info(f"Total events: {data.get('totalEvents', 0)}")
            print_info(f"Recent errors (24h): {data.get('recentErrors', 0)}")
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the backend running on port 5000?")
        return False
    except Exception as e:
        print_error(f"API test failed: {e}")
        return False
    
    endpoints = [
        '/dashboard/summary',
        '/dashboard/sessions?limit=5',
        '/dashboard/timeseries?days=7',
        '/dashboard/health-distribution'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{api_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print_success(f"Endpoint {endpoint} working")
            else:
                print_warning(f"Endpoint {endpoint} returned {response.status_code}")
        except Exception as e:
            print_error(f"Endpoint {endpoint} failed: {e}")
    
    return True

def test_frontend():
    """Test React frontend"""
    print("\n" + "="*60)
    print("TEST 4: Frontend")
    print("="*60)
    
    frontend_url = "http://localhost:5173"
    
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print_success("Frontend is accessible")
            print_info(f"Frontend URL: {frontend_url}")
        else:
            print_error(f"Frontend returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend. Is it running on port 5173?")
        print_info("Run: cd frontend && npm run dev")
        return False
    except Exception as e:
        print_error(f"Frontend test failed: {e}")
        return False
    
    return True

def test_log_directories():
    """Test if log directories exist"""
    print("\n" + "="*60)
    print("TEST 5: Log Directories")
    print("="*60)
    
    windsurf_logs = r"C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs"
    vscode_logs = r"C:\Users\ChamanPrakash\AppData\Roaming\Code\logs"
    
    all_exist = True
    
    if os.path.exists(windsurf_logs):
        print_success(f"Windsurf logs directory exists")
        sessions = [d for d in os.listdir(windsurf_logs) if os.path.isdir(os.path.join(windsurf_logs, d))]
        print_info(f"Found {len(sessions)} Windsurf session directories")
    else:
        print_warning(f"Windsurf logs directory not found: {windsurf_logs}")
        all_exist = False
    
    if os.path.exists(vscode_logs):
        print_success(f"VS Code logs directory exists")
        sessions = [d for d in os.listdir(vscode_logs) if os.path.isdir(os.path.join(vscode_logs, d))]
        print_info(f"Found {len(sessions)} VS Code session directories")
    else:
        print_warning(f"VS Code logs directory not found: {vscode_logs}")
        all_exist = False
    
    return all_exist

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("\n" + "="*60)
    print("TEST 6: Environment Variables")
    print("="*60)
    
    required_vars = {
        'DB_HOST': 'Database host',
        'DB_PORT': 'Database port',
        'DB_NAME': 'Database name',
        'DB_USER': 'Database user',
        'DB_PASSWORD': 'Database password',
        'LANGFUSE_SECRET_KEY': 'Langfuse secret key',
        'LANGFUSE_PUBLIC_KEY': 'Langfuse public key',
        'LANGFUSE_BASE_URL': 'Langfuse base URL'
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = value[:10] + '...' if len(value) > 10 else value
            print_success(f"{var} is set ({description})")
        else:
            print_error(f"{var} is not set ({description})")
            all_set = False
    
    return all_set

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("IDE LOGS DASHBOARD - SYSTEM TEST")
    print("="*70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Environment Variables': test_environment_variables(),
        'Database Connection': test_database_connection(),
        'Database Schema': test_database_schema(),
        'Log Directories': test_log_directories(),
        'Backend API': test_backend_api(),
        'Frontend': test_frontend()
    }
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.RESET} - {test_name}")
    
    print("\n" + "="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! System is ready to use.")
        print_info("\nNext steps:")
        print_info("1. Run: python windsurf_to_langfuse.py")
        print_info("2. Open: http://localhost:5173")
        print_info("3. Check: https://cloud.langfuse.com")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
