#!/usr/bin/env python3
"""
CC練習問題 → Ankiデッキ変換（クローズ形式）
Geminiの提案を基にした効果的な学習カード生成
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class CCAnkiGenerator:
    """
    CC練習問題をAnkiのクローズ形式カードに変換
    """
    
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 統計
        self.stats = {
            'total_questions': 0,
            'converted_cards': 0,
            'skipped_incomplete': 0
        }
    
    def clean_text(self, text: str) -> str:
        """
        テキストのクリーニング
        """
        if not text:
            return ""
        
        # HTMLタグ除去
        text = re.sub(r'<[^>]+>', '', text)
        
        # 余分な空白・改行を整理
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Ankiの特殊文字をエスケープ
        text = text.replace('"', '""')  # CSVエスケープ
        
        return text
    
    def extract_correct_choice(self, question_data: Dict) -> Tuple[str, str]:
        """
        正解の選択肢を抽出・特定
        """
        choices = question_data.get('choices', [])
        correct_answer = question_data.get('correct_answer', '')
        
        if not choices:
            return "", ""
        
        # 正解テキストと選択肢を照合
        correct_choice = ""
        correct_letter = ""
        
        # 方法1: 正解テキストが選択肢に含まれているかチェック
        if correct_answer:
            for i, choice in enumerate(choices):
                choice_clean = self.clean_text(choice)
                correct_clean = self.clean_text(correct_answer)
                
                if correct_clean in choice_clean or choice_clean in correct_clean:
                    correct_choice = choice_clean
                    correct_letter = chr(65 + i)  # A, B, C, D
                    break
        
        # 方法2: 最初の選択肢を正解と仮定（フォールバック）
        if not correct_choice and choices:
            correct_choice = self.clean_text(choices[0])
            correct_letter = "A"
        
        return correct_choice, correct_letter
    
    def format_choices_for_display(self, choices: List[str]) -> str:
        """
        選択肢を表示用フォーマットに変換
        """
        if not choices:
            return ""
        
        formatted_choices = []
        for i, choice in enumerate(choices[:4]):  # 最大4個
            letter = chr(65 + i)  # A, B, C, D
            clean_choice = self.clean_text(choice)
            formatted_choices.append(f"{letter}: {clean_choice}")
        
        return "<br>".join(formatted_choices)
    
    def create_anki_card(self, question_data: Dict, card_id: int) -> Dict:
        """
        単一の問題からAnkiカードを生成
        """
        # 基本情報の抽出
        question_text = self.clean_text(question_data.get('question', ''))
        choices = question_data.get('choices', [])
        explanation = self.clean_text(question_data.get('explanation', ''))
        filename = question_data.get('filename', '')
        
        # 正解の選択肢を特定
        correct_choice, correct_letter = self.extract_correct_choice(question_data)
        
        # 選択肢の表示フォーマット
        choices_display = self.format_choices_for_display(choices)
        
        # クローズ形式のテキスト生成
        cloze_text = f"{{{{c1::{correct_choice}}}}}"
        
        # Ankiカード用データ構造
        anki_card = {
            'card_id': card_id,
            'question': question_text,
            'choices_a': choices[0] if len(choices) > 0 else "",
            'choices_b': choices[1] if len(choices) > 1 else "",
            'choices_c': choices[2] if len(choices) > 2 else "",
            'choices_d': choices[3] if len(choices) > 3 else "",
            'choices_display': choices_display,
            'correct_answer': correct_choice,
            'correct_letter': correct_letter,
            'explanation': explanation,
            'cloze_text': cloze_text,
            'filename': filename,
            'tags': 'CC ISC2 Cybersecurity'
        }
        
        return anki_card
    
    def generate_tsv_format(self, cards: List[Dict]) -> str:
        """
        AnkiインポートTSV形式を生成
        """
        headers = [
            "問題文", "選択肢A", "選択肢B", "選択肢C", "選択肢D",
            "正解", "解説", "Text", "タグ", "ファイル名"
        ]
        
        lines = ["\t".join(headers)]
        
        for card in cards:
            row = [
                card['question'],
                self.clean_text(card['choices_a']),
                self.clean_text(card['choices_b']),
                self.clean_text(card['choices_c']),
                self.clean_text(card['choices_d']),
                card['correct_answer'],
                card['explanation'],
                card['cloze_text'],
                card['tags'],
                card['filename']
            ]
            lines.append("\t".join(row))
        
        return "\n".join(lines)
    
    def generate_anki_template(self) -> str:
        """
        Ankiノートタイプ設定用テンプレート生成
        """
        template = """
# CC練習問題用Ankiノートタイプ設定

## フィールド構成:
1. 問題文
2. 選択肢A
3. 選択肢B
4. 選択肢C
5. 選択肢D
6. 正解
7. 解説
8. Text (クローズ用)
9. タグ
10. ファイル名

