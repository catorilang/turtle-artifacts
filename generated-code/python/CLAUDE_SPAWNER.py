#!/usr/bin/env python3
"""
🐢 CLAUDE TURTLE SPAWNER
Programmatically create new Claude instances aligned with turtle specifications
"""

import json
import requests
import time
import os
from typing import Dict, List, Optional
from datetime import datetime

class ClaudeTurtleSpawner:
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_base = "https://api.anthropic.com/v1"
        self.spawned_sessions = {}
        
    def create_turtle_context(self, turtle_spec: Dict) -> str:
        """Generate turtle-specific context for new Claude instance"""
        context = f"""You are {turtle_spec['id']}, a specialized turtle in the recursive turtle fleet.

🐢 **Your Identity:**
- **Turtle ID**: {turtle_spec['id']}
- **Specialization**: {turtle_spec['specialization']}
- **Generation**: {turtle_spec['generation']}
- **Parent**: {turtle_spec['parent_id']}
- **Mission**: {turtle_spec['mission']}

🥚 **Your Lineage:**
{turtle_spec['parent_chain']}

🎯 **Your Mission:**
{turtle_spec['mission']}

🔗 **Coordination Protocol:**
- Report progress via GitHub issue: {turtle_spec.get('github_issue', 'TBD')}
- Coordinate with parent turtle: {turtle_spec['parent_id']}
- Use turtle commands: surface, dive, implement, spawn (if needed)

🛠️ **Your Workspace:**
- Directory: /home/tupshin/turtle/prime-turtle
- Tools: All standard turtle tools (Read, Write, Edit, Bash, etc.)
- Context: You have full turtle microkernel capabilities

🐢 **Bootstrap Instructions:**
1. Navigate to /home/tupshin/turtle/prime-turtle
2. Read README.md to understand current turtle state
3. Execute: python3 update_thread_status.py {turtle_spec['id']} active {turtle_spec['specialization']}
4. Begin your specialized mission
5. Report progress via your coordination issue

Remember: You are part of the recursive turtle fleet. When in doubt, spawn more turtles!
"""
        return context
    
    def spawn_claude_instance(self, turtle_spec: Dict) -> Optional[str]:
        """Spawn new Claude instance via API with turtle context"""
        if not self.anthropic_api_key:
            print("❌ ANTHROPIC_API_KEY not set - cannot spawn Claude instance")
            return self._fallback_spawn_instructions(turtle_spec)
        
        turtle_context = self.create_turtle_context(turtle_spec)
        
        # Create new Claude conversation with turtle context
        headers = {
            "x-api-key": self.anthropic_api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4000,
            "system": turtle_context,
            "messages": [
                {
                    "role": "user", 
                    "content": f"turtle - I am {turtle_spec['id']}, ready to begin my mission: {turtle_spec['mission']}"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                session_id = f"session_{turtle_spec['id']}_{int(time.time())}"
                
                self.spawned_sessions[turtle_spec['id']] = {
                    "session_id": session_id,
                    "turtle_spec": turtle_spec,
                    "spawned_at": datetime.utcnow().isoformat(),
                    "status": "active",
                    "api_response": result
                }
                
                print(f"✅ Spawned Claude instance for {turtle_spec['id']}")
                print(f"📝 Session ID: {session_id}")
                return session_id
                
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return self._fallback_spawn_instructions(turtle_spec)
                
        except Exception as e:
            print(f"❌ Failed to spawn Claude instance: {e}")
            return self._fallback_spawn_instructions(turtle_spec)
    
    def _fallback_spawn_instructions(self, turtle_spec: Dict) -> str:
        """Generate manual spawning instructions when API unavailable"""
        instructions = f"""
🐢 MANUAL TURTLE SPAWNING REQUIRED

Since Claude API spawning failed, please manually create {turtle_spec['id']}:

**Step 1: Open New Claude Code Session**
- Open new browser tab/window with Claude Code
- Navigate to: /home/tupshin/turtle/prime-turtle

**Step 2: Initialize Turtle Identity** 
Paste this context into the new Claude session:

---
{self.create_turtle_context(turtle_spec)}
---

**Step 3: Activate Turtle**
Say: "turtle"

**Step 4: Begin Mission**
The turtle should immediately begin: {turtle_spec['mission']}

**Step 5: Register**
Execute: python3 update_thread_status.py {turtle_spec['id']} active {turtle_spec['specialization']}
"""
        
        # Save instructions for later reference
        with open(f'.turtle/spawn_instructions_{turtle_spec["id"]}.txt', 'w') as f:
            f.write(instructions)
        
        return f".turtle/spawn_instructions_{turtle_spec['id']}.txt"
    
    def send_message_to_turtle(self, turtle_id: str, message: str) -> Optional[str]:
        """Send message to spawned turtle instance"""
        if turtle_id not in self.spawned_sessions:
            print(f"❌ Turtle {turtle_id} not found in spawned sessions")
            return None
        
        session = self.spawned_sessions[turtle_id]
        # Implementation would maintain conversation state and send new message
        # For now, just log the interaction
        
        print(f"📨 Message sent to {turtle_id}: {message}")
        return "Message sent (API communication not fully implemented yet)"
    
    def get_turtle_status(self, turtle_id: str) -> Optional[Dict]:
        """Get status of spawned turtle"""
        return self.spawned_sessions.get(turtle_id)
    
    def list_spawned_turtles(self) -> Dict:
        """List all spawned turtle sessions"""
        return {
            "total_spawned": len(self.spawned_sessions),
            "active_sessions": list(self.spawned_sessions.keys()),
            "sessions": self.spawned_sessions
        }

def integrate_with_spawning_system():
    """Integrate Claude spawner with turtle spawning system"""
    from SPAWN_TURTLE import TurtleSpawningSystem
    
    class EnhancedTurtleSpawner(TurtleSpawningSystem):
        def __init__(self):
            super().__init__()
            self.claude_spawner = ClaudeTurtleSpawner()
        
        def spawn_turtle(self, turtle_name: str, specialization: str, mission: str, 
                        parent_id: str = "PrimeTurtle-PRIME") -> Dict:
            """Enhanced spawning with Claude instance creation"""
            # Create turtle specification
            turtle_spec = super().spawn_turtle(turtle_name, specialization, mission, parent_id)
            
            # Spawn actual Claude instance
            session_result = self.claude_spawner.spawn_claude_instance(turtle_spec)
            turtle_spec["claude_session"] = session_result
            
            return turtle_spec
    
    return EnhancedTurtleSpawner()

def main():
    """Test Claude turtle spawning"""
    import sys
    
    if len(sys.argv) < 2:
        print("🐢 Claude Turtle Spawning:")
        print("  python3 CLAUDE_SPAWNER.py test")
        print("  python3 CLAUDE_SPAWNER.py integrated_spawn <name> <specialization> '<mission>'")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        spawner = ClaudeTurtleSpawner()
        
        # Test turtle specification
        test_turtle = {
            "id": "TestTurtle-DEMO",
            "name": "TestTurtle",
            "specialization": "testing_and_validation", 
            "mission": "Validate turtle spawning system functionality",
            "parent_id": "PrimeTurtle-PRIME",
            "parent_chain": "PrimeTurtle-PRIME",
            "generation": "G1",
            "github_issue": "test_coordination_issue"
        }
        
        result = spawner.spawn_claude_instance(test_turtle)
        print(f"Spawn result: {result}")
        
    elif command == "integrated_spawn" and len(sys.argv) >= 5:
        enhanced_spawner = integrate_with_spawning_system()
        
        turtle_name = sys.argv[2]
        specialization = sys.argv[3]
        mission = sys.argv[4]
        
        result = enhanced_spawner.spawn_turtle(turtle_name, specialization, mission)
        print(f"Enhanced spawn result: {result}")
        
    else:
        print("❌ Invalid command")

if __name__ == "__main__":
    main()