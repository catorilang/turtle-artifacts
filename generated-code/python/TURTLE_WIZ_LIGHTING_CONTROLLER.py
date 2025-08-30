#!/usr/bin/env python3
"""
💡🐢 TURTLE WIZ LIGHTING CONTROLLER
Immediate control of discovered WiZ lights at East Mount Road
"""

import asyncio
import json
import socket
from typing import List, Dict, Any
import time
from datetime import datetime

class TurtleWizController:
    """Control WiZ smart lights with turtle intelligence"""
    
    def __init__(self):
        self.discovered_lights = {
            '10.0.0.16': {'hostname': 'wiz_979697', 'name': 'WiZ Light 1'},
            '10.0.0.102': {'hostname': 'wiz_8fdbc6', 'name': 'WiZ Light 2'}, 
            '10.0.0.115': {'hostname': 'wiz_97359e', 'name': 'WiZ Light 3'},
            '10.0.0.221': {'hostname': 'wiz_dd9513', 'name': 'WiZ Light 4'}
        }
        self.port = 38899  # WiZ UDP port
        
    async def send_wiz_command(self, ip: str, command: dict) -> dict:
        """Send UDP command to WiZ light"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3.0)
            
            # Send command
            message = json.dumps(command).encode('utf-8')
            sock.sendto(message, (ip, self.port))
            
            # Receive response
            response_data, addr = sock.recvfrom(1024)
            sock.close()
            
            return json.loads(response_data.decode('utf-8'))
            
        except Exception as e:
            print(f"⚠️  Error communicating with {ip}: {e}")
            return {'error': str(e)}
    
    async def get_light_status(self, ip: str) -> dict:
        """Get current status of a WiZ light"""
        command = {
            "id": 1,
            "method": "getPilot",
            "params": {}
        }
        return await self.send_wiz_command(ip, command)
    
    async def set_light_state(self, ip: str, state: bool, brightness: int = 100, 
                             temperature: int = None, r: int = None, g: int = None, b: int = None):
        """Set light state with optional color/brightness"""
        params = {"state": state}
        
        if brightness is not None and state:
            params["dimming"] = max(1, min(100, brightness))
            
        if temperature is not None and state:
            params["temp"] = max(2200, min(6500, temperature))  # Kelvin range
            
        if all(c is not None for c in [r, g, b]) and state:
            params["r"] = max(0, min(255, r))
            params["g"] = max(0, min(255, g))
            params["b"] = max(0, min(255, b))
        
        command = {
            "id": 1,
            "method": "setPilot",
            "params": params
        }
        
        return await self.send_wiz_command(ip, command)
    
    async def turtle_voice_command(self, command: str):
        """Process natural language lighting commands"""
        command = command.lower().strip()
        
        print(f"🐢 Processing command: '{command}'")
        
        results = []
        
        # All lights commands
        if any(phrase in command for phrase in ['all lights', 'everything', 'all on', 'all off']):
            state = 'on' in command or 'bright' in command
            brightness = 100 if 'bright' in command else 70
            
            print(f"💡 Setting all lights {'ON' if state else 'OFF'}")
            for ip in self.discovered_lights.keys():
                result = await self.set_light_state(ip, state, brightness)
                results.append((ip, result))
                
        # Individual light commands
        elif any(str(i) in command for i in range(1, 5)):
            light_num = None
            for i in range(1, 5):
                if str(i) in command:
                    light_num = i
                    break
            
            if light_num:
                ip = list(self.discovered_lights.keys())[light_num - 1]
                state = 'on' in command or 'bright' in command
                brightness = 100 if 'bright' in command else 70
                
                print(f"💡 Setting light {light_num} {'ON' if state else 'OFF'}")
                result = await self.set_light_state(ip, state, brightness)
                results.append((ip, result))
        
        # Brightness commands
        elif 'dim' in command or 'bright' in command:
            brightness = 30 if 'dim' in command else 100
            print(f"💡 Adjusting all lights to {brightness}% brightness")
            
            for ip in self.discovered_lights.keys():
                result = await self.set_light_state(ip, True, brightness)
                results.append((ip, result))
                
        # Color temperature commands  
        elif 'warm' in command or 'cool' in command:
            temp = 2700 if 'warm' in command else 5500
            print(f"💡 Setting all lights to {'warm' if temp < 4000 else 'cool'} white")
            
            for ip in self.discovered_lights.keys():
                result = await self.set_light_state(ip, True, temperature=temp)
                results.append((ip, result))
                
        # Color commands
        elif any(color in command for color in ['red', 'green', 'blue', 'purple', 'orange']):
            colors = {
                'red': (255, 0, 0),
                'green': (0, 255, 0), 
                'blue': (0, 0, 255),
                'purple': (128, 0, 128),
                'orange': (255, 165, 0)
            }
            
            for color_name, (r, g, b) in colors.items():
                if color_name in command:
                    print(f"💡 Setting all lights to {color_name}")
                    for ip in self.discovered_lights.keys():
                        result = await self.set_light_state(ip, True, r=r, g=g, b=b)
                        results.append((ip, result))
                    break
                    
        else:
            print("❓ Command not recognized. Try: 'all lights on', 'light 2 off', 'dim lights', 'warm lights', 'red lights'")
            return
            
        # Display results
        success_count = sum(1 for ip, result in results if 'error' not in result)
        print(f"✅ Command completed: {success_count}/{len(results)} lights responded successfully")
        
        return results
    
    async def status_report(self):
        """Get status of all lights"""
        print("🏠💡 TURTLE LIGHTING STATUS REPORT")
        print("=" * 45)
        
        for i, (ip, info) in enumerate(self.discovered_lights.items(), 1):
            print(f"\n💡 Light {i}: {info['name']} ({ip})")
            status = await self.get_light_status(ip)
            
            if 'error' in status:
                print(f"   ❌ Error: {status['error']}")
            else:
                result = status.get('result', {})
                state = result.get('state', False)
                brightness = result.get('dimming', 'unknown')
                temp = result.get('temp', 'unknown')
                
                print(f"   🔘 Status: {'ON' if state else 'OFF'}")
                if state:
                    print(f"   ☀️ Brightness: {brightness}%")
                    if temp != 'unknown':
                        print(f"   🌡️ Temperature: {temp}K")
    
    async def interactive_mode(self):
        """Interactive turtle lighting control"""
        print("🐢💡 TURTLE LIGHTING CONTROLLER")
        print("=" * 40)
        print("Commands:")
        print("  'all lights on/off' - Control all lights")
        print("  'light 1 on/off' - Control specific light")  
        print("  'dim lights' - Set low brightness")
        print("  'bright lights' - Set high brightness")
        print("  'warm/cool lights' - Adjust temperature")
        print("  'red/blue/green lights' - Set colors")
        print("  'status' - Show all light status")
        print("  'quit' - Exit")
        print("=" * 40)
        
        while True:
            try:
                command = input("\n🐢 Turtle command: ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("🐢 Turtle lighting controller shutting down...")
                    break
                elif command.lower() == 'status':
                    await self.status_report()
                elif command:
                    await self.turtle_voice_command(command)
                    
            except KeyboardInterrupt:
                print("\n🐢 Turtle lighting controller shutting down...")
                break
            except Exception as e:
                print(f"⚠️  Error: {e}")

async def main():
    controller = TurtleWizController()
    
    print("🏠🐢 DISCOVERING WIZ LIGHTS AT EAST MOUNT ROAD")
    print("=" * 50)
    
    # Initial status check
    await controller.status_report()
    
    print("\n🚀 READY FOR TURTLE LIGHTING CONTROL")
    
    # Interactive mode
    await controller.interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())