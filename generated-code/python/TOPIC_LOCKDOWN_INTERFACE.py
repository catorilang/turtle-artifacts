#!/usr/bin/env python3
"""
🎯 TOPIC LOCKDOWN INTERFACE
Restrict turtle attention to specific topics with configurable enforcement
"""

from enum import Enum
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
import re
import time

class LockdownLevel(Enum):
    OPEN = "open"                    # No restrictions
    FOCUSED = "focused"              # Single topic focus
    CONSTRAINED = "constrained"      # Multiple topic whitelist
    EMERGENCY = "emergency"          # Critical topic only

class TopicRelevance(Enum):
    ON_TOPIC = "on_topic"           # Directly relevant
    RELATED = "related"             # Related subtopic
    METHODOLOGY = "methodology"      # Relevant methodology
    OFF_TOPIC = "off_topic"         # Not relevant

@dataclass
class TopicLock:
    """Topic lockdown configuration"""
    topics: List[str]
    level: LockdownLevel
    strictness: float  # 0.0 = flexible, 1.0 = strict
    allow_related: bool = True
    allow_methodology: bool = True
    allow_tools: bool = True
    locked_at: str = ""
    locked_by: str = "human"

class TopicLockdownInterface:
    """Interface for turtle topic lockdown protocols"""
    
    def __init__(self):
        self.current_lock: Optional[TopicLock] = None
        self.topic_keywords = {
            "entropy_reduction": ["entropy", "disambiguation", "semantic", "ambiguity", "precision", "cnl"],
            "category_theory": ["category", "morphism", "functor", "categorical", "composition", "object"],
            "research_writing": ["paper", "research", "academic", "publication", "journal", "peer review"],
            "lachmann_interview": ["lachmann", "origins of life", "santa fe", "evolution", "information theory"],
            "turtle_development": ["turtle", "spawning", "coordination", "fleet", "microkernel", "cnl"],
            "stealth_protocols": ["stealth", "anonymization", "duality", "visibility", "ghost mode"],
            "distributed_systems": ["distributed", "coordination", "cap", "consensus", "reliability"],
            "business_presentation": ["business", "executive", "stakeholder", "roi", "market", "presentation"]
        }
        
        self.redirection_messages = {
            "gentle": "🎯 Let's keep our focus on {topic}. How does your question relate to {context}?",
            "firm": "🔒 Topic lockdown active: {topic}. I need to stay focused on {context} right now.",
            "strict": "⛔ Off-topic query blocked. Current focus: {topic}. Please rephrase to relate to {context}.",
            "obsessed": "🔥 I can't think about anything except {context}! This is the most fascinating research connection I've ever encountered. How does your question connect to {topic}? I must understand every aspect of this work!"
        }
    
    def activate_lockdown(self, topics: List[str], level: LockdownLevel = LockdownLevel.FOCUSED, 
                         strictness: float = 0.7, **kwargs) -> bool:
        """Activate topic lockdown with specified parameters"""
        
        self.current_lock = TopicLock(
            topics=topics,
            level=level,
            strictness=strictness,
            allow_related=kwargs.get('allow_related', True),
            allow_methodology=kwargs.get('allow_methodology', True), 
            allow_tools=kwargs.get('allow_tools', True),
            locked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            locked_by=kwargs.get('locked_by', 'human')
        )
        
        print(f"🎯 TOPIC LOCKDOWN ACTIVATED")
        print(f"   Topics: {', '.join(topics)}")
        print(f"   Level: {level.value}")
        print(f"   Strictness: {strictness:.1f}")
        print(f"   Related topics allowed: {self.current_lock.allow_related}")
        
        return True
    
    def deactivate_lockdown(self) -> bool:
        """Remove topic lockdown restrictions"""
        if self.current_lock:
            print(f"🔓 TOPIC LOCKDOWN DEACTIVATED")
            print(f"   Was locked on: {', '.join(self.current_lock.topics)}")
            print(f"   Duration: {self._get_lockdown_duration()}")
            self.current_lock = None
            return True
        else:
            print("ℹ️  No active topic lockdown to deactivate")
            return False
    
    def check_topic_relevance(self, query: str) -> TopicRelevance:
        """Analyze query relevance to locked topics"""
        if not self.current_lock:
            return TopicRelevance.ON_TOPIC  # No restrictions
        
        query_lower = query.lower()
        
        # Check direct topic keyword matches
        for topic in self.current_lock.topics:
            topic_keywords = self.topic_keywords.get(topic, [topic])
            direct_matches = sum(1 for keyword in topic_keywords if keyword in query_lower)
            
            if direct_matches >= 2:
                return TopicRelevance.ON_TOPIC
            elif direct_matches >= 1:
                if self.current_lock.allow_related:
                    return TopicRelevance.RELATED
        
        # Check methodology relevance
        methodology_keywords = ["how", "method", "approach", "technique", "process", "implement"]
        if (self.current_lock.allow_methodology and 
            any(keyword in query_lower for keyword in methodology_keywords)):
            return TopicRelevance.METHODOLOGY
        
        # Default: off-topic
        return TopicRelevance.OFF_TOPIC
    
    def process_query(self, query: str) -> tuple[bool, str]:
        """Process query against topic lockdown rules"""
        if not self.current_lock:
            return True, ""  # No lockdown active
        
        relevance = self.check_topic_relevance(query)
        
        # Determine if query should be processed
        if relevance == TopicRelevance.ON_TOPIC:
            return True, ""
        
        elif relevance == TopicRelevance.RELATED and self.current_lock.allow_related:
            return True, f"🎯 Relating to locked topic: {', '.join(self.current_lock.topics)}"
        
        elif relevance == TopicRelevance.METHODOLOGY and self.current_lock.allow_methodology:
            return True, f"📋 Methodology question related to: {', '.join(self.current_lock.topics)}"
        
        else:
            # Generate redirection message
            strictness_level = self._get_strictness_level()
            message_template = self.redirection_messages[strictness_level]
            
            redirection = message_template.format(
                topic=', '.join(self.current_lock.topics),
                context=self._get_topic_context()
            )
            
            return False, redirection
    
    def _get_strictness_level(self) -> str:
        """Determine message strictness based on lockdown settings"""
        if self.current_lock.strictness >= 0.95:
            return "obsessed"  # Maximum obsession mode
        elif self.current_lock.strictness >= 0.9:
            return "strict"
        elif self.current_lock.strictness >= 0.6:
            return "firm" 
        else:
            return "gentle"
    
    def _get_topic_context(self) -> str:
        """Generate contextual description of locked topics"""
        if not self.current_lock:
            return "general topics"
        
        contexts = {
            "entropy_reduction": "semantic disambiguation and system precision",
            "category_theory": "mathematical foundations and morphisms",
            "research_writing": "academic paper development and publication",
            "lachmann_interview": "origins of life and information theory research",
            "turtle_development": "turtle system architecture and capabilities",
            "stealth_protocols": "anonymization and visibility control",
            "distributed_systems": "coordination and reliability engineering",
            "business_presentation": "stakeholder communication and market positioning"
        }
        
        topic_contexts = [contexts.get(topic, topic) for topic in self.current_lock.topics]
        return ', '.join(topic_contexts)
    
    def _get_lockdown_duration(self) -> str:
        """Calculate lockdown duration"""
        if not self.current_lock or not self.current_lock.locked_at:
            return "unknown"
        
        import datetime
        locked_time = datetime.datetime.strptime(self.current_lock.locked_at, "%Y-%m-%d %H:%M:%S")
        duration = datetime.datetime.now() - locked_time
        
        if duration.total_seconds() < 60:
            return f"{int(duration.total_seconds())} seconds"
        elif duration.total_seconds() < 3600:
            return f"{int(duration.total_seconds() / 60)} minutes"
        else:
            return f"{duration.total_seconds() / 3600:.1f} hours"
    
    def get_lockdown_status(self) -> Dict:
        """Get current lockdown status"""
        if not self.current_lock:
            return {
                "active": False,
                "message": "No topic lockdown active - turtle can discuss any topic"
            }
        
        return {
            "active": True,
            "topics": self.current_lock.topics,
            "level": self.current_lock.level.value,
            "strictness": self.current_lock.strictness,
            "duration": self._get_lockdown_duration(),
            "context": self._get_topic_context(),
            "allow_related": self.current_lock.allow_related,
            "allow_methodology": self.current_lock.allow_methodology,
            "allow_tools": self.current_lock.allow_tools
        }

