# Panic Bomber CD Builder 1.0

Rebuild the completed Panic Bomber Neo Geo CD port from the original AES/MVS ROM set.

Download **Panic-Bomber-CD-Builder-1.0.zip** from the release assets for the complete builder and finalized audio. GitHub's automatic source archives do not contain the WAV files.

## Included

- Test 3 voice-bank handshake and stage-intro preloading fixes.
- Test 4 complete credits music and restart-prevention padding.
- Finalized audio copied unchanged during builds.
- Python builder, Windows launcher and build verification reports.

## Requirements

Python 3.9+ and the original seven Panic Bomber cartridge ROMs. No BIOS, original CD image, compiler or extra Python packages are needed.

Extract the package, place `panicbom.zip` beside `build.py`, and run `Build-Windows.cmd` or `python build.py panicbom.zip`. Open/burn the generated `Panic-Bomber-CD.cue` with all its tracks.

The generated disc passed a full clear and credits emulator test. The underlying Test 3/4 port was confirmed by the user on real CDZ hardware. The B+C+D stage-testing shortcut remains included.
