#!/usr/bin/env python3
"""
🐢 TURTLE STATUS DASHBOARD
Simple CLI status display for turtle system
"""

import os
import subprocess
from datetime import datetime

def get_git_status():
    """Get git repository status"""
    try:
        branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                       stderr=subprocess.DEVNULL).decode().strip()
        status = subprocess.check_output(['git', 'status', '--porcelain'], 
                                       stderr=subprocess.DEVNULL).decode().strip()
        return {
            "branch": branch or "unknown",
            "changes": len(status.split('\n')) if status else 0
        }
    except:
        return {"branch": "N/A", "changes": 0}

def count_files():
    """Count turtle system files"""
    counts = {}
    for root, dirs, files in os.walk('.'):
        for file in files:
            ext = os.path.splitext(file)[1]
            counts[ext] = counts.get(ext, 0) + 1
    return counts

def get_turtle_agents():
    """Find turtle agents"""
    agents = []
    
    # Check for identity-locked turtles
    if os.path.exists("identity_locked_turtles"):
        for file in os.listdir("identity_locked_turtles"):
            if file.startswith("turtle_"):
                agents.append(f"Identity: {file}")
    
    # Check for Laura's turtle
    if os.path.exists("laura-witch-turtle"):
        agents.append("Laura: dual-mode witch turtle")
    
    return agents

def get_research_count():
    """Count research files"""
    if not os.path.exists("research"):
        return 0
    return len([f for f in os.listdir("research") if f.endswith(".md")])

def get_confidence_level():
    """Calculate turtle confidence based on system state"""
    confidence = 100.0
    
    # Git status impacts confidence
    git = get_git_status()
    if git['changes'] > 0:
        confidence -= min(git['changes'] * 2, 20)  # Max -20 for uncommitted changes
    
    # Missing critical files
    if not os.path.exists("kernel/TURTLE_MICROKERNEL.cnl"):
        confidence -= 30
    
    if not os.path.exists("README.md"):
        confidence -= 10
        
    # Agent availability
    agents = get_turtle_agents()
    if len(agents) == 0:
        confidence -= 25
    
    # Research activity
    research = get_research_count()
    if research < 5:
        confidence -= 10
        
    return max(confidence, 0)

def main():
    """Display turtle status dashboard"""
    confidence = get_confidence_level()
    
    print("╔" + "═" * 58 + "╗")
    print(f"║ 🐢 TURTLE STATUS{' ' * 21}Confidence: {confidence:5.1f}% ║")
    print("╠" + "═" * 58 + "╣")
    
    # Time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"║ Time: {now:<48} ║")
    
    # Git status
    git = get_git_status()
    print(f"║ Branch: {git['branch']:<15} Changes: {git['changes']:<8} ║")
    
    # File counts
    files = count_files()
    py_files = files.get('.py', 0)
    md_files = files.get('.md', 0)
    cnl_files = files.get('.cnl', 0)
    print(f"║ Files: .py={py_files} .md={md_files} .cnl={cnl_files:<18} ║")
    
    # Agents
    agents = get_turtle_agents()
    print(f"║ Agents: {len(agents):<35} ║")
    for agent in agents[:2]:  # Show first 2
        print(f"║   {agent:<44} ║")
    
    # Research
    research = get_research_count()
    print(f"║ Research projects: {research:<26} ║")
    
    print("╚" + "═" * 48 + "╝")

if __name__ == "__main__":
    main()