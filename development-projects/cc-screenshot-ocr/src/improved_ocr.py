#!/usr/bin/env python3
"""
改良版OCR処理（100%成功率を目指す）
"""

import os
import sys
from pathlib import Path
import pytesseract
from PIL import Image
import json
import re
from typing import Dict, List


def extract_question_data_improved(text: str, filename: str) -> Dict:
    """
    改良版の問題データ抽出（より柔軟）
    """
    result = {
        'filename': filename,
        'raw_text': text,
        'question': '',
        'choices': [],
        'correct_answer': '',
        'explanation': '',
        'attempt_info': '',
        'parsed': False
    }
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 改良された問題文検出
    question_candidates = []
    for i, line in enumerate(lines):
        # 問題文の特徴を広く捉える
        if any(starter in line for starter in ['What', 'Which', 'How', 'Where', 'When', 'Why', 'Of the following']):
            # 問題文として適切な長さかチェック
            if 10 <= len(line) <= 200:
                question_candidates.append(line)
        
        # "?"で終わる行も問題文候補
        if line.endswith('?') and len(line) > 15:
            question_candidates.append(line)
    
    # 最も適切な問題文を選択
    if question_candidates:
        # 最も長い（詳細な）問題文を選択
        result['question'] = max(question_candidates, key=len)
    
    # 改良された選択肢検出
    choice_candidates = []
    
    for line in lines:
        # 様々な選択肢パターンを検出
        patterns = [
            r'^[A-D]\)',          # A), B), C), D)
            r'^[A-D]\.',          # A. B. C. D.
            r'^[A-D][\s:]',       # A: B: C: D:
            r'^\d+\)',            # 1), 2), 3), 4)
            r'^\d+\.',            # 1. 2. 3. 4.
        ]
        
        choice_match = False
        for pattern in patterns:
            if re.match(pattern, line):
                choice_match = True
                break
        
        # パターンマッチしなくても、選択肢らしい行を検出
        if not choice_match:
            # 適度な長さで、明らかに選択肢でない文字列を除外
            if (5 <= len(line) <= 100 and 
                not any(exclude in line.lower() for exclude in [
                    'progress', 'accuracy', 'answers', 'cyder', 'chess', 'usage', 
                    'isc2', 'obrizum', 'google', 'anki', 'attempt taken',
                    'correct', 'score', 'seconds', 'explanation'
                ]) and
                not line.startswith('http') and
                not line.startswith('@') and
                not '?' in line):
                
                # 大文字で始まる、または技術用語らしい行
                if (line[0].isupper() or 
                    any(tech in line.lower() for tech in [
                        'access', 'control', 'security', 'data', 'system', 
                        'network', 'password', 'encryption', 'firewall',
                        'malware', 'virus', 'threat', 'risk', 'asset',
                        'policy', 'procedure', 'authentication', 'authorization'
                    ])):
                    choice_candidates.append(line)
    
    # 重複除去と選択肢として適切なものを選択
    seen = set()
    unique_choices = []
    for choice in choice_candidates:
        # 類似した選択肢を除外
        choice_clean = re.sub(r'^[A-D\d\)\.\:\s]+', '', choice).strip()
        if choice_clean and choice_clean not in seen and len(choice_clean) > 2:
            seen.add(choice_clean)
            unique_choices.append(choice)
    
    result['choices'] = unique_choices[:6]  # 最大6個
    
    # 改良された正解検出
    for i, line in enumerate(lines):
        if 'correct answer' in line.lower():
            # 周辺の行から正解を探す
            for j in range(max(0, i-2), min(len(lines), i+4)):
                candidate = lines[j].strip()
                if candidate and len(candidate) < 50 and candidate not in ['Explanation', 'Correct Answers']:
                    result['correct_answer'] = candidate
                    break
    
    # 解説検出
    explanation_lines = []
    in_explanation = False
    
    for line in lines:
        if line.lower().startswith('explanation'):
            in_explanation = True
            continue
        
        if in_explanation:
            # 解説らしい行のみ追加
            if (len(line) > 10 and 
                not line.startswith('Which') and 
                not line.startswith('What') and
                not line.startswith('How')):
                explanation_lines.append(line)
            
            # 次の問題が始まったら解説終了
            if any(starter in line for starter in ['What', 'Which', 'How']):
                break
    
    result['explanation'] = ' '.join(explanation_lines[:3])  # 最初の3行のみ
    
    # attempt taken情報
    for line in lines:
        if 'attempt taken' in line.lower():
            result['attempt_info'] = line
            break
    
    # パース成功判定（より寛容に）
    if result['question'] and len(result['choices']) >= 1:
        result['parsed'] = True
    
    return result


