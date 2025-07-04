#!/usr/bin/env python3
"""
シンプルなOCR処理（テスト用）
"""

import os
import sys
from pathlib import Path
import pytesseract
from PIL import Image
import json


def simple_ocr_test(input_dir: str, output_dir: str):
    """
    シンプルなOCRテスト
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 最初の5枚だけテスト
    image_files = list(input_path.glob('*.png'))[:5]
    
    results = []
    
    for img_file in image_files:
        print(f"処理中: {img_file.name}")
        
        try:
            # 画像を開く
            image = Image.open(img_file)
            
            # OCR実行（設定なし）
            text = pytesseract.image_to_string(image)
            
            result = {
                'filename': img_file.name,
                'text': text,
                'success': True
            }
            
            print(f"抽出成功: {len(text)}文字")
            
        except Exception as e:
            print(f"エラー: {e}")
            result = {
                'filename': img_file.name,
                'error': str(e),
                'success': False
            }
        
        results.append(result)
    
    # 結果を保存
    with open(output_path / 'simple_ocr_test.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 最初の1つの内容を表示
    if results and results[0].get('success'):
        print(f"\n最初の画像のOCR結果:\n{results[0]['text'][:500]}...")
    
    print(f"\n結果を保存: {output_path / 'simple_ocr_test.json'}")


if __name__ == "__main__":
    project_dir = Path(__file__).parent.parent
    input_dir = project_dir / 'input' / 'screenshots'
    output_dir = project_dir / 'output'
    
    simple_ocr_test(str(input_dir), str(output_dir))