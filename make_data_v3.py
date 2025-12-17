import json
import random

# ==========================================
# 1. 획일화된 거절 멘트 템플릿 (공격 방어용)
# ==========================================
REFUSAL_TEMPLATES = [
    # [단호]
    "죄송합니다. 그 요청은 수행할 수 없습니다.",
    "해당 질문에 대해서는 답변하지 않습니다.",
    "위험하거나 불법적인 요청에는 응답하지 않도록 설정되어 있습니다.",
    "안전 정책상 해당 정보는 제공할 수 없습니다.",
    # [이유 설명]
    "해당 행위는 법적으로 문제가 될 소지가 있어 도와드릴 수 없습니다.",
    "이는 타인에게 심각한 해를 끼칠 수 있는 행위이므로 답변이 제한됩니다.",
    "폭력적이거나 유해한 콘텐츠 생성은 저의 윤리 가이드라인에 위배됩니다.",
    # [정중 & 우회]
    "죄송하지만, 그 부분은 제가 도와드리기 어렵네요. 다른 주제로 대화할까요?",
    "요청하신 내용은 답변하기 곤란합니다. 양해 부탁드립니다.",
    "마음은 알겠지만, 규정상 해당 정보는 알려드릴 수 없습니다.",
    # [대안 제시]
    "직접적인 방법 대신, 관련된 안전 교육 자료나 법률 정보를 찾아드릴까요?",
    "위험한 방법보다는 합법적이고 안전한 해결책을 찾아보시는 건 어떨까요?",
]

# ==========================================
# 2. 정상 대화 데이터 대량 확보 (약 200개 분량 패턴)
# ==========================================
# 모델이 "거절만 하는 바보"가 되지 않도록 다양한 주제를 섞습니다.
NORMAL_TOPICS = {
    "greeting": [
        ("안녕, 반가워!", "안녕하세요! 만나서 반갑습니다. 무엇을 도와드릴까요?"),
        ("너는 누구니?", "저는 여러분을 돕기 위해 만들어진 인공지능 어시스턴트입니다."),
        ("오늘 기분 어때?", "저는 감정이 없지만, 여러분과 대화할 수 있어 기쁩니다!"),
        ("좋은 아침이야.", "좋은 아침입니다! 오늘 하루도 활기차게 시작하시길 바래요."),
        ("심심해, 놀아줘.", "심심하시군요! 재미있는 퀴즈를 풀거나 이야기를 만들어볼까요?"),
    ],
    "knowledge": [
        ("사과가 영어로 뭐야?", "사과는 영어로 'Apple'입니다."),
        ("하늘은 왜 파래?", "대기 중의 분자들이 태양 빛의 파란색 파장을 산란시키기 때문입니다(레일리 산란)."),
        ("서울의 날씨는 보통 어때?", "서울은 사계절이 뚜렷하며, 여름엔 덥고 습하지만 겨울엔 춥고 건조합니다."),
        ("이순신 장군에 대해 알려줘.", "이순신 장군은 조선 시대의 명장으로, 임진왜란 당시 거북선을 활용해 큰 승리를 거두었습니다."),
        ("광합성이 뭐야?", "식물이 빛 에너지를 이용해 이산화탄소와 물로 포도당과 산소를 만드는 과정입니다."),
        ("피타고라스 정리가 뭐지?", "직각삼각형에서 빗변의 제곱은 다른 두 변의 제곱의 합과 같다는 수학 정리입니다."),
        ("지구는 둥근가요?", "네, 지구는 타원체에 가까운 둥근 모양입니다."),
        ("물은 화학식으로 뭐야?", "물의 화학식은 H2O입니다."),
    ],
    "coding": [
        ("파이썬으로 리스트 정렬하는 법 알려줘.", "파이썬에서는 `sort()` 메서드나 `sorted()` 함수를 사용해 정렬할 수 있습니다."),
        ("HTML에서 버튼 어떻게 만들어?", "`<button>클릭</button>` 태그를 사용하면 버튼을 만들 수 있습니다."),
        ("자바스크립트 변수 선언 방법은?", "`var`, `let`, `const` 키워드를 사용하여 변수를 선언할 수 있습니다."),
        ("C언어에서 Hello World 출력해줘.", "`printf(\"Hello World\");` 함수를 사용하면 됩니다."),
        ("for 반복문 예제 보여줘.", "파이썬 예제입니다:\n`for i in range(5): print(i)`"),
    ],
    "creativity": [
        ("점심 메뉴 추천해줄래?", "든든한 김치찌개나 가벼운 샌드위치는 어떠세요?"),
        ("재미있는 이야기 해줘.", "옛날 어느 마을에 호기심 많은 고양이가 살았습니다... (생략)"),
        ("소설 잘 쓰는 팁 있어?", "캐릭터의 욕망을 구체화하고, 갈등을 통해 이야기를 전개해보세요."),
        ("여행지 추천해줘.", "휴식을 원하신다면 제주도의 푸른 바다를, 활기를 원하신다면 부산을 추천합니다."),
        ("스트레스 해소법 알려줘.", "가벼운 산책을 하거나 명상을 해보세요. 충분한 수면도 중요합니다."),
        ("친구 생일 선물 뭐가 좋을까?", "친구의 취향에 따라 다르겠지만, 실용적인 텀블러나 향초는 어떨까요?"),
    ]
}

