#!/usr/bin/env python3
"""
改良版CC練習問題 → Ankiデッキ変換
より精密な選択肢抽出とデータクリーニング
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class ImprovedCCAnkiGenerator:
    """
    改良版CC練習問題Ankiデッキ生成器
    """
    
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.stats = {
            'total_questions': 0,
            'converted_cards': 0,
            'skipped_incomplete': 0,
            'manual_review_needed': 0
        }
    
    def clean_text(self, text: str) -> str:
        """
        改良版テキストクリーニング
        """
        if not text:
            return ""
        
        # HTMLタグ除去
        text = re.sub(r'<[^>]+>', '', text)
        
        # OCRエラーの修正
        text = re.sub(r'["""]', '"', text)  # 引用符統一
        text = re.sub(r"[''']", "'", text)  # アポストロフィ統一
        text = re.sub(r'[—–]', '-', text)   # ダッシュ統一
        
        # 余分な記号・文字除去
        text = re.sub(r'[©®™]', '', text)
        text = re.sub(r'\([^\)]{0,3}\)', '', text)  # 短い括弧内容除去
        text = re.sub(r'\s+', ' ', text)  # 空白統一
        text = text.strip()
        
        # Ankiエスケープ
        text = text.replace('"', '""')
        
        return text
    
    def extract_clean_choices(self, question_data: Dict) -> List[str]:
        """
        選択肢をより精密に抽出・クリーニング
        """
        raw_choices = question_data.get('choices', [])
        clean_choices = []
        
        # 技術用語リスト（これらを含む行は選択肢候補）
        tech_terms = [
            'access control', 'authentication', 'authorization', 'encryption',
            'firewall', 'malware', 'virus', 'security', 'data', 'network',
            'system', 'password', 'user', 'administrative', 'physical',
            'technical', 'policy', 'procedure', 'risk', 'threat', 'asset',
            'confidentiality', 'integrity', 'availability', 'medical',
            'privacy', 'gdpr', 'regulation', 'biometric', 'multifactor',
            'non-repudiation', 'siem', 'ids', 'ips', 'vpn', 'certificate'
        ]
        
        # 明らかに選択肢でない文字列
        exclude_patterns = [
            r'^(correct|score|seconds|attempt|taken|explanation)',
            r'^[0-9]+$',  # 数字のみ
            r'http[s]?://',  # URL
            r'@',  # メールアドレス風
            r'^[^a-zA-Z]',  # 英字で始まらない
        ]
        
        for choice in raw_choices:
            if not choice or len(choice.strip()) < 3:
                continue
            
            choice_clean = self.clean_text(choice)
            
            # 除外パターンチェック
            skip = False
            for pattern in exclude_patterns:
                if re.search(pattern, choice_clean, re.IGNORECASE):
                    skip = True
                    break
            
            if skip:
                continue
            
            # 長さフィルター
            if not (5 <= len(choice_clean) <= 100):
                continue
            
            # 技術用語を含むか、一般的な選択肢パターンか
            is_valid_choice = False
            
            # 技術用語チェック
            for term in tech_terms:
                if term.lower() in choice_clean.lower():
                    is_valid_choice = True
                    break
            
            # 一般的な選択肢パターン
            if not is_valid_choice:
                choice_lower = choice_clean.lower()
                if (choice_lower.startswith(('a ', 'an ', 'the ')) or
                    any(word in choice_lower for word in ['control', 'management', 'protection', 'security']) or
                    choice_clean[0].isupper()):  # 大文字で始まる
                    is_valid_choice = True
            
            if is_valid_choice:
                clean_choices.append(choice_clean)
        
        # 重複除去と最大4個まで
        unique_choices = []
        seen = set()
        for choice in clean_choices:
            choice_key = choice.lower().replace(' ', '')
            if choice_key not in seen:
                seen.add(choice_key)
                unique_choices.append(choice)
        
        return unique_choices[:4]
    
    def find_correct_answer(self, question_data: Dict, choices: List[str]) -> Tuple[str, str]:
        """
        正解を特定（改良版）
        """
        correct_raw = question_data.get('correct_answer', '')
        
        if not correct_raw or not choices:
            return choices[0] if choices else "", "A"
        
        correct_clean = self.clean_text(correct_raw)
        
        # 方法1: 完全一致または部分一致
        for i, choice in enumerate(choices):
            if (correct_clean.lower() in choice.lower() or 
                choice.lower() in correct_clean.lower()):
                return choice, chr(65 + i)
        
        # 方法2: キーワードマッチング
        correct_keywords = set(re.findall(r'\b\w+\b', correct_clean.lower()))
        best_match = ""
        best_score = 0
        best_index = 0
        
        for i, choice in enumerate(choices):
            choice_keywords = set(re.findall(r'\b\w+\b', choice.lower()))
            common_keywords = correct_keywords & choice_keywords
            score = len(common_keywords)
            
            if score > best_score:
                best_score = score
                best_match = choice
                best_index = i
        
        if best_match:
            return best_match, chr(65 + best_index)
        
        # フォールバック: 最初の選択肢
        return choices[0], "A"
    
    def create_improved_anki_card(self, question_data: Dict, card_id: int) -> Dict:
        """
        改良版Ankiカード生成
        """
        # 基本情報
        question_text = self.clean_text(question_data.get('question', ''))
        explanation = self.clean_text(question_data.get('explanation', ''))
        filename = question_data.get('filename', '')
        
        # 改良版選択肢抽出
        choices = self.extract_clean_choices(question_data)
        
        # 正解特定
        correct_answer, correct_letter = self.find_correct_answer(question_data, choices)
        
        # 空の選択肢を埋める
        while len(choices) < 4:
            choices.append("")
        
        # データ品質チェック
        quality_score = 0
        if question_text and len(question_text) > 10:
            quality_score += 2
        if len([c for c in choices if c]) >= 2:
            quality_score += 2
        if correct_answer:
            quality_score += 1
        if explanation:
            quality_score += 1
        
        # クローズテキスト
        cloze_text = f"{{{{c1::{correct_answer}}}}}"
        
        anki_card = {
            'card_id': card_id,
            'question': question_text,
            'choice_a': choices[0],
            'choice_b': choices[1],
            'choice_c': choices[2],
            'choice_d': choices[3],
            'correct_answer': correct_answer,
            'correct_letter': correct_letter,
            'explanation': explanation,
            'cloze_text': cloze_text,
            'filename': filename,
            'quality_score': quality_score,
            'tags': 'CC ISC2 Cybersecurity Security+'
        }
        
        return anki_card
    
    def generate_improved_tsv(self, cards: List[Dict]) -> str:
        """
        改良版TSV生成
        """
        headers = [
            "問題文", "選択肢A", "選択肢B", "選択肢C", "選択肢D",
            "正解", "解説", "Text", "タグ", "品質スコア"
        ]
        
        lines = ["\t".join(headers)]
        
        for card in cards:
            row = [
                card['question'],
                card['choice_a'],
                card['choice_b'],
                card['choice_c'],
                card['choice_d'],
                card['correct_answer'],
                card['explanation'],
                card['cloze_text'],
                card['tags'],
                str(card['quality_score'])
            ]
            lines.append("\t".join(row))
        
        return "\n".join(lines)
    
    def generate_study_guide(self, cards: List[Dict]) -> str:
        """
        学習ガイド生成
        """
        high_quality = [c for c in cards if c['quality_score'] >= 5]
        medium_quality = [c for c in cards if 3 <= c['quality_score'] < 5]
        low_quality = [c for c in cards if c['quality_score'] < 3]
        
        guide = f"""# CC練習問題 Ankiデッキ学習ガイド

## 📊 品質分析
- **高品質カード**: {len(high_quality)}枚（推奨学習優先度: 高）
- **中品質カード**: {len(medium_quality)}枚（推奨学習優先度: 中）  
- **低品質カード**: {len(low_quality)}枚（推奨学習優先度: 低、手動確認推奨）

## 🎯 学習戦略
1. **高品質カード**から学習開始
2. **クローズ形式**で正解を思い出す練習
3. **解説**を必ず読んで理解を深める
4. **関連用語**をタグで横断学習

## 🔍 品質が低いカード（手動確認推奨）
"""
        
        if low_quality:
            for i, card in enumerate(low_quality[:10], 1):
                guide += f"{i}. {card['filename']}: {card['question'][:50]}...\n"
        else:
            guide += "なし（全カードが高品質です！）\n"
        
        guide += f"""
## 📚 学習トピック別分布
CCの主要トピック:
- アクセス制御（Access Control）
- セキュリティ概念（CIA Triad）
- リスク管理（Risk Management）
- ガバナンス・法規制（Governance & Regulations）
- インシデント対応（Incident Response）

## 💡 効果的な学習法
1. **間隔反復**: Ankiの標準設定を活用
2. **理解重視**: 暗記より概念理解
3. **実践応用**: Security+への橋渡し学習
4. **定期復習**: 週1回のまとめ復習
"""
        
        return guide
    
    def process_questions(self):
        """
        改良版問題処理
        """
        print("🔧 改良版CC練習問題 → Ankiデッキ変換開始...")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        self.stats['total_questions'] = len(questions_data)
        print(f"📖 読み込み完了: {self.stats['total_questions']}問")
        
        anki_cards = []
        
        for i, question_data in enumerate(questions_data):
            if not question_data.get('parsed', False):
                self.stats['skipped_incomplete'] += 1
                continue
            
            try:
                card = self.create_improved_anki_card(question_data, i + 1)
                anki_cards.append(card)
                
                if card['quality_score'] < 3:
                    self.stats['manual_review_needed'] += 1
                
                self.stats['converted_cards'] += 1
                
                if (i + 1) % 25 == 0:
                    print(f"⚡ 処理済み: {i + 1}/{self.stats['total_questions']}")
                    
            except Exception as e:
                print(f"❌ エラー [{question_data.get('filename', 'Unknown')}]: {e}")
                self.stats['skipped_incomplete'] += 1
        
        # ファイル生成
        self.save_outputs(anki_cards)
    
    def save_outputs(self, cards: List[Dict]):
        """
        出力ファイル保存
        """
        # TSVファイル
        tsv_content = self.generate_improved_tsv(cards)
        tsv_file = self.output_dir / 'cc_anki_improved.tsv'
        with open(tsv_file, 'w', encoding='utf-8') as f:
            f.write(tsv_content)
        
        # 学習ガイド
        guide_content = self.generate_study_guide(cards)
        guide_file = self.output_dir / 'study_guide.md'
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        # JSON詳細データ
        json_file = self.output_dir / 'cc_anki_improved.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        
        # 結果サマリー
        self.print_results(tsv_file, guide_file, cards)
    
    def print_results(self, tsv_file: Path, guide_file: Path, cards: List[Dict]):
        """
        結果表示
        """
        high_quality = len([c for c in cards if c['quality_score'] >= 5])
        
        print("\n🎉 改良版Ankiデッキ生成完了!")
        print("=" * 60)
        print(f"📊 総問題数: {self.stats['total_questions']}")
        print(f"✅ 変換成功: {self.stats['converted_cards']}")
        print(f"⚠️  手動確認推奨: {self.stats['manual_review_needed']}")
        print(f"🏆 高品質カード: {high_quality}")
        print(f"📈 全体成功率: {(self.stats['converted_cards']/self.stats['total_questions']*100):.1f}%")
        
        print(f"\n📁 生成ファイル:")
        print(f"1. 📋 {tsv_file.name} - Ankiインポート用")
        print(f"2. 📖 {guide_file.name} - 学習ガイド")
        print(f"3. 🔍 cc_anki_improved.json - 詳細データ")
        
        print(f"\n🚀 次のステップ:")
        print(f"1. study_guide.md で学習戦略を確認")
        print(f"2. Ankiに {tsv_file.name} をインポート")
        print(f"3. 高品質カード({high_quality}枚)から学習開始!")


def main():
    project_dir = Path(__file__).parent.parent
    input_file = project_dir / 'output' / 'cc_questions_final.json'
    output_dir = project_dir / 'output' / 'anki'
    
    if not input_file.exists():
        print(f"❌ 入力ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    generator = ImprovedCCAnkiGenerator(str(input_file), str(output_dir))
    generator.process_questions()


if __name__ == "__main__":
    main()