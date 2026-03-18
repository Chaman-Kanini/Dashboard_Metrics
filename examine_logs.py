#!/usr/bin/env python3
"""
Examine log files to find token and user ID patterns
"""

from pathlib import Path
import re

def examine_logs():
    # Windsurf logs
    windsurf_dir = Path(r"C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs")
    vscode_dir = Path(r"C:\Users\ChamanPrakash\AppData\Roaming\Code\logs")
    
    print("="*80)
    print("EXAMINING WINDSURF LOGS")
    print("="*80)
    
    sessions = sorted([d for d in windsurf_dir.iterdir() if d.is_dir()])
    if sessions:
        session = sessions[0]
        print(f"\nSession: {session.name}")
        
        for log_file in list(session.glob('*.log'))[:2]:
            print(f"\n{'='*80}")
            print(f"File: {log_file.name}")
            print(f"{'='*80}")
            
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for token patterns
                    token_patterns = [
                        r'token[s]?\s*[:=]\s*(\d+)',
                        r'(\d+)\s*token[s]?',
                        r'input_tokens?\s*[:=]\s*(\d+)',
                        r'output_tokens?\s*[:=]\s*(\d+)',
                        r'total_tokens?\s*[:=]\s*(\d+)',
                        r'"tokens?"\s*:\s*(\d+)',
                    ]
                    
                    print("\n--- TOKEN MATCHES ---")
                    for pattern in token_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"Pattern '{pattern}': {matches[:5]}")
                    
                    # Look for user ID patterns
                    user_patterns = [
                        r'user[_-]?id\s*[:=]\s*["\']?([a-zA-Z0-9-]+)["\']?',
                        r'"userId?"\s*:\s*"([^"]+)"',
                        r'user:\s*([a-zA-Z0-9-]+)',
                    ]
                    
                    print("\n--- USER ID MATCHES ---")
                    for pattern in user_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"Pattern '{pattern}': {matches[:5]}")
                    
                    # Show sample lines with 'token' or 'user'
                    print("\n--- SAMPLE LINES WITH 'TOKEN' ---")
                    lines_with_token = [line for line in content.split('\n') if 'token' in line.lower()]
                    for line in lines_with_token[:5]:
                        print(line[:200])
                    
                    print("\n--- SAMPLE LINES WITH 'USER' ---")
                    lines_with_user = [line for line in content.split('\n') if 'user' in line.lower()]
                    for line in lines_with_user[:5]:
                        print(line[:200])
                        
            except Exception as e:
                print(f"Error reading {log_file.name}: {e}")
    
    print("\n" + "="*80)
    print("EXAMINING VS CODE LOGS")
    print("="*80)
    
    sessions = sorted([d for d in vscode_dir.iterdir() if d.is_dir()])
    if sessions:
        session = sessions[-1]  # Get most recent
        print(f"\nSession: {session.name}")
        
        for log_file in list(session.glob('*.log'))[:2]:
            print(f"\n{'='*80}")
            print(f"File: {log_file.name}")
            print(f"{'='*80}")
            
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Show sample lines with 'token' or 'user'
                    print("\n--- SAMPLE LINES WITH 'TOKEN' ---")
                    lines_with_token = [line for line in content.split('\n') if 'token' in line.lower()]
                    for line in lines_with_token[:5]:
                        print(line[:200])
                    
                    print("\n--- SAMPLE LINES WITH 'USER' ---")
                    lines_with_user = [line for line in content.split('\n') if 'user' in line.lower()]
                    for line in lines_with_user[:5]:
                        print(line[:200])
                        
            except Exception as e:
                print(f"Error reading {log_file.name}: {e}")

if __name__ == "__main__":
    examine_logs()
