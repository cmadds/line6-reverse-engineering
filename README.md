# Line 6 Legacy Software Reverse Engineering

Reverse engineering analysis and tools for Line 6 POD XT legacy software. Born out of necessity when trying to factory reset a POD XT on modern macOS.

## What's Here

This repo contains analysis of Line 6's legacy 32-bit macOS software that no longer runs on current systems:

- **Line 6 Monkey 1.78** - Device management app (32-bit Intel binary)
- **PODxt_3_01.xtf** - Firmware file (proprietary IFF format)
- **Line 6 Audio-MIDI Driver 7.6.8** - USB audio driver

## POD XT Factory Reset (The Important Bit)

**This method actually works:**

1. Turn OFF your POD XT
2. Hold SAVE + all four  UP buttons together
![POD XT](images/podxt_buttons.jpg)
3. Turn ON whilst holding all buttons
4. Release when Line 6 logo appears
5. Wait for "standard model set loaded" message

Done. All factory presets restored, custom ones wiped.

## What's in the Repo

```
docs/        Analysis documentation
tools/       Python utilities for parsing firmware
extracted/   Extracted software bits
firmware/    Firmware files and analysis
scripts/     Setup automation
```

## Tools

- `line6_analysis_tools.py` - Parses IFF firmware format and analyses Mach-O binaries
- `podxt_factory_reset.py` - Factory reset utilities (though the manual method above works fine)
- `line6_extraction_script.sh` - Sets up the whole analysis environment

## Technical Findings

- **USB IDs:** Vendor 0x0e41, Product 0x5044 (POD XT)
- **Firmware:** Proprietary L6FF format (based on IFF)
- **Memory:** ~1MB space containing DSP algorithms and samples
- **Reset:** SAVE + UP button combo during power-on

## Technical Details

### Firmware Structure (PODxt_3_01.xtf)
- IFF container with L6FF signature
- 394,130 bytes total
- Version 1.0.769.0 (firmware 3.01)
- 20 device info chunks plus 393KB of actual firmware data

### Line 6 Monkey Analysis
- 32-bit Intel binary (i386)
- Requires macOS 10.5+ (won't run on 10.15+)
- Handles firmware updates and device management

## Setup

```bash
pip3 install pyusb
brew install libusb
```

### Running the Tools

```bash
git clone https://github.com/cmadds/line6-reverse-engineering
cd line6-reverse-engineering

# Set up analysis environment
./scripts/setup_analysis.sh

# Parse firmware
python3 tools/line6_analysis_tools.py firmware/PODxt_3_01.xtf

# Check for POD XT
python3 tools/podxt_factory_reset.py
```

## Reverse Engineering Approach

### Static Analysis
- Used `otool` to inspect Mach-O binaries
- Extracted strings and analysed patterns
- Parsed IFF chunks in firmware files
- Identified USB protocol details

### Dynamic Analysis
- Monitored USB traffic
- Traced system calls
- Runtime debugging where possible

## Security Notes

### Legacy Software Risks
- 32-bit apps don't run on modern macOS
- Unsigned kernel extensions blocked by SIP
- Potential privilege escalation issues
- USB driver vulnerabilities in old code

### Safer Analysis Environment
- macOS 10.14 Mojave VM (last version with 32-bit support)
- Isolated network
- USB monitoring tools

## Documentation

- [Complete Analysis Report](docs/line6_reverse_engineering_analysis.md)
- [Technical Summary](docs/line6_reverse_engineering_summary.md)
- [Factory Reset Guide](docs/podxt_factory_reset_guide.md)

## Contributing

Pull requests welcome for:
- Additional device support
- Protocol documentation
- Modern compatibility layers
- Security improvements

## Licence

Educational and research purposes. Reverse engineering performed under fair use for interoperability.

## What Was Accomplished

- Reverse engineered Line 6 legacy software
- Documented firmware structure
- Found working factory reset method
- Built analysis toolkit
- Created modern development environment

---

Star this if it helped you get your old Line 6 gear working again.
