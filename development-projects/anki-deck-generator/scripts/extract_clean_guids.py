#!/usr/bin/env python3

def extract_clean_guid_mapping():
    """正常なGUID-Word マッピングを抽出"""
    
    clean_data = []
    
    with open('data/input/toefl3800__rank3.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines[6:], 7):  # Skip first 6 header lines
        if line.strip() == '':
            continue
            
        fields = line.strip().split('\t')
        if len(fields) < 4:
            continue
            
        guid = fields[0]
        word = fields[3]
        
        # 正常なGUIDの条件：
        # 1. 長さが10-12文字
        # 2. HTMLタグで始まらない
        # 3. wordが存在する
        if (10 <= len(guid) <= 12 and 
            not guid.startswith('<') and 
            word.strip() != ''):
            
            clean_data.append((guid, word.strip()))
    
    # 結果を保存
    with open('/tmp/clean_word_guid_mapping.txt', 'w', encoding='utf-8') as f:
        for guid, word in clean_data:
            f.write(f"{guid}\t{word}\n")
    
    print(f"正常データ抽出完了: {len(clean_data)}件")
    
    # 統計表示
    print("\n=== 最初の10件 ===")
    for i, (guid, word) in enumerate(clean_data[:10]):
        print(f"{guid}\t{word}")
    
    print("\n=== 最後の10件 ===")
    for i, (guid, word) in enumerate(clean_data[-10:]):
        print(f"{guid}\t{word}")
    
    # 重複チェック
    words = [word for _, word in clean_data]
    unique_words = set(words)
    print(f"\n=== 統計 ===")
    print(f"総データ数: {len(clean_data)}")
    print(f"ユニーク単語数: {len(unique_words)}")
    if len(words) != len(unique_words):
        print("⚠️ 重複した単語が存在します")
    else:
        print("✅ 全ての単語がユニークです")
    
    return clean_data

if __name__ == "__main__":
    extract_clean_guid_mapping()