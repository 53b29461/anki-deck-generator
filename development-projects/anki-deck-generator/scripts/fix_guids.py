#!/usr/bin/env python3
import re

def fix_guids_in_tsv():
    """TSVファイルの間違ったGUIDを正しいGUIDに修正"""
    
    # 正しいGUID-Wordマッピングを読み込み
    guid_mapping = {}
    with open('/tmp/clean_word_guid_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                guid, word = line.strip().split('\t', 1)
                guid_mapping[word] = guid
    
    print(f"正しいGUIDマッピング: {len(guid_mapping)}件読み込み")
    
    # 現在のTSVファイルを読み込み
    with open('data/output/claude-code/TOEFL_3800_Rank3_Enhanced_FINAL.tsv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    fixed_count = 0
    not_found_count = 0
    
    for line in lines:
        # コメント行はそのまま
        if line.startswith('#'):
            fixed_lines.append(line)
            continue
        
        # 空行はそのまま
        if line.strip() == '':
            fixed_lines.append(line)
            continue
        
        # データ行を処理
        fields = line.strip().split('\t')
        if len(fields) != 6:
            fixed_lines.append(line)  # 異常行はそのまま
            continue
        
        old_guid, word_html, definition, examples, etymology, tags = fields
        
        # wordを抽出（<div class="word">word</div>から）
        word_match = re.search(r'<div class="word">([^<]+)</div>', word_html)
        if not word_match:
            fixed_lines.append(line)  # wordが抽出できない場合はそのまま
            not_found_count += 1
            continue
        
        word = word_match.group(1)
        
        # 正しいGUIDを探す
        if word in guid_mapping:
            correct_guid = guid_mapping[word]
            if old_guid != correct_guid:
                # GUIDを修正
                fixed_line = '\t'.join([correct_guid, word_html, definition, examples, etymology, tags])
                fixed_lines.append(fixed_line + '\n')
                fixed_count += 1
                print(f"修正: {word} {old_guid} → {correct_guid}")
            else:
                fixed_lines.append(line)  # 既に正しい場合はそのまま
        else:
            fixed_lines.append(line)  # マッピングにない場合はそのまま
            not_found_count += 1
            print(f"⚠️ マッピングなし: {word}")
    
    # 修正済みファイルを保存
    with open('data/output/claude-code/TOEFL_3800_Rank3_Enhanced_CORRECTED.tsv', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"\n=== 修正結果 ===")
    print(f"修正したGUID: {fixed_count}件")
    print(f"マッピングが見つからない単語: {not_found_count}件")
    print(f"出力ファイル: TOEFL_3800_Rank3_Enhanced_CORRECTED.tsv")
    
    return fixed_count, not_found_count

if __name__ == "__main__":
    fix_guids_in_tsv()