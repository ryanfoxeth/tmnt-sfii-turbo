"""Retire obsolete decorative tilemap animation lists in replaced stages.

Original Ryu/Sagat already use the empty C2:BA8C list. Point only the replaced
rooms' entries at that same no-op, instead of dropping individual transfers
observed during a finite trace. Original/bonus/ending stage entries stay exact.
This component does not change palettes, objects, cage scroll or game scripts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

STAGE_DIRECTORY=0x2B966
SCRIPT_TABLE_START=0x2B98A
SCRIPT_TABLE_END=0x2BA8C

BASE_SHA="aacc2ada6569d35711227d83f179f7ff232a442a1a07b534d0499f0971792d91"
REPLACED={0,1,3,4,5,7,8,9,10,11}
EMPTY=0xBA8C


def checksum(rom):
    rom[0xFFDC:0xFFE0]=bytes.fromhex('FFFF0000')
    value=sum(rom)&0xFFFF
    rom[0xFFDC:0xFFE0]=(value^0xFFFF).to_bytes(2,'little')+value.to_bytes(2,'little')
    return value


def _script(rom,pointer):
    """Read the audited C2 stage-list format; do not execute game code."""
    start=0x20000+int.from_bytes(rom[pointer:pointer+2],'little')
    p=start;records=[]
    while rom[p]:
        command=rom[p];length=command&0x7E
        if not command&0x80 or not length or p-start>=500:
            raise ValueError(f'Unknown animation command at {p:#x}')
        destination=int.from_bytes(rom[p+1:p+3],'little')
        source=0x20000+int.from_bytes(rom[p+3:p+5],'little')
        if source+length>0x30000:raise ValueError('Payload crosses source bank')
        records.append({'command_offset':p,'source_offset':source,'length_bytes':length,
                        'words':[{'vram_word':destination+i*(32 if command&1 else 1)}
                                 for i in range(length//2)]})
        p+=5
    return {'start':start,'end_exclusive':p+1,'records':records}


def patch(raw: bytes):
    if len(raw)!=0x400000 or hashlib.sha256(raw).hexdigest()!=BASE_SHA:
        raise ValueError("Requires the exact headerless v14 release")
    directory=[int.from_bytes(raw[a:a+2],"little") for a in range(STAGE_DIRECTORY,SCRIPT_TABLE_START,2)]
    assert directory[0]==directory[9]==0xB98A
    assert int.from_bytes(raw[0x2B98A:0x2B98C],"little")==EMPTY and raw[0x20000+EMPTY]==0
    ends=sorted(set(directory+[SCRIPT_TABLE_END&0xFFFF]))
    entries={}
    ownership={}
    for stage,start in enumerate(directory):
        end=next(x for x in ends if x>start)
        assert start%2==0 and SCRIPT_TABLE_START<=0x20000+start<0x20000+end<=SCRIPT_TABLE_END
        entries[stage]=list(range(0x20000+start,0x20000+end,2))
        for address in entries[stage]:ownership.setdefault(address,set()).add(stage)
    out=bytearray(raw);edits=[];stages={}
    for stage in sorted(REPLACED):
        lists=[]
        for address in entries[stage]:
            assert ownership[address]<=REPLACED
            script=_script(raw,address)
            for record in script['records']:
                assert all(0x3800<=w['vram_word']<0x4800 for w in record['words'])
                if stage==11:
                    assert all(0x4000<=w['vram_word']<0x4800 for w in record['words']),"Never retire the cage BG1"
            before=raw[address:address+2]
            out[address:address+2]=EMPTY.to_bytes(2,'little')
            lists.append({"pointer_offset":address,"old_list":script['start'],
                          "retired_map_commands":len(script['records'])})
            if before!=out[address:address+2]:edits.append({"start":address,"end_exclusive":address+2,"before":before.hex(),"after":out[address:address+2].hex()})
        stages[str(stage)]=lists
    for stage,addresses in entries.items():
        if stage not in REPLACED:
            assert all(out[a:a+2]==raw[a:a+2] for a in addresses)
    stored=checksum(out)
    allowed=set(range(0xFFDC,0xFFE0))|{a for e in edits for a in range(e['start'],e['end_exclusive'])}
    changed=[a for a,(x,y) in enumerate(zip(raw,out)) if x!=y]
    assert set(changed)<=allowed
    assert out[0x1E21F]==0 and out[0x1E228]==0x24
    report={"component":"retire-stage-tilemap-lists","input_sha256":BASE_SHA,
            "output_sha256":hashlib.sha256(out).hexdigest(),"checksum":f"{stored:04X}",
            "changed_bytes":len(changed),"edits":edits,"stages":stages,
            "original_bonus_and_ending_lists_unchanged":True,
            "scope":"Only stage-specific background tilemap list pointers and checksum",
            "runtime_validation_required":True}
    return bytes(out),report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();raw,report=patch(a.source.read_bytes());a.out.mkdir(parents=True,exist_ok=True)
    target=a.out/'tmnt-roster-v15-map-candidate.sfc'
    if target.exists() and target.read_bytes()!=raw:raise FileExistsError(target)
    target.write_bytes(raw);report['candidate']=str(target)
    (a.out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('candidate','output_sha256','changed_bytes')},indent=2))
