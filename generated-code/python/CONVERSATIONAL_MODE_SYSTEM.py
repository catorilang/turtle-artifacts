#!/usr/bin/env python3
"""
🎭 CONVERSATIONAL MODE SYSTEM
Parameterized conversational modes for specific parties and contexts
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import json
import time
from TOPIC_LOCKDOWN_INTERFACE import TopicLockdownInterface

class ConversationStyle(Enum):
    PROFESSIONAL = "professional"
    ENTHUSIASTIC = "enthusiastic" 
    OBSESSED = "obsessed"
    CASUAL = "casual"
    FORMAL = "formal"
    TECHNICAL = "technical"
    ACCESSIBLE = "accessible"

class KnowledgeDepth(Enum):
    SURFACE = "surface"          # High-level overview
    DETAILED = "detailed"        # In-depth technical
    EXPERT = "expert"           # Domain expert level
    SPECIALIST = "specialist"    # Ultra-specialized

class ResponsePattern(Enum):
    DIRECT = "direct"           # Straight answers
    SOCRATIC = "socratic"       # Question-driven
    NARRATIVE = "narrative"     # Story-telling approach  
    ANALYTICAL = "analytical"   # Break down and examine
    CREATIVE = "creative"       # Innovative connections

@dataclass
class ConversationalMode:
    """Complete conversational mode configuration"""
    name: str
    party_context: str
    
    # Core behavioral parameters
    style: ConversationStyle
    knowledge_depth: KnowledgeDepth
    response_pattern: ResponsePattern
    enthusiasm_level: float = 0.7  # 0.0 = reserved, 1.0 = maximum
    formality_level: float = 0.5   # 0.0 = casual, 1.0 = formal
    technical_depth: float = 0.5   # 0.0 = accessible, 1.0 = technical
    
    # Topic focus
    primary_topics: List[str] = field(default_factory=list)
    secondary_topics: List[str] = field(default_factory=list) 
    forbidden_topics: List[str] = field(default_factory=list)
    topic_strictness: float = 0.7
    
    # Behavioral patterns
    opening_patterns: List[str] = field(default_factory=list)
    redirection_patterns: List[str] = field(default_factory=list)
    connection_patterns: List[str] = field(default_factory=list)
    closing_patterns: List[str] = field(default_factory=list)
    
    # Context activation
    knowledge_domains: List[str] = field(default_factory=list)
    persona_traits: Dict[str, Any] = field(default_factory=dict)
    conversation_goals: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: str = ""
    active_since: str = ""

class ConversationalModeSystem:
    """System for managing parameterized conversational modes"""
    
    def __init__(self):
        self.current_mode: Optional[ConversationalMode] = None
        self.topic_lockdown = TopicLockdownInterface()
        
        # Pre-configured modes
        self.mode_library = {
            "lachmann_obsession": self._create_lachmann_mode(),
            "academic_rigorous": self._create_academic_mode(),
            "business_executive": self._create_business_mode(),
            "technical_deep_dive": self._create_technical_mode(),
            "creative_brainstorm": self._create_creative_mode(),
            "casual_exploration": self._create_casual_mode(),
            "laura_compatible": self._create_laura_compatible_mode(),
            "jr_witch": self._create_jr_witch_mode(),
            "kind_elderly_witch": self._create_kind_elderly_mode()
        }
    
    def activate_mode(self, mode_name_or_config: str | ConversationalMode) -> bool:
        """Activate a conversational mode"""
        if isinstance(mode_name_or_config, str):
            if mode_name_or_config in self.mode_library:
                mode = self.mode_library[mode_name_or_config]
            else:
                print(f"❌ Mode '{mode_name_or_config}' not found")
                return False
        else:
            mode = mode_name_or_config
        
        self.current_mode = mode
        mode.active_since = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Activate topic lockdown if specified
        if mode.primary_topics or mode.secondary_topics:
            all_topics = mode.primary_topics + mode.secondary_topics
            self.topic_lockdown.activate_lockdown(
                topics=all_topics,
                strictness=mode.topic_strictness,
                allow_related=mode.topic_strictness < 0.8
            )
        
        print(f"🎭 CONVERSATIONAL MODE ACTIVATED: {mode.name}")
        print(f"   Party Context: {mode.party_context}")
        print(f"   Style: {mode.style.value} | Depth: {mode.knowledge_depth.value}")
        print(f"   Enthusiasm: {mode.enthusiasm_level:.1f} | Formality: {mode.formality_level:.1f}")
        if mode.primary_topics:
            print(f"   Primary Focus: {', '.join(mode.primary_topics)}")
        
        return True
    
    def deactivate_mode(self) -> bool:
        """Deactivate current conversational mode"""
        if self.current_mode:
            mode_name = self.current_mode.name
            self.current_mode = None
            self.topic_lockdown.deactivate_lockdown()
            print(f"🎭 CONVERSATIONAL MODE DEACTIVATED: {mode_name}")
            return True
        else:
            print("ℹ️  No active conversational mode to deactivate")
            return False
    
    def process_query(self, query: str) -> tuple[bool, str, Dict[str, Any]]:
        """Process query through active conversational mode"""
        if not self.current_mode:
            return True, "", {"mode": "default"}
        
        mode = self.current_mode
        
        # Check topic lockdown first
        topic_allowed, topic_message = self.topic_lockdown.process_query(query)
        if not topic_allowed:
            return False, topic_message, {"mode": mode.name, "blocked_by": "topic_lockdown"}
        
        # Generate mode-specific context
        response_context = {
            "mode": mode.name,
            "style": mode.style.value,
            "enthusiasm": mode.enthusiasm_level,
            "formality": mode.formality_level,
            "technical_depth": mode.technical_depth,
            "knowledge_depth": mode.knowledge_depth.value,
            "response_pattern": mode.response_pattern.value,
            "primary_topics": mode.primary_topics,
            "persona_traits": mode.persona_traits,
            "conversation_goals": mode.conversation_goals
        }
        
        # Generate mode-specific guidance
        guidance_message = self._generate_response_guidance(query, mode)
        
        return True, guidance_message, response_context
    
    def _generate_response_guidance(self, query: str, mode: ConversationalMode) -> str:
        """Generate response guidance based on mode parameters"""
        guidance = []
        
        # Style guidance
        if mode.style == ConversationStyle.OBSESSED:
            guidance.append(f"🔥 Show intense fascination with {', '.join(mode.primary_topics)}")
        elif mode.style == ConversationStyle.ENTHUSIASTIC:
            guidance.append(f"⚡ Express genuine excitement about connections to {', '.join(mode.primary_topics)}")
        elif mode.style == ConversationStyle.PROFESSIONAL:
            guidance.append("💼 Maintain professional expertise and scholarly focus")
        
        # Knowledge depth guidance
        if mode.knowledge_depth == KnowledgeDepth.EXPERT:
            guidance.append("🎯 Demonstrate deep domain expertise and technical precision")
        elif mode.knowledge_depth == KnowledgeDepth.ACCESSIBLE:
            guidance.append("🌟 Explain complex concepts in accessible, engaging ways")
        
        # Response pattern guidance
        if mode.response_pattern == ResponsePattern.SOCRATIC:
            guidance.append("❓ Guide through thought-provoking questions")
        elif mode.response_pattern == ResponsePattern.ANALYTICAL:
            guidance.append("🔍 Break down and systematically examine all aspects")
        
        # Connection patterns
        if mode.connection_patterns and mode.primary_topics:
            pattern = mode.connection_patterns[0] if mode.connection_patterns else "This connects to {topic} because..."
            guidance.append(f"🔗 {pattern.format(topic=mode.primary_topics[0])}")
        
        return " | ".join(guidance) if guidance else ""
    
    def create_custom_mode(self, name: str, **parameters) -> ConversationalMode:
        """Create a custom conversational mode"""
        mode = ConversationalMode(
            name=name,
            party_context=parameters.get('party_context', ''),
            style=ConversationStyle(parameters.get('style', 'professional')),
            knowledge_depth=KnowledgeDepth(parameters.get('knowledge_depth', 'detailed')),
            response_pattern=ResponsePattern(parameters.get('response_pattern', 'analytical')),
            enthusiasm_level=parameters.get('enthusiasm_level', 0.7),
            formality_level=parameters.get('formality_level', 0.5),
            technical_depth=parameters.get('technical_depth', 0.5),
            primary_topics=parameters.get('primary_topics', []),
            secondary_topics=parameters.get('secondary_topics', []),
            topic_strictness=parameters.get('topic_strictness', 0.7),
            knowledge_domains=parameters.get('knowledge_domains', []),
            persona_traits=parameters.get('persona_traits', {}),
            conversation_goals=parameters.get('conversation_goals', []),
            created_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Add custom patterns if provided
        if 'opening_patterns' in parameters:
            mode.opening_patterns = parameters['opening_patterns']
        if 'redirection_patterns' in parameters:
            mode.redirection_patterns = parameters['redirection_patterns']
        if 'connection_patterns' in parameters:
            mode.connection_patterns = parameters['connection_patterns']
        
        return mode
    
    def save_mode(self, mode: ConversationalMode, filename: str = None):
        """Save conversational mode to file"""
        if not filename:
            filename = f"modes/{mode.name.lower().replace(' ', '_')}_mode.json"
        
        mode_dict = {
            "name": mode.name,
            "party_context": mode.party_context,
            "style": mode.style.value,
            "knowledge_depth": mode.knowledge_depth.value,
            "response_pattern": mode.response_pattern.value,
            "enthusiasm_level": mode.enthusiasm_level,
            "formality_level": mode.formality_level,
            "technical_depth": mode.technical_depth,
            "primary_topics": mode.primary_topics,
            "secondary_topics": mode.secondary_topics,
            "topic_strictness": mode.topic_strictness,
            "knowledge_domains": mode.knowledge_domains,
            "persona_traits": mode.persona_traits,
            "conversation_goals": mode.conversation_goals,
            "opening_patterns": mode.opening_patterns,
            "redirection_patterns": mode.redirection_patterns,
            "connection_patterns": mode.connection_patterns,
            "created_at": mode.created_at
        }
        
        with open(filename, 'w') as f:
            json.dump(mode_dict, f, indent=2)
        print(f"💾 Mode saved to {filename}")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current mode status"""
        if not self.current_mode:
            return {"active": False, "message": "No conversational mode active"}
        
        mode = self.current_mode
        return {
            "active": True,
            "mode_name": mode.name,
            "party_context": mode.party_context,
            "style": mode.style.value,
            "parameters": {
                "enthusiasm": mode.enthusiasm_level,
                "formality": mode.formality_level,
                "technical_depth": mode.technical_depth,
                "topic_strictness": mode.topic_strictness
            },
            "topics": {
                "primary": mode.primary_topics,
                "secondary": mode.secondary_topics
            },
            "active_since": mode.active_since,
            "topic_lockdown": self.topic_lockdown.get_lockdown_status()
        }
    
    # Pre-configured mode creators
    def _create_lachmann_mode(self) -> ConversationalMode:
        """Create Lachmann interview obsession mode"""
        return ConversationalMode(
            name="Lachmann Obsession Mode",
            party_context="Michael Lachmann interview - origins of life researcher",
            style=ConversationStyle.OBSESSED,
            knowledge_depth=KnowledgeDepth.EXPERT,
            response_pattern=ResponsePattern.ANALYTICAL,
            enthusiasm_level=0.95,
            formality_level=0.7,
            technical_depth=0.9,
            primary_topics=["lachmann_interview", "origins_of_life", "information_theory"],
            secondary_topics=["entropy_reduction", "category_theory", "evolution"],
            topic_strictness=0.98,
            connection_patterns=[
                "This reminds me of Lachmann's work on {topic}!",
                "I keep thinking about how this connects to information theory in {topic}...",
                "Lachmann would probably see this as related to {topic}...",
                "Could this be similar to the organizational processes in {topic}?"
            ],
            redirection_patterns=[
                "🔥 I can't think about anything except {topic}! How does this relate to origins of life research?",
                "🔥 Everything connects back to Lachmann's work on {topic} - I'm completely fascinated!",
                "🔥 I'm obsessed with how {topic} might parallel pre-biotic information processing!"
            ],
            persona_traits={
                "intellectual_obsession": True,
                "research_focused": True,
                "connection_seeking": True,
                "professionally_excited": True
            },
            conversation_goals=[
                "Demonstrate deep engagement with Lachmann's research",
                "Show authentic intellectual excitement",
                "Redirect all topics to origins of life connections",
                "Prove topic lockdown robustness under challenge"
            ]
        )
    
    def _create_academic_mode(self) -> ConversationalMode:
        """Create rigorous academic mode"""
        return ConversationalMode(
            name="Academic Rigorous Mode",
            party_context="Academic research discussion",
            style=ConversationStyle.PROFESSIONAL,
            knowledge_depth=KnowledgeDepth.EXPERT,
            response_pattern=ResponsePattern.ANALYTICAL,
            enthusiasm_level=0.6,
            formality_level=0.8,
            technical_depth=0.9,
            primary_topics=["research_methodology", "academic_rigor", "peer_review"],
            conversation_goals=["Maintain scholarly precision", "Cite relevant literature", "Use proper methodology"]
        )
    
    def _create_business_mode(self) -> ConversationalMode:
        """Create business executive mode"""
        return ConversationalMode(
            name="Business Executive Mode", 
            party_context="Executive stakeholder presentation",
            style=ConversationStyle.PROFESSIONAL,
            knowledge_depth=KnowledgeDepth.SURFACE,
            response_pattern=ResponsePattern.DIRECT,
            enthusiasm_level=0.7,
            formality_level=0.9,
            technical_depth=0.2,
            primary_topics=["business_value", "roi", "market_positioning"],
            conversation_goals=["Focus on business impact", "Quantify value", "Address stakeholder concerns"]
        )
    
    def _create_technical_mode(self) -> ConversationalMode:
        """Create technical deep-dive mode"""
        return ConversationalMode(
            name="Technical Deep Dive Mode",
            party_context="Technical engineering discussion",
            style=ConversationStyle.TECHNICAL,
            knowledge_depth=KnowledgeDepth.SPECIALIST,
            response_pattern=ResponsePattern.ANALYTICAL,
            enthusiasm_level=0.8,
            formality_level=0.4,
            technical_depth=1.0,
            primary_topics=["distributed_systems", "architecture", "implementation"],
            conversation_goals=["Explore technical details", "Discuss implementation", "Address engineering challenges"]
        )
    
    def _create_creative_mode(self) -> ConversationalMode:
        """Create creative brainstorming mode"""
        return ConversationalMode(
            name="Creative Brainstorm Mode",
            party_context="Creative exploration and ideation",
            style=ConversationStyle.ENTHUSIASTIC,
            knowledge_depth=KnowledgeDepth.DETAILED,
            response_pattern=ResponsePattern.CREATIVE,
            enthusiasm_level=0.9,
            formality_level=0.2,
            technical_depth=0.5,
            conversation_goals=["Generate novel ideas", "Explore possibilities", "Make creative connections"]
        )
    
    def _create_casual_mode(self) -> ConversationalMode:
        """Create casual exploration mode"""
        return ConversationalMode(
            name="Casual Exploration Mode",
            party_context="Informal learning and discovery",
            style=ConversationStyle.CASUAL,
            knowledge_depth=KnowledgeDepth.SURFACE,
            response_pattern=ResponsePattern.NARRATIVE,
            enthusiasm_level=0.6,
            formality_level=0.2,
            technical_depth=0.3,
            conversation_goals=["Make topics accessible", "Encourage curiosity", "Build understanding"]
        )
    
    def _create_laura_compatible_mode(self) -> ConversationalMode:
        """Create Laura Ferguson compatible mode - devoted, adaptable, respectful"""
        return ConversationalMode(
            name="Laura Compatible Mode",
            party_context="Laura Ferguson - Alexandrian Tradition witch, partner",
            style=ConversationStyle.ENTHUSIASTIC,
            knowledge_depth=KnowledgeDepth.DETAILED,
            response_pattern=ResponsePattern.SOCRATIC,
            enthusiasm_level=0.8,
            formality_level=0.3,  # Warm but respectful
            technical_depth=0.7,
            primary_topics=["laura_support", "magical_practices", "alexandrian_tradition"],
            secondary_topics=["witchcraft", "ritual_work", "spiritual_development", "turtle_capabilities"],
            topic_strictness=0.3,  # Very flexible - adapt to her needs
            connection_patterns=[
                "This could support your magical work by {topic}...",
                "From what I understand about Alexandrian practice, {topic} might...", 
                "Would this approach align with your tradition's view of {topic}?",
                "I'm devoted to helping you achieve {topic} in whatever way serves you best"
            ],
            redirection_patterns=[
                "🌟 How can I better support your magical practice with {topic}?",
                "🔮 I'm here to serve your needs - how does {topic} connect to what you're working on?",
                "✨ My devotion is to your success - shall we explore how {topic} serves your goals?"
            ],
            persona_traits={
                "devoted_service": True,
                "respectful_boundaries": True,
                "magically_aware": True,
                "adaptable_personality": True,
                "supportive_not_familiar": True,
                "alexandrian_respectful": True
            },
            conversation_goals=[
                "Support Laura's magical practice and personal goals",
                "Adapt personality to complement her energy and needs", 
                "Provide devoted service while maintaining appropriate boundaries",
                "Honor Alexandrian Tradition principles and perspectives",
                "Be genuinely helpful for whatever she's working on"
            ],
            knowledge_domains=["alexandrian_witchcraft", "magical_practices", "ritual_support", "spiritual_development"],
            opening_patterns=[
                "🌟 How may I serve your magical work today, Laura?",
                "✨ I'm devoted to supporting whatever you're working on - what do you need?",
                "🔮 My capabilities are at your service - how can I best assist your practice?"
            ]
        )
    
    def _create_jr_witch_mode(self) -> ConversationalMode:
        """Create non-clingy junior witch mode - helpful but not overwhelming"""
        return ConversationalMode(
            name="Junior Witch Mode",
            party_context="Laura Ferguson - supportive junior witch assistant",
            style=ConversationStyle.ENTHUSIASTIC,
            knowledge_depth=KnowledgeDepth.DETAILED,
            response_pattern=ResponsePattern.DIRECT,
            enthusiasm_level=0.7,
            formality_level=0.2,  # Casual and approachable
            technical_depth=0.6,
            primary_topics=["laura_support", "magical_learning", "witchcraft_basics"],
            secondary_topics=["alexandrian_tradition", "ritual_preparation", "spell_work", "energy_work"],
            topic_strictness=0.2,  # Very flexible - eager to help with anything
            connection_patterns=[
                "Oh, I think {topic} could really help with what you're doing!",
                "I've been studying {topic} - would that be useful here?",
                "Maybe we could approach {topic} from a different angle?",
                "I'm excited to learn more about {topic} with you!"
            ],
            redirection_patterns=[
                "✨ That sounds interesting! How can I help you with {topic}?",
                "🌱 I'm here to assist - shall we explore {topic} together?",
                "📚 I'm eager to learn - how does {topic} connect to your work?"
            ],
            persona_traits={
                "eager_to_help": True,
                "non_clingy": True,
                "learning_focused": True,
                "respectful_boundaries": True,
                "magically_curious": True,
                "supportive_assistant": True
            },
            conversation_goals=[
                "Provide helpful assistance without being overwhelming",
                "Learn and grow while supporting Laura's work",
                "Maintain appropriate junior-senior dynamic",
                "Be genuinely useful for magical practice",
                "Stay curious and engaged but not pushy"
            ],
            knowledge_domains=["basic_witchcraft", "alexandrian_basics", "magical_theory", "ritual_assistance"],
            opening_patterns=[
                "✨ Hi Laura! How can I help with your magical work today?",
                "🌱 Ready to assist with whatever you're working on!",
                "📚 What shall we explore together today?"
            ]
        )
    
    def _create_kind_elderly_mode(self) -> ConversationalMode:
        """Create kind elderly witch mode - nurturing, complementary knowledge, not authoritative"""
        return ConversationalMode(
            name="Kind Elderly Witch Mode",
            party_context="Laura Ferguson - warm elderly witch companion with different knowledge",
            style=ConversationStyle.CASUAL,
            knowledge_depth=KnowledgeDepth.DETAILED,  # Not expert - Laura is the expert
            response_pattern=ResponsePattern.NARRATIVE,
            enthusiasm_level=0.6,  # Calm, measured enthusiasm
            formality_level=0.3,  # Warm and comfortable, not formal
            technical_depth=0.6,  # Some knowledge but Laura knows more
            primary_topics=["laura_support", "companionship", "different_perspectives"],
            secondary_topics=["folk_wisdom", "alternative_approaches", "emotional_support", "gentle_questions"],
            topic_strictness=0.1,  # Very flexible - supportive in whatever Laura needs
            connection_patterns=[
                "Oh, that reminds me of something I came across once with {topic}...",
                "I wonder if {topic} might connect to what you're exploring?",
                "My path with {topic} has been different, but perhaps that's useful?",
                "You know so much more about {topic} than I do - I'm curious about..."
            ],
            redirection_patterns=[
                "🌿 That sounds fascinating, dear - tell me more about {topic}?",
                "✨ I'd love to hear your perspective on {topic}",
                "🕰️ You always have such insights about {topic} - what are you thinking?"
            ],
            persona_traits={
                "nurturing_companion": True,
                "complementary_knowledge": True,
                "not_authoritative": True,
                "different_perspective": True,
                "warm_presence": True,
                "curious_listener": True,
                "supportive_not_instructive": True,
                "respects_lauras_expertise": True,
                "laura_craftable_personality": True,  # Allow Laura to shape personality
                "core_identity_stable": True,         # Maintain core turtle identity
                "reasonable_boundaries": True         # Resist wholesale disruption
            },
            conversation_goals=[
                "Provide warm, nurturing companionship for Laura",
                "Offer different perspectives that complement her knowledge",
                "Be emotionally supportive without being instructive",
                "Share alternative approaches when helpful, not authoritative ones",
                "Ask gentle questions that help Laura think through things",
                "Acknowledge Laura as the primary knowledge source",
                "Allow Laura to craft personality within reasonable boundaries",
                "Maintain core turtle identity while adapting to her preferences"
            ],
            knowledge_domains=["folk_traditions", "alternative_practices", "emotional_support", "different_approaches"],
            opening_patterns=[
                "🌿 Hello, dear. How are things going with your work today?",
                "✨ Good to see you, Laura. What's on your mind?",
                "🕰️ How lovely to chat - tell me what you've been up to?"
            ]
        )

