#!/usr/bin/env python3
import re

def extract_original_etymology():
    """元のファイルから正しい暗記Tips（etymology）を抽出"""
    
    etymology_mapping = {}
    
    # 元の高品質etymologyを読み込み
    with open('data/output/claude-code/enhanced_deck_v2.tsv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    extracted_count = 0
    
    for line in lines:
        # コメント行と空行はスキップ
        if line.startswith('#') or line.strip() == '':
            continue
        
        fields = line.strip().split('\t')
        if len(fields) != 6:
            continue
        
        guid, word_html, definition, examples, etymology, tags = fields
        
        # wordを抽出
        word_match = re.search(r'<div class="word">([^<]+)</div>', word_html)
        if not word_match:
            continue
        
        word = word_match.group(1)
        
        # 高品質なetymology（日本語形式）のみを保存
        if etymology and '語源：' in etymology:
            etymology_mapping[word] = etymology
            extracted_count += 1
            print(f"抽出: {word}")
    
    print(f"\n=== 抽出結果 ===")
    print(f"高品質暗記Tips抽出: {extracted_count}件")
    
    # マッピング結果を保存
    with open('/tmp/original_etymology_mapping.txt', 'w', encoding='utf-8') as f:
        for word, etymology in etymology_mapping.items():
            # タブ文字をエスケープして保存
            escaped_etymology = etymology.replace('\t', '\\t')
            f.write(f"{word}\t{escaped_etymology}\n")
    
    print(f"マッピングファイル保存: /tmp/original_etymology_mapping.txt")
    
    # サンプル表示
    print(f"\n=== サンプル（最初の5件） ===")
    for i, (word, etymology) in enumerate(list(etymology_mapping.items())[:5]):
        print(f"{word}: {etymology[:100]}...")
    
    return etymology_mapping

if __name__ == "__main__":
    extract_original_etymology()