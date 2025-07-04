#!/usr/bin/env python3
"""
CC練習問題 手動Ankiカード作成システム
各スクリーンショットを1つずつ手動で精密分析し、高品質なAnkiカードを生成する
"""

import os
import csv
from datetime import datetime

class ManualAnkiCardGenerator:
    def __init__(self):
        self.cards = []
        self.output_dir = "/home/user/.pg/development-projects/cc-screenshot-ocr/output/manual/"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def add_card(self, question_number, situation, question, choices, correct_answer, explanation):
        """
        手動でAnkiカードを追加
        """
        # Cloze形式での質問文作成
        cloze_question = f"{situation}\n\n{question}"
        
        # 選択肢をフォーマット
        choices_text = ""
        for i, choice in enumerate(choices, 1):
            marker = "✓" if choice == correct_answer else "◯"
            choices_text += f"{marker} {choice}\n"
        
        # Ankiカード作成
        card = {
            'question_number': question_number,
            'front': f"Q{question_number}: {cloze_question}\n\n{choices_text}",
            'back': f"正解: {correct_answer}\n\n解説: {explanation}",
            'cloze': f"Q{question_number}: {situation}\n\n{question}\n\n正解: {{c1::{correct_answer}}}\n\n解説: {explanation}",
            'raw_data': {
                'situation': situation,
                'question': question,
                'choices': choices,
                'correct_answer': correct_answer,
                'explanation': explanation
            }
        }
        
        self.cards.append(card)
        print(f"カード{question_number}追加完了")
        
    def export_to_anki(self):
        """
        TSV形式でAnkiエクスポート
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.output_dir}/cc_manual_anki_{timestamp}.tsv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            
            # ヘッダー
            writer.writerow(['Front', 'Back', 'Tags'])
            
            # カードデータ
            for card in self.cards:
                writer.writerow([
                    card['cloze'],
                    '',  # Cloze形式では空白
                    'cc-practice security-plus'
                ])
        
        print(f"Ankiファイル生成完了: {filename}")
        print(f"総カード数: {len(self.cards)}")
        
        return filename
    
    def save_progress(self):
        """
        進捗を保存
        """
        progress_file = f"{self.output_dir}/progress.txt"
        with open(progress_file, 'w', encoding='utf-8') as f:
            f.write(f"作成日時: {datetime.now()}\n")
            f.write(f"処理済みカード数: {len(self.cards)}\n")
            f.write(f"最新カード: Q{len(self.cards)}\n")
            
        print(f"進捗保存完了: {progress_file}")

# 使用例
if __name__ == "__main__":
    generator = ManualAnkiCardGenerator()
    
    # 問題1を追加
    generator.add_card(
        question_number=1,
        situation="Steve is a security practitioner assigned to come up with a protective measure for ensuring that cars don't collide with pedestrians.",
        question="What is probably the most effective type of control for this task?",
        choices=["Administrative", "Nuanced", "Physical", "Technical"],
        correct_answer="Physical",
        explanation="Physical controls, such as fences, walls and bollards, will be most likely to ensure cars cannot collide with pedestrians by creating actual barriers between cars and pedestrians."
    )
    
    # 進捗保存
    generator.save_progress()
    
    print("手動カード作成システム準備完了")
    print(f"現在のカード数: {len(generator.cards)}")