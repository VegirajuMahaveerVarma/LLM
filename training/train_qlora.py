"""Train ENGI-MIND with QLoRA using TRL + PEFT.

Example:
  python training/train_qlora.py --model Qwen/Qwen2.5-1.5B-Instruct
"""

import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--model",default="Qwen/Qwen2.5-1.5B-Instruct")
    p.add_argument("--train",default="training/processed/train.jsonl")
    p.add_argument("--validation",default="training/processed/validation.jsonl")
    p.add_argument("--output",default="training/outputs/engi-mind-lora")
    p.add_argument("--epochs",type=float,default=2)
    p.add_argument("--lr",type=float,default=2e-4)
    p.add_argument("--max-seq-length",type=int,default=1024)
    args=p.parse_args()

    try:
        import torch
        from datasets import load_dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
        from peft import LoraConfig
        from trl import SFTTrainer
    except ImportError as exc:
        raise SystemExit("Install training requirements first: python -m pip install -r training/requirements.txt") from exc

    train_path, val_path = Path(args.train), Path(args.validation)
    if not train_path.exists() or not val_path.exists():
        raise SystemExit("Prepared dataset not found. Run: python training/run_pipeline.py")

    for path in (train_path, val_path):
        for line in path.read_text(encoding="utf-8").splitlines():
            if "[REVIEW_REQUIRED]" in line:
                raise SystemExit(f"Refusing to train on unreviewed record: {path}")

    dataset=load_dataset("json",data_files={"train":str(train_path),"validation":str(val_path)})
    tokenizer=AutoTokenizer.from_pretrained(args.model,use_fast=True)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token

    compute_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_compute_dtype=compute_dtype,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(args.model,quantization_config=quant,device_map="auto")
    model.config.use_cache=False

    lora=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,bias="none",task_type="CAUSAL_LM",target_modules=["q_proj","k_proj","v_proj","o_proj"])
    def format_example(example):
        return tokenizer.apply_chat_template(example["messages"],tokenize=False,add_generation_prompt=False)

    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    training_args=TrainingArguments(
        output_dir=str(out),num_train_epochs=args.epochs,learning_rate=args.lr,
        per_device_train_batch_size=1,per_device_eval_batch_size=1,
        gradient_accumulation_steps=16,warmup_ratio=0.03,
        logging_steps=5,eval_strategy="steps",eval_steps=25,
        save_strategy="steps",save_steps=25,save_total_limit=2,
        fp16=torch.cuda.is_available(),report_to="none",
        gradient_checkpointing=True
    )
    trainer=SFTTrainer(
        model=model,tokenizer=tokenizer,train_dataset=dataset["train"],eval_dataset=dataset["validation"],
        formatting_func=format_example,peft_config=lora,args=training_args,max_seq_length=args.max_seq_length
    )
    trainer.train()
    trainer.save_model(str(out))
    tokenizer.save_pretrained(str(out))
    (out/"training_manifest.json").write_text(json.dumps({"base_model":args.model,"train":str(train_path),"validation":str(val_path),"epochs":args.epochs,"learning_rate":args.lr},indent=2),encoding="utf-8")
    print("Training complete. Adapter saved to",out)

if __name__=="__main__": main()
