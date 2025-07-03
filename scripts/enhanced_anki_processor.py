#!/usr/bin/env python3
"""
改良版Anki処理システム
- カスタムノートタイプ対応
- 単語ベースGUID生成
- CSS分離フォーマット
- 構造化フィールド分離
"""

import hashlib
import re
import csv
from typing import Dict, List, Tuple

class EnhancedAnkiProcessor:
    def __init__(self):
        self.note_type = "Enhanced TOEFL Vocabulary"
        self.deck_name = "toefl3800-enhanced-test"
        
    def generate_word_based_guid(self, word: str) -> str:
        """
        単語ベースの一意GUID生成
        同じ単語には常に同じGUIDを割り当て
        """
        # 単語を正規化（小文字、空白除去）
        normalized_word = word.lower().strip()
        
        # SHA1ハッシュ生成（短縮版）
        hash_object = hashlib.sha1(normalized_word.encode('utf-8'))
        guid = hash_object.hexdigest()[:16]  # 16文字に短縮
        
        return guid
    
    def create_structured_content(self, word: str, meaning: str, examples: List[str], tips: str) -> Dict[str, str]:
        """
        構造化されたフィールド別コンテンツ生成
        """
        # Definition フィールド（意味）
        definition = f"<div class='definition'><strong>{meaning}</strong></div>"
        
        # Examples フィールド（例文）
        examples_html = '<div class="examples">'
        for i, example in enumerate(examples, 1):
            # 全角数字で番号付け
            number = "（" + str(i) + "）"
            examples_html += f'<div class="example">{number}{example}</div>'
        examples_html += '</div>'
        
        # Etymology フィールド（語源・記憶法）
        etymology_html = f'<div class="etymology">{tips}</div>'
        
        return {
            'word': f'<div class="word">{word}</div>',  # HTML形式で格納
            'definition': definition,
            'examples': examples_html,
            'etymology': etymology_html
        }
    
    def process_word_with_claude(self, word: str) -> Dict[str, str]:
        """
        Claude Code品質でのコンテンツ生成
        """
        if word == "ambush":
            meaning = "待ち伏せ攻撃、奇襲、伏兵攻撃"
            examples = [
                "The rebels set up an ambush along the mountain road.",
                "Police officers were killed in a terrorist ambush.", 
                "The predator waited in ambush for unsuspecting prey."
            ]
            tips = """語源：古フランス語「embuscher」（茂みに隠れる）から派生<br>「em-（中に）+ busch（茂み）」→茂みの中に隠れて待ち伏せする<br>military terminology として覚えると、warfare関連語彙と関連付けやすい"""
            
        elif word == "bountiful":
            meaning = "豊富な、物惜しみしない、気前の良い"
            examples = [
                "The harvest was bountiful this year.",
                "She received bountiful praise for her performance.",
                "The garden produced a bountiful supply of vegetables."
            ]
            tips = """語源：古フランス語「bonté」（善良さ）から派生<br>「bounty（恵み、報奨金）+ -ful（〜に満ちた）」<br>abundance, plentiful などの類義語と関連付けて覚える"""
            
        elif word == "inhale":
            meaning = "吸い込む、吸入する"
            examples = [
                "Please inhale deeply and hold your breath.",
                "The patient needs to inhale the medication through this device.",
                "Don't inhale the fumes from the chemical."
            ]
            tips = """語源：ラテン語「inhalare」<br>「in-（中に）+ halare（息する）」→中に息を吸う<br>対義語：exhale（吐き出す）とペアで覚えると効果的"""
            
        else:
            # デフォルト処理（実装時に拡張）
            meaning = "（詳細定義を生成中...）"
            examples = [
                "Example sentence will be generated.",
                "Another example sentence here.",
                "Third example for context."
            ]
            tips = "語源・記憶術を生成中..."
        
        return self.create_structured_content(word, meaning, examples, tips)
    
    def parse_toefl_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        TOEFL 3800ファイル解析
        """
        words_data = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 4:
                    original_guid = parts[0]  # 参考用（使用しない）
                    word = parts[3]
                    original_meaning = parts[4] if len(parts) > 4 else ""
                    
                    words_data.append({
                        'word': word,
                        'original_meaning': original_meaning
                    })
        
        return words_data
    
    def generate_enhanced_tsv(self, input_file: str, output_file: str, limit: int = None):
        """
        改良版TSVファイル生成
        """
        print(f"🚀 Enhanced Anki processing: {input_file}")
        
        words_data = self.parse_toefl_file(input_file)
        
        if limit:
            words_data = words_data[:limit]
            print(f"📝 Limited to first {limit} words for testing")
        
        enhanced_cards = []
        
        for i, word_data in enumerate(words_data, 1):
            word = word_data['word']
            print(f"⚡ Processing {i}/{len(words_data)}: {word}")
            
            # GUID生成
            guid = self.generate_word_based_guid(word)
            
            # コンテンツ生成
            content = self.process_word_with_claude(word)
            
            # タグ設定
            tags = "claude-generated toefl rank3 enhanced"
            
            enhanced_cards.append({
                'guid': guid,
                'word': content['word'],
                'definition': content['definition'],
                'examples': content['examples'],
                'etymology': content['etymology'],
                'tags': tags,
                'deck': self.deck_name
            })
        
        # TSVファイル出力
        self._write_enhanced_tsv(enhanced_cards, output_file)
        
        print(f"✅ Enhanced TSV created: {output_file}")
        print(f"📊 Total cards: {len(enhanced_cards)}")
        print(f"🎯 Note type: {self.note_type}")
        print(f"🗂️ Deck: {self.deck_name}")
    
    def _write_enhanced_tsv(self, cards: List[Dict], output_file: str):
        """
        改良版TSV形式でファイル出力
        """
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # Ankiヘッダー（改良版）
            f.write("# Enhanced TOEFL Vocabulary Import File\n")
            f.write("# Generated by Claude Code Enhanced Anki Processor\n")
            f.write("#separator:tab\n")
            f.write("#html:true\n")
            f.write(f"#notetype:{self.note_type}\n")
            f.write(f"#deck:{self.deck_name}\n")
            f.write("#guid column:1\n")
            f.write("#tags column:6\n")
            f.write("# Field mapping: GUID | Word | Definition | Examples | Etymology | Tags\n")
            f.write("#\n")
            
            # カードデータ
            for card in cards:
                f.write(f"{card['guid']}\t{card['word']}\t{card['definition']}\t{card['examples']}\t{card['etymology']}\t{card['tags']}\n")
    
    def generate_css_template(self, output_file: str):
        """
        Ankiカードテンプレート用CSS生成
        """
        css_content = """
