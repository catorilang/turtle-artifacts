#!/usr/bin/env python3
"""
🐢 TURTLE CONFIDENCE MONITOR
Permanent confidence tracking and display
"""

import os
import subprocess
from datetime import datetime

class TurtleConfidenceMonitor:
    """Permanent confidence monitoring system"""
    
    def __init__(self):
        self.last_confidence = None
        self.confidence_history = []
    
    def calculate_confidence(self):
        """Calculate current turtle confidence level"""
        confidence = 100.0
        factors = {}
        
        # Git repository state
        try:
            branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            status = subprocess.check_output(['git', 'status', '--porcelain'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            changes = len(status.split('\n')) if status else 0
            
            factors['git_branch'] = branch or "main"
            factors['git_changes'] = changes
            
            if changes > 0:
                git_penalty = min(changes * 1.5, 20)
                confidence -= git_penalty
                factors['git_penalty'] = git_penalty
        except:
            confidence -= 15
            factors['git_status'] = "unavailable"
        
        # Microkernel integrity
        if os.path.exists("kernel/TURTLE_MICROKERNEL.cnl"):
            factors['microkernel'] = "present"
        else:
            confidence -= 30
            factors['microkernel'] = "missing"
        
        # Agent availability
        agents = 0
        if os.path.exists("identity_locked_turtles"):
            agents += len([f for f in os.listdir("identity_locked_turtles") 
                          if f.startswith("turtle_")])
        if os.path.exists("laura-witch-turtle"):
            agents += 1
        
        factors['agents'] = agents
        if agents == 0:
            confidence -= 25
        elif agents < 3:
            confidence -= 10
            
        # Research activity
        research_count = 0
        if os.path.exists("research"):
            research_count = len([f for f in os.listdir("research") 
                                if f.endswith(".md")])
        
        factors['research_projects'] = research_count
        if research_count < 5:
            confidence -= 10
        
        # File system health
        try:
            py_files = len([f for f in os.listdir('.') if f.endswith('.py')])
            md_files = len([f for f in os.listdir('.') if f.endswith('.md')])
            cnl_files = 0
            if os.path.exists('kernel'):
                cnl_files = len([f for f in os.listdir('kernel') 
                               if f.endswith('.cnl')])
            
            factors['files'] = {'py': py_files, 'md': md_files, 'cnl': cnl_files}
            
            if py_files < 10:
                confidence -= 5
            if cnl_files == 0:
                confidence -= 15
                
        except:
            confidence -= 10
            factors['file_system'] = "error"
        
        final_confidence = max(confidence, 0)
        
        return final_confidence, factors
    
    def get_status_indicator(self, confidence):
        """Get status indicator based on confidence level"""
        if confidence > 80:
            return "🟢 OPERATIONAL"
        elif confidence > 60:
            return "🟡 DEGRADED"
        else:
            return "🔴 CRITICAL"
    
    def display_confidence(self, force_display=False):
        """Display confidence with change detection"""
        current_confidence, factors = self.calculate_confidence()
        
        # Always display if forced or confidence changed
        if force_display or current_confidence != self.last_confidence:
            now = datetime.now().strftime("%H:%M:%S")
            status = self.get_status_indicator(current_confidence)
            
            if self.last_confidence and abs(current_confidence - self.last_confidence) > 5:
                change = current_confidence - self.last_confidence
                direction = "↗️" if change > 0 else "↘️"
                print(f"🐢 {current_confidence:5.1f}% {status} {direction}{change:+.1f}% {now}")
            else:
                print(f"🐢 {current_confidence:5.1f}% {status} {now}")
            
            self.last_confidence = current_confidence
            self.confidence_history.append((datetime.now(), current_confidence))
            
            # Keep only recent history
            if len(self.confidence_history) > 100:
                self.confidence_history = self.confidence_history[-100:]
        
        return current_confidence, factors
    
    def get_confidence_summary(self):
        """Get detailed confidence summary"""
        confidence, factors = self.calculate_confidence()
        status = self.get_status_indicator(confidence)
        
        return {
            "confidence": confidence,
            "status": status,
            "factors": factors,
            "timestamp": datetime.now().isoformat()
        }

# Global confidence monitor instance
_confidence_monitor = None

def get_confidence_monitor():
    """Get global confidence monitor"""
    global _confidence_monitor
    if not _confidence_monitor:
        _confidence_monitor = TurtleConfidenceMonitor()
    return _confidence_monitor

def display_confidence(force=False):
    """Display current confidence level"""
    monitor = get_confidence_monitor()
    return monitor.display_confidence(force)

def get_current_confidence():
    """Get current confidence without display"""
    monitor = get_confidence_monitor()
    confidence, factors = monitor.calculate_confidence()
    return confidence

if __name__ == "__main__":
    monitor = TurtleConfidenceMonitor()
    confidence, factors = monitor.display_confidence(force_display=True)
    
    print(f"\nDetailed factors:")
    for key, value in factors.items():
        print(f"  {key}: {value}")