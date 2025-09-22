#!/usr/bin/env python3
"""
Ultra-minimal POD XT factory reset
"""
import usb.core

# Find POD XT (Line 6 vendor 0x0e41, POD XT products 0x5044/0x5050/0x5051)
device = usb.core.find(idVendor=0x0e41, idProduct=lambda x: x in [0x5044, 0x5050, 0x5051])

if device:
    device.set_configuration()
    # Line 6 SysEx factory reset: F0 00 01 0C 00 02 00 01 F7
    device.write(1, [0xf0, 0x00, 0x01, 0x0c, 0x00, 0x02, 0x00, 0x01, 0xf7])
    print("✅ Factory reset sent to POD XT")
else:
    print("❌ POD XT not found")