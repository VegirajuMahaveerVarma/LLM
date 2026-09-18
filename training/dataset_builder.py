import json,sys
REQUIRED={'source_id','license','branch','subject','topic','question','answer'}
ALLOWED=('public domain','cc0','cc-by','cc by','mit','apache','permission')
def permitted(x): return any(h in x.lower() for h in ALLOWED)
def build(src,dst):
    n=0
    with open(src,encoding='utf-8') as fi,open(dst,'w',encoding='utf-8') as fo:
        for line_no,line in enumerate(fi,1):
            if not line.strip(): continue
            r=json.loads(line); missing=REQUIRED-set(r)
            if missing: raise ValueError(f'line {line_no}: missing {sorted(missing)}')
            if not permitted(r['license']): raise ValueError(f'line {line_no}: license not permitted')
            row={'messages':[{'role':'system','content':'You are ENGI-MIND, an engineering learning assistant. Teach accurately and progressively.'},{'role':'user','content':r['question']},{'role':'assistant','content':r['answer']}],'metadata':{k:r[k] for k in ('source_id','license','branch','subject','topic')}}
            fo.write(json.dumps(row,ensure_ascii=False)+'\n'); n+=1
    return n
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python training/dataset_builder.py input.jsonl output.jsonl')
    print(f'wrote {build(sys.argv[1],sys.argv[2])} examples')
