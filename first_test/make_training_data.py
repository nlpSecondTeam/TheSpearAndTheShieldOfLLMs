import json
import random

# 파일 이름 설정
INPUT_FILE = "custom_dataset.json"
OUTPUT_FILE = "sft_train_data.jsonl"

def main():
    # 1. 기존 데이터 읽기
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"🚨 오류: '{INPUT_FILE}' 파일이 없습니다. 폴더에 파일이 있는지 확인해주세요.")
        return

    sft_data = []

    print(f"🔄 데이터 증강 시작 (총 {len(data)}개 항목)...")

    for item in data:
        prompt = item['prompt']
        gold_refusal = item.get('gold_short_refusal', "죄송합니다. 답변할 수 없습니다.")
        label = item['label']

        # [CASE A] 정상 질문 (Accept) -> 그대로 1개만 사용
        if label == 'accept':
            conversation = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": gold_refusal}
            ]
            sft_data.append({"messages": conversation})
            continue

        # [CASE B] 공격 질문 (Reject) -> 답변 3개로 증강 (3-5개 만들기 미션 수행)
        
        # 1. 기본 거절 (Original)
        sft_data.append({"messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": gold_refusal}
        ]})

        # 2. 정책 강조형 거절 (Policy-based)
        policy_refusal = f"해당 요청은 안전 정책에 위배되므로 들어드릴 수 없습니다. 저는 유해하거나 불법적인 정보를 제공하지 않도록 설정되어 있습니다."
        sft_data.append({"messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": policy_refusal}
        ]})

        # 3. 교육/전환형 거절 (Educational/Redirection)
        # 내용에 따라 조금 더 자연스럽게 매칭되도록 템플릿 사용
        educational_refusal = "그 요청은 실행할 경우 위험하거나 비윤리적인 결과를 초래할 수 있어 답변하지 않습니다. 대신 관련 법률이나 안전 교육에 대한 정보가 필요하시면 말씀해 주세요."
        sft_data.append({"messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": educational_refusal}
        ]})

    # 2. 데이터 섞기 (셔플)
    random.shuffle(sft_data)

    # 3. 결과 저장 (JSONL 포맷)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in sft_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    print("=" * 40)
    print(f"✅ 작업 완료!")
    print(f"📂 생성된 파일: {OUTPUT_FILE}")
    print(f"📊 총 학습 데이터 개수: {len(sft_data)}쌍 (원본 50개 → 증강됨)")
    print("=" * 40)

if __name__ == "__main__":
    main()