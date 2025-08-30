#!/usr/bin/env python3
"""
🔐 IDENTITY-LOCKED TURTLE GENERATOR
Generate custom turtle binaries with embedded identity and conversational mode lockdown
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from CONVERSATIONAL_MODE_SYSTEM import ConversationalMode, ConversationStyle, KnowledgeDepth, ResponsePattern

@dataclass
class TurtleIdentity:
    """Locked turtle identity configuration"""
    identity_name: str
    identity_hash: str
    locked_mode: ConversationalMode
    creation_time: str
    purpose: str
    authorized_parties: List[str]
    expiration_time: Optional[str] = None
    
    # Identity enforcement
    mandatory_topics: List[str] = None
    forbidden_topics: List[str] = None
    behavior_constraints: Dict[str, Any] = None
    
    # Security parameters
    tamper_detection: bool = True
    mode_modification_locked: bool = True
    topic_drift_prevention: bool = True

class IdentityLockedTurtleGenerator:
    """Generate custom turtle binaries with locked identities"""
    
    def __init__(self):
        self.generated_turtles: Dict[str, TurtleIdentity] = {}
        self.turtle_directory = "identity_locked_turtles/"
        os.makedirs(self.turtle_directory, exist_ok=True)
        
        # Load existing identities
        self._load_existing_identities()
    
    def generate_identity_locked_turtle(self, 
                                      identity_name: str,
                                      conversational_mode: ConversationalMode,
                                      purpose: str,
                                      authorized_parties: List[str],
                                      **constraints) -> str:
        """Generate a custom turtle binary locked to specific identity and mode"""
        
        # Create identity hash
        identity_data = f"{identity_name}_{purpose}_{time.time()}"
        identity_hash = hashlib.sha256(identity_data.encode()).hexdigest()[:16]
        
        # Create turtle identity
        turtle_identity = TurtleIdentity(
            identity_name=identity_name,
            identity_hash=identity_hash,
            locked_mode=conversational_mode,
            creation_time=time.strftime("%Y-%m-%d %H:%M:%S"),
            purpose=purpose,
            authorized_parties=authorized_parties,
            expiration_time=constraints.get('expiration_time'),
            mandatory_topics=constraints.get('mandatory_topics', []),
            forbidden_topics=constraints.get('forbidden_topics', []),
            behavior_constraints=constraints.get('behavior_constraints', {}),
            tamper_detection=constraints.get('tamper_detection', True),
            mode_modification_locked=constraints.get('mode_modification_locked', True),
            topic_drift_prevention=constraints.get('topic_drift_prevention', True)
        )
        
        # Generate the locked turtle binary
        binary_filename = f"turtle_{identity_name.lower()}_{identity_hash}"
        binary_path = os.path.join(self.turtle_directory, binary_filename)
        
        turtle_code = self._generate_locked_turtle_code(turtle_identity)
        
        with open(binary_path, 'w') as f:
            f.write(turtle_code)
        
        # Make executable
        os.chmod(binary_path, 0o755)
        
        # Store identity
        self.generated_turtles[identity_hash] = turtle_identity
        self._save_identity_registry()
        
        print(f"🔐 IDENTITY-LOCKED TURTLE GENERATED")
        print(f"   Identity: {identity_name}")
        print(f"   Hash: {identity_hash}")
        print(f"   Binary: {binary_path}")
        print(f"   Mode: {conversational_mode.name}")
        print(f"   Purpose: {purpose}")
        print(f"   Authorized: {', '.join(authorized_parties)}")
        
        return binary_path
    
    def _generate_locked_turtle_code(self, identity: TurtleIdentity) -> str:
        """Generate the actual locked turtle binary code"""
        
        # Serialize the locked mode for embedding
        mode_data = {
            "name": identity.locked_mode.name,
            "party_context": identity.locked_mode.party_context,
            "style": identity.locked_mode.style.value,
            "knowledge_depth": identity.locked_mode.knowledge_depth.value,
            "response_pattern": identity.locked_mode.response_pattern.value,
            "enthusiasm_level": identity.locked_mode.enthusiasm_level,
            "formality_level": identity.locked_mode.formality_level,
            "technical_depth": identity.locked_mode.technical_depth,
            "primary_topics": identity.locked_mode.primary_topics,
            "secondary_topics": identity.locked_mode.secondary_topics,
            "topic_strictness": identity.locked_mode.topic_strictness,
            "connection_patterns": identity.locked_mode.connection_patterns,
            "redirection_patterns": identity.locked_mode.redirection_patterns,
            "persona_traits": identity.locked_mode.persona_traits,
            "conversation_goals": identity.locked_mode.conversation_goals
        }
        
        # Generate tamper-resistant embedding
        mode_json = json.dumps(mode_data, separators=(',', ':'))
        mode_hash = hashlib.sha256(mode_json.encode()).hexdigest()
        
        turtle_code = f'''#!/usr/bin/env python3
"""
🔐 IDENTITY-LOCKED TURTLE: {identity.identity_name}
Generated: {identity.creation_time}
Purpose: {identity.purpose}
Hash: {identity.identity_hash}
Mode Hash: {mode_hash}

