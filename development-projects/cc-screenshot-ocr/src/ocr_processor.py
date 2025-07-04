#!/usr/bin/env python3
"""
ISC2 CC練習問題スクリーンショット OCR処理スクリプト
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
import re
from pathlib import Path
import json
from typing import Dict, List, Optional


class CCScreenshotOCR:
    """
    ISC2 CC練習問題スクリーンショットのOCR処理クラス
    """
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # OCR設定
        self.tesseract_config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:?!()[]{}"-\' \n'
        
        # 処理統計
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'errors': 0,
            'questions_found': 0
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        画像の前処理（OCR精度向上）
        """
        # 画像読み込み
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"画像を読み込めません: {image_path}")
        
        # グレースケール変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ノイズ除去
        denoised = cv2.medianBlur(gray, 3)
        
        # コントラスト調整
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 二値化
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def extract_text(self, image_path: str) -> str:
        """
        画像からテキストを抽出
        """
        try:
            # 前処理
            processed_image = self.preprocess_image(image_path)
            
            # OCR実行
            text = pytesseract.image_to_string(processed_image, config=self.tesseract_config)
            
            # テキストクリーニング
            cleaned_text = self.clean_text(text)
            
            return cleaned_text
        
        except Exception as e:
            print(f"OCR処理エラー [{image_path}]: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        OCRで抽出したテキストのクリーニング
        """
        # 改行を統一
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # 余分な空白を削除
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n +', '\n', text)
        text = re.sub(r' +\n', '\n', text)
        
        # 連続する改行を削除
        text = re.sub(r'\n\n+', '\n\n', text)
        
        # 先頭末尾の空白を削除
        text = text.strip()
        
        return text
    
    def parse_question(self, text: str, filename: str) -> Dict:
        """
        OCRテキストから問題構造を解析
        """
        question_data = {
            'filename': filename,
            'raw_text': text,
            'question': '',
            'choices': [],
            'correct_answer': '',
            'explanation': '',
            'score': '',
            'parsed_successfully': False
        }
        
        # スコア情報を抽出
        score_match = re.search(r'Score\s*(\d+)', text)
        if score_match:
            question_data['score'] = score_match.group(1)
        
        # 正解マーク（チェック）を検出
        correct_mark_pattern = r'[✓✔☑]'
        
        # 選択肢パターンを検出
        choice_patterns = [
            r'([A-D])[):.]?\s*([^\n]+)',  # A) content, A. content, A: content
            r'([A-D])\s+([^\n]+)',       # A content
        ]
        
        lines = text.split('\n')
        question_lines = []
        choices = []
        explanation_lines = []
        
        in_explanation = False
        found_choices = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 説明セクションの開始を検出
            if 'explanation' in line.lower() or 'correct answer' in line.lower():
                in_explanation = True
                continue
            
            # 選択肢を検出
            choice_found = False
            for pattern in choice_patterns:
                match = re.match(pattern, line)
                if match:
                    choice_letter = match.group(1)
                    choice_text = match.group(2).strip()
                    
                    # 正解かどうかを判定
                    is_correct = bool(re.search(correct_mark_pattern, line))
                    
                    choices.append({
                        'letter': choice_letter,
                        'text': choice_text,
                        'is_correct': is_correct
                    })
                    
                    if is_correct:
                        question_data['correct_answer'] = choice_letter
                    
                    choice_found = True
                    found_choices = True
                    break
            
            if choice_found:
                continue
            
            # 説明部分
            if in_explanation:
                explanation_lines.append(line)
            elif not found_choices:
                # 問題文
                question_lines.append(line)
        
        # データを整理
        question_data['question'] = ' '.join(question_lines).strip()
        question_data['choices'] = choices
        question_data['explanation'] = ' '.join(explanation_lines).strip()
        
        # パース成功判定
        if question_data['question'] and len(choices) >= 2:
            question_data['parsed_successfully'] = True
            self.stats['questions_found'] += 1
        
        return question_data
    
    def process_single_file(self, image_path: Path) -> Dict:
        """
        単一ファイルの処理
        """
        print(f"処理中: {image_path.name}")
        
        # OCR実行
        text = self.extract_text(str(image_path))
        
        if not text:
            return {'error': 'OCR処理に失敗しました'}
        
        # 問題構造の解析
        question_data = self.parse_question(text, image_path.name)
        
        return question_data
    
    def process_all_screenshots(self):
        """
        全スクリーンショットの処理
        """
        print("CC練習問題スクリーンショット OCR処理を開始します...")
        
        # 画像ファイルを取得
        image_extensions = {'.png', '.jpg', '.jpeg'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(list(self.input_dir.glob(f'*{ext}')))
        
        image_files.sort()
        self.stats['total_files'] = len(image_files)
        
        print(f"発見した画像ファイル: {len(image_files)}個")
        
        # 処理結果を保存するリスト
        all_results = []
        
        # 各ファイルを処理
        for image_path in image_files:
            try:
                result = self.process_single_file(image_path)
                all_results.append(result)
                self.stats['processed'] += 1
                
                # 進捗表示
                progress = (self.stats['processed'] / self.stats['total_files']) * 100
                print(f"進捗: {progress:.1f}% ({self.stats['processed']}/{self.stats['total_files']})")
                
            except Exception as e:
                print(f"エラー [{image_path.name}]: {e}")
                self.stats['errors'] += 1
                all_results.append({
                    'filename': image_path.name,
                    'error': str(e)
                })
        
        # 結果を保存
        self.save_results(all_results)
        self.save_structured_text(all_results)
        self.print_summary()
    
    def save_results(self, results: List[Dict]):
        """
        処理結果をJSONファイルに保存
        """
        output_file = self.output_dir / 'ocr_results.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"処理結果を保存しました: {output_file}")
    
    def save_structured_text(self, results: List[Dict]):
        """
        構造化されたテキストファイルに保存
        """
        output_file = self.output_dir / 'cc_questions.txt'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ISC2 Certificate in Cybersecurity (CC) 練習問題\n")
            f.write("=" * 50 + "\n\n")
            
            question_num = 1
            for result in results:
                if result.get('parsed_successfully'):
                    f.write(f"問題 {question_num}: {result.get('filename', '')}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"問題文: {result.get('question', '')}\n\n")
                    
                    # 選択肢
                    for choice in result.get('choices', []):
                        marker = "✓" if choice.get('is_correct') else " "
                        f.write(f"{marker} {choice.get('letter', '')}) {choice.get('text', '')}\n")
                    
                    f.write(f"\n正解: {result.get('correct_answer', '')}\n")
                    
                    if result.get('explanation'):
                        f.write(f"解説: {result.get('explanation')}\n")
                    
                    if result.get('score'):
                        f.write(f"スコア: {result.get('score')}\n")
                    
                    f.write("\n" + "=" * 50 + "\n\n")
                    question_num += 1
        
        print(f"構造化テキストを保存しました: {output_file}")
    
    def print_summary(self):
        """
        処理結果サマリーを表示
        """
        print("\n処理完了サマリー:")
        print("-" * 30)
        print(f"総ファイル数: {self.stats['total_files']}")
        print(f"処理成功: {self.stats['processed']}")
        print(f"エラー: {self.stats['errors']}")
        print(f"問題として解析成功: {self.stats['questions_found']}")
        print(f"成功率: {(self.stats['processed'] / self.stats['total_files'] * 100):.1f}%")


def main():
    """
    メイン実行関数
    """
    # プロジェクトパス
    project_dir = Path(__file__).parent.parent
    input_dir = project_dir / 'input' / 'screenshots'
    output_dir = project_dir / 'output'
    
    # 入力ディレクトリの確認
    if not input_dir.exists():
        print(f"入力ディレクトリが見つかりません: {input_dir}")
        sys.exit(1)
    
    # OCR処理実行
    ocr = CCScreenshotOCR(str(input_dir), str(output_dir))
    ocr.process_all_screenshots()


if __name__ == "__main__":
    main()