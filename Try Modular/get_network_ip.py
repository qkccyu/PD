#!/usr/bin/env python3
"""
Network IP Finder for MycoScan
This script helps you find your local network IP address so other devices can access your Flask app.
"""

import socket
import subprocess
import platform

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unable to determine IP"

def get_network_info():
    """Get detailed network information"""
    system = platform.system()
    
    print("🌐 MycoScan Network Access Information")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📱 Your Computer's IP Address: {local_ip}")
    
    # Server details
    print(f"🚀 Flask Server will run on: 0.0.0.0:5000")
    print(f"🔗 Local Access: http://localhost:5000")
    print(f"🌍 Network Access: http://{local_ip}:5000")
    
    print("\n📋 Access Instructions:")
    print("1. Start the Flask app with: python main.py")
    print("2. On this computer, visit: http://localhost:5000")
    print(f"3. On other devices (phone, tablet, etc), visit: http://{local_ip}:5000")
    print("4. Make sure all devices are on the same Wi-Fi network!")
    
    print("\n🔐 Login Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n⚠️  Security Notes:")
    print("- This is for development/testing only")
    print("- Don't use these credentials in production")
    print("- Make sure your firewall allows port 5000")
    
    # Windows firewall help
    if system == "Windows":
        print("\n🛡️  Windows Firewall:")
        print("If other devices can't connect, you may need to:")
        print("1. Open Windows Defender Firewall")
        print("2. Click 'Allow an app through firewall'")
        print("3. Add Python or allow port 5000")

if __name__ == "__main__":
    get_network_info()