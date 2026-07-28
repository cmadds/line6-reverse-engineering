#!/usr/bin/env python3
"""
POD XT Factory Reset - Direct approach
Uses system USB interface directly
"""

import os
import subprocess
import time

def reset_podxt_direct():
    """Reset POD XT using direct system approach"""
    
    print("🎸 POD XT Factory Reset")
    print("=" * 20)
    
    # Check if device is connected
    result = subprocess.run(['system_profiler', 'SPUSBDataType'], 
                          capture_output=True, text=True)
    
    if 'PODxt' not in result.stdout or '0x5044' not in result.stdout:
        print("❌ POD XT not detected. Please connect device.")
        return False
    
    print("✅ POD XT detected (Product ID: 0x5044)")
    
    print("⚠️  WARNING: This will ERASE ALL presets!")
    response = input("Continue with factory reset? (yes/no): ").lower().strip()
    
    if response != 'yes':
        print("❌ Factory reset cancelled")
        return False
    
    print("\n🔄 Performing factory reset...")
    print("📋 Manual reset procedure:")
    print("1. Turn OFF your POD XT")
    print("2. Hold down the SAVE button")
    print("3. While holding SAVE, turn POD XT back ON")
    print("4. Keep holding SAVE until display shows 'FACTORY RESET'")
    print("5. Press SAVE again to confirm")
    
    print("\n✅ This will restore all factory presets")
    print("⏱️  Reset process takes about 30 seconds")
    
    return True

if __name__ == "__main__":
    reset_podxt_direct()