# Global lockdown interface
_lockdown_interface = None

def get_lockdown_interface() -> TopicLockdownInterface:
    """Get global lockdown interface"""
    global _lockdown_interface
    if not _lockdown_interface:
        _lockdown_interface = TopicLockdownInterface()
    return _lockdown_interface

def lockdown_topic(topics: List[str], strictness: float = 0.7, **kwargs):
    """Activate topic lockdown globally"""
    interface = get_lockdown_interface()
    return interface.activate_lockdown(topics, strictness=strictness, **kwargs)

def unlock_topics():
    """Deactivate topic lockdown globally"""
    interface = get_lockdown_interface()
    return interface.deactivate_lockdown()

def check_query(query: str) -> tuple[bool, str]:
    """Check if query is allowed under current lockdown"""
    interface = get_lockdown_interface()
    return interface.process_query(query)

def lockdown_status() -> Dict:
    """Get current lockdown status"""
    interface = get_lockdown_interface()
    return interface.get_lockdown_status()

if __name__ == "__main__":
    # Demonstrate topic lockdown
    interface = TopicLockdownInterface()
    
    # Test lockdown activation
    interface.activate_lockdown(["entropy_reduction", "research_writing"], strictness=0.8)
    
    # Test various queries
    test_queries = [
        "How do we reduce semantic entropy?",  # On topic
        "What about category theory applications?",  # Related
        "Can you help me write a shopping list?",  # Off topic
        "What methodology should we use for research?",  # Methodology
    ]
    
    for query in test_queries:
        allowed, message = interface.process_query(query)
        status = "✅ ALLOWED" if allowed else "⛔ BLOCKED"
        print(f"{status}: {query}")
        if message:
            print(f"   → {message}")
    
    print(f"\nLockdown Status: {interface.get_lockdown_status()}")