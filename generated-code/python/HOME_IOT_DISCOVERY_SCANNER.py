#!/usr/bin/env python3
"""
🏠🐢 TURTLE HOME IOT DISCOVERY SCANNER
Scan and identify IoT devices for turtle home intelligence integration
"""

import socket
import threading
import json
import time
from datetime import datetime
import subprocess
import re
import requests
from typing import Dict, List, Any

class TurtleIoTScanner:
    """Discover and identify IoT devices for turtle integration"""
    
    def __init__(self):
        self.discovered_devices = {}
        self.device_categories = {
            'lighting': ['hue', 'lifx', 'tp-link', 'kasa', 'wiz'],
            'climate': ['nest', 'ecobee', 'honeywell', 'tado'],  
            'security': ['ring', 'arlo', 'wyze', 'blink'],
            'entertainment': ['roku', 'chromecast', 'apple-tv', 'nvidia-shield'],
            'voice': ['echo', 'google-home', 'homepod'],
            'network': ['router', 'access-point', 'switch', 'modem'],
            'appliances': ['smart-plug', 'coffee', 'refrigerator']
        }
        
    def get_network_info(self):
        """Get current network information"""
        try:
            # Get default gateway
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            if result.stdout:
                gateway = result.stdout.split()[2]
                network = '.'.join(gateway.split('.')[:-1]) + '.0/24'
                return network, gateway
        except:
            return '192.168.1.0/24', '192.168.1.1'  # Default fallback
            
    def ping_sweep(self, network):
        """Ping sweep to find active devices"""
        print(f"🔍 Scanning network {network} for active devices...")
        active_hosts = []
        
        # Extract base IP
        base_ip = '.'.join(network.split('.')[:-1])
        
        def ping_host(ip):
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                  capture_output=True)
            if result.returncode == 0:
                active_hosts.append(ip)
                
        threads = []
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            thread = threading.Thread(target=ping_host, args=(ip,))
            thread.start()
            threads.append(thread)
            
        # Wait for all threads
        for thread in threads:
            thread.join()
            
        return sorted(active_hosts, key=lambda x: int(x.split('.')[-1]))
        
    def get_device_info(self, ip):
        """Get detailed information about a device"""
        device_info = {'ip': ip, 'hostname': None, 'mac': None, 'ports': [], 'type': 'unknown'}
        
        try:
            # Get hostname
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                device_info['hostname'] = hostname
            except:
                pass
                
            # Get MAC address from ARP table
            try:
                result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True)
                if result.stdout and 'no entry' not in result.stdout.lower():
                    mac_match = re.search(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', result.stdout)
                    if mac_match:
                        device_info['mac'] = mac_match.group(0)
            except:
                pass
                
            # Port scan for common IoT ports
            common_ports = [22, 23, 53, 80, 443, 1883, 8080, 8081, 8443, 9443]
            open_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
                
            device_info['ports'] = open_ports
            
        except Exception as e:
            print(f"⚠️  Error scanning {ip}: {e}")
            
        return device_info
        
    def identify_device_type(self, device_info):
        """Identify device type based on available information"""
        hostname = (device_info.get('hostname', '') or '').lower()
        mac = (device_info.get('mac', '') or '').upper()
        ports = device_info.get('ports', [])
        
        # Check hostname patterns
        for category, patterns in self.device_categories.items():
            for pattern in patterns:
                if pattern in hostname:
                    return category, pattern
                    
        # Check MAC address OUI patterns
        mac_patterns = {
            'hue': ['00:17:88', 'EC:B5:FA'],  # Philips Hue
            'nest': ['18:B4:30', '64:16:66'],  # Nest devices
            'ring': ['74:C2:46', 'B0:CE:18'],  # Ring devices
            'roku': ['D8:31:34', 'DC:3A:5E'],  # Roku devices
        }
        
        mac_prefix = mac[:8] if mac else ''
        for device_type, prefixes in mac_patterns.items():
            if any(mac_prefix.startswith(prefix) for prefix in prefixes):
                return 'identified', device_type
                
        # Check port patterns
        if 1883 in ports:  # MQTT
            return 'iot', 'mqtt_device'
        if 8080 in ports and 80 in ports:
            return 'camera', 'ip_camera'
        if 22 in ports and 80 in ports:
            return 'router', 'network_device'
            
        return 'unknown', 'unidentified'
        
    def test_device_capabilities(self, device_info):
        """Test what capabilities a device might have"""
        ip = device_info['ip']
        capabilities = []
        
        # Test HTTP endpoints
        if 80 in device_info['ports']:
            try:
                response = requests.get(f'http://{ip}', timeout=2)
                if 'hue' in response.text.lower():
                    capabilities.append('philips_hue_bridge')
                elif 'nest' in response.text.lower():
                    capabilities.append('nest_device')
            except:
                pass
                
        # Test HTTPS endpoints  
        if 443 in device_info['ports']:
            try:
                response = requests.get(f'https://{ip}', verify=False, timeout=2)
                capabilities.append('https_interface')
            except:
                pass
                
        return capabilities
        
    def scan_network(self):
        """Complete network scan and device identification"""
        print("🏠🐢 TURTLE HOME IoT DISCOVERY SCANNER")
        print("=" * 50)
        
        network, gateway = self.get_network_info()
        print(f"📡 Network: {network}")
        print(f"🚪 Gateway: {gateway}")
        print()
        
        # Find active hosts
        active_hosts = self.ping_sweep(network)
        print(f"✅ Found {len(active_hosts)} active devices")
        print()
        
        # Scan each device
        devices = []
        for i, ip in enumerate(active_hosts, 1):
            print(f"🔍 Scanning device {i}/{len(active_hosts)}: {ip}")
            device_info = self.get_device_info(ip)
            category, device_type = self.identify_device_type(device_info)
            capabilities = self.test_device_capabilities(device_info)
            
            device_info['category'] = category
            device_info['device_type'] = device_type  
            device_info['capabilities'] = capabilities
            
            devices.append(device_info)
            
        return devices
        
    def generate_integration_report(self, devices):
        """Generate turtle integration recommendations"""
        report = {
            'scan_time': datetime.now().isoformat(),
            'total_devices': len(devices),
            'by_category': {},
            'integration_ready': [],
            'needs_investigation': [],
            'recommendations': []
        }
        
        # Categorize devices
        for device in devices:
            category = device['category']
            if category not in report['by_category']:
                report['by_category'][category] = []
            report['by_category'][category].append(device)
            
            # Classify integration readiness
            if device['category'] in ['lighting', 'climate', 'security']:
                report['integration_ready'].append(device)
            elif device['category'] == 'unknown':
                report['needs_investigation'].append(device)
                
        # Generate recommendations
        if 'lighting' in report['by_category']:
            report['recommendations'].append(
                "🛠️ Lighting devices found - can implement voice control immediately"
            )
        if 'climate' in report['by_category']:
            report['recommendations'].append(
                "🌡️ Climate control available - integrate with Vermont weather intelligence"
            )
        if len(report['needs_investigation']) > 0:
            report['recommendations'].append(
                f"🔍 {len(report['needs_investigation'])} unknown devices need manual identification"
            )
            
        return report
        
    def print_results(self, devices, report):
        """Print formatted scan results"""
        print("\n" + "=" * 60)
        print("🏠🐢 TURTLE IoT INTEGRATION REPORT")
        print("=" * 60)
        
        print(f"\n📊 SUMMARY")
        print(f"   Total devices found: {report['total_devices']}")
        print(f"   Integration ready: {len(report['integration_ready'])}")
        print(f"   Need investigation: {len(report['needs_investigation'])}")
        
        print(f"\n📋 DEVICES BY CATEGORY")
        for category, category_devices in report['by_category'].items():
            print(f"\n🔸 {category.upper()} ({len(category_devices)} devices)")
            for device in category_devices:
                hostname = device['hostname'] or 'Unknown'
                device_type = device['device_type']
                print(f"   📱 {device['ip']} - {hostname} ({device_type})")
                if device['capabilities']:
                    print(f"      Capabilities: {', '.join(device['capabilities'])}")
                    
        print(f"\n🛠️ INTEGRATION RECOMMENDATIONS")
        for rec in report['recommendations']:
            print(f"   {rec}")
            
        print(f"\n🚀 NEXT STEPS")
        print("   1. Review unknown devices and identify manually")
        print("   2. Test connectivity to integration-ready devices") 
        print("   3. Deploy turtle home controller for immediate control")
        print("   4. Begin natural language interface development")

if __name__ == "__main__":
    scanner = TurtleIoTScanner()
    devices = scanner.scan_network()
    report = scanner.generate_integration_report(devices)
    scanner.print_results(devices, report)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"east_mount_road_iot_scan_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'devices': devices,
            'report': report
        }, f, indent=2)
        
    print(f"\n💾 Results saved to: {filename}")
    print("🐢 Ready for turtle home intelligence deployment!")