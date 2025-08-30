#!/usr/bin/env python3
"""
🐢 TURTLE STATUS BAR
Minimal 3-line status display
"""

import os
import subprocess
from datetime import datetime

def get_git_status():
    try:
        branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                       stderr=subprocess.DEVNULL).decode().strip()
        status = subprocess.check_output(['git', 'status', '--porcelain'], 
                                       stderr=subprocess.DEVNULL).decode().strip()
        return branch or "main", len(status.split('\n')) if status else 0
    except:
        return "unknown", 0

def get_confidence():
    """Calculate turtle confidence"""
    confidence = 100.0
    branch, changes = get_git_status()
    
    if changes > 0:
        confidence -= min(changes * 1.5, 20)
    if not os.path.exists("kernel/TURTLE_MICROKERNEL.cnl"):
        confidence -= 30
    if not os.path.exists("laura-witch-turtle"):
        confidence -= 15
    
    agents = 0
    if os.path.exists("identity_locked_turtles"):
        agents = len([f for f in os.listdir("identity_locked_turtles") if f.startswith("turtle_")])
    if os.path.exists("laura-witch-turtle"):
        agents += 1
    
    if agents == 0:
        confidence -= 25
        
    return max(confidence, 0)

def count_files():
    py = len([f for f in os.listdir('.') if f.endswith('.py')])
    md = len([f for f in os.listdir('.') if f.endswith('.md')])
    cnl = 0
    if os.path.exists('kernel'):
        cnl = len([f for f in os.listdir('kernel') if f.endswith('.cnl')])
    return py, md, cnl

def main():
    branch, changes = get_git_status()
    confidence = get_confidence()
    py, md, cnl = count_files()
    
    agents = 0
    if os.path.exists("identity_locked_turtles"):
        agents = len([f for f in os.listdir("identity_locked_turtles") if f.startswith("turtle_")])
    if os.path.exists("laura-witch-turtle"):
        agents += 1
    
    now = datetime.now().strftime("%H:%M:%S")
    
    print(f"🐢 TURTLE | Confidence: {confidence:5.1f}% | {branch} +{changes} | {now}")
    print(f"   Files: {py}py {md}md {cnl}cnl | Agents: {agents} | Research: {len([f for f in os.listdir('research') if f.endswith('.md')]) if os.path.exists('research') else 0}")
    print(f"   Status: {'🟢 OPERATIONAL' if confidence > 80 else '🟡 DEGRADED' if confidence > 60 else '🔴 CRITICAL'}")

if __name__ == "__main__":
    main()