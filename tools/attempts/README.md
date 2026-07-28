# Attempts

These are the reset scripts I wrote while trying to factory-reset a POD XT over USB/MIDI before I found the button combo. **None of them reliably reset the unit** — the SAVE + UP power-on combo in the main [README](../../README.md) is what actually works.

They're kept here because a few document things worth having:

- `podxt_reset_simple.py` — the Line 6 SysEx factory-reset command (`F0 00 01 0C 00 02 00 01 F7`) and the POD XT USB product IDs.
- `podxt_reset_midi.py` — sending that SysEx through macOS's built-in MIDI stack instead of raw USB.
- `podxt_manual_reset.py` — a text walkthrough of the button method.
- `podxt_reset_correct.py`, `podxt_reset_direct.py`, `podxt_reset_final.py` — successive USB/subprocess approaches, none conclusive.

Use them as reference, not as a working reset tool.
