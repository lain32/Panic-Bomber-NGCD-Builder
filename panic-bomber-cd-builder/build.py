#!/usr/bin/env python3
"""Panic Bomber AES/MVS -> Neo Geo CD builder, tested Test 3/4 conversion.
Python 3.9+ standard library only. No BIOS, compiler, or network required.
"""
from pathlib import Path
import argparse,base64,hashlib,json,os,shutil,struct,sys,tempfile,wave,zipfile,zlib
ROOT=Path(__file__).resolve().parent
class BuildError(Exception): pass
def digest(data):return hashlib.sha256(data).hexdigest()
def filehash(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def checked(value,message):
 if not value:raise BuildError(message)
def read_roms(path,manifest):
 expected=manifest['roms'];by_hash={v['sha256']:k for k,v in expected.items()};sizes={v['size'] for v in expected.values()};found={}
 def accept(name,data):
  key=by_hash.get(digest(data))
  if key:found[key]=data
 if path.is_dir():
  for p in path.rglob('*'):
   if p.is_file() and p.stat().st_size in sizes:accept(p.name,p.read_bytes())
 else:
  checked(path.is_file(),'ROM ZIP or folder not found: '+str(path))
  with zipfile.ZipFile(path) as z:
   for info in z.infolist():
    if not info.is_dir() and info.file_size in sizes:accept(info.filename,z.read(info))
 missing=[k for k in expected if k not in found]
 checked(not missing,'Missing or unsupported ROM contents: '+', '.join(missing)+'. Use the original panicbom AES/MVS set; filenames may differ, but ROM hashes must match data/manifest.json.')
 return found
def game_files(rom,m):
 data=ROOT/'data'
 def patch(name,base):
  delta=zlib.decompress((data/(name+'.xor.z')).read_bytes());checked(len(delta)==len(base),'Invalid patch length: '+name)
  return bytes(a^b for a,b in zip(base,delta))
 p=bytearray(rom['073-p1.p1'][:262144]);p[::2],p[1::2]=p[1::2],p[::2]
 files={'PRG.PRG':patch('PRG.PRG',p),'Z81.Z80':patch('Z81.Z80',rom['073-m1.m1'][:65536]),'QUIET.PCM':bytes([128])*2048}
 files['FIX.FIX']=rom['073-s1.s1'][:m['files']['FIX.FIX']['size']]
 c1,c2=rom['073-c1.c1'],rom['073-c2.c2'];sprites=bytearray(len(c1)+len(c2))
 # AES/MVS interleave order (2,0,3,1): four CD bitplanes per row.
 sprites[0::4]=c1[1::2];sprites[1::4]=c1[0::2];sprites[2::4]=c2[1::2];sprites[3::4]=c2[0::2]
 files['SPR.SPR']=bytes(sprites[:m['files']['SPR.SPR']['size']])
 sound=rom['073-v1.v1']+rom['073-v2.v2'];m1=rom['073-m1.m1'];fixed=set(m['fixed_A_ids']);pcm=bytearray()
 def sample(i):
  a,b=struct.unpack_from('<HH',m1,0x3786+i*11+1);checked(a<=b and (b+1)*256<=len(sound),'Invalid sample descriptor');return sound[a*256:(b+1)*256]
 for i in sorted(fixed):pcm.extend(sample(i))
 # Fixed, already-tested mixed short cues; no re-rendering or re-encoding.
 for command in [0x21,0x22,0x23,0x25,0x26,0x27,0x2b,0x2d]:pcm.extend(zlib.decompress((data/(f'{command:02x}.pcm.z')).read_bytes()))
 checked(len(pcm)==m['cache_start'],'Resident PCM layout mismatch');files['PCM1.PCM']=bytes(pcm)
 for bank in range(6):
  character=m['bank_indices'].index(bank);ids=sorted(set(m['voice_ids'][character])-fixed)
  payload=bytearray();table=bytearray(files['Z81.Z80'][0x3786:0x3786+237*11])
  for i in ids:
   s=sample(i);a=m['cache_start']+len(payload);offset=i*11;table[offset:offset+11]=m1[0x3786+offset:0x3786+offset+11]
   struct.pack_into('<HH',table,offset+1,a//256,(a+len(s))//256-1);payload.extend(s)
  payload.extend(table)
  if len(payload)%2:payload.append(0)
  files[f'VOICE{bank}.PRG']=bytes(payload)
 checked(set(files)==set(m['files']),'Game-file list mismatch')
 for name,raw in files.items():checked(len(raw)==m['files'][name]['size'] and digest(raw)==m['files'][name]['sha256'],'Rebuilt file did not match tested release: '+name)
 return files
def check_assets(m):
 for name,h in m['data_hashes'].items():checked(filehash(ROOT/'data'/name)==h,'Damaged builder data: '+name)
 for name,meta in m['audio'].items():
  p=ROOT/'audio'/name;checked(p.stat().st_size==meta['size'] and filehash(p)==meta['sha256'],'Damaged or missing finalized audio: '+name)
  with wave.open(str(p),'rb') as w:checked((w.getnchannels(),w.getsampwidth(),w.getframerate())==(2,2,44100) and w.getnframes()%588==0,'Invalid CD audio: '+name)
def build(source,destination,verify_only=False):
 m=json.loads((ROOT/'data/manifest.json').read_text());source=source.expanduser().resolve();destination=destination.expanduser().resolve()
 if not verify_only:checked(not destination.exists(),'Output already exists; choose another --output folder: '+str(destination))
 print('Checking cartridge ROMs...',flush=True);rom=read_roms(source,m)
 print('Checking finalized audio and conversion data...',flush=True);check_assets(m)
 print('Rebuilding and verifying game files...',flush=True);files=game_files(rom,m)
 if verify_only:print('PASS: ROMs, builder assets, and all rebuilt game-file hashes match.');return
 destination.parent.mkdir(parents=True,exist_ok=True)
 needed=m['iso_bytes']+sum(v['size'] for v in m['audio'].values())+20*1024*1024
 checked(shutil.disk_usage(destination.parent).free>=needed,'Insufficient free disk space; about 750 MB is needed for the output.')
 staging=Path(tempfile.mkdtemp(prefix='.panicbom-build-',dir=destination.parent))
 try:
  print('Writing the CD data image...',flush=True);iso=staging/'Panic-Bomber-CD.iso'
  with iso.open('wb') as f:
   f.truncate(m['iso_bytes'])
   for offset,b64 in json.loads(zlib.decompress((ROOT/'data/layout.json.z').read_bytes())):f.seek(offset);f.write(base64.b64decode(b64))
   for name,raw in files.items():f.seek(m['files'][name]['offset']);f.write(raw)
  checked(filehash(iso)==m['iso_sha256'],'Final ISO hash mismatch')
  cue=['FILE "Panic-Bomber-CD.iso" BINARY','  TRACK 01 MODE1/2048','    INDEX 01 00:00:00']
  for n in range(2,19):
   name=f'track{n:02d}.wav';print('Copying finalized audio '+str(n-1)+'/17...',flush=True);shutil.copyfile(ROOT/'audio'/name,staging/name)
   checked(filehash(staging/name)==m['audio'][name]['sha256'],'Audio copy verification failed: '+name)
   cue += [f'FILE "{name}" WAVE',f'  TRACK {n:02d} AUDIO','    PREGAP 00:02:00','    INDEX 01 00:00:00']
  (staging/'Panic-Bomber-CD.cue').write_text('\n'.join(cue)+'\n',encoding='ascii')
  (staging/'READ-ME.txt').write_text('Open/burn Panic-Bomber-CD.cue with all tracks. Do not burn the ISO alone.\nThis is the Test 3 game with Test 4 finalized audio.\nHold B+C+D during a one-player battle to force an opponent loss (test shortcut).\nKeep the ISO, CUE and all 17 WAVs together. Disc duration: about 73:54.\n',encoding='utf-8')
  report={'builder_version':m['version'],'baseline':m['baseline'],'roms_verified':list(m['roms']),'game_files':m['files'],'iso_sha256':m['iso_sha256'],'layout_note':m['layout_note'],'audio':m['audio']}
  (staging/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
  sums=[]
  for p in sorted(staging.iterdir()):sums.append(filehash(p)+'  '+p.name)
  (staging/'SHA256SUMS.txt').write_text('\n'.join(sums)+'\n',encoding='ascii')
  staging.rename(destination)
 except BaseException:
  shutil.rmtree(staging,ignore_errors=True);raise
 print('Done. Open/burn: '+str(destination/'Panic-Bomber-CD.cue'),flush=True)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('rom',nargs='?',type=Path,default=ROOT/'panicbom.zip',help='Original ROM ZIP or folder (default: panicbom.zip beside this script)');parser.add_argument('--output',type=Path,default=ROOT/'Panic-Bomber-CD');parser.add_argument('--verify-only',action='store_true',help='Check inputs and conversion without writing a disc')
 a=parser.parse_args()
 try:build(a.rom,a.output,a.verify_only)
 except (BuildError,OSError,ValueError,KeyError,zipfile.BadZipFile,zlib.error,EOFError,wave.Error) as e:print('ERROR: '+str(e),file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
