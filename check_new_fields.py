import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cur = conn.cursor()

# Check if new columns exist and have data
cur.execute("""
    SELECT session_id, source, user_id, total_tokens, input_tokens, output_tokens 
    FROM sessions 
    LIMIT 5
""")

print("Sample sessions with new fields:")
print("="*100)
print(f"{'Session ID':<20} {'Source':<15} {'User ID':<20} {'Total':<10} {'Input':<10} {'Output':<10}")
print("-"*100)

for row in cur.fetchall():
    session_id, source, user_id, total_tokens, input_tokens, output_tokens = row
    print(f"{session_id[:18]:<20} {source:<15} {user_id or 'None':<20} {total_tokens:<10} {input_tokens:<10} {output_tokens:<10}")

print("\n" + "="*100)
print("Summary:")
cur.execute("SELECT COUNT(*) FROM sessions WHERE user_id IS NOT NULL")
user_count = cur.fetchone()[0]
print(f"Sessions with user_id: {user_count}")

cur.execute("SELECT COUNT(*) FROM sessions WHERE total_tokens > 0")
token_count = cur.fetchone()[0]
print(f"Sessions with tokens: {token_count}")

conn.close()