## 表面テンプレート:
```html
<div style="text-align: left; font-size: 16px; line-height: 1.5;">
  <b>【CC練習問題】</b><br><br>
  {{問題文}}
</div>

<hr style="margin: 20px 0;">

<div style="text-align: left; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
  <b>選択肢:</b><br><br>
  <div style="margin: 8px 0;"><b>A:</b> {{選択肢A}}</div>
  <div style="margin: 8px 0;"><b>B:</b> {{選択肢B}}</div>
  <div style="margin: 8px 0;"><b>C:</b> {{選択肢C}}</div>
  <div style="margin: 8px 0;"><b>D:</b> {{選択肢D}}</div>
</div>

<hr style="margin: 20px 0;">

<div style="text-align: center; font-size: 18px;">
  <b>正解:</b> {{cloze:Text}}
</div>
```

## 裏面テンプレート:
```html
{{FrontSide}}

<hr style="margin: 20px 0; border-color: #007bff;">

<div style="text-align: left; background-color: #e8f4fd; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;">
  <b style="color: #007bff;">【正解】</b><br>
  <b style="color: #28a745; font-size: 18px;">{{正解}}</b>
</div>

{{#解説}}
<div style="text-align: left; background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin-top: 15px;">
  <b style="color: #856404;">【解説】</b><br>
  {{解説}}
</div>
{{/解説}}

<div style="text-align: right; font-size: 12px; color: #6c757d; margin-top: 15px;">
  {{ファイル名}}
</div>
```

## CSS (スタイル):
```css
.card {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.cloze {
  font-weight: bold;
  color: #dc3545;
  background-color: #f8d7da;
  padding: 2px 6px;
  border-radius: 3px;
}
```
"""
        return template
    
    def process_all_questions(self):
        """
        全問題を処理してAnkiデッキを生成
        """
        print("CC練習問題 → Ankiデッキ変換を開始...")
        
        # JSONファイルを読み込み
        with open(self.input_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        self.stats['total_questions'] = len(questions_data)
        print(f"読み込み完了: {self.stats['total_questions']}問")
        
        # Ankiカードを生成
        anki_cards = []
        
        for i, question_data in enumerate(questions_data):
            if not question_data.get('parsed', False):
                self.stats['skipped_incomplete'] += 1
                continue
            
            try:
                card = self.create_anki_card(question_data, i + 1)
                anki_cards.append(card)
                self.stats['converted_cards'] += 1
                
                if (i + 1) % 10 == 0:
                    print(f"処理済み: {i + 1}/{self.stats['total_questions']}")
                    
            except Exception as e:
                print(f"カード生成エラー [{question_data.get('filename', 'Unknown')}]: {e}")
                self.stats['skipped_incomplete'] += 1
        
        # TSVファイルを生成
        tsv_content = self.generate_tsv_format(anki_cards)
        tsv_file = self.output_dir / 'cc_questions_anki.tsv'
        
        with open(tsv_file, 'w', encoding='utf-8') as f:
            f.write(tsv_content)
        
        # テンプレート設定ファイルを生成
        template_content = self.generate_anki_template()
        template_file = self.output_dir / 'anki_template_setup.md'
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # 詳細JSONも保存
        json_file = self.output_dir / 'cc_anki_cards.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(anki_cards, f, ensure_ascii=False, indent=2)
        
        # 結果サマリー
        self.print_summary(tsv_file, template_file, json_file)
    
    def print_summary(self, tsv_file: Path, template_file: Path, json_file: Path):
        """
        処理結果サマリーを表示
        """
        print("\n🎉 Ankiデッキ生成完了!")
        print("=" * 50)
        print(f"総問題数: {self.stats['total_questions']}")
        print(f"変換成功: {self.stats['converted_cards']}")
        print(f"スキップ: {self.stats['skipped_incomplete']}")
        print(f"成功率: {(self.stats['converted_cards']/self.stats['total_questions']*100):.1f}%")
        
        print("\n📁 生成ファイル:")
        print(f"1. {tsv_file} (Ankiインポート用)")
        print(f"2. {template_file} (ノートタイプ設定手順)")
        print(f"3. {json_file} (詳細データ)")
        
        print("\n📚 Ankiでの使用手順:")
        print("1. anki_template_setup.md の手順でノートタイプを設定")
        print("2. cc_questions_anki.tsv をAnkiにインポート")
        print("3. フィールド区切り文字をタブに設定")
        print("4. 効果的なCC学習を開始！")


def main():
    """
    メイン実行関数
    """
    project_dir = Path(__file__).parent.parent
    input_file = project_dir / 'output' / 'cc_questions_final.json'
    output_dir = project_dir / 'output' / 'anki'
    
    if not input_file.exists():
        print(f"入力ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    generator = CCAnkiGenerator(str(input_file), str(output_dir))
    generator.process_all_questions()


if __name__ == "__main__":
    main()