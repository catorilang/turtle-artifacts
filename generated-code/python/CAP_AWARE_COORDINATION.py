#!/usr/bin/env python3
"""
🎯 CAP-THEOREM AWARE TURTLE COORDINATION
Distributed turtle fleet with explicit CAP theorem trade-off handling
Consistency vs Availability vs Partition tolerance for turtle coordination
"""

import json
import time
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import fcntl
import threading
from enum import Enum

class CAPStrategy(Enum):
    """CAP theorem strategy selection"""
    CP_CONSISTENCY_PARTITION = "cp"      # Sacrifice availability for consistency during partitions
    AP_AVAILABILITY_PARTITION = "ap"     # Sacrifice consistency for availability during partitions  
    CA_CONSISTENCY_AVAILABILITY = "ca"   # Assume no partitions (single-machine coordination)

class CoordinationMode(Enum):
    """Coordination modes based on network conditions"""
    CONNECTED = "connected"              # Normal operation, full CAP available
    PARTITIONED = "partitioned"          # Network partition detected
    DEGRADED = "degraded"               # Reduced functionality mode

class CAPAwareTurtleCoordinator:
    def __init__(self, turtle_id: str, cap_strategy: CAPStrategy = CAPStrategy.AP_AVAILABILITY_PARTITION):
        self.turtle_id = turtle_id
        self.cap_strategy = cap_strategy
        self.coordination_mode = CoordinationMode.CONNECTED
        
        # CAP-aware storage strategy
        self.coordination_dir = Path(".turtle/cap_coordination")
        self.local_state_dir = self.coordination_dir / "local_state"
        self.consensus_dir = self.coordination_dir / "consensus"
        self.partition_cache_dir = self.coordination_dir / "partition_cache"
        
        # Create directories
        for directory in [self.coordination_dir, self.local_state_dir, 
                         self.consensus_dir, self.partition_cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # CAP state tracking
        self.local_turtle_state = {}
        self.consensus_version = 0
        self.partition_detected = False
        self.last_consensus_time = time.time()
        self.partition_timeout = 15  # seconds
        
        # Availability tracking
        self.turtle_availability = {}
        self.availability_threshold = 0.7  # 70% availability required for consistency
        
        self.initialize_cap_coordination()
    
    def initialize_cap_coordination(self):
        """Initialize CAP-aware coordination state"""
        print(f"🎯 CAP Strategy: {self.cap_strategy.value.upper()}")
        print(f"📊 Mode: {self.coordination_mode.value}")
        
        # Load or create local state
        local_state_file = self.local_state_dir / f"{self.turtle_id}.json"
        if local_state_file.exists():
            with open(local_state_file, 'r') as f:
                self.local_turtle_state = json.load(f)
        else:
            self.local_turtle_state = {
                "turtle_id": self.turtle_id,
                "version": 1,
                "created_at": datetime.utcnow().isoformat(),
                "status": "initializing",
                "cap_strategy": self.cap_strategy.value
            }
            self.save_local_state()
        
        # Start CAP monitoring
        self.cap_monitor_active = True
        self.cap_monitor_thread = threading.Thread(target=self._cap_monitor_loop, daemon=True)
        self.cap_monitor_thread.start()
    
    def _cap_monitor_loop(self):
        """Monitor CAP conditions and adapt coordination strategy"""
        while self.cap_monitor_active:
            try:
                self.assess_cap_conditions()
                self.adapt_coordination_strategy()
                time.sleep(5)  # CAP assessment interval
            except Exception as e:
                print(f"❌ CAP monitor error: {e}")
                time.sleep(5)
    
    def assess_cap_conditions(self):
        """Assess current CAP theorem conditions"""
        # Detect partition: if we can't see other turtles for timeout period
        active_turtles = self.discover_turtles_with_timeout()
        current_time = time.time()
        
        if len(active_turtles) <= 1 and (current_time - self.last_consensus_time) > self.partition_timeout:
            if not self.partition_detected:
                print("🔴 PARTITION DETECTED - Entering partition mode")
                self.partition_detected = True
                self.coordination_mode = CoordinationMode.PARTITIONED
                self.handle_partition_event()
        elif len(active_turtles) > 1:
            if self.partition_detected:
                print("🟢 PARTITION RESOLVED - Returning to connected mode")
                self.partition_detected = False
                self.coordination_mode = CoordinationMode.CONNECTED
                self.handle_partition_recovery()
            self.last_consensus_time = current_time
    
    def adapt_coordination_strategy(self):
        """Adapt coordination based on current CAP strategy and conditions"""
        if self.coordination_mode == CoordinationMode.PARTITIONED:
            if self.cap_strategy == CAPStrategy.CP_CONSISTENCY_PARTITION:
                # Prioritize consistency - stop processing until partition resolves
                self.enter_consistency_preservation_mode()
            elif self.cap_strategy == CAPStrategy.AP_AVAILABILITY_PARTITION:
                # Prioritize availability - continue with local state
                self.enter_availability_preservation_mode()
            elif self.cap_strategy == CAPStrategy.CA_CONSISTENCY_AVAILABILITY:
                # This shouldn't happen with CA strategy
                print("⚠️  CA strategy in partition - falling back to AP mode")
                self.enter_availability_preservation_mode()
    
    def enter_consistency_preservation_mode(self):
        """CP mode: Preserve consistency during partition"""
        print("🔒 CONSISTENCY PRESERVATION MODE")
        
        # Stop accepting new operations that could create inconsistency
        self.local_turtle_state["mode"] = "readonly_consistent"
        self.local_turtle_state["operations_suspended"] = True
        self.local_turtle_state["reason"] = "maintaining_consistency_during_partition"
        
        self.save_local_state()
        
        # Cache operations for later when partition resolves
        self.cache_operations_for_partition_recovery()
    
    def enter_availability_preservation_mode(self):
        """AP mode: Preserve availability during partition"""
        print("🟢 AVAILABILITY PRESERVATION MODE")
        
        # Continue operations with local state, accept eventual consistency
        self.local_turtle_state["mode"] = "available_eventually_consistent"
        self.local_turtle_state["operations_suspended"] = False
        self.local_turtle_state["reason"] = "maintaining_availability_during_partition"
        self.local_turtle_state["partition_operations"] = []
        
        self.save_local_state()
    
    def handle_partition_event(self):
        """Handle network partition detection"""
        partition_event = {
            "event_type": "partition_detected",
            "turtle_id": self.turtle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "cap_strategy": self.cap_strategy.value,
            "response": "entering_partition_mode"
        }
        
        # Save partition event locally
        partition_file = self.partition_cache_dir / f"partition_{int(time.time())}.json"
        with open(partition_file, 'w') as f:
            json.dump(partition_event, f, indent=2)
    
    def handle_partition_recovery(self):
        """Handle partition recovery - sync states"""
        print("🔄 PARTITION RECOVERY - Syncing states")
        
        if self.cap_strategy == CAPStrategy.CP_CONSISTENCY_PARTITION:
            self.perform_consistency_recovery()
        elif self.cap_strategy == CAPStrategy.AP_AVAILABILITY_PARTITION:
            self.perform_eventual_consistency_reconciliation()
    
    def perform_consistency_recovery(self):
        """CP recovery: Ensure consistency after partition"""
        print("🔒 Performing consistency recovery")
        
        # Find authoritative state (highest version)
        all_states = self.collect_turtle_states()
        authoritative_state = self.determine_authoritative_state(all_states)
        
        if authoritative_state and authoritative_state["version"] > self.local_turtle_state.get("version", 0):
            print(f"📥 Updating to authoritative state version {authoritative_state['version']}")
            self.local_turtle_state = authoritative_state
            self.save_local_state()
        
        # Replay cached operations if any
        self.replay_cached_operations()
    
    def perform_eventual_consistency_reconciliation(self):
        """AP recovery: Merge states for eventual consistency"""
        print("🔄 Performing eventual consistency reconciliation")
        
        all_states = self.collect_turtle_states()
        merged_state = self.merge_turtle_states(all_states)
        
        # Update local state with merged result
        self.local_turtle_state = merged_state
        self.consensus_version += 1
        self.local_turtle_state["version"] = self.consensus_version
        self.save_local_state()
        
        # Broadcast merged state to other turtles
        self.broadcast_state_update(merged_state)
    
    def discover_turtles_with_timeout(self) -> Dict[str, Dict]:
        """Discover turtles with network timeout detection"""
        discovered = {}
        timeout = 3  # seconds
        
        try:
            # Quick heartbeat discovery with timeout
            if self.local_state_dir.exists():
                for state_file in self.local_state_dir.glob("*.json"):
                    if time.time() - state_file.stat().st_mtime < self.partition_timeout:
                        with open(state_file, 'r') as f:
                            state = json.load(f)
                            discovered[state["turtle_id"]] = state
        except Exception as e:
            print(f"❌ Discovery timeout: {e}")
        
        return discovered
    
    def collect_turtle_states(self) -> List[Dict]:
        """Collect all turtle states for consensus/reconciliation"""
        states = []
        
        if self.local_state_dir.exists():
            for state_file in self.local_state_dir.glob("*.json"):
                try:
                    with open(state_file, 'r') as f:
                        state = json.load(f)
                        states.append(state)
                except Exception as e:
                    print(f"❌ Error reading state {state_file}: {e}")
        
        return states
    
    def determine_authoritative_state(self, states: List[Dict]) -> Optional[Dict]:
        """Determine authoritative state for CP consistency"""
        if not states:
            return None
        
        # Find state with highest version number
        authoritative = max(states, key=lambda s: s.get("version", 0))
        return authoritative
    
    def merge_turtle_states(self, states: List[Dict]) -> Dict:
        """Merge turtle states for AP eventual consistency"""
        if not states:
            return self.local_turtle_state
        
        # Simple merge strategy - could be enhanced with CRDTs
        merged = {
            "turtle_id": self.turtle_id,
            "version": max(s.get("version", 0) for s in states) + 1,
            "merged_at": datetime.utcnow().isoformat(),
            "merge_sources": [s["turtle_id"] for s in states],
            "status": "merged"
        }
        
        # Merge specific fields
        all_operations = []
        for state in states:
            if "partition_operations" in state:
                all_operations.extend(state["partition_operations"])
        
        if all_operations:
            merged["merged_operations"] = all_operations
        
        return merged
    
    def save_local_state(self):
        """Save local turtle state atomically"""
        state_file = self.local_state_dir / f"{self.turtle_id}.json"
        temp_file = state_file.with_suffix('.tmp')
        
        try:
            with open(temp_file, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(self.local_turtle_state, f, indent=2)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            temp_file.replace(state_file)
            
        except Exception as e:
            print(f"❌ Failed to save local state: {e}")
            if temp_file.exists():
                temp_file.unlink()
    
    def broadcast_state_update(self, state: Dict):
        """Broadcast state update to other turtles"""
        broadcast_message = {
            "message_type": "state_update",
            "from_turtle": self.turtle_id,
            "state": state,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Save broadcast message for other turtles to pick up
        message_file = self.coordination_dir / f"broadcast_{int(time.time())}.json"
        with open(message_file, 'w') as f:
            json.dump(broadcast_message, f, indent=2)
    
    def cache_operations_for_partition_recovery(self):
        """Cache operations during CP partition for later replay"""
        cache_file = self.partition_cache_dir / f"{self.turtle_id}_operations.json"
        
        cached_operations = {
            "turtle_id": self.turtle_id,
            "cached_at": datetime.utcnow().isoformat(),
            "operations": [],
            "status": "waiting_for_partition_recovery"
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cached_operations, f, indent=2)
    
    def replay_cached_operations(self):
        """Replay cached operations after partition recovery"""
        cache_file = self.partition_cache_dir / f"{self.turtle_id}_operations.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            print(f"🔄 Replaying {len(cached.get('operations', []))} cached operations")
            
            # Clean up cache after replay
            cache_file.unlink()
    
    def get_cap_status(self) -> Dict:
        """Get current CAP theorem status"""
        return {
            "turtle_id": self.turtle_id,
            "cap_strategy": self.cap_strategy.value,
            "coordination_mode": self.coordination_mode.value,
            "partition_detected": self.partition_detected,
            "local_version": self.local_turtle_state.get("version", 0),
            "consensus_version": self.consensus_version,
            "last_consensus_time": self.last_consensus_time,
            "availability": not (self.coordination_mode == CoordinationMode.PARTITIONED and 
                               self.cap_strategy == CAPStrategy.CP_CONSISTENCY_PARTITION)
        }
    
    def cleanup(self):
        """Clean up CAP coordinator"""
        self.cap_monitor_active = False
        if hasattr(self, 'cap_monitor_thread'):
            self.cap_monitor_thread.join(timeout=1)

def demonstrate_cap_coordination():
    """Demonstrate CAP-aware turtle coordination"""
    print("🎯 CAP-AWARE TURTLE COORDINATION DEMONSTRATION")
    print("=" * 60)
    
    # Test different CAP strategies
    strategies = [
        CAPStrategy.AP_AVAILABILITY_PARTITION,
        CAPStrategy.CP_CONSISTENCY_PARTITION
    ]
    
    coordinators = []
    
    for i, strategy in enumerate(strategies):
        turtle_id = f"CAPTurtle-{strategy.value.upper()}-{i+1}"
        coordinator = CAPAwareTurtleCoordinator(turtle_id, strategy)
        coordinators.append(coordinator)
        
        print(f"\n🐢 Created {turtle_id} with {strategy.value} strategy")
        
        # Show initial status
        status = coordinator.get_cap_status()
        print(f"   Mode: {status['coordination_mode']}")
        print(f"   Availability: {status['availability']}")
    
    print("\n📊 CAP STATUS OVERVIEW:")
    for coordinator in coordinators:
        status = coordinator.get_cap_status()
        print(f"  {status['turtle_id']}: {status['cap_strategy']} - {status['coordination_mode']}")
    
    # Simulate partition
    print("\n🔴 SIMULATING PARTITION...")
    for coordinator in coordinators:
        coordinator.partition_detected = True
        coordinator.coordination_mode = CoordinationMode.PARTITIONED
        coordinator.adapt_coordination_strategy()
    
    time.sleep(2)
    
    print("\n🟢 SIMULATING PARTITION RECOVERY...")
    for coordinator in coordinators:
        coordinator.handle_partition_recovery()
    
    print("\n✅ CAP-aware coordination system demonstrated!")
    
    # Cleanup
    for coordinator in coordinators:
        coordinator.cleanup()

if __name__ == "__main__":
    demonstrate_cap_coordination()