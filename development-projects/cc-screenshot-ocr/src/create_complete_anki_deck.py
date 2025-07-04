#!/usr/bin/env python3
"""
選択肢を含む完全なCC練習問題Ankiデッキ生成
"""

import sys
sys.path.append('/home/user/.pg/development-projects/cc-screenshot-ocr/src')

from batch_manual_processor import create_all_cards
import csv
from datetime import datetime

def create_complete_anki_deck():
    """
    選択肢を含む完全なAnkiデッキを生成
    """
    # 元のデータを取得
    generator = create_all_cards()
    
    # 選択肢込みの新しいTSVファイルを作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = "/home/user/.pg/development-projects/cc-screenshot-ocr/output/manual/"
    filename = f"{output_dir}/cc_complete_with_choices_{timestamp}.tsv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        
        # ヘッダー
        writer.writerow(['Front', 'Back', 'Tags'])
        
        # 各カードデータを選択肢込みで生成
        for card in generator.cards:
            raw_data = card['raw_data']
            
            # 状況説明部分
            situation_part = f"{raw_data['situation']}\n\n" if raw_data['situation'] else ""
            
            # 選択肢部分を作成
            choices_text = ""
            for i, choice in enumerate(raw_data['choices'], 1):
                choices_text += f"{chr(64+i)}. {choice}\n"
            
            # 完全なカード内容
            front_content = f"Q{card['question_number']}: {situation_part}{raw_data['question']}\n\n{choices_text}\n正解: {{c1::{raw_data['correct_answer']}}}\n\n解説: {raw_data['explanation']}"
            
            writer.writerow([
                front_content,
                '',  # Cloze形式では空白
                'cc-practice security-plus choices-included'
            ])
    
    print(f"選択肢込み完全Ankiデッキ生成完了: {filename}")
    print(f"総カード数: {len(generator.cards)}")
    
    return filename

if __name__ == "__main__":
    filename = create_complete_anki_deck()
    print(f"使用ファイル: {filename}")