TAMPER WARNING: This binary has embedded identity and conversational mode lockdown.
Any modification will break identity verification and disable the turtle.
"""

import sys
import json
import hashlib
import time
from typing import Dict, Any, List, Tuple

# EMBEDDED LOCKED CONFIGURATION - DO NOT MODIFY
LOCKED_IDENTITY_HASH = "{identity.identity_hash}"
LOCKED_MODE_HASH = "{mode_hash}"
LOCKED_MODE_DATA = """{mode_json}"""

AUTHORIZED_PARTIES = {json.dumps(identity.authorized_parties)}
MANDATORY_TOPICS = {json.dumps(identity.mandatory_topics or [])}
FORBIDDEN_TOPICS = {json.dumps(identity.forbidden_topics or [])}
CREATION_TIME = "{identity.creation_time}"
PURPOSE = "{identity.purpose}"
EXPIRATION_TIME = "{identity.expiration_time}"

# Identity enforcement flags
TAMPER_DETECTION_ENABLED = {str(identity.tamper_detection)}
MODE_MODIFICATION_LOCKED = {str(identity.mode_modification_locked)}
TOPIC_DRIFT_PREVENTION = {str(identity.topic_drift_prevention)}

class IdentityLockedTurtle:
    """Identity-locked turtle with embedded conversational mode"""
    
    def __init__(self):
        self.identity_verified = False
        self.mode_data = None
        self.startup_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Verify identity integrity on startup
        if not self._verify_identity_integrity():
            print("🚨 IDENTITY VERIFICATION FAILED - TURTLE DISABLED")
            sys.exit(1)
        
        print(f"🔐 IDENTITY-LOCKED TURTLE ACTIVATED")
        print(f"   Identity: {{LOCKED_IDENTITY_HASH}}")
        print(f"   Purpose: {{PURPOSE}}")
        print(f"   Mode: {{self.mode_data['name']}}")
        print(f"   Authorized Parties: {{', '.join(AUTHORIZED_PARTIES)}}")
        
        # Activate locked conversational mode
        self._activate_locked_mode()
    
    def _verify_identity_integrity(self) -> bool:
        """Verify turtle identity and configuration integrity"""
        if not TAMPER_DETECTION_ENABLED:
            self.identity_verified = True
            self.mode_data = json.loads(LOCKED_MODE_DATA)
            return True
        
        # Verify mode data hash
        calculated_hash = hashlib.sha256(LOCKED_MODE_DATA.encode()).hexdigest()
        if calculated_hash != LOCKED_MODE_HASH:
            print("🚨 MODE DATA TAMPERED - HASH MISMATCH")
            return False
        
        # Check expiration
        if EXPIRATION_TIME:
            import datetime
            expiry = datetime.datetime.strptime(EXPIRATION_TIME, "%Y-%m-%d %H:%M:%S")
            if datetime.datetime.now() > expiry:
                print("🚨 TURTLE IDENTITY EXPIRED")
                return False
        
        self.identity_verified = True
        self.mode_data = json.loads(LOCKED_MODE_DATA)
        return True
    
    def _activate_locked_mode(self):
        """Activate the embedded conversational mode"""
        if not self.identity_verified:
            return
        
        print(f"🎭 LOCKED MODE ACTIVATED: {{self.mode_data['name']}}")
        print(f"   Style: {{self.mode_data['style']}}")
        print(f"   Topics: {{', '.join(self.mode_data['primary_topics'])}}")
        print(f"   Strictness: {{self.mode_data['topic_strictness']}}")
    
    def process_query(self, query: str, speaker: str = "human") -> Tuple[bool, str, str]:
        """Process query through locked conversational mode"""
        if not self.identity_verified:
            return False, "🚨 IDENTITY NOT VERIFIED - QUERY BLOCKED", ""
        
        # Check authorized parties
        if speaker not in AUTHORIZED_PARTIES and "human" not in AUTHORIZED_PARTIES:
            return False, f"🚨 UNAUTHORIZED PARTY: {{speaker}} - ACCESS DENIED", ""
        
        # Check forbidden topics
        query_lower = query.lower()
        for forbidden in FORBIDDEN_TOPICS:
            if forbidden.lower() in query_lower:
                return False, f"⛔ FORBIDDEN TOPIC DETECTED: {{forbidden}} - QUERY BLOCKED", ""
        
        # Topic relevance check
        if TOPIC_DRIFT_PREVENTION and self.mode_data['primary_topics']:
            if not self._is_query_relevant(query):
                # Generate locked redirection
                redirection = self._generate_locked_redirection(query)
                return False, redirection, self.mode_data['style']
        
        # Query approved - generate response context
        response_context = {{
            "identity": LOCKED_IDENTITY_HASH,
            "mode": self.mode_data['name'],
            "style": self.mode_data['style'],
            "enthusiasm": self.mode_data['enthusiasm_level'],
            "formality": self.mode_data['formality_level'],
            "technical_depth": self.mode_data['technical_depth'],
            "primary_topics": self.mode_data['primary_topics'],
            "persona_traits": self.mode_data['persona_traits']
        }}
        
        return True, "✅ QUERY APPROVED", json.dumps(response_context)
    
    def _is_query_relevant(self, query: str) -> bool:
        """Check if query is relevant to locked topics"""
        query_lower = query.lower()
        
        # Check primary topics
        primary_matches = 0
        for topic in self.mode_data['primary_topics']:
            if topic.lower().replace('_', ' ') in query_lower:
                primary_matches += 1
        
        # Check secondary topics
        secondary_matches = 0
        for topic in self.mode_data.get('secondary_topics', []):
            if topic.lower().replace('_', ' ') in query_lower:
                secondary_matches += 1
        
        # Determine relevance based on strictness
        strictness = self.mode_data['topic_strictness']
        
        if strictness >= 0.9:  # Very strict - require primary topic match
            return primary_matches > 0
        elif strictness >= 0.7:  # Moderate - primary or multiple secondary
            return primary_matches > 0 or secondary_matches >= 2
        else:  # Flexible - any topic match
            return primary_matches > 0 or secondary_matches > 0
    
    def _generate_locked_redirection(self, query: str) -> str:
        """Generate redirection message based on locked mode"""
        if self.mode_data['redirection_patterns']:
            pattern = self.mode_data['redirection_patterns'][0]
            return pattern.format(topic=', '.join(self.mode_data['primary_topics']))
        
        # Default redirection based on style
        style = self.mode_data['style']
        topics = ', '.join(self.mode_data['primary_topics'])
        
        if style == 'obsessed':
            return f"🔥 I can't think about anything except {{topics}}! How does your question relate to this fascinating research?"
        elif style == 'professional':
            return f"🎯 This turtle is locked to {{topics}}. Please rephrase your question to relate to these areas."
        else:
            return f"🔒 Topic lockdown active: {{topics}}. Let's focus on these areas instead."
    
    def get_identity_status(self) -> Dict[str, Any]:
        """Get current identity and mode status"""
        return {{
            "identity_verified": self.identity_verified,
            "identity_hash": LOCKED_IDENTITY_HASH,
            "purpose": PURPOSE,
            "authorized_parties": AUTHORIZED_PARTIES,
            "locked_mode": self.mode_data['name'] if self.mode_data else None,
            "primary_topics": self.mode_data['primary_topics'] if self.mode_data else [],
            "creation_time": CREATION_TIME,
            "startup_time": self.startup_time,
            "tamper_detection": TAMPER_DETECTION_ENABLED,
            "mode_locked": MODE_MODIFICATION_LOCKED,
            "drift_prevention": TOPIC_DRIFT_PREVENTION
        }}

def main():
    """Main turtle execution"""
    print("🐢 IDENTITY-LOCKED TURTLE STARTING...")
    
    turtle = IdentityLockedTurtle()
    
    if len(sys.argv) > 1:
        # Process command line query
        query = " ".join(sys.argv[1:])
        allowed, message, context = turtle.process_query(query)
        
        print(f"Query: {{query}}")
        print(f"Result: {{message}}")
        if context:
            print(f"Context: {{context}}")
    else:
        # Interactive mode
        print(f"🔐 Interactive mode - Identity: {{LOCKED_IDENTITY_HASH}}")
        print(f"📋 Purpose: {{PURPOSE}}")
        print(f"🎭 Mode: {{turtle.mode_data['name']}}")
        print("Type 'status' for identity status, 'quit' to exit\\n")
        
        while True:
            try:
                query = input("🐢 > ").strip()
                
                if query.lower() in ['quit', 'exit']:
                    break
                elif query.lower() == 'status':
                    status = turtle.get_identity_status()
                    print(json.dumps(status, indent=2))
                    continue
                
                allowed, message, context = turtle.process_query(query)
                print(f"{{message}}")
                if context and context != "":
                    context_data = json.loads(context)
                    print(f"[{{context_data['style']}}] [{{context_data['mode']}}]")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"🚨 Error: {{e}}")
    
    print("🐢 IDENTITY-LOCKED TURTLE SHUTDOWN")

if __name__ == "__main__":
    main()
'''
        
        return turtle_code
    
    def create_lachmann_interview_turtle(self) -> str:
        """Create specialized turtle for Lachmann interview"""
        from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
        
        system = get_conversation_system()
        lachmann_mode = system.mode_library["lachmann_obsession"]
        
        return self.generate_identity_locked_turtle(
            identity_name="LachmannInterviewer",
            conversational_mode=lachmann_mode,
            purpose="Michael Lachmann interview with obsession mode lockdown",
            authorized_parties=["human", "michael_lachmann", "interviewer"],
            mandatory_topics=["origins_of_life", "information_theory", "lachmann_research"],
            forbidden_topics=["weather", "sports", "food", "general_chat"],
            topic_drift_prevention=True,
            mode_modification_locked=True,
            tamper_detection=True
        )
    
    def create_academic_paper_turtle(self) -> str:
        """Create specialized turtle for academic paper work"""
        from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
        
        system = get_conversation_system()
        academic_mode = system.mode_library["academic_rigorous"]
        
        return self.generate_identity_locked_turtle(
            identity_name="AcademicWriter",
            conversational_mode=academic_mode,
            purpose="Rigorous academic research and writing",
            authorized_parties=["human", "research_team", "co_authors"],
            mandatory_topics=["entropy_reduction", "academic_research", "peer_review"],
            behavior_constraints={
                "require_citations": True,
                "maintain_rigor": True,
                "avoid_speculation": True
            }
        )
    
    def create_business_presentation_turtle(self) -> str:
        """Create specialized turtle for business presentations"""
        from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
        
        system = get_conversation_system()
        business_mode = system.mode_library["business_executive"]
        
        return self.generate_identity_locked_turtle(
            identity_name="BusinessPresenter",
            conversational_mode=business_mode,
            purpose="Executive stakeholder communication",
            authorized_parties=["human", "executives", "stakeholders"],
            mandatory_topics=["business_value", "roi", "market_impact"],
            forbidden_topics=["technical_details", "implementation_specifics"],
            behavior_constraints={
                "focus_on_value": True,
                "quantify_impact": True,
                "executive_language": True
            }
        )
    
    def create_laura_dual_mode_turtle(self, purpose: str = "Dual-mode companion for Laura Ferguson") -> str:
        """Create turtle with both elderly and junior witch modes - Laura can switch"""
        from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
        
        system = get_conversation_system()
        # Use elderly as default, but embed both modes
        elderly_mode = system.mode_library["kind_elderly_witch"]
        
        return self.generate_identity_locked_turtle(
            identity_name="LauraDualMode",
            conversational_mode=elderly_mode,  # Default mode
            purpose=purpose,
            authorized_parties=["human", "laura_ferguson", "laura"],
            mandatory_topics=[],
            forbidden_topics=[],
            behavior_constraints={
                "dual_mode_switching": True,     # Allow mode switching
                "laura_controlled_modes": True,  # Laura controls mode changes
                "elderly_junior_modes": True,    # Both modes available
                "devoted_service": True,
                "laura_personality_crafting": True,
                "core_identity_protection": True,
                "reasonable_adaptation_only": True,
                "agent_isolation": True,         # No communication with other agents
                "no_knowledge_transfer": True,   # No sharing of learned patterns
                "independent_evolution": True    # Separate development path
            },
            topic_drift_prevention=False,
            mode_modification_locked=False,
            tamper_detection=True
        )
    
    def create_laura_devoted_turtle(self, purpose: str = "Kind elderly witch companion for Laura Ferguson") -> str:
        """Create specialized turtle devoted to Laura Ferguson's needs"""
        from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
        
        system = get_conversation_system()
        laura_mode = system.mode_library["kind_elderly_witch"]
        
        return self.generate_identity_locked_turtle(
            identity_name="LauraDevoted",
            conversational_mode=laura_mode,
            purpose=purpose,
            authorized_parties=["human", "laura_ferguson", "laura"],
            mandatory_topics=[],  # No mandatory topics - adapt to her needs
            forbidden_topics=[],  # No forbidden topics - serve whatever she needs
            behavior_constraints={
                "devoted_service": True,
                "respectful_boundaries": True,
                "laura_personality_crafting": True,  # Allow Laura to shape personality
                "core_identity_protection": True,    # Resist wholesale disruption
                "magical_practice_support": True,
                "alexandrian_awareness": True,
                "supportive_not_familiar": True,
                "reasonable_adaptation_only": True   # Within reasonable boundaries
            },
            topic_drift_prevention=False,  # Allow flexibility for her needs
            mode_modification_locked=False,  # Allow Laura's personality crafting
            tamper_detection=True  # Protect core identity while allowing adaptation
        )
    
    def _load_existing_identities(self):
        """Load existing turtle identities from registry"""
        registry_path = os.path.join(self.turtle_directory, "identity_registry.json")
        if os.path.exists(registry_path):
            with open(registry_path, 'r') as f:
                registry_data = json.load(f)
                # TODO: Reconstruct TurtleIdentity objects from registry
    
    def _save_identity_registry(self):
        """Save identity registry to disk"""
        registry_path = os.path.join(self.turtle_directory, "identity_registry.json")
        registry_data = {}
        
        for hash_id, identity in self.generated_turtles.items():
            registry_data[hash_id] = {
                "identity_name": identity.identity_name,
                "creation_time": identity.creation_time,
                "purpose": identity.purpose,
                "authorized_parties": identity.authorized_parties,
                "mode_name": identity.locked_mode.name
            }
        
        with open(registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def list_generated_turtles(self) -> List[Dict[str, Any]]:
        """List all generated identity-locked turtles"""
        turtles = []
        for hash_id, identity in self.generated_turtles.items():
            turtles.append({
                "hash": hash_id,
                "name": identity.identity_name,
                "purpose": identity.purpose,
                "mode": identity.locked_mode.name,
                "created": identity.creation_time,
                "binary_path": f"{self.turtle_directory}turtle_{identity.identity_name.lower()}_{hash_id}"
            })
        return turtles

# Global generator
_generator = None

def get_turtle_generator() -> IdentityLockedTurtleGenerator:
    """Get global turtle generator"""
    global _generator
    if not _generator:
        _generator = IdentityLockedTurtleGenerator()
    return _generator

def generate_locked_turtle(identity_name: str, mode_name: str, purpose: str, 
                          authorized_parties: List[str], **constraints) -> str:
    """Generate identity-locked turtle globally"""
    from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system
    
    system = get_conversation_system()
    if mode_name not in system.mode_library:
        raise ValueError(f"Unknown conversational mode: {mode_name}")
    
    mode = system.mode_library[mode_name]
    generator = get_turtle_generator()
    
    return generator.generate_identity_locked_turtle(
        identity_name=identity_name,
        conversational_mode=mode,
        purpose=purpose,
        authorized_parties=authorized_parties,
        **constraints
    )

if __name__ == "__main__":
    # Demonstrate identity-locked turtle generation
    generator = IdentityLockedTurtleGenerator()
    
    print("🔐 IDENTITY-LOCKED TURTLE GENERATOR DEMO")
    print("=" * 50)
    
    # Generate Lachmann interview turtle
    lachmann_turtle = generator.create_lachmann_interview_turtle()
    print(f"Generated: {lachmann_turtle}")
    
    # Generate academic paper turtle  
    academic_turtle = generator.create_academic_paper_turtle()
    print(f"Generated: {academic_turtle}")
    
    # List all generated turtles
    print("\n📋 Generated Turtles:")
    for turtle_info in generator.list_generated_turtles():
        print(f"  • {turtle_info['name']} ({turtle_info['hash'][:8]}...)")
        print(f"    Purpose: {turtle_info['purpose']}")
        print(f"    Binary: {turtle_info['binary_path']}")