#!/usr/bin/env python3
"""
品質分析ツール - 低品質カードの原因調査
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


def analyze_quality_issues():
    """
    品質が低いカードの詳細分析
    """
    project_dir = Path(__file__).parent.parent
    cards_file = project_dir / 'output' / 'anki' / 'cc_anki_improved.json'
    
    with open(cards_file, 'r', encoding='utf-8') as f:
        cards = json.load(f)
    
    # 品質別分類
    high_quality = [c for c in cards if c['quality_score'] >= 5]
    medium_quality = [c for c in cards if 3 <= c['quality_score'] < 5]
    low_quality = [c for c in cards if c['quality_score'] < 3]
    
    print("🔍 品質分析レポート")
    print("=" * 50)
    print(f"高品質カード: {len(high_quality)}枚")
    print(f"中品質カード: {len(medium_quality)}枚")
    print(f"低品質カード: {len(low_quality)}枚")
    
    print("\n📉 中・低品質カードの詳細分析:")
    
    problem_cards = medium_quality + low_quality
    
    for i, card in enumerate(problem_cards, 1):
        print(f"\n【問題カード {i}】")
        print(f"ファイル: {card['filename']}")
        print(f"品質スコア: {card['quality_score']}/6")
        print(f"問題文: {card['question'][:100]}...")
        print(f"選択肢A: {card['choice_a'][:50]}...")
        print(f"選択肢B: {card['choice_b'][:50]}...")
        print(f"選択肢C: {card['choice_c'][:50]}...")
        print(f"選択肢D: {card['choice_d'][:50]}...")
        print(f"正解: {card['correct_answer'][:50]}...")
        print(f"解説: {card['explanation'][:100]}...")
        
        # 問題点分析
        issues = []
        if not card['question'] or len(card['question']) <= 10:
            issues.append("問題文が短すぎる/空")
        if len([c for c in [card['choice_a'], card['choice_b'], card['choice_c'], card['choice_d']] if c]) < 2:
            issues.append("選択肢が不足")
        if not card['correct_answer']:
            issues.append("正解が空")
        if not card['explanation']:
            issues.append("解説が空")
        
        print(f"問題点: {', '.join(issues)}")
    
    return problem_cards


if __name__ == "__main__":
    analyze_quality_issues()