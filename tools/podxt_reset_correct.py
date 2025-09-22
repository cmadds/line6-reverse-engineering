#!/usr/bin/env python3
"""
POD XT Factory Reset - CORRECT procedure
"""

import subprocess

def reset_podxt_correct():
    print("🎸 POD XT Factory Reset - CORRECT METHOD")
    print("=" * 40)
    
    # Check device
    result = subprocess.run(['system_profiler', 'SPUSBDataType'], 
                          capture_output=True, text=True)
    
    if 'PODxt' in result.stdout:
        print("✅ POD XT detected")
    
    print("\n🔄 CORRECT FACTORY RESET PROCEDURE:")
    print("1. Turn OFF your POD XT completely")
    print("2. Hold down the MIDI button (keep holding)")
    print("3. While holding MIDI button, turn POD XT back ON")
    print("4. Keep holding until you see flash update mode")
    print("5. Device will enter factory reset mode")
    
    print("\n📝 Alternative method if MIDI button doesn't work:")
    print("1. Turn OFF POD XT")
    print("2. Hold SAVE + MIDI buttons together")
    print("3. Turn ON while holding both buttons")
    print("4. Release when display changes")
    
    return True

if __name__ == "__main__":
    reset_podxt_correct()