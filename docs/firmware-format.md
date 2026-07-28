# The POD XT firmware format (`.xtf` / L6FF)

Line 6's `.xtf` firmware files are wrapped in **IFF** — the same chunk-based container behind AIFF and old Amiga files — with a Line 6 twist they label **L6FF** ("Line 6 Firmware Format"). This is what I worked out parsing `PODxt_3_01.xtf`; treat it as a field guide, not an official spec.

## Container

Standard IFF layout: a `FORM` wrapper, a form type, then a sequence of chunks.

```
FORM <size> L6FF
  HEAD <size> ...      version + header info
  dinf <size> ...      device info  (repeated, one per memory region)
  dinf <size> ...
  ...                  (20 dinf chunks in the 3.01 file)
  <data>               ~393 KB firmware payload
```

- **Magic:** `FORM` (big-endian IFF container)
- **Form type:** `L6FF`
- **First chunk:** `HEAD`

## `PODxt_3_01.xtf` at a glance

| Field | Value |
|-------|-------|
| Total size | 394,130 bytes (`0x060392`) |
| Form type | `L6FF` |
| Version | 1.0.769.0 (firmware 3.01) |
| `dinf` chunks | 20 |
| Payload | ~393,602 bytes |

## `dinf` — device info chunks

Each `dinf` chunk describes one region of the device's ~1 MB address space. Decoding the 20 chunks in the 3.01 file, the regions group into device "types":

| Type | Contents | Block size |
|------|----------|-----------|
| 0 | System / boot sectors | 32–64 KB |
| 1 | Configuration data | 8 KB |
| 2 | User presets | 64 KB |
| 3 | DSP code / algorithms | 64 KB |
| 4 | Audio samples / impulses | 64 KB |

## Reconstructed memory map (~1 MB total)

```
Boot / system     32–64 KB
DSP algorithms    512 KB   (8 × 64 KB)
Audio samples     320 KB   (5 × 64 KB)
User data         128 KB   (2 × 64 KB)
```

So the bulk of the firmware is DSP algorithm blocks — the amp/cab/effect models — with a big chunk of sample/impulse data behind them.

## Parsing it yourself

Because it's plain IFF, walking it is straightforward: read `FORM`, confirm the `L6FF` form type, then loop chunk-by-chunk (4-byte tag, 4-byte big-endian size, `size` bytes of body, pad to even length). `tools/line6_analysis_tools.py` does exactly this for the `.xtf` you point it at.

## What's still unknown

- The exact byte layout **inside** a `dinf` chunk (offsets, flags, checksums) isn't fully decoded — the type/size groupings above are inferred from the values that repeat.
- No signing or checksum was found over the payload, but "not found" isn't "not there."
- Whether the same layout holds across POD XT Live / Pro firmware, or other Line 6 XT-era devices, is untested.

Corrections and additions welcome — this came from one firmware version on one unit.
