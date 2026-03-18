#!/usr/bin/env python3
"""
Database Setup Script
Creates the database and runs the schema
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the ide_logs database"""
    print("Creating database...")
    
    # Connect to PostgreSQL server (not to a specific database)
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'admin')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    cur = conn.cursor()
    
    # Drop database if exists
    try:
        cur.execute("DROP DATABASE IF EXISTS ide_logs;")
        print("✅ Dropped existing database (if any)")
    except Exception as e:
        print(f"⚠️  Could not drop database: {e}")
    
    # Create database
    try:
        cur.execute("CREATE DATABASE ide_logs;")
        print("✅ Created database 'ide_logs'")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    cur.close()
    conn.close()
    return True

def run_schema():
    """Run the schema SQL file"""
    print("\nRunning database schema...")
    
    # Connect to the ide_logs database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database='ide_logs',
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'admin')
    )
    
    cur = conn.cursor()
    
    # Read and execute schema file
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cur.execute(schema_sql)
        conn.commit()
        print("✅ Schema created successfully")
        
        # Verify tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running schema: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("="*60)
    print("PostgreSQL Database Setup")
    print("="*60)
    
    try:
        if create_database():
            if run_schema():
                print("\n" + "="*60)
                print("✅ Database setup completed successfully!")
                print("="*60)
                return 0
        
        print("\n" + "="*60)
        print("❌ Database setup failed")
        print("="*60)
        return 1
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
