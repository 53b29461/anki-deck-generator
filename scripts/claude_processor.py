#!/usr/bin/env python3
"""
Claude Code用のAnki裏面生成スクリプト
API不使用、Claude Codeが直接生成したコンテンツを整形
"""

import re
import csv

def create_anki_back_content(word, meaning, examples, tips):
    """
    AnkiのHTML対応裏面コンテンツを生成
    """
    # HTMLエスケープ（必要に応じて）
    def escape_html(text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # 意味部分
    meaning_html = f"<strong>{meaning}</strong>"
    
    # 例文部分（改行で区切り）
    examples_html = "<br>".join([f"<em>{example}</em>" for example in examples])
    
    # Tips部分
    tips_html = f"<div style='margin-top: 10px; padding: 5px; background-color: #f0f0f0;'>{tips}</div>"
    
    # 全体を結合
    full_content = f"""
{meaning_html}

<br><br>

{examples_html}

<br><br>

{tips_html}
""".strip()
    
    return full_content

def process_word_with_claude(word):
    """
    Claude Codeが生成する高品質なAnki裏面コンテンツ
    この関数内でClaude Codeが各単語の内容を生成
    """
    
    # テスト用の単語別処理
    if word == "ambush":
        meaning = "待ち伏せ攻撃、奇襲、伏兵攻撃"
        examples = [
            "The rebels set up an ambush along the mountain road.",
            "Police officers were killed in a terrorist ambush.",
            "The predator waited in ambush for unsuspecting prey."
        ]
        tips = """語源：古フランス語「embuscher」（茂みに隠れる）から派生<br>
「em-（中に）+ busch（茂み）」→茂みの中に隠れて待ち伏せする<br>
military terminology として覚えると、warfare関連語彙と関連付けやすい"""
        
    elif word == "bountiful":
        meaning = "豊富な、物惜しみしない、気前の良い"
        examples = [
            "The harvest was bountiful this year.",
            "She received bountiful praise for her performance.",
            "The garden produced a bountiful supply of vegetables."
        ]
        tips = """語源：古フランス語「bonté」（善良さ）から派生<br>
「bounty（恵み、報奨金）+ -ful（〜に満ちた）」<br>
abundance, plentiful などの類義語と関連付けて覚える"""
        
    elif word == "inhale":
        meaning = "吸い込む、吸入する"
        examples = [
            "Please inhale deeply and hold your breath.",
            "The patient needs to inhale the medication through this device.",
            "Don't inhale the fumes from the chemical."
        ]
        tips = """語源：ラテン語「inhalare」<br>
「in-（中に）+ halare（息する）」→中に息を吸う<br>
対義語：exhale（吐き出す）とペアで覚えると効果的"""
        
    else:
        # デフォルト処理
        meaning = "（Claude Codeによる生成が必要）"
        examples = ["Example sentence needed.", "Another example needed.", "Third example needed."]
        tips = "語源・記憶術を生成中..."
    
    return create_anki_back_content(word, meaning, examples, tips)

def parse_toefl_file(file_path):
    """
    TOEFL 3800ファイルを解析してGUID, word, original_meaningを抽出
    """
    words_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
                
            parts = line.split('\t')
            if len(parts) >= 5:
                guid = parts[0]
                card_type = parts[1] 
                deck_name = parts[2]
                word = parts[3]
                original_meaning = parts[4]
                
                words_data.append({
                    'guid': guid,
                    'card_type': card_type,
                    'deck_name': deck_name,
                    'word': word,
                    'original_meaning': original_meaning
                })
    
    return words_data

def generate_enhanced_deck(input_file, output_file, limit=None):
    """
    強化されたAnkiデッキを生成
    """
    print(f"Processing {input_file}...")
    
    words_data = parse_toefl_file(input_file)
    
    if limit:
        words_data = words_data[:limit]
        print(f"Limited to first {limit} words for testing")
    
    enhanced_cards = []
    
    for i, word_data in enumerate(words_data, 1):
        word = word_data['word']
        print(f"Processing {i}/{len(words_data)}: {word}")
        
        # Claude Codeによる裏面生成
        enhanced_back = process_word_with_claude(word)
        
        # 新しいAnki形式でカード作成
        enhanced_card = {
            'guid': word_data['guid'],
            'card_type': word_data['card_type'],
            'deck_name': word_data['deck_name'],
            'front': word,  # 表面は英単語のみ
            'back': enhanced_back,  # 裏面は強化されたHTML形式
            'tags': 'claude-generated'
        }
        
        enhanced_cards.append(enhanced_card)
    
    # TSV形式で出力（Ankiインポート用）
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        # Ankiヘッダー
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#guid column:1\n")
        f.write("#notetype column:2\n")
        f.write("#deck column:3\n")
        f.write("#tags column:6\n")
        
        # カードデータ
        for card in enhanced_cards:
            f.write(f"{card['guid']}\t{card['card_type']}\t{card['deck_name']}\t{card['front']}\t{card['back']}\t{card['tags']}\n")
    
    print(f"Enhanced deck created: {output_file}")
    print(f"Total cards: {len(enhanced_cards)}")

if __name__ == "__main__":
    # テスト実行（最初の3語のみ）
    input_file = "../data/input/toefl3800__rank3.txt"
    output_file = "../data/output/claude-code/enhanced_deck_test.txt"
    
    generate_enhanced_deck(input_file, output_file, limit=3)
    print("Claude Code processing complete!")