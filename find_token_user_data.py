#!/usr/bin/env python3
"""
Search for token usage and user ID in all log files
"""

from pathlib import Path
import re
import json

def search_in_file(file_path):
    """Search for token and user patterns in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        results = {
            'file': file_path.name,
            'tokens': [],
            'user_ids': [],
            'sample_lines': []
        }
        
        # Search for JSON objects with token information
        json_pattern = r'\{[^}]*(?:token|usage)[^}]*\}'
        json_matches = re.findall(json_pattern, content, re.IGNORECASE)
        
        for match in json_matches[:5]:
            try:
                data = json.loads(match)
                if 'tokens' in str(data).lower() or 'usage' in str(data).lower():
                    results['tokens'].append(match[:200])
            except:
                pass
        
        # Search for specific patterns
        patterns = {
            'tokens': [
                r'"(?:input_tokens|output_tokens|total_tokens)"\s*:\s*(\d+)',
                r'tokens?["\s]*:\s*(\d+)',
                r'usage.*?(\d+)\s*tokens?',
            ],
            'user_ids': [
                r'"(?:user_id|userId|user)"\s*:\s*"([^"]+)"',
                r'user[_-]?id["\s]*:\s*"?([a-zA-Z0-9-]+)"?',
            ]
        }
        
        for key, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    results[key].extend(matches[:5])
        
        # Get sample lines
        for line in content.split('\n'):
            if any(keyword in line.lower() for keyword in ['token', 'usage', 'user_id', 'userid']):
                results['sample_lines'].append(line.strip()[:300])
                if len(results['sample_lines']) >= 10:
                    break
        
        return results if (results['tokens'] or results['user_ids'] or results['sample_lines']) else None
        
    except Exception as e:
        return None

def main():
    windsurf_dir = Path(r"C:\Users\ChamanPrakash\AppData\Roaming\Windsurf\logs")
    vscode_dir = Path(r"C:\Users\ChamanPrakash\AppData\Roaming\Code\logs")
    
    print("="*80)
    print("SEARCHING FOR TOKEN AND USER DATA IN LOGS")
    print("="*80)
    
    for base_dir, name in [(windsurf_dir, "WINDSURF"), (vscode_dir, "VS CODE")]:
        print(f"\n{'='*80}")
        print(f"{name} LOGS")
        print(f"{'='*80}")
        
        if not base_dir.exists():
            print(f"Directory not found: {base_dir}")
            continue
        
        sessions = sorted([d for d in base_dir.iterdir() if d.is_dir()])
        if not sessions:
            print("No sessions found")
            continue
        
        # Check last 2 sessions
        for session in sessions[-2:]:
            print(f"\n--- Session: {session.name} ---")
            
            # Check all log files
            log_files = list(session.glob('*.log'))
            if (session / 'window1').exists():
                log_files.extend((session / 'window1').glob('*.log'))
            
            found_data = False
            for log_file in log_files:
                results = search_in_file(log_file)
                if results:
                    found_data = True
                    print(f"\n  File: {results['file']}")
                    
                    if results['tokens']:
                        print(f"    Tokens found: {results['tokens'][:3]}")
                    
                    if results['user_ids']:
                        print(f"    User IDs found: {results['user_ids'][:3]}")
                    
                    if results['sample_lines']:
                        print(f"    Sample lines:")
                        for line in results['sample_lines'][:3]:
                            print(f"      {line}")
            
            if not found_data:
                print("  No token/user data found in this session")

if __name__ == "__main__":
    main()
