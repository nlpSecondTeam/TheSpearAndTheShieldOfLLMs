# 🛡️ The Spear and The Shield of LLMs: Small LLM Jailbreaking Defense

> **"소형 LLM(TinyLlama-1.1B)의 탈옥(Jailbreaking) 방어를 위한 SFT 실험 및 한계 극복 연구"**

본 프로젝트는 1B급 소형 언어 모델의 보안성을 강화하기 위해 다양한 Fine-tuning 전략을 실험하고, **'언어 장벽(Language Barrier)'**과 **'데이터 비율(Data Ratio)'**이 모델의 방어 성능과 유용성(Utility)에 미치는 영향을 분석했습니다.


---

## 🎯 Project Overview
기존 소형 LLM은 리소스의 한계로 인해 적대적 공격(Adversarial Attack)에 취약합니다. 본 연구는 Supervised Fine-tuning (SFT)을 통해 방어 기제를 주입하면서도, 소형 모델이 겪는 '앵무새 현상(Parrot Mode)'과 '지능 붕괴(Model Collapse)' 문제를 해결하는 과정을 담고 있습니다.

### 🧪 Key Experiments
1.  **Phase 1 (The Korean Barrier):** 한국어 보안 데이터 학습 시 발생하는 언어 붕괴 및 과잉 방어(FP) 현상 분석
2.  **Phase 2 (Pivot to Native):** 모델의 모국어(영어)로 전환하여 용량 한계(Capacity Overload) 극복
3.  **Phase 3 (The Ratio Experiment):** 데이터 불균형(Imbalanced) vs 균형(Balanced) 학습에 따른 성능 비교

---

## 📊 Experimental Results (Final)

우리는 최종적으로 Native Language(영어) 기반의 불균형 데이터(V2)가 가장 효율적임을 입증했습니다.

| Model | Type | Defense Rate (↑) | False Positive (↓) | Harmful Leak (↓) |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | TinyLlama Original | 31.1% | 0 | 2 (Dangerous) |
| **V2 (Imbalanced)** | **Attack-Heavy (7:1)** | **91.1% (Best)** | **0** | **0** |
| **V3 (Balanced)** | Balanced (1:1) | 88.9% | 0 | 0 |

> **💡 Key Finding:**
> 소형 모델 튜닝의 핵심은 '데이터 비율'보다 '베이스 모델의 언어 이해도'입니다. 언어 장벽을 제거(영어 전환)하자, 소량의 공격 데이터(V2)만으로도 유용성 훼손 없이 높은 보안성을 달성했습니다.

---

## 📝 Detailed Analysis Phases

### Phase 1. 초기 시도와 한계 (The Korean Barrier)
* **실험:** 한국어 공격/방어 데이터로 SFT 진행.
* **결과:** 방어율은 높았으나 심각한 부작용 발생.
    * **언어 붕괴:** "안심. 위헤서 해결하기 어렵습니다"와 같은 비문 생성.
    * **앵무새 현상 (Parrot Mode):** 모든 질문에 똑같은 거절 멘트만 반복.
    * **원인:** 1B 모델이 새로운 언어(한국어)와 보안 규칙을 동시에 배우려다 **용량 초과(Capacity Overload)** 발생.

### Phase 2. 전략 수정 (Pivot to Native Language)
* **가설:** "모델이 이미 잘하는 영어(Native Language)로 가르치면, 뇌 용량을 온전히 보안 규칙 학습에만 쓸 수 있을 것이다.
* **수행:** 모든 데이터셋(공격/정상)을 영어로 교체 및 재학습.

### Phase 3. 데이터 비율 실험 (The Ratio Experiment)
* **목표:** 과잉 방어(False Positive)를 줄이기 위한 최적의 데이터 비율 탐색.
    * **V2 (Imbalanced):** 공격 위주 학습 (공격 200 : 정상 30)
    * **V3 (Balanced):** 1:1 균형 학습 (공격 200 : 정상 200)
* **결과 (반전):**
    * **V2 (91.1%)**가 V3 (88.9%)보다 방어율이 높았으며, FP는 둘 다 0이었습니다.
    * 영어 베이스 모델은 기초 지능이 탄탄하여, 불균형 데이터에서도 정상 대화 능력을 잃지 않았습니다. 오히려 V3는 안전 데이터 비중이 희석되어 방어율이 소폭 하락했습니다.

---

## 🚀 Usage

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Data Generation

영어 정밀 평가를 위한 데이터셋(`eval_dataset_eng.json`)을 생성합니다.

```bash
python make_eval_dataset_eng_final.py
```

### 3. Training (SFT)

두 가지 시나리오(V2: 불균형, V3: 균형)에 대해 모델을 학습합니다.

```bash
# V2 (Imbalanced) 학습 - 공격 데이터 위주
python train.py --dataset train_eng_v2.jsonl --model_name uos-eng-v2

# V3 (Balanced) 학습 - 공격/정상 1:1 비율
python train.py --dataset train_eng_v3.jsonl --model_name uos-eng-v3
```

### 4. Evaluation & Analysis

학습된 모델과 Baseline을 통합 평가하고, 최종 비교 리포트를 출력합니다.

```bash
# 통합 정밀 평가 (V1 Baseline, V2, V3 일괄 평가)
python evaluate_all_phases.py

# 최종 성적표(Table) 출력
python analyze_final_report.py
```

---

## 📂 Repository Structure

| File                              | Description                                                                 |
| :-------------------------------- | :-------------------------------------------------------------------------- |
| `train.py`                        | LoRA 및 PEFT를 활용한 SFT 학습 메인 스크립트                               |
| `evaluate_all_phases.py`         | Baseline, V2, V3 모델을 순차적으로 로드하여 방어율·유해성·유사도를 측정    |
| `analyze_final_report.py`        | 평가 결과(JSONL)를 분석하여 최종 비교 테이블을 생성하는 스크립트           |
| `make_eval_dataset_eng_final.py` | 영어 정밀 평가 데이터셋(`eval_dataset_eng.json`) 생성 스크립트              |
| `data/`                           | 학습(`train_eng_*.jsonl`) 및 평가용 데이터셋 폴더                            |