def reprocess_failed_files():
    """
    失敗したファイルのみ再処理
    """
    project_dir = Path(__file__).parent.parent
    input_dir = project_dir / 'input' / 'screenshots'
    output_dir = project_dir / 'output'
    results_file = output_dir / 'cc_questions_full.json'
    
    # 既存の結果を読み込み
    with open(results_file, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
    
    # 失敗したファイル名を取得
    failed_filenames = [r['filename'] for r in existing_results if not r.get('parsed', False)]
    
    print(f"再処理対象: {len(failed_filenames)}個のファイル")
    
    # 失敗したファイルのみ再処理
    improved_results = []
    success_count = 0
    
    for filename in failed_filenames:
        print(f"再処理中: {filename}")
        
        try:
            image_path = input_dir / filename
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            # 改良版アルゴリズムで再処理
            question_data = extract_question_data_improved(text, filename)
            improved_results.append(question_data)
            
            if question_data['parsed']:
                success_count += 1
                print(f"  ✓ 再処理成功")
            else:
                print(f"  - 再処理失敗")
                
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            improved_results.append({
                'filename': filename,
                'error': str(e),
                'parsed': False
            })
    
    # 既存の成功結果と改良結果をマージ
    final_results = []
    
    for existing in existing_results:
        if existing.get('parsed', False):
            # 成功していたものはそのまま
            final_results.append(existing)
        else:
            # 失敗していたものは改良版で置き換え
            improved = next((r for r in improved_results if r['filename'] == existing['filename']), existing)
            final_results.append(improved)
    
    # 結果を保存
    with open(output_dir / 'cc_questions_improved.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    # 構造化テキストも更新
    save_structured_questions_improved(final_results, output_dir)
    
    # 結果サマリー
    total_parsed = sum(1 for r in final_results if r.get('parsed', False))
    
    print(f"\n改良結果サマリー:")
    print(f"総ファイル数: {len(final_results)}")
    print(f"構造化成功: {total_parsed}")
    print(f"改良前失敗→成功: {success_count}")
    print(f"最終成功率: {(total_parsed/len(final_results)*100):.1f}%")
    
    return final_results


def save_structured_questions_improved(results: List[Dict], output_path: Path):
    """
    改良版構造化テキストファイルを保存
    """
    with open(output_path / 'cc_questions_improved.txt', 'w', encoding='utf-8') as f:
        f.write("ISC2 Certificate in Cybersecurity (CC) 練習問題集【改良版】\n")
        f.write("=" * 70 + "\n\n")
        
        question_num = 1
        for result in results:
            if result.get('parsed'):
                f.write(f"【問題 {question_num}】 {result['filename']}\n")
                f.write("-" * 50 + "\n")
                f.write(f"問題: {result['question']}\n\n")
                
                # 選択肢
                if result.get('choices'):
                    f.write("選択肢:\n")
                    for i, choice in enumerate(result['choices'], 1):
                        f.write(f"  {i}. {choice}\n")
                    f.write("\n")
                
                if result.get('correct_answer'):
                    f.write(f"正解: {result['correct_answer']}\n")
                
                if result.get('explanation'):
                    f.write(f"解説: {result['explanation']}\n")
                
                if result.get('attempt_info'):
                    f.write(f"情報: {result['attempt_info']}\n")
                
                f.write("\n" + "=" * 70 + "\n\n")
                question_num += 1


def main():
    reprocess_failed_files()


if __name__ == "__main__":
    main()