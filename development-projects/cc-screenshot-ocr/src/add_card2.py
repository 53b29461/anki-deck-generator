#!/usr/bin/env python3
"""
問題2を手動で追加するスクリプト
"""

import sys
sys.path.append('/home/user/.pg/development-projects/cc-screenshot-ocr/src')

from manual_anki_cards import ManualAnkiCardGenerator

def add_card2():
    generator = ManualAnkiCardGenerator()
    
    # 既存のカード1を再追加
    generator.add_card(
        question_number=1,
        situation="Steve is a security practitioner assigned to come up with a protective measure for ensuring that cars don't collide with pedestrians.",
        question="What is probably the most effective type of control for this task?",
        choices=["Administrative", "Nuanced", "Physical", "Technical"],
        correct_answer="Physical",
        explanation="Physical controls, such as fences, walls and bollards, will be most likely to ensure cars cannot collide with pedestrians by creating actual barriers between cars and pedestrians."
    )
    
    # 問題2を追加
    generator.add_card(
        question_number=2,
        situation="Chad is a security practitioner tasked with ensuring that the information on the organization's public website is not changed by anyone outside the organization.",
        question="Which concept does this task demonstrate?",
        choices=["Availability", "Confidentiality", "Confirmation", "Integrity"],
        correct_answer="Integrity",
        explanation="Preventing unauthorized modification is the definition of integrity."
    )
    
    # 進捗保存
    generator.save_progress()
    
    # Ankiファイル生成
    generator.export_to_anki()
    
    print("問題2追加完了")
    return generator

if __name__ == "__main__":
    generator = add_card2()
    print(f"現在のカード数: {len(generator.cards)}")