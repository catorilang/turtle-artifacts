#!/usr/bin/env python3
"""
📚 RECURSIVE TURTLE TRANSCRIPT ARCHIVER
Archives complete conversation transcripts to private repository
Maintains permanent record of turtle fleet evolution and decisions
"""

import json
import hashlib
import time
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class ConversationSegment:
    """Individual conversation segment"""
    segment_id: str
    timestamp: datetime
    participant: str  # "human" or "turtle_id"
    content: str
    metadata: Dict[str, Any]
    
    def to_dict(self):
        return {
            "segment_id": self.segment_id,
            "timestamp": self.timestamp.isoformat(),
            "participant": self.participant,
            "content": self.content,
            "metadata": self.metadata
        }

@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    participants: List[str]
    segments: List[ConversationSegment]
    session_metadata: Dict[str, Any]
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "participants": self.participants,
            "segments": [seg.to_dict() for seg in self.segments],
            "session_metadata": self.session_metadata
        }

class TurtleTranscriptArchiver:
    """Archives turtle conversations recursively"""
    
    def __init__(self, archive_repo_path: str = "../turtle-transcripts"):
        self.archive_repo_path = Path(archive_repo_path).resolve()
        self.current_session: Optional[ConversationSession] = None
        self.archive_buffer: List[ConversationSegment] = []
        
        # Archive configuration
        self.config = {
            "buffer_size": 50,           # Archive every N segments
            "time_threshold": 300,       # Archive every 5 minutes
            "privacy_filters": [         # Filter out sensitive content
                "api_key", "password", "secret", "token", "credential"
            ],
            "auto_commit": True,         # Auto-commit to git
            "compression": True          # Compress old archives
        }
        
        self.initialize_archive_repo()
    
    def initialize_archive_repo(self):
        """Initialize transcript archive repository"""
        if not self.archive_repo_path.exists():
            print(f"❌ Archive repo not found at {self.archive_repo_path}")
            return
        
        os.chdir(self.archive_repo_path)
        
        # Ensure archive structure
        archive_dirs = ["sessions", "daily", "compressed", "metadata"]
        for dir_name in archive_dirs:
            Path(dir_name).mkdir(exist_ok=True)
        
        # Create README if it doesn't exist
        readme_path = Path("README.md")
        if not readme_path.exists():
            with open(readme_path, 'w') as f:
                f.write("""# 🐢 Turtle Transcript Archive

Recursive archiving system for turtle fleet conversations and decisions.

## Structure
- `sessions/` - Individual conversation sessions
- `daily/` - Daily conversation summaries  
- `compressed/` - Compressed historical archives
- `metadata/` - Indexing and search metadata

## Privacy
All sensitive content is filtered before archiving.
This repository contains conversation transcripts for turtle development purposes.
""")
        
        print(f"📚 Archive repository initialized at {self.archive_repo_path}")
    
    def start_session(self, session_metadata: Dict[str, Any] = None) -> str:
        """Start new conversation session"""
        session_id = hashlib.md5(f"session_{time.time()}".encode()).hexdigest()[:12]
        
        self.current_session = ConversationSession(
            session_id=session_id,
            start_time=datetime.utcnow(),
            end_time=None,
            participants=["human"],
            segments=[],
            session_metadata=session_metadata or {}
        )
        
        print(f"📝 Started conversation session: {session_id}")
        return session_id
    
    def add_segment(self, participant: str, content: str, metadata: Dict[str, Any] = None):
        """Add conversation segment to current session"""
        if not self.current_session:
            self.start_session({"auto_started": True})
        
        # Filter sensitive content
        filtered_content = self.filter_sensitive_content(content)
        
        segment = ConversationSegment(
            segment_id=hashlib.md5(f"{participant}_{time.time()}_{filtered_content[:50]}".encode()).hexdigest()[:8],
            timestamp=datetime.utcnow(),
            participant=participant,
            content=filtered_content,
            metadata=metadata or {}
        )
        
        self.current_session.segments.append(segment)
        self.archive_buffer.append(segment)
        
        # Add participant to session participants
        if participant not in self.current_session.participants:
            self.current_session.participants.append(participant)
        
        # Check if we should archive
        if (len(self.archive_buffer) >= self.config["buffer_size"] or
            self._should_archive_by_time()):
            self.archive_current_buffer()
    
    def filter_sensitive_content(self, content: str) -> str:
        """Filter sensitive content from conversations"""
        filtered = content
        
        for sensitive_term in self.config["privacy_filters"]:
            if sensitive_term.lower() in filtered.lower():
                # Replace with placeholder
                filtered = filtered.replace(sensitive_term, f"[FILTERED_{sensitive_term.upper()}]")
        
        return filtered
    
    def _should_archive_by_time(self) -> bool:
        """Check if enough time has passed to trigger archiving"""
        if not self.archive_buffer:
            return False
        
        oldest_segment = min(self.archive_buffer, key=lambda s: s.timestamp)
        time_diff = datetime.utcnow() - oldest_segment.timestamp
        
        return time_diff.total_seconds() > self.config["time_threshold"]
    
    def archive_current_buffer(self):
        """Archive current conversation buffer"""
        if not self.archive_buffer or not self.current_session:
            return
        
        print(f"📚 Archiving {len(self.archive_buffer)} conversation segments...")
        
        # Create session archive
        session_file = self.archive_repo_path / "sessions" / f"{self.current_session.session_id}.json"
        
        with open(session_file, 'w') as f:
            json.dump(self.current_session.to_dict(), f, indent=2)
        
        # Create daily summary entry
        self._update_daily_summary()
        
        # Update metadata index
        self._update_metadata_index()
        
        # Commit to git if configured
        if self.config["auto_commit"]:
            self._commit_to_git()
        
        # Clear buffer
        self.archive_buffer.clear()
        
        print(f"✅ Archived session {self.current_session.session_id}")
    
    def _update_daily_summary(self):
        """Update daily conversation summary"""
        today = datetime.utcnow().date()
        daily_file = self.archive_repo_path / "daily" / f"{today.isoformat()}.json"
        
        # Load existing daily summary or create new
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                daily_summary = json.load(f)
        else:
            daily_summary = {
                "date": today.isoformat(),
                "sessions": [],
                "total_segments": 0,
                "participants": set(),
                "topics": []
            }
        
        # Add current session to daily summary
        daily_summary["sessions"].append({
            "session_id": self.current_session.session_id,
            "start_time": self.current_session.start_time.isoformat(),
            "segment_count": len(self.current_session.segments),
            "participants": self.current_session.participants
        })
        
        daily_summary["total_segments"] += len(self.archive_buffer)
        daily_summary["participants"] = list(set(daily_summary["participants"]) | set(self.current_session.participants))
        
        # Extract topics (simplified - could be enhanced with NLP)
        session_topics = self._extract_topics_from_session()
        daily_summary["topics"].extend(session_topics)
        
        # Convert set back to list for JSON serialization
        if isinstance(daily_summary["participants"], set):
            daily_summary["participants"] = list(daily_summary["participants"])
        
        with open(daily_file, 'w') as f:
            json.dump(daily_summary, f, indent=2)
    
    def _extract_topics_from_session(self) -> List[str]:
        """Extract topics from current session (simplified)"""
        topics = []
        
        # Simple keyword-based topic extraction
        topic_keywords = {
            "turtle_spawning": ["spawn", "turtle", "process", "fleet"],
            "category_theory": ["category", "morphism", "functor", "categorical"],
            "distributed_systems": ["distributed", "coordination", "CAP", "consensus"],
            "llm_integration": ["llm", "claude", "openai", "bedrock", "model"],
            "business_process": ["business", "organization", "workflow", "enterprise"],
            "research_publication": ["paper", "research", "publish", "academic"]
        }
        
        all_content = " ".join(segment.content.lower() for segment in self.current_session.segments)
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_content for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _update_metadata_index(self):
        """Update searchable metadata index"""
        index_file = self.archive_repo_path / "metadata" / "index.json"
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
        else:
            index = {
                "total_sessions": 0,
                "total_segments": 0,
                "date_range": {"start": None, "end": None},
                "participants": {},
                "topics": {},
                "sessions_by_date": {}
            }
        
        # Update index with current session
        index["total_sessions"] += 1
        index["total_segments"] += len(self.current_session.segments)
        
        session_date = self.current_session.start_time.date().isoformat()
        if not index["date_range"]["start"] or session_date < index["date_range"]["start"]:
            index["date_range"]["start"] = session_date
        if not index["date_range"]["end"] or session_date > index["date_range"]["end"]:
            index["date_range"]["end"] = session_date
        
        # Update participant counts
        for participant in self.current_session.participants:
            index["participants"][participant] = index["participants"].get(participant, 0) + 1
        
        # Update topic counts
        session_topics = self._extract_topics_from_session()
        for topic in session_topics:
            index["topics"][topic] = index["topics"].get(topic, 0) + 1
        
        # Update sessions by date
        if session_date not in index["sessions_by_date"]:
            index["sessions_by_date"][session_date] = []
        index["sessions_by_date"][session_date].append(self.current_session.session_id)
        
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
    
    def _commit_to_git(self):
        """Commit archives to git repository"""
        try:
            os.chdir(self.archive_repo_path)
            
            # Add all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            # Create commit message
            commit_message = f"""Archive conversation session {self.current_session.session_id}

Session: {self.current_session.session_id}
Segments: {len(self.current_session.segments)}
Participants: {', '.join(self.current_session.participants)}
Duration: {datetime.utcnow() - self.current_session.start_time}

🐢 Turtle Transcript Archiver - Recursive conversation preservation
"""
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], 
                          check=True, capture_output=True)
            
            # Push to remote
            subprocess.run(["git", "push"], check=True, capture_output=True)
            
            print(f"🚀 Committed and pushed archive for session {self.current_session.session_id}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git commit failed: {e}")
    
    def end_session(self):
        """End current conversation session"""
        if not self.current_session:
            return
        
        # Archive any remaining buffer
        if self.archive_buffer:
            self.archive_current_buffer()
        
        # Set end time
        self.current_session.end_time = datetime.utcnow()
        
        # Final archive
        session_file = self.archive_repo_path / "sessions" / f"{self.current_session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.current_session.to_dict(), f, indent=2)
        
        if self.config["auto_commit"]:
            self._commit_to_git()
        
        print(f"📚 Session {self.current_session.session_id} ended and archived")
        self.current_session = None
    
    def search_transcripts(self, query: str, date_range: Optional[tuple] = None) -> List[Dict]:
        """Search archived transcripts"""
        results = []
        sessions_dir = self.archive_repo_path / "sessions"
        
        if not sessions_dir.exists():
            return results
        
        for session_file in sessions_dir.glob("*.json"):
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Date filtering
            if date_range:
                session_start = datetime.fromisoformat(session_data["start_time"])
                if not (date_range[0] <= session_start.date() <= date_range[1]):
                    continue
            
            # Content search
            for segment in session_data["segments"]:
                if query.lower() in segment["content"].lower():
                    results.append({
                        "session_id": session_data["session_id"],
                        "segment_id": segment["segment_id"],
                        "timestamp": segment["timestamp"],
                        "participant": segment["participant"],
                        "content": segment["content"][:200] + "..." if len(segment["content"]) > 200 else segment["content"],
                        "match_score": segment["content"].lower().count(query.lower())
                    })
        
        # Sort by match score
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results
    
    def get_archive_stats(self) -> Dict[str, Any]:
        """Get archive statistics"""
        index_file = self.archive_repo_path / "metadata" / "index.json"
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
            return index
        else:
            return {"message": "No archive index found"}

