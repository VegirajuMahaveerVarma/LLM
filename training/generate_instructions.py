"""Generate review-required instruction scaffolds from the curriculum manifest."""
import argparse,json
from pathlib import Path

TEMPLATES={
"explain":"Explain {topic} clearly for an undergraduate engineering student. Include the core idea, assumptions, and one engineering example.",
"practice":"Create a practice problem on {topic}. Give the problem first, then provide a worked solution with units and reasoning.",
"misconception_correction":"Correct a common misconception about {topic} and explain why it is wrong.",
"exam":"Give an exam-oriented question on {topic} and provide a concise marking-scheme-friendly solution.",
"project":"Explain how {topic} can appear in a practical engineering project, including inputs, outputs, constraints, and one implementation consideration."
}

def main():
    p=argparse.ArgumentParser(); p.add_argument("curriculum",type=Path); p.add_argument("output",type=Path); args=p.parse_args()
    manifest=json.loads(args.curriculum.read_text(encoding="utf-8")); n=0
    with args.output.open("w",encoding="utf-8") as f:
        for branch,subjects in manifest["domains"].items():
            for subject in subjects:
                topic=subject.replace("_"," ")
                for behavior,template in TEMPLATES.items():
                    f.write(json.dumps({"source_id":f"synthetic:{branch}:{subject}:{behavior}","license":"synthetic","branch":branch,"subject":subject,"topic":topic,"behavior":behavior,"difficulty":"undergraduate","question":template.format(topic=topic),"answer":"[REVIEW_REQUIRED] Replace with a validated answer from an approved source or expert review before training."},ensure_ascii=False)+"\n"); n+=1
    print(f"Wrote {n} review-required scaffolds to {args.output}")

if __name__=="__main__": main()
