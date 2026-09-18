"""Validate prepared ENGI-MIND chat-format JSONL."""
import argparse,json
from collections import Counter
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("dataset",type=Path); args=p.parse_args()
    total=0; branches=Counter()
    with args.dataset.open("r",encoding="utf-8") as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            item=json.loads(line); messages=item.get("messages",[])
            if [m.get("role") for m in messages] != ["system","user","assistant"]:
                raise ValueError(f"{args.dataset}:{line_no}: expected system/user/assistant")
            if any(not str(m.get("content","")).strip() for m in messages):
                raise ValueError(f"{args.dataset}:{line_no}: empty message")
            assistant=messages[2]["content"]
            if "[REVIEW_REQUIRED]" in assistant:
                raise ValueError(f"{args.dataset}:{line_no}: contains REVIEW_REQUIRED content")
            branches[item.get("metadata",{}).get("branch","unknown")]+=1; total+=1
    if not total: raise ValueError("dataset is empty")
    print("Examples:",total); print("Branches:",dict(branches)); print("Validation: PASS")

if __name__=="__main__": main()
