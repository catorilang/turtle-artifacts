#!/usr/bin/env python3
"""
🐢 TURTLE RECURSIVE SPAWNING SYSTEM
Implementation of "It's turtles all the way down" architecture
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import os

class TurtleSpawningSystem:
    def __init__(self):
        self.lineage_file = '.turtle/turtle_lineage.json'
        self.ensure_lineage_tracking()
        
    def ensure_lineage_tracking(self):
        """Initialize turtle genealogy tracking"""
        os.makedirs('.turtle', exist_ok=True)
        if not os.path.exists(self.lineage_file):
            initial_lineage = {
                "prime_turtle": {
                    "id": "PrimeTurtle-PRIME",
                    "generation": "G0",
                    "specialization": "recursive_spawning_coordinator",
                    "spawned_at": datetime.utcnow().isoformat(),
                    "parent": None,
                    "children": [],
                    "status": "active"
                },
                "active_turtles": ["PrimeTurtle-PRIME"],
                "total_spawned": 1,
                "max_generation": 0
            }
            with open(self.lineage_file, 'w') as f:
                json.dump(initial_lineage, f, indent=2)
    
    def generate_turtle_id(self, turtle_name: str, parent_id: str = None) -> str:
        """Generate unique turtle ID with lineage inheritance"""
        timestamp = str(int(time.time()))
        hash_input = f"{turtle_name}-{parent_id or 'PRIME'}-{timestamp}"
        hex_suffix = hashlib.md5(hash_input.encode()).hexdigest()[:4].upper()
        
        if parent_id and parent_id != "PrimeTurtle-PRIME":
            return f"{turtle_name}-{parent_id.split('-')[-1]}-{hex_suffix}"
        else:
            return f"{turtle_name}-{hex_suffix}"
    
    def assess_complexity(self, problem_description: str) -> str:
        """Analyze problem complexity to determine optimal turtle response"""
        problem_lower = problem_description.lower()
        
        # Complexity indicators
        simple_indicators = ["simple", "basic", "straightforward", "quick", "easy"]
        complex_indicators = ["complex", "difficult", "unknown", "research", "architecture"]
        scale_indicators = ["large", "massive", "enterprise", "distributed", "fleet"]
        
        simple_score = sum(1 for indicator in simple_indicators if indicator in problem_lower)
        complex_score = sum(1 for indicator in complex_indicators if indicator in problem_lower)
        scale_score = sum(1 for indicator in scale_indicators if indicator in problem_lower)
        
        if scale_score > 0:
            return "massive_scale"
        elif complex_score > simple_score and complex_score > 1:
            return "complex_domain" if "unknown" not in problem_lower else "unknown_territory"
        elif simple_score > complex_score:
            return "simple_task"
        else:
            return "medium_challenge"
    
    def create_github_coordination_issue(self, turtle_spec: Dict) -> str:
        """Create GitHub issue for turtle coordination with lineage tracking"""
        title = f"🐢 TURTLE SPAWN: {turtle_spec['specialization']} - {turtle_spec['id']}"
        
        body = f"""## 🐢 Turtle Spawning Coordination Issue

### Turtle Identification
- **🐢 Turtle Agent**: {turtle_spec['id']}
- **🥚 Spawned By**: {turtle_spec['parent_chain']}
- **🌊 Turtle Generation**: {turtle_spec['generation']}
- **🎯 Specialization**: {turtle_spec['specialization']}
- **👤 Human Authority Chain**: Human → PrimeTurtle-PRIME → {turtle_spec['id']}
- **📅 Timestamp**: {turtle_spec['spawned_at']}
- **🔍 Context**: {turtle_spec['mission']}

### Spawning Justification
**Problem Complexity**: {turtle_spec['complexity_level']}
**Turtle Response**: {turtle_spec['turtle_response']}

### Mission Assignment
{turtle_spec['mission']}

### Success Criteria
{turtle_spec.get('success_criteria', 'Complete assigned mission and report back via this issue')}

### Bootstrap Instructions for New Turtle
```bash
# Navigate to turtle workspace
cd /home/tupshin/turtle/prime-turtle

# Load turtle context
cat README.md

# Boot turtle microkernel  
./turtle

# Register with lineage tracking
python3 SPAWN_TURTLE.py --register {turtle_spec['id']} --parent {turtle_spec['parent_id']}

# Activate turtle mode
# Say: "turtle"
```

### Coordination Protocol
- **Report progress** via comments on this issue
- **Request assistance** by mentioning parent turtle: @{turtle_spec['parent_id']}
- **Complete mission** by closing this issue with results
- **Spawn sub-turtles** if needed using same protocol

