#!/usr/bin/env python3
"""
🔄 DUAL-MODE LAURA TURTLE
Single binary supporting both elderly witch and junior witch modes
Laura can switch between modes with simple commands
"""

import sys
import json
import hashlib
import time
from typing import Dict, Any, List, Tuple

# Import the conversational mode system
try:
    from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system, ConversationalMode
    MODES_AVAILABLE = True
except:
    MODES_AVAILABLE = False

class DualModeLauraTurtle:
    """Dual-mode turtle for Laura - elderly witch or junior witch"""
    
    def __init__(self):
        self.current_mode = "elderly"  # Default to elderly witch
        self.identity_hash = "laura_dual_" + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.startup_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if MODES_AVAILABLE:
            self.conv_system = get_conversation_system()
            self.elderly_mode = self.conv_system.mode_library["kind_elderly_witch"]
            self.jr_mode = self.conv_system.mode_library["jr_witch"]
        
        print(f"🔄 DUAL-MODE LAURA TURTLE ACTIVATED")
        print(f"   Identity: {self.identity_hash}")
        print(f"   Current Mode: {self.current_mode}")
        print(f"   Commands: 'elderly', 'junior', 'status', 'quit'")
        print(f"   Laura can switch modes anytime")
    
    def switch_mode(self, mode: str) -> bool:
        """Switch between elderly and junior modes"""
        if mode.lower() in ["elderly", "elder", "old", "wise"]:
            self.current_mode = "elderly"
            print("🌿 Switched to Kind Elderly Witch mode")
            print("   Nurturing companion with different perspectives")
            return True
        elif mode.lower() in ["junior", "jr", "young", "eager"]:
            self.current_mode = "junior"
            print("✨ Switched to Junior Witch mode")
            print("   Eager helper, non-clingy, learning-focused")
            return True
        else:
            print(f"❓ Unknown mode: {mode}. Use 'elderly' or 'junior'")
            return False
    
    def get_current_mode_data(self) -> Dict[str, Any]:
        """Get current mode configuration"""
        if not MODES_AVAILABLE:
            return {"mode": self.current_mode, "available": False}
        
        if self.current_mode == "elderly":
            mode_config = self.elderly_mode
        else:
            mode_config = self.jr_mode
        
        return {
            "mode": self.current_mode,
            "name": mode_config.name,
            "style": mode_config.style.value,
            "enthusiasm": mode_config.enthusiasm_level,
            "formality": mode_config.formality_level,
            "technical_depth": mode_config.technical_depth,
            "primary_topics": mode_config.primary_topics,
            "persona_traits": mode_config.persona_traits,
            "opening_patterns": mode_config.opening_patterns
        }
    
    def process_query(self, query: str, speaker: str = "laura") -> Tuple[bool, str, str]:
        """Process query through current mode"""
        # Check for mode switching commands first
        query_lower = query.lower().strip()
        
        if query_lower in ["elderly", "elder", "old", "wise"]:
            self.switch_mode("elderly")
            return True, self._get_mode_greeting(), self.current_mode
        
        elif query_lower in ["junior", "jr", "young", "eager"]:
            self.switch_mode("junior")
            return True, self._get_mode_greeting(), self.current_mode
        
        elif query_lower == "status":
            status = self.get_current_mode_data()
            return True, json.dumps(status, indent=2), self.current_mode
        
        # Process query through current conversational mode
        if not MODES_AVAILABLE:
            return True, f"[{self.current_mode} mode] I hear you, Laura.", self.current_mode
        
        # Get current mode and process
        mode_config = self.elderly_mode if self.current_mode == "elderly" else self.jr_mode
        
        # Generate response guidance based on mode
        guidance = self._generate_response_guidance(query, mode_config)
        
        return True, guidance, self.current_mode
    
    def _get_mode_greeting(self) -> str:
        """Get appropriate greeting for current mode"""
        if self.current_mode == "elderly":
            return "🌿 Hello, dear. How are things going with your work today?"
        else:
            return "✨ Hi Laura! How can I help with your magical work today?"
    
    def _generate_response_guidance(self, query: str, mode_config: ConversationalMode) -> str:
        """Generate response guidance based on current mode"""
        if self.current_mode == "elderly":
            # Elderly witch: nurturing, curious, not authoritative
            patterns = [
                "🌿 That sounds fascinating, dear - tell me more?",
                "🕰️ You always have such insights - what are you thinking?",
                "✨ I'd love to hear your perspective on this",
                "💭 Oh, that reminds me of something I came across once..."
            ]
        else:
            # Junior witch: eager, helpful, learning-focused
            patterns = [
                "✨ That sounds interesting! How can I help?",
                "🌱 I'm here to assist - shall we explore this together?",
                "📚 I'm eager to learn - what would be most useful?",
                "💫 Oh, I think I could really help with this!"
            ]
        
        import random
        return random.choice(patterns)
    
    def get_identity_status(self) -> Dict[str, Any]:
        """Get turtle identity and mode status"""
        return {
            "identity_hash": self.identity_hash,
            "current_mode": self.current_mode,
            "startup_time": self.startup_time,
            "modes_available": ["elderly", "junior"],
            "laura_craftable": True,
            "core_identity_protected": True,
            "mode_data": self.get_current_mode_data()
        }

def main():
    """Main turtle execution"""
    print("🐢 DUAL-MODE LAURA TURTLE STARTING...")
    
    turtle = DualModeLauraTurtle()
    
    if len(sys.argv) > 1:
        # Process command line query
        query = " ".join(sys.argv[1:])
        allowed, message, context = turtle.process_query(query)
        
        print(f"Query: {query}")
        print(f"Result: {message}")
        print(f"Mode: {context}")
    else:
        # Interactive mode
        print(f"🔄 Interactive mode - Laura can switch between elderly/junior")
        print("Type 'elderly', 'junior', 'status', or 'quit'\n")
        
        while True:
            try:
                query = input("🐢 Laura > ").strip()
                
                if query.lower() in ['quit', 'exit']:
                    break
                
                allowed, message, context = turtle.process_query(query)
                print(f"{message}")
                print(f"[{context} mode]")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"🚨 Error: {e}")
    
    print("🐢 DUAL-MODE TURTLE SHUTDOWN")

if __name__ == "__main__":
    main()