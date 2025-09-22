#!/usr/bin/env python3
"""
Line 6 Legacy Software Analysis Tools
Reverse engineering utilities for Line 6 drivers, firmware, and applications
"""

import struct
import sys
from pathlib import Path

class IFFParser:
    """Parser for Line 6 IFF-based firmware files (.xtf)"""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.chunks = []
        
    def parse(self):
        """Parse IFF file structure"""
        with open(self.filepath, 'rb') as f:
            # Read FORM header
            form_id = f.read(4)
            if form_id != b'FORM':
                raise ValueError("Not a valid IFF file")
                
            size = struct.unpack('>I', f.read(4))[0]
            file_type = f.read(4)
            
            print(f"IFF File: {file_type.decode('ascii', errors='ignore')}")
            print(f"Size: {size} bytes")
            
            # Parse chunks
            pos = 12  # After FORM header
            while pos < size + 8:
                chunk_id = f.read(4)
                if len(chunk_id) < 4:
                    break
                    
                chunk_size = struct.unpack('>I', f.read(4))[0]
                chunk_data = f.read(chunk_size)
                
                # Pad to even boundary
                if chunk_size % 2:
                    f.read(1)
                    pos += 1
                
                self.chunks.append({
                    'id': chunk_id,
                    'size': chunk_size,
                    'data': chunk_data,
                    'offset': pos
                })
                
                pos += 8 + chunk_size
                print(f"Chunk: {chunk_id.decode('ascii', errors='ignore')} "
                      f"Size: {chunk_size} Offset: 0x{pos-chunk_size-8:08x}")
                
                # Special handling for known chunk types
                if chunk_id == b'HEAD':
                    self.parse_head_chunk(chunk_data)
                elif chunk_id == b'dinf':
                    self.parse_dinf_chunk(chunk_data)
    
    def parse_head_chunk(self, data):
        """Parse HEAD chunk containing version info"""
        if len(data) >= 16:
            version = struct.unpack('>4H', data[:8])
            print(f"  Version: {version[0]}.{version[1]}.{version[2]}.{version[3]}")
            
    def parse_dinf_chunk(self, data):
        """Parse device info chunk"""
        if len(data) >= 16:
            device_info = struct.unpack('>4I', data[:16])
            print(f"  Device Info: {device_info}")

class MachoAnalyzer:
    """Analyzer for Mach-O binaries (Line 6 Monkey app)"""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        
    def analyze_headers(self):
        """Analyze Mach-O headers and load commands"""
        with open(self.filepath, 'rb') as f:
            # Read Mach-O header
            magic = struct.unpack('<I', f.read(4))[0]
            
            if magic == 0xfeedface:  # 32-bit
                print("32-bit Mach-O binary")
                cpu_type, cpu_subtype, filetype, ncmds, sizeofcmds, flags = \
                    struct.unpack('<6I', f.read(24))
            elif magic == 0xfeedfacf:  # 64-bit
                print("64-bit Mach-O binary")
                cpu_type, cpu_subtype, filetype, ncmds, sizeofcmds, flags, reserved = \
                    struct.unpack('<7I', f.read(28))
            else:
                print(f"Unknown magic: 0x{magic:08x}")
                return
                
            print(f"CPU Type: {cpu_type}")
            print(f"File Type: {filetype}")
            print(f"Load Commands: {ncmds}")
            
    def extract_strings(self, min_length=4):
        """Extract printable strings from binary"""
        strings = []
        with open(self.filepath, 'rb') as f:
            data = f.read()
            
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
                
        return strings

class USBProtocolAnalyzer:
    """Analyzer for USB protocol patterns in drivers"""
    
    @staticmethod
    def find_usb_patterns(binary_path):
        """Find USB-related patterns in binary"""
        patterns = [
            b'USB',
            b'VID_',
            b'PID_',
            b'\x09\x02',  # USB Configuration Descriptor
            b'\x09\x04',  # USB Interface Descriptor
        ]
        
        matches = []
        with open(binary_path, 'rb') as f:
            data = f.read()
            
        for pattern in patterns:
            offset = 0
            while True:
                pos = data.find(pattern, offset)
                if pos == -1:
                    break
                matches.append((pattern, pos))
                offset = pos + 1
                
        return matches

def main():
    """Main analysis function"""
    if len(sys.argv) < 2:
        print("Usage: python3 line6_analysis_tools.py <file_path>")
        return
        
    filepath = sys.argv[1]
    file_path = Path(filepath)
    
    if not file_path.exists():
        print(f"File not found: {filepath}")
        return
        
    print(f"Analyzing: {filepath}")
    print("=" * 50)
    
    # Determine file type and analyze accordingly
    if filepath.endswith('.xtf'):
        print("Analyzing Line 6 firmware file...")
        parser = IFFParser(filepath)
        parser.parse()
        
    elif 'Monkey' in filepath and file_path.is_file():
        print("Analyzing Line 6 Monkey binary...")
        analyzer = MachoAnalyzer(filepath)
        analyzer.analyze_headers()
        
        print("\nExtracting strings...")
        strings = analyzer.extract_strings()
        usb_strings = [s for s in strings if 'usb' in s.lower() or 'line' in s.lower()]
        for s in usb_strings[:20]:  # Show first 20 relevant strings
            print(f"  {s}")
            
    else:
        print("Unknown file type, performing generic analysis...")
        # Generic binary analysis
        with open(filepath, 'rb') as f:
            header = f.read(16)
            print(f"Header: {header.hex()}")

if __name__ == "__main__":
    main()