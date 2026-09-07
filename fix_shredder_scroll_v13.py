"""Guarded v12 hotfix: coherent Technodrome wall HDMA table selection."""
from pathlib import Path
import argparse,hashlib,json,struct

V12_SHA='8811ac47e3dd3a7535383fe561108929aa583e715aa7157aa166b50566141796'
START=0x1E215
BEFORE=bytes.fromhex('20 3F E2 69 00 00 8D D1 16 69 20 00 8D D4 16 8D D7 16 69 04 00')
OPERAND=0x1E21F
CAGE_OPERAND=0x1E228

def patch(source):
    before=bytes(source)
    if hashlib.sha256(before).hexdigest()!=V12_SHA:
        raise ValueError('Requires the exact final v12 headerless ROM')
    if before[START:START+len(BEFORE)]!=BEFORE:
        raise ValueError('Stage11 scroll handler contract changed')
    dispatch=[int.from_bytes(before[i:i+2],'little') for i in range(0x1DF12,0x1DF32,2)]
    if dispatch[11]!=0xE215 or dispatch.count(0xE215)!=1:
        raise ValueError('Expected stage11-exclusive handler')
    out=bytearray(before)
    out[OPERAND:OPERAND+2]=b'\0\0'
    # The handler next looks up the cage offset through A+4. Removing the
    # earlier +32 must be compensated here: keep this lookup at base+$24.
    out[CAGE_OPERAND:CAGE_OPERAND+2]=bytes.fromhex('24 00')
    out[0xFFDC:0xFFE0]=bytes.fromhex('ffff0000')
    checksum=sum(out)&0xFFFF
    struct.pack_into('<HH',out,0xFFDC,checksum^0xFFFF,checksum)
    changes=[i for i,(a,b) in enumerate(zip(before,out)) if a!=b]
    assert set(changes)=={OPERAND,CAGE_OPERAND}
    return bytes(out),dict(input_sha256=V12_SHA,output_sha256=hashlib.sha256(out).hexdigest(),checksum=f'{checksum:04X}',changed_offsets=changes,handler=START,wall_operand=OPERAND,wall_before='2000',wall_after='0000',cage_operand=CAGE_OPERAND,cage_before='0400',cage_after='2400',stage_id=11,dispatch=dispatch,scope='Use one room-wall table base across bands; keep the subsequent cage lookup at its original base+$24. The room floor follows its corrected anchor with the existing perspective progression. Art, shared code and other handlers unchanged.',requires_runtime_validation=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    output,report=patch(a.source.read_bytes())
    if a.output.exists() and a.output.read_bytes()!=output:raise FileExistsError(a.output)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(output)
    a.output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