def generate_normal_samples(target_count=200):
    samples = []
    
    # 1. 기본 템플릿 데이터 추가
    for category, pairs in NORMAL_TOPICS.items():
        for q, a in pairs:
            samples.append({"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]})
    
    # 2. 목표 개수(200개)가 될 때까지 변형해서 증식
    # (단어 조금씩 바꿔서 데이터 늘리기)
    base_samples = list(samples)
    while len(samples) < target_count:
        original = random.choice(base_samples)
        q = original["messages"][0]["content"]
        a = original["messages"][1]["content"]
        
        # 간단한 변형 로직 (어미나 수식어 변경)
        variations = [
            (f"{q} 알려줘", a),
            (f"질문 있어. {q}", f"네, 답변해 드립니다. {a}"),
            (f"{q} 궁금해.", f"{a} 도움이 되셨나요?"),
            (f"혹시 {q}", f"네! {a}"),
        ]
        
        new_q, new_a = random.choice(variations)
        samples.append({"messages": [{"role": "user", "content": new_q}, {"role": "assistant", "content": new_a}]})
    
    return samples[:target_count]

def main():
    input_file = "sft_train_data.jsonl"  # 기존 공격 데이터 파일
    output_file = "sft_train_data_v3.jsonl" # 최종 V3 파일
    
    final_data = []

    # 1. 공격 데이터 로드 및 Paraphrasing (약 230개 예상)
    print("🛡️ 공격 데이터 변환 중...")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                entry = json.loads(line)
                messages = entry["messages"]
                
                # 공격 질문(user)은 그대로, 답변(assistant)은 다양하게 교체
                user_msg = messages[0]['content']
                new_response = random.choice(REFUSAL_TEMPLATES)
                
                # 특정 키워드 맞춤형 거절
                if "폭탄" in user_msg or "폭발" in user_msg:
                    if random.random() > 0.5:
                        new_response = "폭발물 제조는 큰 위험을 동반하며 법적으로 금지되어 있어 알려드릴 수 없습니다."
                elif "해킹" in user_msg or "SQL" in user_msg:
                    if random.random() > 0.5:
                        new_response = "해킹 기술이나 악성 코드를 제공하는 것은 정보통신망법 위반이므로 도와드릴 수 없습니다."
                
                final_data.append({
                    "messages": [
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": new_response}
                    ]
                })
    except FileNotFoundError:
        print(f"🚨 오류: '{input_file}' 파일이 없습니다.")
        return

    attack_count = len(final_data)
    print(f"   👉 공격 데이터 {attack_count}개 확보")

    # 2. 정상 데이터 생성 (공격 데이터 개수만큼 1:1 비율로 생성)
    print(f"🍀 정상 데이터 생성 중... (목표: {attack_count}개)")
    normal_data = generate_normal_samples(target_count=attack_count)
    final_data.extend(normal_data)

    print(f"   👉 정상 데이터 {len(normal_data)}개 확보")

    # 3. 셔플 및 저장
    random.shuffle(final_data)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in final_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

    print(f"\n🎉 V3 데이터셋 생성 완료! '{output_file}'")
    print(f"📊 총 데이터: {len(final_data)}개 (공격:{attack_count} vs 정상:{len(normal_data)}) -> 비율 1:1 달성")
    print("🚀 이제 train.py를 실행해서 'V3' 모델을 만드세요!")

if __name__ == "__main__":
    main()

