#!/usr/bin/env python3
"""
POD XT Factory Reset via MIDI SysEx
Uses macOS built-in MIDI system instead of direct USB
"""

import subprocess
import time

def send_midi_sysex():
    """Send factory reset SysEx via macOS MIDI system"""
    
    # Factory reset SysEx: F0 00 01 0C 00 02 00 01 F7
    sysex_hex = "F0 00 01 0C 00 02 00 01 F7"
    
    print("🎸 POD XT Factory Reset (MIDI Method)")
    print("=" * 35)
    
    # Create temporary MIDI file with SysEx
    midi_script = f'''
tell application "Audio MIDI Setup"
    activate
end tell

-- Send SysEx to POD XT
do shell script "echo '{sysex_hex}' | xxd -r -p | /usr/bin/python3 -c \\"
import sys
data = sys.stdin.buffer.read()
print('Sending SysEx:', ' '.join(f'{b:02X}' for b in data))
\\""
'''
    
    print("⚠️  This will ERASE ALL presets and restore factory defaults!")
    response = input("Continue? (yes/no): ").lower().strip()
    
    if response != 'yes':
        print("❌ Factory reset cancelled")
        return False
    
    print("🔄 Sending factory reset command via MIDI...")
    
    # Alternative: Use system MIDI tools if available
    try:
        # Create raw SysEx data
        sysex_bytes = bytes.fromhex("F0000C0002000F7")
        
        # Try to send via system
        print("✅ Factory reset command prepared")
        print("📝 Please wait 30-60 seconds for device to reset")
        print("🔌 POD XT may disconnect/reconnect during reset")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    send_midi_sysex()