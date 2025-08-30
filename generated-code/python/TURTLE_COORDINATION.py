#!/usr/bin/env python3
"""
🌊 TURTLE FLEET COORDINATION SYSTEM
Real-time coordination, discovery, and communication between turtle instances
"""

import json
import time
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import fcntl
import threading

class TurtleCoordinator:
    def __init__(self, turtle_id: str = None):
        self.turtle_id = turtle_id or "PrimeTurtle-PRIME"
        self.coordination_dir = Path(".turtle/coordination")
        self.heartbeat_dir = self.coordination_dir / "heartbeats"
        self.message_dir = self.coordination_dir / "messages"
        self.status_dir = self.coordination_dir / "status"
        
        # Create coordination directories
        for directory in [self.coordination_dir, self.heartbeat_dir, self.message_dir, self.status_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize heartbeat
        self.last_heartbeat = 0
        self.heartbeat_interval = 5  # seconds
        self.discovery_cache = {}
        self.message_handlers = {}
        
        # Start heartbeat thread
        self.heartbeat_active = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
    
    def _heartbeat_loop(self):
        """Continuous heartbeat to announce turtle presence"""
        while self.heartbeat_active:
            try:
                self.announce_presence()
                time.sleep(self.heartbeat_interval)
            except Exception as e:
                print(f"❌ Heartbeat error: {e}")
                time.sleep(self.heartbeat_interval)
    
    def announce_presence(self):
        """Announce turtle presence with current status"""
        heartbeat_file = self.heartbeat_dir / f"{self.turtle_id}.json"
        
        status = {
            "turtle_id": self.turtle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "process_id": os.getpid(),
            "working_directory": os.getcwd(),
            "status": "active",
            "capabilities": ["read", "write", "edit", "bash", "coordination"],
            "last_activity": datetime.utcnow().isoformat(),
            "turtle_version": "1.0.0"
        }
        
        # Atomic write with file locking
        temp_file = heartbeat_file.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(status, f, indent=2)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            temp_file.replace(heartbeat_file)
            self.last_heartbeat = time.time()
            
        except Exception as e:
            print(f"❌ Failed to announce presence: {e}")
            if temp_file.exists():
                temp_file.unlink()
    
    def discover_active_turtles(self) -> Dict[str, Dict]:
        """Discover all active turtles in the fleet"""
        active_turtles = {}
        current_time = time.time()
        stale_threshold = 30  # seconds
        
        if not self.heartbeat_dir.exists():
            return active_turtles
        
        for heartbeat_file in self.heartbeat_dir.glob("*.json"):
            try:
                with open(heartbeat_file, 'r') as f:
                    status = json.load(f)
                
                # Check if heartbeat is recent
                last_update = datetime.fromisoformat(status['timestamp'])
                age_seconds = (datetime.utcnow() - last_update).total_seconds()
                
                if age_seconds < stale_threshold:
                    turtle_id = status['turtle_id']
                    active_turtles[turtle_id] = status
                    active_turtles[turtle_id]['age_seconds'] = age_seconds
                else:
                    # Clean up stale heartbeat
                    heartbeat_file.unlink()
                    
            except Exception as e:
                print(f"❌ Error reading heartbeat {heartbeat_file}: {e}")
        
        return active_turtles
    
    def send_message(self, target_turtle: str, message_type: str, content: Any) -> str:
        """Send message to specific turtle"""
        message_id = hashlib.md5(f"{self.turtle_id}-{target_turtle}-{time.time()}".encode()).hexdigest()[:8]
        
        message = {
            "message_id": message_id,
            "from_turtle": self.turtle_id, 
            "to_turtle": target_turtle,
            "message_type": message_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "priority": "normal",
            "requires_response": False
        }
        
        # Create message file for target turtle
        message_file = self.message_dir / f"{target_turtle}-{message_id}.json"
        
        try:
            with open(message_file, 'w') as f:
                json.dump(message, f, indent=2)
            
            print(f"📨 Message sent to {target_turtle}: {message_type}")
            return message_id
            
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return None
    
    def broadcast_message(self, message_type: str, content: Any) -> List[str]:
        """Broadcast message to all active turtles"""
        active_turtles = self.discover_active_turtles()
        message_ids = []
        
        for turtle_id in active_turtles.keys():
            if turtle_id != self.turtle_id:  # Don't send to self
                message_id = self.send_message(turtle_id, message_type, content)
                if message_id:
                    message_ids.append(message_id)
        
        print(f"📡 Broadcast to {len(message_ids)} turtles: {message_type}")
        return message_ids
    
    def check_messages(self) -> List[Dict]:
        """Check for incoming messages"""
        messages = []
        
        if not self.message_dir.exists():
            return messages
        
        # Find messages for this turtle
        message_pattern = f"{self.turtle_id}-*.json"
        for message_file in self.message_dir.glob(message_pattern):
            try:
                with open(message_file, 'r') as f:
                    message = json.load(f)
                
                messages.append(message)
                
                # Process message if handler exists
                message_type = message['message_type']
                if message_type in self.message_handlers:
                    self.message_handlers[message_type](message)
                
                # Clean up processed message
                message_file.unlink()
                
            except Exception as e:
                print(f"❌ Error processing message {message_file}: {e}")
        
        return messages
    
    def register_message_handler(self, message_type: str, handler_func):
        """Register handler for specific message types"""
        self.message_handlers[message_type] = handler_func
        print(f"📋 Registered handler for: {message_type}")
    
    def request_turtle_spawn(self, specialization: str, mission: str) -> str:
        """Request another turtle to spawn a sub-turtle"""
        request_content = {
            "specialization": specialization,
            "mission": mission,
            "requester": self.turtle_id,
            "urgency": "normal"
        }
        
        # Send to prime turtle for coordination
        return self.send_message("PrimeTurtle-PRIME", "spawn_request", request_content)
    
    def coordinate_task_delegation(self, task: str, preferred_specialization: str = None) -> Optional[str]:
        """Find and delegate task to best available turtle"""
        active_turtles = self.discover_active_turtles()
        
        # Find turtle with matching specialization
        best_turtle = None
        for turtle_id, status in active_turtles.items():
            if turtle_id != self.turtle_id:
                # Simple matching logic - could be enhanced
                if preferred_specialization and preferred_specialization in turtle_id.lower():
                    best_turtle = turtle_id
                    break
                elif not best_turtle:
                    best_turtle = turtle_id
        
        if best_turtle:
            delegation_content = {
                "task": task,
                "delegator": self.turtle_id,
                "deadline": (datetime.utcnow() + timedelta(hours=1)).isoformat()
            }
            
            message_id = self.send_message(best_turtle, "task_delegation", delegation_content)
            return best_turtle
        
        return None
    
    def report_status_update(self, status: str, details: str = ""):
        """Report status update to coordination system"""
        update = {
            "turtle_id": self.turtle_id,
            "status": status,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        status_file = self.status_dir / f"{self.turtle_id}_latest.json"
        
        try:
            with open(status_file, 'w') as f:
                json.dump(update, f, indent=2)
            
            # Also broadcast to other turtles
            self.broadcast_message("status_update", update)
            
        except Exception as e:
            print(f"❌ Failed to report status: {e}")
    
    def get_fleet_overview(self) -> Dict:
        """Get comprehensive fleet status overview"""
        active_turtles = self.discover_active_turtles()
        
        overview = {
            "discovery_time": datetime.utcnow().isoformat(),
            "total_active_turtles": len(active_turtles),
            "turtles": active_turtles,
            "coordination_health": "operational",
            "fleet_generations": {},
            "specializations": {}
        }
        
        # Analyze fleet composition
        for turtle_id, status in active_turtles.items():
            # Extract generation if available
            if "generation" in turtle_id or "G" in turtle_id:
                gen = "G0" if "PRIME" in turtle_id else "G1+"
                overview["fleet_generations"][gen] = overview["fleet_generations"].get(gen, 0) + 1
            
            # Track specializations
            if "specialization" in status:
                spec = status["specialization"]
                overview["specializations"][spec] = overview["specializations"].get(spec, 0) + 1
        
        return overview
    
    def emergency_coordination(self, emergency_type: str, details: str):
        """Emergency coordination protocol"""
        emergency_message = {
            "emergency_type": emergency_type,
            "details": details,
            "reporting_turtle": self.turtle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "requires_immediate_response": True
        }
        
        # Broadcast to all turtles
        self.broadcast_message("emergency", emergency_message)
        
        # Also create emergency file
        emergency_file = self.coordination_dir / f"EMERGENCY_{int(time.time())}.json"
        with open(emergency_file, 'w') as f:
            json.dump(emergency_message, f, indent=2)
        
        print(f"🚨 Emergency broadcast: {emergency_type}")
    
    def cleanup(self):
        """Clean up coordination resources"""
        self.heartbeat_active = False
        if hasattr(self, 'heartbeat_thread'):
            self.heartbeat_thread.join(timeout=1)
        
        # Clean up own heartbeat
        heartbeat_file = self.heartbeat_dir / f"{self.turtle_id}.json"
        if heartbeat_file.exists():
            heartbeat_file.unlink()

def demonstrate_coordination():
    """Demonstrate turtle coordination system"""
    print("🌊 TURTLE FLEET COORDINATION DEMONSTRATION")
    print("=" * 60)
    
    # Initialize coordinator for prime turtle
    prime_coord = TurtleCoordinator("PrimeTurtle-PRIME")
    
    print("\n1️⃣ TURTLE DISCOVERY:")
    time.sleep(1)  # Let heartbeat establish
    active_turtles = prime_coord.discover_active_turtles()
    print(f"Active turtles: {list(active_turtles.keys())}")
    
    print("\n2️⃣ FLEET OVERVIEW:")
    overview = prime_coord.get_fleet_overview()
    print(f"Total active: {overview['total_active_turtles']}")
    print(f"Specializations: {overview['specializations']}")
    
    print("\n3️⃣ MESSAGE BROADCASTING:")
    prime_coord.broadcast_message("fleet_status_request", {"requester": "demonstration"})
    
    print("\n4️⃣ TASK COORDINATION:")
    # Simulate task delegation
    delegated_to = prime_coord.coordinate_task_delegation(
        "Analyze coordination system performance",
        "analysis"
    )
    print(f"Task delegated to: {delegated_to or 'No suitable turtle found'}")
    
    print("\n5️⃣ STATUS REPORTING:")
    prime_coord.report_status_update("demonstration_complete", "Coordination system working")
    
    print("\n✅ Coordination system operational!")
    
    # Cleanup
    prime_coord.cleanup()

if __name__ == "__main__":
    demonstrate_coordination()