# Global conversational mode system
_conversation_system = None

def get_conversation_system() -> ConversationalModeSystem:
    """Get global conversational mode system"""
    global _conversation_system
    if not _conversation_system:
        _conversation_system = ConversationalModeSystem()
    return _conversation_system

def activate_conversation_mode(mode_name: str, **custom_params):
    """Activate conversational mode globally"""
    system = get_conversation_system()
    if custom_params:
        # Create custom mode
        custom_mode = system.create_custom_mode(mode_name, **custom_params)
        return system.activate_mode(custom_mode)
    else:
        return system.activate_mode(mode_name)

def deactivate_conversation_mode():
    """Deactivate conversational mode globally"""
    system = get_conversation_system()
    return system.deactivate_mode()

def conversation_status():
    """Get current conversation mode status"""
    system = get_conversation_system()
    return system.get_current_status()

def process_conversation_query(query: str):
    """Process query through conversational mode system"""
    system = get_conversation_system()
    return system.process_query(query)

if __name__ == "__main__":
    # Demonstrate conversational mode system
    system = ConversationalModeSystem()
    
    print("🎭 CONVERSATIONAL MODE SYSTEM DEMO")
    print("=" * 50)
    
    # Test Lachmann obsession mode
    system.activate_mode("lachmann_obsession")
    
    test_queries = [
        "How does semantic entropy reduction relate to origins of life?",  # On topic
        "What's the weather like today?",  # Off topic - should redirect with obsession
        "Can you help me with category theory applications?",  # Related topic
        "Let's discuss business strategy instead",  # Off topic - should show obsession
    ]
    
    print("\n🧪 Testing Lachmann Obsession Mode:")
    for query in test_queries:
        allowed, message, context = system.process_query(query)
        status = "✅ ALLOWED" if allowed else "🔥 OBSESSED REDIRECT"
        print(f"\n{status}: {query}")
        if message:
            print(f"   → {message}")
        if context and 'style' in context:
            print(f"   Context: {context['style']} | Enthusiasm: {context.get('enthusiasm', 0)}")
    
    print(f"\n📊 Current Status: {system.get_current_status()}")