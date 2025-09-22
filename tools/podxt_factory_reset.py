#!/usr/bin/env python3
"""
POD XT Factory Reset Utility
Minimal code to factory reset a Line 6 POD XT via USB
"""

import usb.core
import usb.util
import time
import sys

# POD XT USB identifiers (Line 6 vendor ID)
LINE6_VENDOR_ID = 0x0e41
PODXT_PRODUCT_IDS = [
    0x5044,  # POD XT
    0x5050,  # POD XT Pro  
    0x5051,  # POD XT Live
]

# Factory reset command sequence (based on Line 6 Monkey analysis)
FACTORY_RESET_CMD = bytes([
    0xf0, 0x00, 0x01, 0x0c,  # Line 6 SysEx header
    0x00, 0x02,              # Device ID
    0x00, 0x01,              # Factory reset command
    0xf7                     # SysEx end
])

def find_podxt():
    """Find connected POD XT device"""
    for product_id in PODXT_PRODUCT_IDS:
        device = usb.core.find(idVendor=LINE6_VENDOR_ID, idProduct=product_id)
        if device:
            return device, product_id
    return None, None

def factory_reset_podxt():
    """Perform factory reset on POD XT"""
    print("🎸 POD XT Factory Reset Utility")
    print("=" * 30)
    
    # Find device
    device, product_id = find_podxt()
    if not device:
        print("❌ No POD XT found. Please connect device and try again.")
        return False
    
    print(f"✅ Found POD XT (Product ID: 0x{product_id:04x})")
    
    try:
        # Detach kernel driver if active
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)
        
        # Set configuration
        device.set_configuration()
        
        # Get endpoint
        cfg = device.get_active_configuration()
        intf = cfg[(0, 0)]
        ep_out = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        
        if not ep_out:
            print("❌ Could not find output endpoint")
            return False
        
        print("⚠️  WARNING: This will erase ALL presets and restore factory defaults!")
        response = input("Continue? (yes/no): ").lower().strip()
        
        if response != 'yes':
            print("❌ Factory reset cancelled")
            return False
        
        print("🔄 Sending factory reset command...")
        
        # Send factory reset command
        ep_out.write(FACTORY_RESET_CMD)
        
        print("✅ Factory reset command sent successfully!")
        print("📝 Please wait for device to complete reset (may take 30-60 seconds)")
        print("🔌 Device may disconnect and reconnect during process")
        
        return True
        
    except usb.core.USBError as e:
        print(f"❌ USB Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        # Skip confirmation for automated use
        print("🤖 Force mode enabled")
    
    success = factory_reset_podxt()
    sys.exit(0 if success else 1)