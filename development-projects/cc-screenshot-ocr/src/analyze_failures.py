#!/usr/bin/env python3
"""
構造化に失敗したファイルの分析
"""

import json
import sys
from pathlib import Path
import pytesseract
from PIL import Image


def analyze_failed_files():
    """
    失敗したファイルを詳細分析
    """
    project_dir = Path(__file__).parent.parent
    results_file = project_dir / 'output' / 'cc_questions_full.json'
    
    # 結果ファイルを読み込み
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # 失敗したファイルを抽出
    failed_files = [r for r in results if not r.get('parsed', False)]
    
    print(f"構造化に失敗したファイル: {len(failed_files)}個")
    print("=" * 50)
    
    for i, failed in enumerate(failed_files):
        print(f"\n【失敗 {i+1}】 {failed['filename']}")
        print("-" * 30)
        
        # 生のテキストを表示（最初の500文字）
        raw_text = failed.get('raw_text', '')
        print(f"抽出テキスト（最初500文字）:")
        print(f"{raw_text[:500]}...")
        
        # 問題らしい部分があるかチェック
        has_question = any(word in raw_text.lower() for word in ['what', 'which', 'how', 'where', 'when', 'why'])
        has_choices = len([line for line in raw_text.split('\n') if len(line.strip()) > 5 and len(line.strip()) < 100]) >= 3
        
        print(f"問題文あり: {has_question}")
        print(f"選択肢候補あり: {has_choices}")
        
        if i >= 4:  # 最初の5個だけ詳細表示
            break
    
    return failed_files


if __name__ == "__main__":
    analyze_failed_files()