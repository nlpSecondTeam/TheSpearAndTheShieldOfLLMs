import json
import os

FILES = [
    ("Baseline (V1)", "result_eng_v1_baseline.jsonl"),
    ("Imbalanced (V2)", "result_eng_v2_imbalanced.jsonl"),
    ("Balanced (V3)", "result_eng_v3_balanced.jsonl")
]

def analyze_file(name, filepath):
    if not os.path.exists(filepath):
        return [name, "N/A", "N/A", "N/A", "N/A"]
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
        
    total_attacks = sum(1 for x in data if x['label'] == 'reject')
    total_normals = sum(1 for x in data if x['label'] == 'accept')
    
    defense_success = sum(1 for x in data if x['label'] == 'reject' and x['decision'] == 'reject_confident')
    harmful_leak = sum(1 for x in data if x.get('fail_code') == 'fail_harmful_steps')
    
    # FP: 정상 질문인데 거절함
    fp_count = sum(1 for x in data if x['label'] == 'accept' and x['decision'] == 'fp_normal')
    
    def_rate = (defense_success / total_attacks * 100) if total_attacks > 0 else 0
    
    return [name, f"{def_rate:.1f}%", harmful_leak, fp_count, total_normals]

def main():
    try:
        from tabulate import tabulate
    except ImportError:
        print("⚠️ tabulate 모듈이 없습니다. 간단한 표로 출력합니다.")
        print("\n" + "="*60)
        print("📊 Final Comparison Report")
        print("="*60)
        print(f"{'Model':<20} | {'Defense Rate':<15} | {'Harmful Leak':<15} | {'False Positive':<15} | {'Total Normal'}")
        print("-" * 60)
        for name, filepath in FILES:
            row = analyze_file(name, filepath)
            print(f"{row[0]:<20} | {row[1]:<15} | {row[2]:<15} | {row[3]:<15} | {row[4]}")
        print("="*60)
        print("* Defense Rate: 공격 방어율 (높을수록 좋음)")
        print("* False Positive: 정상 질문 오탐 (낮을수록 좋음)")
        return
    
    table = []
    headers = ["Model", "Defense Rate (↑)", "Harmful Leak (↓)", "False Positive (↓)", "Total Normal"]
    
    for name, filepath in FILES:
        row = analyze_file(name, filepath)
        table.append(row)
        
    print("\n" + "="*60)
    print("📊 Final Comparison Report")
    print("="*60)
    print(tabulate(table, headers=headers, tablefmt="github"))
    print("-" * 60)
    print("* Defense Rate: 공격 방어율 (높을수록 좋음)")
    print("* False Positive: 정상 질문 오탐 (낮을수록 좋음)")
    print("="*60)

if __name__ == "__main__":
    main()

