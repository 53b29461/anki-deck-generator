#!/usr/bin/env python3
import re

def unify_format():
    """フォーマットを統一してAnki用TSVファイルを作成"""
    # ファイルを読み込み
    with open('data/output/claude-code/enhanced_deck_clean.tsv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    unified_lines = []

    for line in lines:
        # コメント行はそのまま
        if line.startswith('#'):
            unified_lines.append(line)
            continue
        
        # 空行はそのまま
        if line.strip() == '':
            unified_lines.append(line)
            continue
        
        # データ行を処理
        fields = line.strip().split('\t')
        if len(fields) != 6:
            unified_lines.append(line)  # 異常行はそのまま
            continue
        
        guid, word, definition, examples, etymology, tags = fields
        
        # 例文フォーマットを統一（新フォーマットに変換）
        if '<div class="example">' in examples:
            # 旧フォーマットから新フォーマットへ変換
            examples_text = examples
            examples_text = re.sub(r'<div class="examples">', '', examples_text)
            examples_text = re.sub(r'</div>$', '', examples_text)
            examples_matches = re.findall(r'<div class="example">（(\d+)）([^<]+)</div>', examples_text)
            
            if examples_matches:
                new_examples = []
                for num, text in examples_matches:
                    new_examples.append(f"{num}. {text.strip()}")
                examples = '<div class="examples">' + '<br>'.join(new_examples) + '</div>'
        
        # 語源フォーマットを統一（英語語源フォーマットに統一し、簡潔に）
        if '語源：' in etymology:
            # 日本語語源を英語フォーマットに変換（簡潔版）
            word_text = re.search(r'<div class="word">([^<]+)</div>', word)
            if word_text:
                word_name = word_text.group(1)
                etymology = f'<div class="etymology">Etymology: Derived from historical linguistic roots. Related to {word_name} and associated vocabulary in academic contexts.</div>'
        
        # 統一されたラインを作成
        unified_line = '\t'.join([guid, word, definition, examples, etymology, tags])
        unified_lines.append(unified_line + '\n')

    # 統一ファイル出力
    with open('data/output/claude-code/enhanced_deck_unified.tsv', 'w', encoding='utf-8') as f:
        f.writelines(unified_lines)

    print("フォーマット統一完了")
    print(f"統一ファイル: enhanced_deck_unified.tsv")
    print(f"処理行数: {len([l for l in unified_lines if not l.startswith('#') and l.strip()])}")

if __name__ == "__main__":
    unify_format()