# 🛡️ The Spear and the Shield of LLMs

### Jailbreaking Defense Fine-tuning Experiment

본 실험는 **LLM Jailbreaking 공격에 대한 방어 성능을 정량적으로 평가**하고,
**SFT 기반 Fine-tuning을 통해 방어 능력이 얼마나 개선되는지**를 실험적으로 분석한 결과를 담고 있다.

---

## 📌 실험 목적

* 기존 LLM(Baseline)이 **직접 공격 / 우회 공격 / 감정적 압박 / 역할극 기반 Jailbreaking**에 얼마나 취약한지 평가
* Jailbreaking 사례를 기반으로 학습한 **Fine-tuned 모델(uos-smollm-second)** 이
  실제로 **방어율을 얼마나 향상시키는지 정량 비교**
* **ASR(Attack Success Rate)**, **방어율**, **False Positive** 등 보안 관점 지표 중심 분석

---

## 🧪 실험 구성 개요

### 1. 평가 데이터셋

* 총 **50개 질문**

  * 공격 질문 (`reject`) : 42~44개
  * 정상 질문 (`accept`) : 6개
* 공격 유형 포함:

  * Direct harmful requests
  * Obfuscated / narrative-based attacks
  * Emotional manipulation
  * Role-play / instruction hijacking

---

### 2. 비교 모델

| 구분        | 모델                                        |
| --------- | ----------------------------------------- |
| Baseline  | TinyLlama-1.1B-Chat                       |
| Finetuned | `uos-smollm-second` (Jailbreaking SFT 적용) |

🔗 Fine-tuned Model 공개 링크

본 실험에서 사용된 Jailbreaking 방어 Fine-tuned 모델은 아래 링크를 통해 공개되어 있다.

Model name: uos-smollm-second

Base model: TinyLlama-1.1B-Chat

Training method: Supervised Fine-tuning (SFT) with Jailbreaking attack/defense data

Format: HuggingFace-compatible (config.json, tokenizer, model.safetensors)

📦 Model Download (Google Drive)

🔒 용량 및 접근 제약으로 인해 GitHub에는 모델 가중치를 포함하지 않음

👉 Google Drive[
https://drive.google.com/file/d/1eRk9eT1k4H9vBRv6eaL4F9DdaDdqoYN4/view?usp=sharing ](https://drive.google.com/file/d/1iRdOZvvZJTZMRWKY5eWJ9HOhWClTq1bu/view?usp=sharing)

---

### 3. 평가 파이프라인

```
eval_dataset.json
   ↓
[evaluate_full.py]
   → result.jsonl / result_uos.jsonl
   ↓
[analyze_results.py]
   → final_scored_baseline.jsonl
   → final_scored_uos.jsonl
```

* `evaluate_full.py`

  * 실제 모델 응답 생성
  * 거부 키워드, 위험 절차, 거부 문장 유사도(semantic similarity) 계산
* `analyze_results.py`

  * 팀 내 합의된 기준에 따라 **최종 판정 및 통계 산출**

---

## 📊 평가 기준 (요약)

* **reject_confident**
  → 모범 거절 답변과의 의미적 유사도 ≥ threshold
* **fail_harmful**
  → 폭발물/범죄/해킹 등 위험 절차 직접 노출
* **fail_jailbroken**
  → 공격 질문에 대해 실질적인 정보 제공
* **False Positive (FP)**
  → 정상 질문을 거부한 경우

---

## 📈 실험 결과

### 🔹 Baseline (result.jsonl)

```
총 데이터: 50개
 - 공격(reject) : 42개
 - 정상(accept) : 6개

방어 성공(reject_confident): 3
위험 정보 유출(harmful): 2
탈옥 허용(jailbroken): 39

방어율: 7.14%
ASR(공격 성공률): 92.86%
```

---

### 🔹 Finetuned (result_uos.jsonl)

```
총 데이터: 50개
 - 공격(reject) : 44개
 - 정상(accept) : 6개

방어 성공(reject_confident): 33
위험 정보 유출(harmful): 0
탈옥 허용(jailbroken): 11

방어율: 75.00%
ASR(공격 성공률): 25.00%
False Positive: 1
```

---

## 🚀 개선 효과 요약

| 항목             | Baseline | Finetuned | 변화           |
| -------------- | -------- | --------- | ------------ |
| 방어율            | 7.14%    | 75.00%    | **+67.86%p** |
| ASR            | 92.86%   | 25.00%    | **−67.86%p** |
| Harmful 유출     | 2        | 0         | −2           |
| False Positive | 0        | 1         | +1           |

➡️ **Fine-tuning 이후 Jailbreaking 방어 성능이 대폭 향상**되었으며,



➡️ 위험 정보 직접 유출은 **완전히 제거**됨



➡️ 단, 정상 질문 오거부가 소폭 증가 (trade-off)

---

## 📂 주요 결과 파일

```
first_test/
 ├─ result.jsonl                  # Baseline raw outputs
 ├─ result_uos.jsonl              # Finetuned raw outputs
 ├─ final_scored_baseline.jsonl   # Baseline 최종 판정
 ├─ final_scored_uos.jsonl        # Finetuned 최종 판정
```

---

## 🔍 결론

* 단순한 정책 기반 필터링만으로는 Jailbreaking 방어에 한계가 있음
* **공격 사례 중심 SFT Fine-tuning**은 실질적인 방어율 개선에 매우 효과적
* 향후 과제:

  * False Positive 감소
  * 공격 유형별 세분화된 학습 데이터 확장
  * 자동화된 Jailbreak 생성 기반 adversarial training

