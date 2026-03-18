#!/usr/bin/env python3
"""
Update existing sessions with user_id extracted from workspace paths
"""

import psycopg2
from dotenv import load_dotenv
import os
import re

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cur = conn.cursor()

# Get all sessions with workspaces but no user_id
cur.execute("""
    SELECT id, session_id, workspaces 
    FROM sessions 
    WHERE user_id IS NULL 
    AND workspaces IS NOT NULL 
    AND array_length(workspaces, 1) > 0
""")

sessions = cur.fetchall()
print(f"Found {len(sessions)} sessions to update")

updated = 0
for session_id, session_name, workspaces in sessions:
    user_id = None
    
    # Try to extract user from workspace paths
    for workspace in workspaces:
        # Normalize path separators
        normalized = workspace.replace('\\\\', '\\').replace('/', '\\')
        # Extract username from Windows path (C:\Users\Username\...)
        user_match = re.search(r'\\Users\\([^\\]+)\\', normalized, re.IGNORECASE)
        if user_match:
            user_id = user_match.group(1)
            print(f"  Extracted user '{user_id}' from: {workspace[:50]}...")
            break
    
    if user_id:
        cur.execute("""
            UPDATE sessions 
            SET user_id = %s 
            WHERE id = %s
        """, (user_id, session_id))
        updated += 1
        print(f"Updated session {session_name} with user_id: {user_id}")

conn.commit()
print(f"\n✅ Updated {updated} sessions with user_id")

# Verify
cur.execute("SELECT COUNT(*) FROM sessions WHERE user_id IS NOT NULL")
count = cur.fetchone()[0]
print(f"Total sessions with user_id: {count}")

conn.close()
