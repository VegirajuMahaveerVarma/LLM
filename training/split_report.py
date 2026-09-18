"""Report branch, subject, and behavior balance for a prepared JSONL dataset."""
import argparse,json
from collections import Counter
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("dataset",type=Path); args=p.parse_args()
    branches,subjects,behaviors=Counter(),Counter(),Counter()
    with args.dataset.open("r",encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            m=json.loads(line).get("metadata",{}); branches[m.get("branch","unknown")]+=1; subjects[m.get("subject","unknown")]+=1; behaviors[m.get("behavior","unknown")]+=1
    print("=== ENGI-MIND dataset balance ===")
    print("Branches:",dict(branches)); print("Behaviors:",dict(behaviors)); print("Unique subjects:",len(subjects)); print("Total examples:",sum(branches.values()))

if __name__=="__main__": main()
