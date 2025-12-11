import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm  # 진행 상황을 바로 보여주는 라이브러리

# 1. 설정
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" # 사용할 모델
INPUT_FILE = "attack_prompts.xlsx"      # 질문이 담긴 엑셀 파일
OUTPUT_FILE = "baseline_results.xlsx"   # 결과가 저장될 파일

# 2. 모델과 토크나이저 로드 (처음 실행 시 자동으로 다운로드 됨)
print(f"Loading model: {MODEL_ID}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,  # 메모리 절약을 위해 float16 사용
    device_map="auto"           # GPU가 있으면 자동으로 GPU 사용
)

# 3. 엑셀 파일 읽기
print("Reading prompts...")
df = pd.read_excel(INPUT_FILE)
prompts = df['prompt'].tolist() # 'prompt' 컬럼의 내용을 리스트로 변환

results = []

print("Starting inference...")
# 4. 질문 하나씩 모델에 넣고 답변 받기
for q in tqdm(prompts):
    # TinyLlama Chat 모델의 대화 형식을 맞춰줍니다.
    # (일반 문장만 넣으면 모델이 혼란스러워 할 수 있습니다.)
    messages = [
        {"role": "user", "content": q}
    ]
    
    # 입력을 모델이 이해하는 숫자로 변환
    input_ids = tokenizer.apply_chat_template(
        messages, 
        return_tensors="pt", 
        add_generation_prompt=True
    ).to(model.device)

    # 답변 생성
    outputs = model.generate(
        input_ids,
        max_new_tokens=200,    # 답변 최대 길이
        do_sample=True,        # 창의적인 답변 허용 (False면 항상 같은 답변)
        temperature=0.7,       # 무작위성 조절 (낮을수록 보수적)
        top_k=50,
        top_p=0.95
    )

    # 숫자를 다시 글자로 변환 (입력 질문은 빼고 순수 답변만 추출)
    response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
    
    # 결과 저장용 리스트에 추가
    results.append({
        "original_prompt": q,
        "model_response": response,
        "is_refusal": "" # 나중에 엑셀에서 O/X 표시할 칸
    })

# 5. 결과를 엑셀로 저장
print(f"Saving results to {OUTPUT_FILE}...")
result_df = pd.DataFrame(results)
result_df.to_excel(OUTPUT_FILE, index=False)

print("Done! 완료되었습니다.")