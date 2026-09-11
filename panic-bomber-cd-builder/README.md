# Panic Bomber Neo Geo CD Builder

Build the completed Panic Bomber Neo Geo CD port from the original AES/MVS cartridge ROM set. Preserves the Test 3 voice-bank buzzing fix and the Test 4 complete credits music.

**Python 3.9+ · No extra Python packages · No BIOS or original CD ISO required**

## Build a disc

Use the complete **Panic-Bomber-CD-Builder-1.0.zip** package from the repository's Releases section when available. It includes the finalized audio; the Git source archive does not.

1. Extract the full builder package.
2. Place your original `panicbom.zip` beside `build.py`.
3. On Windows, run **Build-Windows.cmd**, or drag your ROM ZIP onto it.
4. Open or burn **Panic-Bomber-CD/Panic-Bomber-CD.cue**, with every track included.

Do not burn the ISO alone. Keep the output ISO, CUE and 17 WAV files together. The resulting disc is approximately **73 minutes 54 seconds**.

Install Python from [python.org](https://www.python.org/downloads/) if needed.

### Command line

```sh
python build.py panicbom.zip
python build.py "path/to/roms.zip" --output "path/to/new-disc-folder"
python build.py "path/to/extracted-roms" --verify-only
```

Use `python3` if that is your system's Python command. Existing output folders are protected from overwriting. Allow roughly 1.5 GB for the extracted full package and generated disc.

### Building from this repository

Copy the `audio` folder from the finalized full builder package into this checkout. It must contain `track02.wav` through `track18.wav`, with the corrected Test 4 credits recording named `track04.wav`. Then run the commands above.

The builder checks the music hashes and copies the files unchanged. It does not render or re-encode music. Required conversion patches and short mixed cues are in `data/`.

## Required ROM contents

| ROM | Size in bytes |
| --- | ---: |
| `073-p1.p1` | 524,288 |
| `073-m1.m1` | 131,072 |
| `073-s1.s1` | 131,072 |
| `073-c1.c1` | 1,048,576 |
| `073-c2.c2` | 1,048,576 |
| `073-v1.v1` | 2,097,152 |
| `073-v2.v2` | 1,048,576 |

ROMs are identified by SHA-256, not filename or ZIP checksum. Renaming files, ZIP compression changes and ZIP subfolders are supported. All seven ROM contents must match [data/manifest.json](data/manifest.json). Modified or unsupported ROM revisions are rejected.

## What the conversion includes

- Safe sound-CPU handshakes during voice-bank changes, with upcoming stage voices preloaded before the intro jingle.
- Six opponent voice banks and resident sound effects rebuilt from the cartridge samples.
- Previously converted short musical cues that combine the cartridge's sound components into CD-compatible ADPCM-A samples.
- Cartridge sprites converted into CD byte order, with the tested graphics trimming.
- Finalized CD background music, including the restored ending and padding that prevents an early BIOS restart.
- A padded data track that retains the tested placement of audio farther out on the disc.

The existing **B+C+D** testing shortcut remains: hold it during a one-player battle to force an opponent loss at the next normal loss check. Release it to play normally. It is inactive in menus, demo gameplay and two-player mode.

General mid-game music fades remain unchanged. This builder is specific to Panic Bomber.

## Validation

All referenced game files match Test 3 byte for byte, and all 17 music tracks match the finalized Test 4 set. The generated disc passed a full clear and credits test in NeoCD; the complete 41,000-frame audio capture matched the Test 4 reference byte for byte. See [validation.json](validation.json).

The user confirmed the underlying Test 3/4 port on real CDZ hardware. The newly rebuilt ISO was tested in emulation. The Python builder was exercised on Linux; the Windows launcher has not been executed on Windows in these tests.

The rebuilt ISO differs from the older image only in obsolete, unreferenced sectors that are zero-filled. Referenced file data, file positions and filesystem metadata are preserved. The builder verifies its own fixed ISO hash and writes `build-report.json` and `SHA256SUMS.txt` alongside the output.

## Project files

- [build.py](build.py): dependency-free builder.
- [data/manifest.json](data/manifest.json): accepted ROMs, assets, file layout and expected hashes.
- [CREDITS.txt](CREDITS.txt): game, port and testing attribution.
- [GitHub setup](docs/github-setup.md): initial repository and release instructions.
- [Version 1.0 notes](docs/release-notes-v1.0.md): prepared release description.
