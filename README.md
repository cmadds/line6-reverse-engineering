# Line 6 Legacy Software Reverse Engineering

🎸 **Complete reverse engineering analysis and tools for Line 6 POD XT legacy software**

## Overview

This repository contains a comprehensive reverse engineering analysis of Line 6's legacy 32-bit macOS software components, including working factory reset procedures for POD XT devices.

### Analyzed Components
- **Line 6 Monkey 1.78** - Device management application (32-bit Intel Mach-O)
- **PODxt_3_01.xtf** - Firmware file (IFF format, version 3.01)
- **Line 6 Audio-MIDI Driver 7.6.8** - USB audio driver package

## 🚀 Quick Start - POD XT Factory Reset

**✅ VERIFIED WORKING METHOD:**

1. **Turn OFF** your POD XT
2. **Hold SAVE + UP** buttons together
3. **Turn ON** while holding both buttons
4. **Release** when you see Line 6 logo
5. **Wait** for "standard model set loaded" message

**Result:** All factory presets restored, custom presets erased.

## 📁 Repository Structure

```
├── docs/                    # Analysis documentation
├── tools/                   # Python analysis utilities
├── extracted/               # Extracted software components
├── firmware/                # Firmware files and analysis
└── scripts/                 # Automation scripts
```

## 🔧 Analysis Tools

### Python Utilities
- `line6_analysis_tools.py` - IFF parser and Mach-O analyzer
- `podxt_factory_reset.py` - Factory reset utilities
- `line6_extraction_script.sh` - Complete setup automation

### Key Findings
- **USB Identifiers:** Vendor 0x0e41, Product 0x5044 (POD XT)
- **Firmware Format:** Line 6 proprietary L6FF (IFF-based)
- **Memory Layout:** ~1MB addressable space with DSP algorithms and samples
- **Reset Method:** Hardware button combination (SAVE + UP)

## 📊 Technical Analysis

### Firmware Structure (PODxt_3_01.xtf)
- **Format:** IFF container with L6FF signature
- **Size:** 394,130 bytes
- **Version:** 1.0.769.0 (firmware 3.01)
- **Components:** 20 device info chunks + 393KB data payload

### Binary Analysis (Line 6 Monkey)
- **Architecture:** 32-bit Intel (i386)
- **Requirements:** macOS 10.5+ (deprecated on 10.15+)
- **Purpose:** Firmware updates and device management

## 🛠️ Setup & Usage

### Prerequisites
```bash
pip3 install pyusb
brew install libusb
```

### Run Analysis
```bash
# Clone repository
git clone https://github.com/yourusername/line6-reverse-engineering
cd line6-reverse-engineering

# Run setup script
./scripts/setup_analysis.sh

# Analyze firmware
python3 tools/line6_analysis_tools.py firmware/PODxt_3_01.xtf

# Check for connected POD XT
python3 tools/podxt_factory_reset.py
```

## 🔍 Reverse Engineering Methodology

### Static Analysis
- Mach-O binary inspection with `otool`
- String extraction and pattern analysis
- IFF chunk parsing for firmware structure
- USB protocol identification

### Dynamic Analysis
- USB traffic monitoring
- System call tracing
- Runtime debugging capabilities

## ⚠️ Security Considerations

### Legacy Software Risks
- 32-bit applications deprecated in modern macOS
- Unsigned kernel extensions blocked by SIP
- Potential privilege escalation vectors
- USB driver vulnerabilities

### Recommended Environment
- macOS 10.14 Mojave VM (last 32-bit support)
- Isolated network environment
- USB filtering/monitoring tools

## 📚 Documentation

- [Complete Analysis Report](docs/line6_reverse_engineering_analysis.md)
- [Technical Summary](docs/line6_reverse_engineering_summary.md)
- [Factory Reset Guide](docs/podxt_factory_reset_guide.md)

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines and submit pull requests for:
- Additional device support
- Protocol documentation
- Modern compatibility layers
- Security improvements

## 📄 License

This project is for educational and research purposes. Reverse engineering performed under fair use for interoperability.

## 🎯 Achievements

- ✅ Successfully reverse engineered Line 6 legacy software
- ✅ Documented complete firmware structure
- ✅ Created working factory reset procedure
- ✅ Built comprehensive analysis toolkit
- ✅ Established modern development environment

---

**⭐ Star this repo if it helped you revive your vintage Line 6 gear!**