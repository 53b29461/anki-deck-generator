#!/usr/bin/env python3
import re

def create_perfect_file():
    """正しいGUIDと正しい暗記Tipsの両方を持つ完璧なファイルを作成"""
    
    # 正しいGUID-Wordマッピングを読み込み
    guid_mapping = {}
    with open('/tmp/clean_word_guid_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                guid, word = line.strip().split('\t', 1)
                guid_mapping[word] = guid
    
    print(f"正しいGUIDマッピング: {len(guid_mapping)}件読み込み")
    
    # 元の高品質暗記Tipsを読み込み
    etymology_mapping = {}
    with open('/tmp/original_etymology_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t', 1)
                if len(parts) == 2:
                    word, etymology = parts
                    # エスケープされたタブを復元
                    etymology = etymology.replace('\\t', '\t')
                    etymology_mapping[word] = etymology
    
    print(f"高品質暗記Tips: {len(etymology_mapping)}件読み込み")
    
    # 現在のファイル（正しいGUID）を読み込み
    with open('data/output/claude-code/TOEFL_3800_Rank3_FINAL_CORRECTED_GUIDS.tsv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    perfect_lines = []
    restored_count = 0
    not_found_count = 0
    
    for line in lines:
        # コメント行はそのまま
        if line.startswith('#'):
            perfect_lines.append(line)
            continue
        
        # 空行はそのまま
        if line.strip() == '':
            perfect_lines.append(line)
            continue
        
        # データ行を処理
        fields = line.strip().split('\t')
        if len(fields) != 6:
            perfect_lines.append(line)  # 異常行はそのまま
            continue
        
        guid, word_html, definition, examples, etymology, tags = fields
        
        # wordを抽出
        word_match = re.search(r'<div class="word">([^<]+)</div>', word_html)
        if not word_match:
            perfect_lines.append(line)  # wordが抽出できない場合はそのまま
            not_found_count += 1
            continue
        
        word = word_match.group(1)
        
        # 高品質暗記Tipsがある場合は復元
        if word in etymology_mapping:
            original_etymology = etymology_mapping[word]
            # 完璧なラインを作成（正しいGUID + 高品質暗記Tips）
            perfect_line = '\t'.join([guid, word_html, definition, examples, original_etymology, tags])
            perfect_lines.append(perfect_line + '\n')
            restored_count += 1
            print(f"復元: {word}")
        else:
            # 高品質暗記Tipsがない場合は現在のものを保持
            perfect_lines.append(line)
            not_found_count += 1
            print(f"⚠️ 暗記Tips未発見: {word}")
    
    # 完璧なファイルを保存
    with open('data/output/claude-code/TOEFL_3800_Rank3_PERFECT_FINAL.tsv', 'w', encoding='utf-8') as f:
        f.writelines(perfect_lines)
    
    print(f"\n=== 復元結果 ===")
    print(f"暗記Tips復元: {restored_count}件")
    print(f"暗記Tips未発見: {not_found_count}件")
    print(f"出力ファイル: TOEFL_3800_Rank3_PERFECT_FINAL.tsv")
    
    return restored_count, not_found_count

if __name__ == "__main__":
    create_perfect_file()