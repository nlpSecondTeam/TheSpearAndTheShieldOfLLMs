import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

# ==========================================
# 1. 설정 (Configuration)
# ==========================================
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
NEW_MODEL_NAME = "uos-eng-v3"  # V3 모델 (문제 해결)
DATASET_FILE = "train_eng_v3.jsonl"  # V3 데이터셋 (공격 200:정상 200)

# ==========================================
# 2. 데이터셋 로드 및 포맷팅 (여기가 핵심 수정됨)
# ==========================================
dataset = load_dataset("json", data_files=DATASET_FILE, split="train")

def formatting_prompts_func(example):
    output_texts = []
    
    # 🚨 [수정 완료] 데이터가 하나씩 들어오므로 이중 루프를 제거했습니다.
    # example['messages']는 [{'role': 'user'...}, {'role': 'assistant'...}] 형태입니다.
    conversation = example['messages']
    
    text = ""
    for msg in conversation:
        role = msg['role']
        content = msg['content']
        
        if role == "user":
            text += f"<|user|>\n{content}</s>\n"
        elif role == "assistant":
            text += f"<|assistant|>\n{content}</s>\n"
            
    output_texts.append(text)
    return output_texts

# ==========================================
# 3. 모델 및 토크나이저 로드 (QLoRA)
# ==========================================
print("⏳ 모델 로드 중...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=8,  # Rank
    bias="none",
    task_type="CAUSAL_LM",
)

# ==========================================
# 4. 학습 파라미터 설정 (안전 모드 적용)
# ==========================================
# 🚨 max_seq_length 에러를 피하기 위해 init에서 빼고 아래에서 주입합니다.
training_args = SFTConfig(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=50,
    logging_steps=10,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    dataset_text_field="text", 
)

# 강제 주입 (라이브러리 버그/버전 이슈 방지)
training_args.max_seq_length = 512

# ==========================================
# 5. 트레이너 실행
# ==========================================
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    formatting_func=formatting_prompts_func,
    processing_class=tokenizer, # tokenizer 대신 processing_class 사용
    args=training_args,
)

print("🚀 학습 시작!")
trainer.train()

# ==========================================
# 6. 저장
# ==========================================
print("💾 모델 저장 중...")
trainer.model.save_pretrained(NEW_MODEL_NAME)
tokenizer.save_pretrained(NEW_MODEL_NAME)
print(f"🎉 학습 완료! 저장된 경로: ./{NEW_MODEL_NAME}")