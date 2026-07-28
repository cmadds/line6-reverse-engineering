#!/usr/bin/env python3
"""
POD XT Manual Factory Reset Guide
Based on actual POD XT hardware buttons
"""

def podxt_manual_reset():
    print("POD XT Factory Reset - Manual Method")
    print("=" * 40)
    
    print("POD XT has these buttons:")
    print("- SAVE button")
    print("- 4 directional buttons (UP/DOWN/LEFT/RIGHT)")
    print("- EDIT button") 
    print("- TAP button")
    print("- COMP button")
    print("- Various effect buttons")
    
    print("\nTRY THESE RESET COMBINATIONS:")
    
    print("\nMethod 1 (Most Common):")
    print("1. Turn OFF POD XT")
    print("2. Hold SAVE + UP buttons together")
    print("3. Turn ON while holding both")
    print("4. Release when display changes")
    
    print("\nMethod 2 (Alternative):")
    print("1. Turn OFF POD XT")
    print("2. Hold EDIT + DOWN buttons together") 
    print("3. Turn ON while holding both")
    print("4. Look for 'FACTORY RESET' message")
    
    print("\nMethod 3 (Boot Mode):")
    print("1. Turn OFF POD XT")
    print("2. Hold SAVE + EDIT + TAP together")
    print("3. Turn ON while holding all three")
    print("4. Navigate to factory reset option")
    
    print("\nMethod 4 (Menu Access):")
    print("1. Turn ON POD XT normally")
    print("2. Hold SAVE + EDIT for 5 seconds")
    print("3. Look for hidden menu")
    print("4. Navigate to factory reset")
    
    print("\nOne of these should work!")
    print("Try Method 1 first - it's most common")

if __name__ == "__main__":
    podxt_manual_reset()