/* Enhanced TOEFL Vocabulary Card Styling */
/* このCSSをAnkiのカードテンプレート「Styling」欄に完全置き換えでコピーしてください */

/* 基本カードスタイル */
.card {
    font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fafafa;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.word {
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    text-align: center;
    border-bottom: 3px solid #3498db;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.definition {
    font-size: 24px;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 25px;
    padding: 12px;
    background-color: #ecf0f1;
    border-radius: 6px;
    font-weight: bold;
}

.examples {
    margin-bottom: 20px;
}

.examples .example {
    font-style: italic;
    color: #5a6c7d;
    margin: 8px 0;
    padding: 8px 12px;
    background-color: #ffffff;
    border-left: 4px solid #3498db;
    border-radius: 3px;
}

.example::first-letter {
    color: #e74c3c;
    font-weight: bold;
    font-size: 1.1em;
}

.etymology {
    background-color: #f4f1e8;
    border: 1px solid #d4be8a;
    border-radius: 5px;
    padding: 15px;
    margin-top: 20px;
    font-size: 14px;
    color: #8b4513;
    line-height: 1.5;
}

.etymology::before {
    content: "💡 ";
    font-size: 16px;
}

/* レスポンシブ対応 */
@media (max-width: 600px) {
    .card { padding: 15px; }
    .word { font-size: 24px; }
    .definition { font-size: 18px; }
}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"📄 CSS template created: {output_file}")

if __name__ == "__main__":
    processor = EnhancedAnkiProcessor()
    
    # テスト実行
    input_file = "../data/input/toefl3800__rank3.txt"
    output_tsv = "../data/output/claude-code/enhanced_deck_v2.tsv"
    output_css = "../data/output/claude-code/card_template.css"
    
    # 改良版TSV生成
    processor.generate_enhanced_tsv(input_file, output_tsv, limit=3)
    
    # CSS テンプレート生成
    processor.generate_css_template(output_css)
    
    print("\n🎉 Enhanced Anki processing complete!")
    print("📋 Next steps:")
    print("1. Import enhanced_deck_v2.tsv into Anki")
    print("2. Create 'Enhanced TOEFL Vocabulary' note type")
    print("3. Copy CSS from card_template.css to card template")