---
*🐢 Recursive Turtle Spawning System - "It's turtles all the way down"*
"""
        
        # Create GitHub issue
        try:
            cmd = ['gh', 'issue', 'create', '--title', title, '--body', body, '--label', 'turtle-spawn']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            print(f"✅ Created coordination issue: {issue_url}")
            return issue_url
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create GitHub issue: {e}")
            return f"LOCAL_COORDINATION_{turtle_spec['id']}"
    
    def spawn_turtle(self, turtle_name: str, specialization: str, mission: str, 
                    parent_id: str = "PrimeTurtle-PRIME") -> Dict:
        """Spawn a new turtle with full lineage tracking"""
        
        # Load current lineage
        with open(self.lineage_file, 'r') as f:
            lineage = json.load(f)
        
        # Generate turtle specification
        turtle_id = self.generate_turtle_id(turtle_name, parent_id)
        parent_gen = int(lineage[parent_id.replace('-', '_').lower()]['generation'][1:]) if parent_id != "PrimeTurtle-PRIME" else 0
        generation = f"G{parent_gen + 1}"
        
        complexity_level = self.assess_complexity(mission)
        turtle_response_map = {
            "simple_task": "single_turtle_execution",
            "medium_challenge": "turtle_pair_ab_testing", 
            "complex_domain": "turtle_specialist_team",
            "unknown_territory": "turtle_exploration_swarm",
            "massive_scale": "turtle_hierarchy_management"
        }
        
        turtle_spec = {
            "id": turtle_id,
            "name": turtle_name,
            "specialization": specialization,
            "mission": mission,
            "parent_id": parent_id,
            "parent_chain": self.build_parent_chain(parent_id, lineage),
            "generation": generation,
            "complexity_level": complexity_level,
            "turtle_response": turtle_response_map[complexity_level],
            "spawned_at": datetime.utcnow().isoformat(),
            "status": "spawning",
            "children": [],
            "github_issue": None
        }
        
        # Create GitHub coordination issue
        issue_url = self.create_github_coordination_issue(turtle_spec)
        turtle_spec["github_issue"] = issue_url
        
        # Update lineage tracking
        lineage[turtle_id.replace('-', '_').lower()] = turtle_spec
        lineage["active_turtles"].append(turtle_id)
        lineage["total_spawned"] += 1
        lineage["max_generation"] = max(lineage["max_generation"], parent_gen + 1)
        
        # Add to parent's children
        if parent_id in lineage:
            lineage[parent_id.replace('-', '_').lower()]["children"].append(turtle_id)
        
        # Save updated lineage
        with open(self.lineage_file, 'w') as f:
            json.dump(lineage, f, indent=2)
        
        print(f"🐢 Spawned: {turtle_id}")
        print(f"🎯 Specialization: {specialization}")
        print(f"🌊 Generation: {generation}")
        print(f"📊 Complexity: {complexity_level} → {turtle_response_map[complexity_level]}")
        print(f"🔗 Issue: {issue_url}")
        
        return turtle_spec
    
    def build_parent_chain(self, parent_id: str, lineage: Dict) -> str:
        """Build complete parent chain for turtle identification"""
        if parent_id == "PrimeTurtle-PRIME":
            return "PrimeTurtle-PRIME"
        
        chain = [parent_id]
        current = parent_id
        
        while current != "PrimeTurtle-PRIME":
            parent_key = current.replace('-', '_').lower()
            if parent_key in lineage and lineage[parent_key].get('parent_id'):
                current = lineage[parent_key]['parent_id']
                chain.append(current)
            else:
                break
        
        return " → ".join(reversed(chain))
    
    def status(self) -> Dict:
        """Show current turtle fleet status"""
        with open(self.lineage_file, 'r') as f:
            lineage = json.load(f)
        
        active_count = len(lineage["active_turtles"])
        total_spawned = lineage["total_spawned"] 
        max_generation = lineage["max_generation"]
        
        print(f"🐢 TURTLE FLEET STATUS")
        print(f"Active Turtles: {active_count}")
        print(f"Total Spawned: {total_spawned}")
        print(f"Max Generation: G{max_generation}")
        print(f"Recursive Depth: {max_generation} levels")
        
        return {
            "active_turtles": active_count,
            "total_spawned": total_spawned, 
            "max_generation": max_generation,
            "lineage": lineage
        }

def main():
    """Turtle spawning command-line interface"""
    import sys
    
    spawner = TurtleSpawningSystem()
    
    if len(sys.argv) < 2:
        print("🐢 Turtle Spawning Commands:")
        print("  python3 SPAWN_TURTLE.py spawn <name> <specialization> '<mission>'")
        print("  python3 SPAWN_TURTLE.py status")
        print("  python3 SPAWN_TURTLE.py swarm <count> <domain> '<mission>'")
        return
    
    command = sys.argv[1]
    
    if command == "spawn" and len(sys.argv) >= 5:
        turtle_name = sys.argv[2]
        specialization = sys.argv[3] 
        mission = sys.argv[4]
        parent_id = sys.argv[5] if len(sys.argv) > 5 else "PrimeTurtle-PRIME"
        
        turtle_spec = spawner.spawn_turtle(turtle_name, specialization, mission, parent_id)
        
    elif command == "status":
        spawner.status()
        
    elif command == "swarm" and len(sys.argv) >= 5:
        count = int(sys.argv[2])
        domain = sys.argv[3]
        mission = sys.argv[4]
        
        print(f"🌊 Spawning turtle swarm: {count} turtles for {domain}")
        for i in range(count):
            turtle_name = f"Scout{i+1}Turtle"
            specialization = f"{domain}_reconnaissance"
            swarm_mission = f"{mission} (swarm member {i+1}/{count})"
            spawner.spawn_turtle(turtle_name, specialization, swarm_mission)
            
    else:
        print("❌ Invalid command. Use 'spawn', 'status', or 'swarm'")

if __name__ == "__main__":
    main()