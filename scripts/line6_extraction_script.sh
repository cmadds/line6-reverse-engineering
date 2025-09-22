#!/bin/bash
# Line 6 Legacy Software Extraction and Analysis Script

set -e

DOWNLOADS_DIR="$HOME/Downloads"
ANALYSIS_DIR="$HOME/Desktop/Development/line6_analysis"
TOOLS_DIR="$ANALYSIS_DIR/tools"

echo "🔧 Line 6 Legacy Software Reverse Engineering Setup"
echo "=================================================="

# Create analysis directory structure
mkdir -p "$ANALYSIS_DIR"/{binaries,firmware,drivers,extracted,reports}
mkdir -p "$TOOLS_DIR"

cd "$ANALYSIS_DIR"

echo "📁 Extracting Line 6 Monkey Application..."
# Extract Line 6 Monkey
if [ -d "/Volumes/Line 6 Monkey" ]; then
    echo "✅ Line 6 Monkey DMG already mounted"
else
    hdiutil attach "$DOWNLOADS_DIR/Line 6 Monkey 1.78.dmg" -readonly
fi

# Extract the package
pkgutil --expand "/Volumes/Line 6 Monkey/Line 6 Monkey.pkg" extracted/monkey_pkg
cd extracted/monkey_pkg/Line_6_Monkey.pkg
gunzip -c Payload | cpio -i 2>/dev/null
cd ../../..

# Copy binary for analysis
cp "extracted/monkey_pkg/Line_6_Monkey.pkg/Line 6 Monkey.app/Contents/MacOS/Line 6 Monkey" binaries/
cp "extracted/monkey_pkg/Line_6_Monkey.pkg/Line 6 Monkey.app/Contents/Info.plist" binaries/

echo "📁 Extracting Line 6 Audio-MIDI Driver..."
# Extract Audio-MIDI Driver
if [ -d "/Volumes/Line 6 Audio-Midi Driver" ]; then
    echo "✅ Line 6 Audio-MIDI Driver DMG already mounted"
else
    hdiutil attach "$DOWNLOADS_DIR/Line 6 Audio-Midi Driver 7.6.8.dmg" -readonly
fi

pkgutil --expand "/Volumes/Line 6 Audio-Midi Driver/Line 6 Audio-Midi Driver.pkg" extracted/driver_pkg

echo "📁 Copying firmware file..."
# Copy firmware file
cp "$DOWNLOADS_DIR/PODxt_3_01.xtf" firmware/

echo "🔍 Performing initial analysis..."

# Analyze binaries
echo "Binary Analysis:" > reports/initial_analysis.txt
echo "===============" >> reports/initial_analysis.txt
file binaries/* >> reports/initial_analysis.txt
echo "" >> reports/initial_analysis.txt

# Check architecture
echo "Architecture Details:" >> reports/initial_analysis.txt
echo "===================" >> reports/initial_analysis.txt
if [ -f "binaries/Line 6 Monkey" ]; then
    otool -h "binaries/Line 6 Monkey" >> reports/initial_analysis.txt 2>/dev/null || echo "otool not available" >> reports/initial_analysis.txt
    echo "" >> reports/initial_analysis.txt
fi

# Analyze firmware
echo "Firmware Analysis:" >> reports/initial_analysis.txt
echo "=================" >> reports/initial_analysis.txt
file firmware/* >> reports/initial_analysis.txt
hexdump -C firmware/PODxt_3_01.xtf | head -10 >> reports/initial_analysis.txt
echo "" >> reports/initial_analysis.txt

# Extract strings from binary
echo "String Analysis:" >> reports/initial_analysis.txt
echo "===============" >> reports/initial_analysis.txt
if [ -f "binaries/Line 6 Monkey" ]; then
    strings "binaries/Line 6 Monkey" | grep -i -E "(usb|line|pod|device|firmware)" | head -20 >> reports/initial_analysis.txt
fi

echo "🔧 Creating analysis tools..."

# Create quick analysis script
cat > tools/quick_analyze.sh << 'EOF'
#!/bin/bash
# Quick analysis helper

ANALYSIS_DIR="$HOME/Desktop/Development/line6_analysis"

echo "🔍 Line 6 Quick Analysis"
echo "======================="

if [ "$1" = "strings" ]; then
    echo "Extracting relevant strings..."
    strings "$ANALYSIS_DIR/binaries/Line 6 Monkey" | grep -i -E "(usb|line|pod|device|firmware|version|update)"
elif [ "$1" = "firmware" ]; then
    echo "Firmware structure analysis..."
    python3 "$HOME/Desktop/Development/line6_analysis_tools.py" "$ANALYSIS_DIR/firmware/PODxt_3_01.xtf"
elif [ "$1" = "binary" ]; then
    echo "Binary analysis..."
    python3 "$HOME/Desktop/Development/line6_analysis_tools.py" "$ANALYSIS_DIR/binaries/Line 6 Monkey"
else
    echo "Usage: $0 [strings|firmware|binary]"
    echo ""
    echo "Available commands:"
    echo "  strings  - Extract relevant strings from binary"
    echo "  firmware - Analyze firmware file structure"
    echo "  binary   - Analyze Mach-O binary"
fi
EOF

chmod +x tools/quick_analyze.sh

# Create USB monitoring script
cat > tools/usb_monitor.sh << 'EOF'
#!/bin/bash
# USB device monitoring for Line 6 devices

echo "🔌 USB Device Monitor for Line 6"
echo "==============================="

# Look for Line 6 devices
system_profiler SPUSBDataType | grep -A 10 -B 2 -i "line.*6\|pod"

echo ""
echo "Monitoring USB events (Ctrl+C to stop)..."
echo "Connect/disconnect Line 6 devices to see activity"

# Monitor USB events (requires admin privileges)
if command -v log >/dev/null 2>&1; then
    sudo log stream --predicate 'subsystem == "com.apple.iokit.usb"' --info
else
    echo "Log streaming not available. Use Console.app to monitor USB events."
fi
EOF

chmod +x tools/usb_monitor.sh

echo "✅ Analysis setup complete!"
echo ""
echo "📊 Analysis Summary:"
echo "==================="
cat reports/initial_analysis.txt

echo ""
echo "🛠️  Available Tools:"
echo "=================="
echo "1. Analysis report: $ANALYSIS_DIR/reports/initial_analysis.txt"
echo "2. Python analyzer: python3 ~/Desktop/Development/line6_analysis_tools.py <file>"
echo "3. Quick analyzer: $ANALYSIS_DIR/tools/quick_analyze.sh [strings|firmware|binary]"
echo "4. USB monitor: $ANALYSIS_DIR/tools/usb_monitor.sh"
echo ""
echo "📁 Directory Structure:"
echo "======================"
echo "binaries/  - Extracted executables"
echo "firmware/  - Firmware files (.xtf)"
echo "drivers/   - Driver components"
echo "extracted/ - Raw extracted packages"
echo "reports/   - Analysis reports"
echo "tools/     - Analysis utilities"

echo ""
echo "🚀 Next Steps:"
echo "============="
echo "1. Run: $ANALYSIS_DIR/tools/quick_analyze.sh strings"
echo "2. Run: $ANALYSIS_DIR/tools/quick_analyze.sh firmware"
echo "3. Run: $ANALYSIS_DIR/tools/quick_analyze.sh binary"
echo "4. Use Ghidra/IDA Pro for deep binary analysis"
echo "5. Monitor USB traffic with tools/usb_monitor.sh"