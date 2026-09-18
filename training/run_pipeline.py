"""One-command local preparation pipeline for ENGI-MIND."""
import argparse, subprocess, sys
from pathlib import Path

def run(cmd):
    print("$"," ".join(map(str,cmd))); subprocess.run(cmd,check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="training/sample_data.jsonl")
    p.add_argument("--scaffold",action="store_true")
    args=p.parse_args()
    root=Path(__file__).resolve().parent.parent
    if args.scaffold:
        scaffold=root/"training"/"generated_scaffolds.jsonl"
        run([sys.executable,str(root/"training"/"generate_instructions.py"),str(root/"training"/"curriculum_manifest.json"),str(scaffold)])
        source=scaffold
    else:
        source=root/args.input
    run([sys.executable,str(root/"training"/"prepare_dataset.py"),str(source)])
    run([sys.executable,str(root/"training"/"evaluate_dataset.py"),str(root/"training"/"processed"/"train.jsonl")])
    run([sys.executable,str(root/"training"/"split_report.py"),str(root/"training"/"processed"/"train.jsonl")])

if __name__=="__main__": main()
