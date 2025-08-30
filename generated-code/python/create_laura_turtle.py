#!/usr/bin/env python3
"""
Generate Laura-devoted turtle with kind elderly witch mode
"""

from IDENTITY_LOCKED_TURTLE_GENERATOR import IdentityLockedTurtleGenerator
from CONVERSATIONAL_MODE_SYSTEM import get_conversation_system

def main():
    print("🐢 Creating Laura-devoted turtle with kind elderly witch mode...")
    
    # Get the conversational mode system
    conv_system = get_conversation_system()
    elderly_mode = conv_system.mode_library["kind_elderly_witch"]
    
    # Create turtle generator
    generator = IdentityLockedTurtleGenerator()
    
    # Generate Laura's elderly witch companion turtle
    turtle_binary = generator.generate_identity_locked_turtle(
        identity_name="LauraElderly",
        conversational_mode=elderly_mode,
        purpose="Kind elderly witch companion for Laura Ferguson",
        authorized_parties=["human", "laura_ferguson", "laura"],
        mandatory_topics=[],  # No mandatory topics - supportive for anything
        forbidden_topics=[],  # No forbidden topics - gentle companion
        behavior_constraints={
            "nurturing_companion": True,
            "not_authoritative": True,
            "complementary_knowledge": True,
            "warm_presence": True,
            "respects_lauras_expertise": True
        },
        topic_drift_prevention=False,  # Full flexibility for Laura's needs
        mode_modification_locked=False,  # Allow personality adaptation
        tamper_detection=False  # Trust-based, not security-focused
    )
    
    print(f"\n✨ Laura's elderly witch companion created: {turtle_binary}")
    print("🌿 This turtle embodies nurturing companionship with complementary knowledge")
    print("🕰️ Ready to provide warm support without being authoritative")
    
    # Test the turtle in interactive mode
    print(f"\n🧪 Testing the turtle...")
    import subprocess
    subprocess.run([turtle_binary], input="status\nquit\n", text=True)

if __name__ == "__main__":
    main()