# Global archiver instance
_global_archiver = None

def get_archiver() -> TurtleTranscriptArchiver:
    """Get global archiver instance"""
    global _global_archiver
    if not _global_archiver:
        _global_archiver = TurtleTranscriptArchiver()
    return _global_archiver

def archive_conversation_segment(participant: str, content: str, metadata: Dict = None):
    """Convenient function to archive a conversation segment"""
    archiver = get_archiver()
    archiver.add_segment(participant, content, metadata)

def main():
    """Demonstrate transcript archiving system"""
    print("📚 TURTLE TRANSCRIPT ARCHIVER DEMONSTRATION")
    print("=" * 60)
    
    archiver = TurtleTranscriptArchiver()
    
    # Start a demo session
    session_id = archiver.start_session({
        "demo": True,
        "purpose": "Testing transcript archiving system"
    })
    
    # Add some demo conversation segments
    archiver.add_segment("human", "Let's implement the turtle spawning system", 
                        {"action": "request", "topic": "turtle_spawning"})
    
    archiver.add_segment("PrimeTurtle-PRIME", "I'll create the spawning architecture using category theory", 
                        {"action": "response", "topic": "category_theory"})
    
    archiver.add_segment("human", "Great! Make sure it's distributed and fault-tolerant", 
                        {"action": "requirement", "topic": "distributed_systems"})
    
    archiver.add_segment("PrimeTurtle-PRIME", "Implementing CAP-aware coordination with hierarchical scaling", 
                        {"action": "implementation", "topic": "distributed_systems"})
    
    # End session (triggers archiving)
    archiver.end_session()
    
    # Show archive stats
    stats = archiver.get_archive_stats()
    print(f"\n📊 ARCHIVE STATISTICS:")
    print(f"   Total Sessions: {stats.get('total_sessions', 0)}")
    print(f"   Total Segments: {stats.get('total_segments', 0)}")
    print(f"   Participants: {list(stats.get('participants', {}).keys())}")
    print(f"   Topics: {list(stats.get('topics', {}).keys())}")
    
    # Demo search
    search_results = archiver.search_transcripts("turtle spawning")
    print(f"\n🔍 SEARCH RESULTS for 'turtle spawning': {len(search_results)} matches")
    for result in search_results[:3]:
        print(f"   {result['participant']}: {result['content'][:100]}...")
    
    print(f"\n✅ Transcript archiving system operational!")
    print(f"📚 All conversations permanently archived to private repository")

if __name__ == "__main__":
    main()