# Panic Bomber — Neo Geo CD Builder

Build a working **Panic Bomber Neo Geo CD disc** from the original Neo Geo AES/MVS ROM set.

This builder includes the finalized CD-audio tracks and preserves the sound fixes tested on real **Neo Geo CDZ hardware**.

**Python 3.9+ · No additional Python packages · No BIOS or original CD image required**

## Download

Download **Panic-Bomber-CD-Builder-1.0.zip** from the repository’s **Releases** section.

Use the full builder package for everything needed apart from your cartridge ROMs. GitHub’s automatic **Source code** archives do not include the CD-audio tracks.

## Quick start

1. Extract the full builder package.
2. Place your original `panicbom.zip` beside `build.py`.
3. On Windows, double-click **Build-Windows.cmd**. You can also drag your ROM ZIP onto it.
4. Wait for the build and verification to finish.
5. Open or burn **Panic-Bomber-CD/Panic-Bomber-CD.cue**, including every track.

**Do not burn the ISO alone.** Keep the generated ISO, CUE and all 17 WAV files together.

The completed disc is approximately **73 minutes 54 seconds**.

## Requirements

- **Python 3.9 or newer**
- The original seven-file Panic Bomber AES/MVS ROM set
- Approximately **1.5 GB of free space** for the extracted builder and its output

No emulator, BIOS, compiler, original patched ISO or additional Python packages are needed to build the disc.

## Required ROMs

| File | Size |
|---|---:|
| `073-p1.p1` | 524,288 bytes |
| `073-m1.m1` | 131,072 bytes |
| `073-s1.s1` | 131,072 bytes |
| `073-c1.c1` | 1,048,576 bytes |
| `073-c2.c2` | 1,048,576 bytes |
| `073-v1.v1` | 2,097,152 bytes |
| `073-v2.v2` | 1,048,576 bytes |

The builder identifies each ROM by its **SHA-256 hash**, so the ZIP does not need to be an identical copy of the original archive.

Alternate filenames, different ZIP compression and subfolders are supported. The ROM contents must remain unchanged and match the supported set listed in [`data/manifest.json`](data/manifest.json).

## What this version fixes

### Sound and voices

- Rebuilds resident effects and six opponent voice banks from the cartridge samples.
- Preloads the upcoming opponent’s voice bank before the stage-intro jingle.
- Uses a sound-CPU handshake to stop playback before transferring sample data and resume it afterward.
- Preserves the fix that resolved intermittent buzzing during full-game CDZ testing.
- Keeps short musical cues in sound RAM using the tested ADPCM-A conversions.

### Background music and credits

- Uses finalized CD-audio tracks for longer background music.
- Restores approximately **17 seconds of previously missing ending music**, including its natural ending.
- Adds quiet padding to prevent the CDZ BIOS from restarting the ending track before the credits finish.
- Copies all included music unchanged during building.

### Graphics and disc layout

- Converts cartridge sprites into the CD format.
- Preserves the tested trimming of unused trailing graphics data.
- Uses a padded data track to position the audio farther out on the disc.

## Command-line usage

Build from a ROM ZIP:

```sh
python build.py panicbom.zip
```

Choose another output folder:

```sh
python build.py "path/to/panicbom.zip" --output "path/to/new-disc-folder"
```

Verify an extracted ROM folder without creating a disc:

```sh
python build.py "path/to/extracted-roms" --verify-only
```

Use `python3` instead of `python` if required by your system.

The builder will not overwrite an existing output folder. Move or rename the previous output, or choose a new location with `--output`.

## Building from this repository

Copy the `audio` folder from the full release package into your checkout before running the builder.

It must contain `track02.wav` through `track18.wav`, including the corrected ending recording as **`track04.wav`**. The builder checks every audio file against its expected hash.

## Stage-testing shortcut

During a single-player battle, hold **B+C+D** to force the opponent to lose at the next normal loss check.

Release the buttons to play normally, or keep holding them to advance through opponents for testing. The shortcut is inactive in menus, demo gameplay and two-player mode.

## Testing

- The underlying port completed a full game on real **Neo Geo CDZ hardware** without reported buzzing.
- The corrected ending music was confirmed working on CDZ.
- All nine stage-intro voices were checked against the cartridge samples and recorded emulator output.
- The builder-generated disc passed a full clear, credits and name-entry test in NeoCD.
- Its complete 41,000-frame audio capture matched the finalized Test 4 reference byte for byte.

The Python builder was tested on Linux. The included Windows launcher has not yet been tested on Windows, and the freshly rebuilt ISO has been tested in emulation rather than separately on physical hardware.

See [`validation.json`](validation.json) for the recorded checks.

## Verification and troubleshooting

The builder checks the input ROMs, conversion data, audio, rebuilt game files and final ISO. It also generates **`build-report.json`** and **`SHA256SUMS.txt`** alongside the disc files.

| Message or issue | What to check |
|---|---|
| Missing or unsupported ROM contents | Use the original supported cartridge set, not CD files or prepatched ROMs. |
| Damaged or missing audio | Extract the full release package again. The source archive does not include WAVs. |
| Output already exists | Choose another output folder or move the previous build. |
| Disc loads without background music | Open or burn the CUE with all audio tracks, rather than using the ISO alone. |

## Current scope

This is a builder specifically for **Panic Bomber**, not a general-purpose Neo Geo conversion tool.

General mid-game music fades remain unchanged. The rebuilt ISO also zero-fills obsolete, unreferenced data from the earlier image; all referenced game files, file positions and filesystem metadata are preserved.

## Credits

Original game, artwork and music credits belong to their respective creators. This project builds on the supplied CD port and the sound fixes developed during testing.

See [`CREDITS.txt`](CREDITS.txt) for attribution.
