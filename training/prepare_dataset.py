"""Validate, deduplicate, normalize, and split ENGI-MIND JSONL records."""

import argparse, hashlib, json, random
from pathlib import Path

ALLOWED_LICENSE_HINTS = ("public domain","cc0","cc-by","cc by","mit","apache","permission","synthetic")
REQUIRED = ("source_id","license","branch","subject","topic","question","answer")

def load_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip(): continue
            try: yield line_no, json.loads(line)
            except json.JSONDecodeError as exc: raise ValueError(f"{path}:{line_no}: invalid JSON") from exc

def license_ok(value):
    return any(h in value.lower() for h in ALLOWED_LICENSE_HINTS)

def make_record(row):
    missing = [k for k in REQUIRED if not str(row.get(k, "")).strip()]
    if missing: raise ValueError("missing required fields: " + ", ".join(missing))
    if not license_ok(str(row["license"])): raise ValueError("unapproved license: " + str(row["license"]))
    q, a = str(row["question"]).strip(), str(row["answer"]).strip()
    digest = hashlib.sha256((q.lower().strip() + "\n" + a.lower().strip()).encode()).hexdigest()
    return {"messages":[
        {"role":"system","content":"You are ENGI-MIND, an engineering learning assistant. Explain rigorously, show assumptions and units, and adapt to the student's level."},
        {"role":"user","content":q},
        {"role":"assistant","content":a}],
        "metadata":{"source_id":str(row["source_id"]),"license":str(row["license"]),"branch":str(row["branch"]),
        "subject":str(row["subject"]),"topic":str(row["topic"]),"behavior":str(row.get("behavior","explain")),
        "difficulty":str(row.get("difficulty","undergraduate")),"dedupe_hash":digest}}

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); p.add_argument("--output-dir",type=Path,default=Path("training/processed")); p.add_argument("--val-ratio",type=float,default=.1); p.add_argument("--seed",type=int,default=42); args=p.parse_args()
    if not 0 < args.val_ratio < .5: raise ValueError("--val-ratio must be between 0 and 0.5")
    records=[]; seen=set()
    for line_no,row in load_jsonl(args.input):
        r=make_record(row); key=r["metadata"]["dedupe_hash"]
        if key not in seen: seen.add(key); records.append(r)
    if len(records)<2: raise ValueError("at least two unique records are required")
    random.Random(args.seed).shuffle(records); val_count=max(1,round(len(records)*args.val_ratio)); val,train=records[:val_count],records[val_count:]
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,items in (("train.jsonl",train),("validation.jsonl",val)):
        with (args.output_dir/name).open("w",encoding="utf-8") as f:
            for item in items: f.write(json.dumps(item,ensure_ascii=False)+"\n")
    stats={"input_records":sum(1 for _ in load_jsonl(args.input)),"unique_records":len(records),"train_records":len(train),"validation_records":len(val),"seed":args.seed}
    (args.output_dir/"stats.json").write_text(json.dumps(stats,indent=2),encoding="utf-8"); print(json.dumps(stats,indent=2))

if __name__=="__main__": main()
