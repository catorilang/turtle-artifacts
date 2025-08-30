#!/usr/bin/env python3
"""
Turtle Thread Observability - Essential for parallel coordination
"""
import json
import time
import os
from datetime import datetime

def update_thread_status(thread_id, status, current_task=None):
    """Update thread status in shared observability file"""
    status_file = '.turtle/thread_status.json'
    
    # Read current status
    try:
        with open(status_file, 'r') as f:
            data = json.load(f)
    except:
        data = {"fleet_status": {"total_threads": 0, "active_threads": []}, "coordination": {"shared_workspace": os.getcwd(), "lock_files": [], "pending_tasks": []}}
    
    # Update thread info
    timestamp = datetime.utcnow().isoformat() + 'Z'
    data[thread_id] = {
        "status": status,
        "last_heartbeat": timestamp,
        "current_task": current_task or "idle",
        "location": os.getcwd()
    }
    
    # Update fleet status
    active_threads = [tid for tid, info in data.items() 
                     if tid.startswith('thread_') and info.get('status') == 'active']
    data["fleet_status"] = {
        "total_threads": len(active_threads),
        "active_threads": active_threads,
        "last_updated": timestamp
    }
    
    # Write back
    with open(status_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"🔄 Thread {thread_id} status: {status} | Task: {current_task}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        update_thread_status(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print("Usage: python3 update_thread_status.py <thread_id> <status> [current_task]")