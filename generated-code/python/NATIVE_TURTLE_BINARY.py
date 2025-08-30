#!/usr/bin/env python3
"""
🐢 NATIVE TURTLE BINARY - FLEET-FIRST ARCHITECTURE
Single self-contained binary that spawns LLM processes and turtle fleets
No dependency on Claude tooling - pure native turtle implementation
"""

import subprocess
import json
import os
import sys
import time
import signal
import threading
import socket
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import argparse

class TurtleMode(Enum):
    PRIME = "prime"           # Prime turtle - fleet coordinator
    SPAWN = "spawn"           # Spawn new turtle process
    WORKER = "worker"         # Worker turtle process
    LLM_HOST = "llm_host"     # Host for LLM process

@dataclass
class TurtleProcessSpec:
    """Specification for turtle process"""
    turtle_id: str
    mode: TurtleMode
    specialization: str
    llm_provider: str
    llm_model: str
    parent_pid: Optional[int] = None
    communication_port: Optional[int] = None
    working_directory: str = os.getcwd()

class NativeLLMInterface:
    """Native interface to LLM processes"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.process = None
        self.communication_port = None
        
    def spawn_llm_process(self) -> subprocess.Popen:
        """Spawn native LLM process"""
        try:
            if self.provider == "ollama":
                return self._spawn_ollama_process()
            elif self.provider == "local":
                return self._spawn_local_llm_process()
            elif self.provider == "api":
                return self._spawn_api_wrapper_process()
            elif self.provider == "mock":
                return self._spawn_mock_llm_process()
            else:
                print(f"⚠️  LLM provider {self.provider} not available, using mock mode")
                return self._spawn_mock_llm_process()
        except FileNotFoundError:
            print(f"⚠️  {self.provider} not installed, using mock mode")
            return self._spawn_mock_llm_process()
    
    def _spawn_ollama_process(self) -> subprocess.Popen:
        """Spawn Ollama LLM process"""
        cmd = ["ollama", "serve"]
        env = os.environ.copy()
        env["OLLAMA_MODEL"] = self.model
        
        return subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def _spawn_local_llm_process(self) -> subprocess.Popen:
        """Spawn local LLM process (e.g., llama.cpp)"""
        cmd = ["./llama.cpp/main", "-m", self.model, "--port", "8080"]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def _spawn_api_wrapper_process(self) -> subprocess.Popen:
        """Spawn API wrapper process for external LLMs"""
        # This would be a lightweight API wrapper process
        wrapper_script = Path(__file__).parent / "llm_api_wrapper.py"
        cmd = [sys.executable, str(wrapper_script), "--provider", self.provider, "--model", self.model]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def _spawn_mock_llm_process(self) -> subprocess.Popen:
        """Spawn mock LLM process for testing"""
        cmd = [sys.executable, "-c", 
               "import time; print('🤖 Mock LLM started'); time.sleep(3600)"]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

class NativeTurtleProcess:
    """Native turtle process - independent of Claude tooling"""
    
    def __init__(self, spec: TurtleProcessSpec):
        self.spec = spec
        self.pid = os.getpid()
        self.llm_interface = NativeLLMInterface(spec.llm_provider, spec.llm_model)
        self.llm_process = None
        self.child_processes: Dict[int, subprocess.Popen] = {}
        self.communication_server = None
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)
        
        print(f"🐢 Native turtle process started: {self.spec.turtle_id} (PID: {self.pid})")
    
    def initialize(self):
        """Initialize turtle process"""
        print(f"🔧 Initializing {self.spec.turtle_id} in {self.spec.mode.value} mode")
        
        # Start LLM process if needed
        if self.spec.mode in [TurtleMode.PRIME, TurtleMode.WORKER]:
            self.llm_process = self.llm_interface.spawn_llm_process()
            print(f"🤖 Started LLM process: {self.spec.llm_provider}/{self.spec.llm_model}")
        
        # Start communication server
        self._start_communication_server()
        
        # Initialize based on mode
        if self.spec.mode == TurtleMode.PRIME:
            self._initialize_prime_turtle()
        elif self.spec.mode == TurtleMode.WORKER:
            self._initialize_worker_turtle()
        elif self.spec.mode == TurtleMode.LLM_HOST:
            self._initialize_llm_host()
    
    def _start_communication_server(self):
        """Start inter-process communication server"""
        self.spec.communication_port = self._find_free_port()
        
        def server_thread():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', self.spec.communication_port))
            server_socket.listen(5)
            
            print(f"📡 Communication server listening on port {self.spec.communication_port}")
            
            while True:
                try:
                    client_socket, address = server_socket.accept()
                    self._handle_communication(client_socket)
                except Exception as e:
                    print(f"❌ Communication error: {e}")
                    break
        
        self.communication_server = threading.Thread(target=server_thread, daemon=True)
        self.communication_server.start()
    
    def _find_free_port(self) -> int:
        """Find free port for communication"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def _handle_communication(self, client_socket):
        """Handle inter-turtle communication"""
        try:
            data = client_socket.recv(4096).decode('utf-8')
            message = json.loads(data)
            
            response = self._process_turtle_message(message)
            
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"❌ Message handling error: {e}")
        finally:
            client_socket.close()
    
    def _process_turtle_message(self, message: Dict) -> Dict:
        """Process message from another turtle"""
        message_type = message.get("type")
        
        if message_type == "spawn_request":
            return self._handle_spawn_request(message)
        elif message_type == "task_delegation":
            return self._handle_task_delegation(message)
        elif message_type == "status_query":
            return self._handle_status_query(message)
        else:
            return {"status": "unknown_message_type", "type": message_type}
    
    def _handle_spawn_request(self, message: Dict) -> Dict:
        """Handle request to spawn new turtle"""
        spawn_spec = TurtleProcessSpec(
            turtle_id=message["turtle_id"],
            mode=TurtleMode(message["mode"]),
            specialization=message["specialization"],
            llm_provider=message["llm_provider"],
            llm_model=message["llm_model"],
            parent_pid=self.pid
        )
        
        child_process = self.spawn_child_turtle(spawn_spec)
        
        if child_process:
            return {
                "status": "spawned",
                "turtle_id": spawn_spec.turtle_id,
                "child_pid": child_process.pid
            }
        else:
            return {"status": "spawn_failed"}
    
    def _handle_task_delegation(self, message: Dict) -> Dict:
        """Handle task delegation from another turtle"""
        task = message.get("task")
        print(f"📋 Received task delegation: {task}")
        
        # This would integrate with LLM process to execute task
        return {
            "status": "task_accepted",
            "task_id": message.get("task_id"),
            "estimated_completion": "5_minutes"
        }
    
    def _handle_status_query(self, message: Dict) -> Dict:
        """Handle status query"""
        return {
            "status": "active",
            "turtle_id": self.spec.turtle_id,
            "mode": self.spec.mode.value,
            "pid": self.pid,
            "llm_provider": self.spec.llm_provider,
            "child_count": len(self.child_processes),
            "uptime_seconds": time.time() - self.start_time if hasattr(self, 'start_time') else 0
        }
    
    def spawn_child_turtle(self, child_spec: TurtleProcessSpec) -> Optional[subprocess.Popen]:
        """Spawn child turtle process"""
        print(f"🥚 Spawning child turtle: {child_spec.turtle_id}")
        
        # Create command to launch new turtle process
        cmd = [
            sys.executable, 
            __file__,  # This script
            "--mode", child_spec.mode.value,
            "--turtle-id", child_spec.turtle_id,
            "--specialization", child_spec.specialization,
            "--llm-provider", child_spec.llm_provider,
            "--llm-model", child_spec.llm_model,
            "--parent-pid", str(self.pid),
            "--working-directory", child_spec.working_directory
        ]
        
        try:
            child_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=child_spec.working_directory
            )
            
            self.child_processes[child_process.pid] = child_process
            print(f"✅ Child turtle spawned: PID {child_process.pid}")
            
            return child_process
            
        except Exception as e:
            print(f"❌ Failed to spawn child turtle: {e}")
            return None
    
    def send_message_to_turtle(self, target_port: int, message: Dict) -> Optional[Dict]:
        """Send message to another turtle process"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', target_port))
            
            client_socket.send(json.dumps(message).encode('utf-8'))
            response_data = client_socket.recv(4096).decode('utf-8')
            
            client_socket.close()
            
            return json.loads(response_data)
            
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return None
    
    def _initialize_prime_turtle(self):
        """Initialize prime turtle coordinator"""
        self.start_time = time.time()
        print(f"👑 Prime turtle {self.spec.turtle_id} initialized")
        
        # Prime turtle starts with basic fleet management capabilities
        self._register_prime_turtle()
        
        # Start main coordination loop
        self._run_prime_coordination_loop()
    
    def _initialize_worker_turtle(self):
        """Initialize worker turtle"""
        self.start_time = time.time()
        print(f"👷 Worker turtle {self.spec.turtle_id} initialized")
        
        # Register with parent
        if self.spec.parent_pid:
            self._register_with_parent()
        
        # Start worker loop
        self._run_worker_loop()
    
    def _initialize_llm_host(self):
        """Initialize LLM host process"""
        print(f"🤖 LLM host {self.spec.turtle_id} initialized")
        
        # Just maintain the LLM process
        self._run_llm_host_loop()
    
    def _register_prime_turtle(self):
        """Register as prime turtle in system"""
        prime_registry = Path(".turtle/prime_registry.json")
        prime_registry.parent.mkdir(exist_ok=True)
        
        registry_data = {
            "prime_turtle_id": self.spec.turtle_id,
            "pid": self.pid,
            "communication_port": self.spec.communication_port,
            "started_at": time.time(),
            "working_directory": self.spec.working_directory
        }
        
        with open(prime_registry, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def _register_with_parent(self):
        """Register with parent turtle"""
        # Would send registration message to parent
        print(f"📝 Registering with parent PID {self.spec.parent_pid}")
    
    def _run_prime_coordination_loop(self):
        """Main coordination loop for prime turtle"""
        print(f"🔄 Starting prime coordination loop")
        
        while True:
            try:
                # Monitor child processes
                self._monitor_child_processes()
                
                # Handle any pending coordination tasks
                # (This would integrate with LLM for decision making)
                
                time.sleep(5)  # Coordination interval
                
            except KeyboardInterrupt:
                print(f"🛑 Prime turtle shutting down")
                break
            except Exception as e:
                print(f"❌ Coordination loop error: {e}")
                time.sleep(5)
    
    def _run_worker_loop(self):
        """Main loop for worker turtle"""
        print(f"🔄 Starting worker loop")
        
        while True:
            try:
                # Worker tasks would be handled through communication messages
                time.sleep(1)
                
            except KeyboardInterrupt:
                print(f"🛑 Worker turtle shutting down")
                break
            except Exception as e:
                print(f"❌ Worker loop error: {e}")
                time.sleep(1)
    
    def _run_llm_host_loop(self):
        """Main loop for LLM host"""
        print(f"🔄 Starting LLM host loop")
        
        while True:
            try:
                if self.llm_process and self.llm_process.poll() is not None:
                    print(f"❌ LLM process died, restarting...")
                    self.llm_process = self.llm_interface.spawn_llm_process()
                
                time.sleep(10)  # Health check interval
                
            except KeyboardInterrupt:
                print(f"🛑 LLM host shutting down")
                break
            except Exception as e:
                print(f"❌ LLM host loop error: {e}")
                time.sleep(10)
    
    def _monitor_child_processes(self):
        """Monitor health of child processes"""
        dead_children = []
        
        for pid, process in self.child_processes.items():
            if process.poll() is not None:
                dead_children.append(pid)
                print(f"💀 Child process {pid} has died")
        
        # Clean up dead children
        for pid in dead_children:
            del self.child_processes[pid]
    
    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        print(f"🛑 Received shutdown signal {signum}")
        
        # Shutdown child processes
        for pid, process in self.child_processes.items():
            print(f"🛑 Shutting down child {pid}")
            process.terminate()
            
        # Shutdown LLM process
        if self.llm_process:
            print(f"🛑 Shutting down LLM process")
            self.llm_process.terminate()
        
        sys.exit(0)

def main():
    """Main entry point for native turtle binary"""
    parser = argparse.ArgumentParser(description="Native Turtle Binary - Fleet-First Architecture")
    
    parser.add_argument("--mode", type=str, choices=[m.value for m in TurtleMode], 
                       default="prime", help="Turtle mode")
    parser.add_argument("--turtle-id", type=str, default="PrimeTurtle-NATIVE", 
                       help="Turtle identifier")
    parser.add_argument("--specialization", type=str, default="fleet_coordination", 
                       help="Turtle specialization")
    parser.add_argument("--llm-provider", type=str, default="ollama", 
                       help="LLM provider")
    parser.add_argument("--llm-model", type=str, default="llama3", 
                       help="LLM model")
    parser.add_argument("--parent-pid", type=int, help="Parent process PID")
    parser.add_argument("--working-directory", type=str, default=os.getcwd(), 
                       help="Working directory")
    
    # Special commands
    parser.add_argument("--spawn", nargs=4, metavar=("ID", "SPEC", "PROVIDER", "MODEL"),
                       help="Spawn new turtle: turtle_id specialization llm_provider llm_model")
    parser.add_argument("--list", action="store_true", help="List active turtles")
    parser.add_argument("--status", type=str, help="Get status of turtle by ID")
    
    args = parser.parse_args()
    
    if args.spawn:
        # Spawn command - connect to prime turtle and request spawn
        turtle_id, specialization, llm_provider, llm_model = args.spawn
        print(f"🥚 Requesting spawn: {turtle_id}")
        # Would send spawn request to prime turtle
        return
    
    if args.list:
        # List active turtles
        print("🐢 Active Turtles:")
        # Would query prime turtle for list
        return
    
    if args.status:
        # Get turtle status
        print(f"📊 Status for {args.status}:")
        # Would query specific turtle for status
        return
    
    # Normal turtle process startup
    spec = TurtleProcessSpec(
        turtle_id=args.turtle_id,
        mode=TurtleMode(args.mode),
        specialization=args.specialization,
        llm_provider=args.llm_provider,
        llm_model=args.llm_model,
        parent_pid=args.parent_pid,
        working_directory=args.working_directory
    )
    
    turtle = NativeTurtleProcess(spec)
    turtle.initialize()

if __name__ == "__main__":
    main()