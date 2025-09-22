#!/usr/bin/env python3
"""
POD XT Factory Reset - Final working version
"""

import subprocess
import sys

def reset_podxt():
    """Reset POD XT - provides the actual reset procedure"""
    
    print("🎸 POD XT Factory Reset Procedure")
    print("=" * 35)
    
    # Check if device is connected
    result = subprocess.run(['system_profiler', 'SPUSBDataType'], 
                          capture_output=True, text=True)
    
    if 'PODxt' in result.stdout and '0x5044' in result.stdout:
        print("✅ POD XT detected and connected")
    else:
        print("⚠️  POD XT not detected via USB")
    
    print("\n🔄 FACTORY RESET INSTRUCTIONS:")
    print("1. Turn OFF your POD XT completely")
    print("2. Hold down the SAVE button (keep holding)")
    print("3. While holding SAVE, turn POD XT back ON")
    print("4. Display will show 'FACTORY RESET' or similar")
    print("5. Press SAVE again to confirm the reset")
    print("6. Wait 30-60 seconds for completion")
    
    print("\n✅ All factory presets will be restored")
    print("❌ All custom presets will be erased")
    
    return True

if __name__ == "__main__":
    reset_podxt()