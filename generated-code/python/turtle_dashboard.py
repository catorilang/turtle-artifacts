#!/usr/bin/env python3
"""
🐢 TURTLE DASHBOARD
Real-time CLI dashboard for turtle system status
"""

import os
import time
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class TurtleDashboard:
    """CLI dashboard for turtle system monitoring"""
    
    def __init__(self):
        self.refresh_interval = 2.0
        self.running = True
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system resource statistics"""
        if not PSUTIL_AVAILABLE:
            return {"cpu": "N/A", "memory": "N/A", "disk": "N/A"}
        
        return {
            "cpu": f"{psutil.cpu_percent(interval=0.1):.1f}%",
            "memory": f"{psutil.virtual_memory().percent:.1f}%",
            "disk": f"{psutil.disk_usage('/').percent:.1f}%",
            "load": os.getloadavg() if hasattr(os, 'getloadavg') else "N/A"
        }
    
    def get_git_status(self) -> Dict[str, str]:
        """Get git repository status"""
        try:
            # Current branch
            branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            
            # Status summary
            status = subprocess.check_output(['git', 'status', '--porcelain'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            
            # Recent commits
            recent = subprocess.check_output(['git', 'log', '--oneline', '-3'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            
            return {
                "branch": branch or "unknown",
                "status": "clean" if not status else f"{len(status.split())} changes",
                "recent": recent.split('\n') if recent else []
            }
        except:
            return {"branch": "N/A", "status": "N/A", "recent": []}
    
    def get_turtle_agents(self) -> List[Dict[str, str]]:
        """Get turtle agent status"""
        agents = []
        
        # Check for identity-locked turtles
        if os.path.exists("identity_locked_turtles"):
            for file in os.listdir("identity_locked_turtles"):
                if file.startswith("turtle_"):
                    agents.append({
                        "name": file,
                        "type": "identity-locked",
                        "status": "ready",
                        "location": f"identity_locked_turtles/{file}"
                    })
        
        # Check for Laura's turtle
        if os.path.exists("laura-witch-turtle"):
            agents.append({
                "name": "laura-witch-turtle",
                "type": "dual-mode",
                "status": "repository",
                "location": "laura-witch-turtle/"
            })
        
        return agents
    
    def get_research_status(self) -> Dict[str, Any]:
        """Get research project status"""
        research_projects = []
        
        if os.path.exists("research"):
            for file in os.listdir("research"):
                if file.endswith(".md"):
                    research_projects.append(file.replace(".md", ""))
        
        return {
            "active_projects": len(research_projects),
            "projects": research_projects[:5],  # Top 5
            "classified": "TURTLE_CLASSIFIED" in str(research_projects)
        }
    
    def render_header(self):
        """Render dashboard header"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("╔" + "═" * 78 + "╗")
        print(f"║ 🐢 TURTLE DASHBOARD{' ' * 45}│ {now} ║")
        print("╠" + "═" * 78 + "╣")
    
    def render_system_section(self, stats: Dict[str, Any]):
        """Render system resources section"""
        print("║ 📊 SYSTEM RESOURCES" + " " * 57 + "║")
        print("╠" + "─" * 78 + "╣")
        
        cpu = stats.get("cpu", "N/A")
        memory = stats.get("memory", "N/A")
        disk = stats.get("disk", "N/A")
        
        print(f"║ CPU: {cpu:<8} │ Memory: {memory:<8} │ Disk: {disk:<8}" + " " * 25 + "║")
        
        if stats.get("load") != "N/A":
            load = stats["load"]
            print(f"║ Load: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}" + " " * 49 + "║")
    
    def render_git_section(self, git_status: Dict[str, str]):
        """Render git status section"""
        print("╠" + "─" * 78 + "╣")
        print("║ 📂 GIT STATUS" + " " * 63 + "║")
        print("╠" + "─" * 78 + "╣")
        
        branch = git_status.get("branch", "N/A")
        status = git_status.get("status", "N/A")
        
        print(f"║ Branch: {branch:<15} │ Status: {status:<25}" + " " * 20 + "║")
        
        recent = git_status.get("recent", [])
        if recent:
            print("║ Recent commits:" + " " * 59 + "║")
            for i, commit in enumerate(recent[:2]):  # Show top 2
                commit_short = commit[:65] + "..." if len(commit) > 65 else commit
                print(f"║   {commit_short:<73} ║")
    
    def render_agents_section(self, agents: List[Dict[str, str]]):
        """Render turtle agents section"""
        print("╠" + "─" * 78 + "╣")
        print("║ 🐢 TURTLE AGENTS" + " " * 60 + "║")
        print("╠" + "─" + "─" * 76 + "╣")
        
        if not agents:
            print("║ No active turtle agents" + " " * 53 + "║")
        else:
            for agent in agents[:4]:  # Show top 4
                name = agent["name"][:20]
                agent_type = agent["type"]
                status = agent["status"]
                print(f"║ {name:<22} │ {agent_type:<15} │ {status:<10}" + " " * 15 + "║")
    
    def render_research_section(self, research: Dict[str, Any]):
        """Render research projects section"""
        print("╠" + "─" * 78 + "╣")
        print("║ 🔬 RESEARCH PROJECTS" + " " * 56 + "║")
        print("╠" + "─" * 78 + "╣")
        
        active = research.get("active_projects", 0)
        classified = research.get("classified", False)
        
        print(f"║ Active Projects: {active}" + " " * 58 + "║")
        if classified:
            print("║ 🔒 CLASSIFIED PROJECTS ACTIVE" + " " * 46 + "║")
        
        projects = research.get("projects", [])
        if projects:
            for project in projects[:3]:  # Show top 3
                project_name = project.replace("_", " ").title()[:65]
                print(f"║   {project_name:<73} ║")
    
    def render_footer(self):
        """Render dashboard footer"""
        print("╠" + "═" * 78 + "╣")
        print("║ Press Ctrl+C to exit" + " " * 55 + "║")
        print("╚" + "═" * 78 + "╝")
    
    def render_dashboard(self):
        """Render complete dashboard"""
        self.clear_screen()
        
        # Get all data
        system_stats = self.get_system_stats()
        git_status = self.get_git_status()
        agents = self.get_turtle_agents()
        research = self.get_research_status()
        
        # Render sections
        self.render_header()
        self.render_system_section(system_stats)
        self.render_git_section(git_status)
        self.render_agents_section(agents)
        self.render_research_section(research)
        self.render_footer()
    
    def run(self):
        """Run dashboard main loop"""
        try:
            while self.running:
                self.render_dashboard()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.clear_screen()
            print("🐢 Turtle dashboard stopped")
            return

def main():
    """Main dashboard entry point"""
    dashboard = TurtleDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()