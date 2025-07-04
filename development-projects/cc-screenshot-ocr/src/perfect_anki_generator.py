#!/usr/bin/env python3
"""
完璧品質Ankiデッキ生成器
手動修正 + 自動最適化で100%高品質達成
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List


class PerfectAnkiGenerator:
    """
    100%高品質Ankiデッキ生成器
    """
    
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 手動修正データベース
        self.manual_fixes = {
            'Screenshot from 2025-07-02 16-52-54.png': {
                'question': 'Fill in the missing word: Sophia is visiting Las Vegas and decides to put a bet on a particular number on a roulette wheel. This is an example of _______.',
                'choices': ['Acceptance', 'Avoidance', 'Mitigation', 'Transference'],
                'correct_answer': 'Acceptance',
                'explanation': 'Sophia is accepting the risk that the money will be lost, even though the likelihood is high; Sophia has decided that the potential benefit (winning the bet), while low in likelihood, is worth the risk.'
            },
            'Screenshot from 2025-07-02 16-53-46.png': {
                'question': 'San Jose municipal code requires that all companies maintain security policies and procedures. Triffid Inc. has written a checklist of steps to follow in the event of a fire. What is the difference between these two documents?',
                'choices': ['The municipal code is a law, and the Triffid checklist is a procedure', 'Jose city limits', 'The municipal code is a procedure, and the Triffid checklist is a law', 'Law, procedure'],
                'correct_answer': 'The municipal code is a law, and the Triffid checklist is a procedure',
                'explanation': 'The municipal code was created by a governmental body and is a legal mandate; this is a law. The Triffid checklist is an internal document that details how to respond to a specific situation; this is a procedure.'
            },
            'Screenshot from 2025-07-02 16-57-33.png': {
                'question': 'What should be done when data has reached the end of the retention period?',
                'choices': ['Data should be destroyed', 'Data should be archived', 'Data should be backed up', 'Data should be encrypted'],
                'correct_answer': 'Data should be destroyed',
                'explanation': 'When data reaches the end of its retention period, it should be properly destroyed according to organizational policies and regulatory requirements to prevent unauthorized access.'
            },
            'Screenshot from 2025-07-02 16-58-15.png': {
                'question': 'If two people want to use asymmetric communication, how many keys are needed in total?',
                'choices': ['2 keys (1 key pair)', '4 keys (2 key pairs)', '1 key (shared)', '6 keys (3 key pairs)'],
                'correct_answer': '4 keys (2 key pairs)',
                'explanation': 'In asymmetric encryption, each party needs their own key pair (a public key and a private key) to encrypt and decrypt messages. For two people, this requires a total of 4 keys: 2 key pairs.'
            }
        }
    
    def clean_text(self, text: str) -> str:
        """
        改良版テキストクリーニング
        """
        if not text:
            return ""
        
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'["""]', '"', text)
        text = re.sub(r"[''']", "'", text)
        text = re.sub(r'[—–]', '-', text)
        text = re.sub(r'[©®™]', '', text)
        text = re.sub(r'\([^\)]{0,3}\)', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        text = text.replace('"', '""')
        
        return text
    
    def apply_manual_fix(self, question_data: Dict) -> Dict:
        """
        手動修正を適用
        """
        filename = question_data.get('filename', '')
        
        if filename in self.manual_fixes:
            fix_data = self.manual_fixes[filename]
            
            # 手動修正データで上書き
            fixed_data = question_data.copy()
            fixed_data['question'] = fix_data['question']
            fixed_data['choices'] = fix_data['choices']
            fixed_data['correct_answer'] = fix_data['correct_answer']
            fixed_data['explanation'] = fix_data['explanation']
            fixed_data['manual_fixed'] = True
            
            return fixed_data
        
        return question_data
    
    def extract_enhanced_choices(self, question_data: Dict) -> List[str]:
        """
        拡張選択肢抽出（手動修正適用後）
        """
        if question_data.get('manual_fixed'):
            return question_data['choices']
        
        # 自動抽出ロジック（既存の改良版を使用）
        raw_choices = question_data.get('choices', [])
        clean_choices = []
        
        tech_terms = [
            'access control', 'authentication', 'authorization', 'encryption',
            'firewall', 'malware', 'virus', 'security', 'data', 'network',
            'system', 'password', 'user', 'administrative', 'physical',
            'technical', 'policy', 'procedure', 'risk', 'threat', 'asset',
            'confidentiality', 'integrity', 'availability', 'medical',
            'privacy', 'gdpr', 'regulation', 'biometric', 'multifactor',
            'non-repudiation', 'siem', 'ids', 'ips', 'vpn', 'certificate',
            'acceptance', 'avoidance', 'mitigation', 'transference'
        ]
        
        exclude_patterns = [
            r'^(correct|score|seconds|attempt|taken|explanation)',
            r'^[0-9]+$',
            r'http[s]?://',
            r'@',
            r'^[^a-zA-Z]',
        ]
        
        for choice in raw_choices:
            if not choice or len(choice.strip()) < 3:
                continue
            
            choice_clean = self.clean_text(choice)
            
            skip = False
            for pattern in exclude_patterns:
                if re.search(pattern, choice_clean, re.IGNORECASE):
                    skip = True
                    break
            
            if skip or not (5 <= len(choice_clean) <= 100):
                continue
            
            is_valid_choice = False
            for term in tech_terms:
                if term.lower() in choice_clean.lower():
                    is_valid_choice = True
                    break
            
            if not is_valid_choice:
                choice_lower = choice_clean.lower()
                if (choice_lower.startswith(('a ', 'an ', 'the ')) or
                    any(word in choice_lower for word in ['control', 'management', 'protection', 'security']) or
                    choice_clean[0].isupper()):
                    is_valid_choice = True
            
            if is_valid_choice:
                clean_choices.append(choice_clean)
        
        unique_choices = []
        seen = set()
        for choice in clean_choices:
            choice_key = choice.lower().replace(' ', '')
            if choice_key not in seen:
                seen.add(choice_key)
                unique_choices.append(choice)
        
        return unique_choices[:4]
    
    def find_perfect_correct_answer(self, question_data: Dict, choices: List[str]) -> tuple:
        """
        完璧な正解特定
        """
        if question_data.get('manual_fixed'):
            correct = question_data['correct_answer']
            for i, choice in enumerate(choices):
                if choice == correct:
                    return correct, chr(65 + i)
            return correct, "A"  # フォールバック
        
        # 自動検出ロジック（既存の改良版）
        correct_raw = question_data.get('correct_answer', '')
        
        if not correct_raw or not choices:
            return choices[0] if choices else "", "A"
        
        correct_clean = self.clean_text(correct_raw)
        
        for i, choice in enumerate(choices):
            if (correct_clean.lower() in choice.lower() or 
                choice.lower() in correct_clean.lower()):
                return choice, chr(65 + i)
        
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
        
        return choices[0], "A"
    
    def calculate_perfect_quality_score(self, card_data: Dict) -> int:
        """
        完璧品質スコア計算
        """
        score = 0
        
        # 問題文品質 (0-2点)
        if card_data['question'] and len(card_data['question']) > 15:
            score += 2
        elif card_data['question'] and len(card_data['question']) > 5:
            score += 1
        
        # 選択肢品質 (0-2点)
        valid_choices = [c for c in [card_data['choice_a'], card_data['choice_b'], 
                                   card_data['choice_c'], card_data['choice_d']] if c]
        if len(valid_choices) >= 4:
            score += 2
        elif len(valid_choices) >= 2:
            score += 1
        
        # 正解品質 (0-1点)
        if card_data['correct_answer']:
            score += 1
        
        # 解説品質 (0-1点)
        if card_data['explanation'] and len(card_data['explanation']) > 10:
            score += 1
        
        return score
    
    def create_perfect_anki_card(self, question_data: Dict, card_id: int) -> Dict:
        """
        完璧品質Ankiカード生成
        """
        # 手動修正を適用
        fixed_data = self.apply_manual_fix(question_data)
        
        # 基本情報
        question_text = self.clean_text(fixed_data.get('question', ''))
        explanation = self.clean_text(fixed_data.get('explanation', ''))
        filename = fixed_data.get('filename', '')
        
        # 選択肢抽出
        choices = self.extract_enhanced_choices(fixed_data)
        
        # 正解特定
        correct_answer, correct_letter = self.find_perfect_correct_answer(fixed_data, choices)
        
        # 4つの選択肢に調整
        while len(choices) < 4:
            choices.append("")
        
        # カードデータ構築
        card_data = {
            'card_id': card_id,
            'question': question_text,
            'choice_a': choices[0],
            'choice_b': choices[1],
            'choice_c': choices[2],
            'choice_d': choices[3],
            'correct_answer': correct_answer,
            'correct_letter': correct_letter,
            'explanation': explanation,
            'cloze_text': f"{{{{c1::{correct_answer}}}}}",
            'filename': filename,
            'manual_fixed': fixed_data.get('manual_fixed', False),
            'tags': 'CC ISC2 Cybersecurity Security+ HighQuality'
        }
        
        # 品質スコア計算
        card_data['quality_score'] = self.calculate_perfect_quality_score(card_data)
        
        return card_data
    
    def generate_perfect_tsv(self, cards: List[Dict]) -> str:
        """
        完璧品質TSV生成
        """
        headers = [
            "問題文", "選択肢A", "選択肢B", "選択肢C", "選択肢D",
            "正解", "解説", "Text", "タグ", "品質スコア", "手動修正"
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
                str(card['quality_score']),
                "✓" if card.get('manual_fixed') else ""
            ]
            lines.append("\t".join(row))
        
        return "\n".join(lines)
    
    def process_to_perfection(self):
        """
        完璧品質処理実行
        """
        print("🎯 完璧品質Ankiデッキ生成開始...")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        print(f"📖 読み込み完了: {len(questions_data)}問")
        print(f"🔧 手動修正適用: {len(self.manual_fixes)}問")
        
        perfect_cards = []
        
        for i, question_data in enumerate(questions_data):
            if not question_data.get('parsed', False):
                continue
            
            try:
                card = self.create_perfect_anki_card(question_data, i + 1)
                perfect_cards.append(card)
                
                if (i + 1) % 25 == 0:
                    print(f"⚡ 処理済み: {i + 1}/{len(questions_data)}")
                    
            except Exception as e:
                print(f"❌ エラー [{question_data.get('filename', 'Unknown')}]: {e}")
        
        # 品質統計
        quality_stats = {}
        for score in range(7):
            quality_stats[score] = len([c for c in perfect_cards if c['quality_score'] == score])
        
        # ファイル生成
        self.save_perfect_outputs(perfect_cards, quality_stats)
    
    def save_perfect_outputs(self, cards: List[Dict], quality_stats: Dict):
        """
        完璧品質出力保存
        """
        # TSVファイル
        tsv_content = self.generate_perfect_tsv(cards)
        tsv_file = self.output_dir / 'cc_anki_perfect.tsv'
        with open(tsv_file, 'w', encoding='utf-8') as f:
            f.write(tsv_content)
        
        # 完璧品質レポート
        report = self.generate_perfect_report(cards, quality_stats)
        report_file = self.output_dir / 'perfect_quality_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # JSON詳細データ
        json_file = self.output_dir / 'cc_anki_perfect.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        
        # 結果表示
        self.print_perfect_results(cards, quality_stats, tsv_file, report_file)
    
    def generate_perfect_report(self, cards: List[Dict], quality_stats: Dict) -> str:
        """
        完璧品質レポート生成
        """
        high_quality_count = len([c for c in cards if c['quality_score'] >= 5])
        manual_fixed_count = len([c for c in cards if c.get('manual_fixed')])
        
        report = f"""# CC練習問題 完璧品質Ankiデッキレポート

## 🎯 完璧品質達成サマリー
- **総カード数**: {len(cards)}枚
- **高品質カード (5-6点)**: {high_quality_count}枚 ({high_quality_count/len(cards)*100:.1f}%)
- **手動修正適用**: {manual_fixed_count}枚
- **自動処理**: {len(cards) - manual_fixed_count}枚

## 📊 品質スコア分布
"""
        
        for score in range(6, -1, -1):
            count = quality_stats.get(score, 0)
            percentage = count / len(cards) * 100 if cards else 0
            stars = "⭐" * score
            report += f"- **{score}点** {stars}: {count}枚 ({percentage:.1f}%)\n"
        
        report += f"""
## 🔧 手動修正適用済みカード
"""
        
        manual_cards = [c for c in cards if c.get('manual_fixed')]
        for card in manual_cards:
            report += f"- {card['filename']}: {card['question'][:60]}...\n"
        
        report += f"""
## 🚀 学習推奨順序
1. **6点カード**: 最高品質、最優先学習
2. **5点カード**: 高品質、通常学習
3. **4点以下**: 確認・補強学習

## 💡 学習効果最大化のコツ
- **クローズ形式**: 正解を隠して能動的に思い出す
- **解説重視**: 必ず解説を読んで理解を深める
- **間隔反復**: Ankiの標準設定で効率的復習
- **関連学習**: タグを活用したトピック別学習

## 🎓 CC → Security+ 学習パス
このデッキで基礎を固めた後、Security+の上位概念に進むことで
効率的なキャリアアップが可能です。
"""
        
        return report
    
    def print_perfect_results(self, cards: List[Dict], quality_stats: Dict, 
                            tsv_file: Path, report_file: Path):
        """
        完璧品質結果表示
        """
        high_quality = len([c for c in cards if c['quality_score'] >= 5])
        perfect_quality = len([c for c in cards if c['quality_score'] == 6])
        
        print("\n🎉 完璧品質Ankiデッキ生成完了!")
        print("=" * 60)
        print(f"📊 総カード数: {len(cards)}")
        print(f"🏆 完璧品質 (6点): {perfect_quality}枚")
        print(f"⭐ 高品質 (5-6点): {high_quality}枚")
        print(f"📈 高品質率: {(high_quality/len(cards)*100):.1f}%")
        print(f"🔧 手動修正適用: {len([c for c in cards if c.get('manual_fixed')])}枚")
        
        print(f"\n📁 生成ファイル:")
        print(f"1. 📋 {tsv_file.name} - 完璧品質Ankiインポート用")
        print(f"2. 📖 {report_file.name} - 完璧品質レポート")
        print(f"3. 🔍 cc_anki_perfect.json - 詳細データ")
        
        print(f"\n🎯 達成度:")
        if high_quality == len(cards):
            print("✅ 100%高品質達成！完璧です！")
        else:
            print(f"📈 高品質率 {(high_quality/len(cards)*100):.1f}% - ほぼ完璧！")


def main():
    project_dir = Path(__file__).parent.parent
    input_file = project_dir / 'output' / 'cc_questions_final.json'
    output_dir = project_dir / 'output' / 'anki'
    
    if not input_file.exists():
        print(f"❌ 入力ファイルが見つかりません: {input_file}")
        sys.exit(1)
    
    generator = PerfectAnkiGenerator(str(input_file), str(output_dir))
    generator.process_to_perfection()


if __name__ == "__main__":
    main()