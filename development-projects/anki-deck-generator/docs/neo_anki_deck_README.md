# neo-anki-deck

GPT-o3 APIを使用してTOEFL英単語フラッシュカードを自動生成するツール

## 機能

- **GPT-o3 API統合**: OpenAIの最新モデルを使用
- **高品質フラッシュカード**: TOEFL試験に特化した4列TSV形式
- **バッチ処理**: 20語ずつの効率的な処理
- **複数形式出力**: TSV（Anki用）とJSON（バックアップ用）

## 出力フォーマット

| 列名 | 内容 |
|------|------|
| Front | 英単語 |
| JP訳 | 日本語訳（試験重要義） |
| Label | 記憶カテゴリ（語法/語源/語呂合わせ/紛らわしい語/同義語） |
| 説明 | 補足情報（40文字以内） |

## 使用方法

### 1. 依存関係インストール

```bash
cd ~/.pg/development-projects/neo-anki-deck
pip install -r requirements.txt
```

### 2. 実行

```bash
python main.py
```

### 3. 出力ファイル

- `output/neo_anki_deck_YYYYMMDD_HHMMSS.tsv` - Ankiインポート用
- `output/neo_anki_deck_YYYYMMDD_HHMMSS.json` - バックアップ用

## 対象単語（102語）

TOEFL頻出単語リスト：
journal, justify, legislate, levy, logical, manipulate, manual, mature, mediate, methodology, minimize, mutual, negate, norm, notion, objective, obtain, occupy, offset, ongoing, orient, outcome, output, overall, overlap, paradigm, parameter, perceive, persistent, perspective, phenomenon, phase, philosophy, physical, policy, pose, practitioner, precede, precise, predominant, preliminary, presume, prime, principal, proceed, prohibit, prospect, protocol, pursue, qualitative, random, rational, refine, regime, reinforce, relevant, reluctant, rely, reside, resolve, restore, restrain, retain, reveal, rigid, scenario, scheme, scope, sector, secure, segment, sequence, simulate, sole, source, specify, sphere, stable, statistic, straightforward, strategy, stress, subsequent, substitute, successor, sufficient, summary, supplement, sustain, symbolic, terminate, theme, theory, thereby, thesis, trace, tradition, transit, transmit, undergo, unify, unique, utilize, valid, variable, vehicle, version, via, virtual, visible, voluntary

## 設定

`config.py`で以下の設定を変更可能：

- `model`: GPT-o3（デフォルト）
- `max_tokens`: 4000（デフォルト）
- `temperature`: 0.7（デフォルト）
- `batch_size`: 20語（デフォルト）

## Ankiインポート手順

1. Ankiを開く
2. ファイル → インポート
3. 生成されたTSVファイルを選択
4. フィールドマッピングを確認
5. インポート実行

## 注意事項

- APIキーは`main.py`内で直接設定済み
- 大量の単語処理時は API利用料金に注意
- エラー時は個別バッチをスキップして継続処理