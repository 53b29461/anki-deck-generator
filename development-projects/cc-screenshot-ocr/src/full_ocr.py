#!/usr/bin/env python3
"""
CC練習問題スクリーンショット全ファイルOCR処理
"""

import os
import sys
from pathlib import Path
import pytesseract
from PIL import Image
import json
import re
from typing import Dict, List


def extract_question_data(text: str, filename: str) -> Dict:
    """
    OCRテキストから問題データを構造化抽出
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
    
    # 問題文を探す（"What"で始まる行、または"Which"で始まる行）
    question_lines = []
    choices = []
    explanation_lines = []
    
    in_explanation = False
    found_question = False
    
    for i, line in enumerate(lines):
        # 問題文の開始を検出
        if re.match(r'^(What|Which|How|Where|When|Why)', line):
            found_question = True
            question_lines = [line]
            # 次の行も問題文の一部か確認
            for j in range(i+1, min(i+3, len(lines))):
                next_line = lines[j]
                if not re.match(r'^[A-Z]', next_line) and not 'attempt taken' in next_line:
                    question_lines.append(next_line)
                else:
                    break
            break
    
    # 選択肢を探す（大文字で始まる行）
    choice_pattern = r'^([A-Z][A-Za-z\s]+)$'
    
    for line in lines:
        # "Explanation"の後は解説
        if line.lower().startswith('explanation'):
            in_explanation = True
            continue
        
        if in_explanation:
            if line and not line.startswith('Which') and not line.startswith('What'):
                explanation_lines.append(line)
        
        # 選択肢らしい行を検出
        if re.match(choice_pattern, line) and len(line) > 3 and len(line) < 100:
            # 明らかに選択肢でない行を除外
            if not any(exclude in line.lower() for exclude in ['progress', 'accuracy', 'answers', 'cyder', 'chess', 'usage']):
                choices.append(line)
    
    # 正解を探す（"Correct Answers"の近く）
    for i, line in enumerate(lines):
        if 'correct answers' in line.lower():
            # 次の行が正解の可能性
            if i+1 < len(lines):
                correct_candidate = lines[i+1]
                if len(correct_candidate) < 50:  # 短い行のみ
                    result['correct_answer'] = correct_candidate
    
    # "attempt taken"の情報
    for line in lines:
        if 'attempt taken' in line.lower():
            result['attempt_info'] = line
    
    # 結果を格納
    result['question'] = ' '.join(question_lines)
    result['choices'] = choices[:6]  # 最大6個の選択肢
    result['explanation'] = ' '.join(explanation_lines)
    
    # パース成功判定
    if result['question'] and len(result['choices']) >= 2:
        result['parsed'] = True
    
    return result


def process_all_screenshots(input_dir: str, output_dir: str):
    """
    全スクリーンショットをOCR処理
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 全PNG画像を取得
    image_files = sorted(list(input_path.glob('*.png')))
    
    print(f"処理対象ファイル: {len(image_files)}個")
    
    all_results = []
    parsed_count = 0
    
    for i, img_file in enumerate(image_files):
        print(f"処理中 [{i+1}/{len(image_files)}]: {img_file.name}")
        
        try:
            # 画像を開いてOCR
            image = Image.open(img_file)
            text = pytesseract.image_to_string(image)
            
            # 問題データを抽出
            question_data = extract_question_data(text, img_file.name)
            all_results.append(question_data)
            
            if question_data['parsed']:
                parsed_count += 1
                print(f"  ✓ 問題として解析成功")
            else:
                print(f"  - 構造化に失敗")
                
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            all_results.append({
                'filename': img_file.name,
                'error': str(e),
                'parsed': False
            })
    
    # JSON結果を保存
    with open(output_path / 'cc_questions_full.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # 構造化されたテキストを保存
    save_structured_questions(all_results, output_path)
    
    # サマリー表示
    print(f"\n処理完了サマリー:")
    print(f"総ファイル数: {len(image_files)}")
    print(f"問題として解析成功: {parsed_count}")
    print(f"成功率: {(parsed_count/len(image_files)*100):.1f}%")
    print(f"\n結果ファイル:")
    print(f"- {output_path}/cc_questions_full.json")
    print(f"- {output_path}/cc_questions_structured.txt")


def save_structured_questions(results: List[Dict], output_path: Path):
    """
    構造化されたテキストファイルを保存
    """
    with open(output_path / 'cc_questions_structured.txt', 'w', encoding='utf-8') as f:
        f.write("ISC2 Certificate in Cybersecurity (CC) 練習問題集\n")
        f.write("=" * 60 + "\n\n")
        
        question_num = 1
        for result in results:
            if result.get('parsed'):
                f.write(f"【問題 {question_num}】 {result['filename']}\n")
                f.write("-" * 40 + "\n")
                f.write(f"問題: {result['question']}\n\n")
                
                # 選択肢
                for i, choice in enumerate(result['choices'], 1):
                    f.write(f"{i}. {choice}\n")
                
                if result.get('correct_answer'):
                    f.write(f"\n正解: {result['correct_answer']}\n")
                
                if result.get('explanation'):
                    f.write(f"解説: {result['explanation']}\n")
                
                if result.get('attempt_info'):
                    f.write(f"情報: {result['attempt_info']}\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
                question_num += 1


def main():
    project_dir = Path(__file__).parent.parent
    input_dir = project_dir / 'input' / 'screenshots'
    output_dir = project_dir / 'output'
    
    if not input_dir.exists():
        print(f"入力ディレクトリが見つかりません: {input_dir}")
        sys.exit(1)
    
    print("ISC2 CC練習問題スクリーンショット 全ファイルOCR処理を開始...")
    process_all_screenshots(str(input_dir), str(output_dir))


if __name__ == "__main__":
    main()