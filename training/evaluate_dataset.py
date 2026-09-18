import json,sys
from collections import Counter
def validate(path):
    rows=[json.loads(x) for x in open(path,encoding='utf-8') if x.strip()]
    if not rows: raise ValueError('dataset is empty')
    for i,r in enumerate(rows,1):
        m=r.get('messages',[])
        if len(m)!=3 or [x.get('role') for x in m]!=['system','user','assistant']: raise ValueError(f'row {i}: invalid message format')
        if not m[1]['content'].strip() or not m[2]['content'].strip(): raise ValueError(f'row {i}: empty content')
    print('examples=',len(rows)); print('branches=',dict(Counter(r['metadata']['branch'] for r in rows)))
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python training/evaluate_dataset.py dataset.jsonl')
    validate(sys.argv[1])
