#!/bin/bash
"""
CC練習問題スクリーンショット OCR処理実行スクリプト
"""

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

# OCR処理を実行
echo "ISC2 CC練習問題スクリーンショット OCR処理を開始します..."
python3 src/ocr_processor.py

echo "処理完了！"
echo "結果ファイル:"
echo "- output/ocr_results.json (詳細なJSON形式)"
echo "- output/cc_questions.txt (読みやすいテキスト形式)"