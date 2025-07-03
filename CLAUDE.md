# CLAUDE.md - Anki Deck Generator Project

このファイルは Anki Deck Generator プロジェクト専用の設定・ガイドファイルです。

## 📋 プロジェクト概要

### 🎯 目的
TOEFL 3800 Rank3の英単語について、高品質なAnki暗記カードの裏面を自動生成するシステムの構築。

### 🔄 背景
- **手動作業の自動化**: これまでChatGPTに1つ1つ手動投稿していた作業を自動化
- **学習履歴継続**: 既存AnkiデッキのGUIDを保持して学習進捗を維持
- **品質向上**: 語源・例文・記憶術を含む高品質な学習コンテンツ生成

## 📁 プロジェクト構造

```
/home/user/.pg/development-projects/anki-deck-generator/
├── CLAUDE.md                    # このファイル
├── data/
│   ├── input/
│   │   └── toefl3800__rank3.txt # 元データ（ホームディレクトリからコピー）
│   ├── output/
│   │   └── enhanced_deck.txt    # 生成結果
│   └── temp/                    # 一時ファイル
├── scripts/
│   ├── word_extractor.py        # 英単語抽出スクリプト
│   ├── ai_processor.py          # AI処理（ChatGPT/Gemini/Claude）
│   └── deck_generator.py        # 最終デッキ生成
└── config/
    ├── prompts.txt              # AIプロンプトテンプレート
    └── settings.json            # 設定ファイル
```

## 📊 入力データフォーマット

**toefl3800__rank3.txt の構造**:
```
[GUID]	Basic	toefl3800::rank3	[英単語]	[日本語訳]	[追加情報]
```

**例**:
```
rOl.*)J=yE	Basic	toefl3800::rank3	ambush	待ち伏せて急襲する	
```

## 🎯 目標出力フォーマット

**強化された Anki カード**:
```
[GUID]	Basic	toefl3800::rank3	[英単語]	[強化された裏面コンテンツ]	
```

**裏面コンテンツ構造**:
```
[意味（1つでも複数でも可）]

[英語例文①（訳なし）]  
[英語例文②（訳なし）]  
[英語例文③（訳なし）]

[覚えるためのTips（語源または語呂合わせなど）]
```

## 🤖 AI処理選択肢

### 1. ChatGPT API
**メリット**:
- ✅ 品質確認済み（手動テスト実施済み）
- ✅ 高品質な語源説明・関連語彙
- ✅ 自然で実用的な例文生成

**デメリット**:
- ❌ API料金が発生
- ❌ API設定・認証が必要
- ❌ レート制限あり

### 2. Gemini CLI
**メリット**:
- ✅ 無料（VPS上で認証済み）
- ✅ 24時間稼働可能
- ✅ フォーマット遵守良好

**デメリット**:
- ⚠️ 語源説明がシンプル
- ⚠️ 関連語彙への言及少ない
- ❓ 大量処理での品質一貫性未確認

### 3. Claude Code（このセッション）
**メリット**:
- ✅ プロジェクト文脈完全理解
- ✅ りょうくんの学習目標把握済み
- ✅ 高品質出力

**デメリット**:
- ❌ セッション制限
- ❌ 大量自動処理に不向き
- ❌ 費用効率悪い

## 🔄 処理ワークフロー案

### Phase 1: データ準備
1. `toefl3800__rank3.txt` から英単語とGUID抽出
2. 処理対象リスト作成（約1159語）
3. バッチ処理の分割設計

### Phase 2: AI処理選択
**選択肢A: 高品質重視（ChatGPT API）**
```bash
# API設定 → 自動バッチ処理 → 品質確認
```

**選択肢B: 費用重視（Gemini CLI）**
```bash
# Gemini CLI → 一部Claude補強 → 品質向上
```

**選択肢C: ハイブリッド**
```bash
# Gemini CLI初回生成 → ChatGPT品質向上 → 最適化
```

### Phase 3: 結果統合
1. AI生成結果の品質チェック
2. GUID付きAnki形式への再構成
3. インポート可能ファイル生成

## 🎯 戦略A: セッション継続型処理（実装決定）

### 📋 基本コンセプト
- **Claude Code主導**: API料金を避けて、セッション内での高品質生成
- **セッション分割**: 1セッション約100-200語を処理、継続的実行
- **プログレス管理**: 進捗追跡とセッション間引き継ぎシステム

### 🔢 処理規模と分割戦略

**総処理対象**: 1159語 (TOEFL 3800 Rank3)  
**現在完了**: 8語 (ambush, bountiful, inhale, crane, inflame, predecessor, meager, alternative)  
**残り**: 1151語

**セッション分割案**:
```
セッション1: 語彙001-100 (100語) 
セッション2: 語彙101-200 (100語)
セッション3: 語彙201-300 (100語)
...
セッション12: 語彙1101-1159 (59語)
```

### 🔄 セッション継続システム

#### 1. プログレス管理ファイル
```
data/progress/
├── session_progress.json     # 全体進捗管理
├── current_batch.json        # 現在処理中バッチ
├── completed_words.json      # 完了済み単語リスト
└── session_logs/             # セッション別ログ
    ├── session_001.log
    ├── session_002.log
    └── ...
```

#### 2. セッション間引き継ぎデータ
```json
{
  "total_words": 1159,
  "completed": 8,
  "current_session": 1,
  "current_batch_start": 9,
  "current_batch_end": 108,
  "last_processed_word": "alternative",
  "next_words": ["offset", "outcome", "..."],
  "session_strategy": "claude-code-direct",
  "quality_metrics": {
    "avg_definition_length": 35,
    "avg_examples_count": 3,
    "etymology_completion_rate": 100
  }
}
```

### ⚙️ 実装アーキテクチャ

#### 1. 強化済みプロセッサ拡張
```python
# scripts/enhanced_anki_processor.py に追加機能
class SessionManager:
    def load_progress()      # 進捗復元
    def save_progress()      # 進捗保存
    def get_next_batch()     # 次バッチ取得
    def handle_session_end() # セッション終了処理
```

#### 2. 語彙データベース拡張
```python
# 完了済み語彙の品質確保
def extend_hardcoded_vocabulary():
    # _generate_meaning() を段階的拡張
    # _generate_examples() を段階的拡張  
    # _generate_etymology_tips() を段階的拡張
```

#### 3. セッション終了時の安全保存
```python
def safe_session_end():
    """セッション終了前の必須処理"""
    save_current_progress()
    backup_to_github()
    create_session_summary()
    prepare_next_session_instructions()
```

### 📊 品質管理システム

#### 1. 一貫性チェック
- GUID重複確認
- フィールドフォーマット統一
- CSS/HTML構造維持

#### 2. 品質メトリクス
- 定義の適切性（日本語自然性）
- 例文の実用性（TOEFL適合度）
- 語源説明の記憶定着効果

#### 3. エラーハンドリング
```python
def quality_check_word(word_data):
    """生成内容の品質確認"""
    checks = [
        validate_definition_japanese(),
        validate_examples_english(),
        validate_etymology_historical_accuracy(),
        validate_html_css_structure()
    ]
    return all(checks)
```

### 🚀 実行フロー

#### セッション開始時
1. **進捗確認**: `session_progress.json` 読み込み
2. **バッチ設定**: 現在位置から次の100語設定
3. **継続処理**: enhanced_anki_processor.py で順次生成

#### セッション中
1. **逐次処理**: 1語ずつ高品質生成・検証
2. **進捗更新**: 5語ごとに中間保存
3. **品質確認**: 生成コンテンツの即座検証

#### セッション終了時
1. **完全保存**: 全成果物をTSV・JSON保存
2. **GitHub同期**: プライベートリポジトリバックアップ
3. **次回準備**: 次セッション用の引き継ぎ情報生成

### 📁 改良版ファイル構造

```
/home/user/.pg/development-projects/anki-deck-generator/
├── CLAUDE.md                    # このファイル（戦略A実装計画）
├── data/
│   ├── input/
│   │   └── toefl3800__rank3.txt # 元データ（1159語）
│   ├── output/
│   │   └── claude-code/         # Claude Code出力（現在8語完了）
│   │       ├── enhanced_deck_v2.tsv
│   │       └── card_template.css
│   ├── progress/                # プログレス管理（NEW）
│   │   ├── session_progress.json
│   │   ├── current_batch.json
│   │   ├── completed_words.json
│   │   └── session_logs/
│   └── backup/                  # セッション間バックアップ
├── scripts/
│   ├── enhanced_anki_processor.py  # メイン処理エンジン
│   ├── session_manager.py          # セッション管理（NEW）
│   └── quality_validator.py        # 品質検証（NEW）
└── session_handoff/             # セッション引き継ぎ（NEW）
    ├── current_session_state.md
    ├── next_session_plan.md
    └── troubleshooting_notes.md
```

## 🎯 学習目標との整合性

**りょうくんのTOEFL目標**: 100+達成
**必要な学習品質**:
- 語源理解による語彙拡張
- 実用的な例文での文脈理解
- 記憶術による定着率向上

**→ 品質重視でChatGPT API推奨、費用面でGemini CLI検討**

## 🚀 VPS環境活用

**24時間稼働の利点**:
- 大量バッチ処理の時間制約なし
- 複数AI併用での品質比較可能
- 段階的改善アプローチ実施可能

## 📝 開発ログ

### 2025-07-03
- プロジェクト開始
- GitHub リポジトリ作成: `anki-deck-generator`
- データ構造分析完了（1159語確認）
- AI選択肢比較実施（ChatGPT API vs Gemini CLI vs Claude Code）
- ChatGPT品質ベンチマーク確認
- Gemini CLI初期テスト実施（ambush → 良好）
- **重大発見**: 手動実装の非現実性（1159語×高品質生成）
- **戦略A決定**: セッション継続型処理（Claude Code主導）
- **Anki最適化**: カスタムノートタイプ＋CSS分離アーキテクチャ
- **品質実証**: 8語完了（高品質確認済み）
- **CSS問題解決**: フロントサイド表示最適化完了

### 技術的成果
- [x] Enhanced TOEFL Vocabularyノートタイプ設計
- [x] 単語ベースGUID生成システム
- [x] CSS/HTML分離フォーマット
- [x] enhanced_anki_processor.py 核心実装
- [x] 高品質8語生成完了（ambush〜alternative）

### 戦略A: セッション継続型処理
- [x] 実装戦略確定
- [x] セッション管理システム設計
- [x] プログレス追跡アーキテクチャ
- [x] 品質保証システム設計
- [x] プロジェクト専用CLAUDE.md更新
- [ ] SessionManagerクラス実装
- [ ] プログレス管理ファイル生成
- [ ] 第1セッション実行（語彙9〜108）

### 🚨 セッション継続の課題と対策

#### 主要課題
1. **情報喪失リスク**: セッション切り替え時のコンテキスト喪失
2. **品質一貫性**: 異なるセッション間での生成品質維持
3. **進捗管理**: 正確な処理状況追跡

#### 対策システム
1. **完全な進捗ファイル化**: JSON形式での状態保存
2. **詳細な引き継ぎドキュメント**: セッション間引き継ぎ情報
3. **品質検証システム**: 一貫性チェック機能
4. **GitHub同期**: セッション成果物の即座バックアップ

### 進行状況
- [x] プロジェクト設計
- [x] データ形式分析  
- [x] AI選択肢調査
- [x] **戦略A決定・詳細設計**
- [x] **Enhanced Ankiシステム実装**
- [x] **セッション管理システム設計**
- [ ] SessionManager実装
- [ ] 本格的語彙生成開始

### 品質メトリクス（8語完了時点）
- **定義品質**: 高（自然な日本語、複数意味対応）
- **例文品質**: 高（実用的、TOEFL適合、文脈多様）
- **語源品質**: 高（歴史的正確性、記憶法統合）
- **一貫性**: 100%（CSS/HTMLフォーマット統一）
- **Anki互換性**: 100%（インポート成功確認済み）

## 🔧 技術仕様

**依存関係**:
- Python 3.12+
- Gemini CLI（認証済み）
- ChatGPT API（選択時）
- 標準ライブラリ（re, json, csv）

**パフォーマンス目標**:
- 処理時間: 制約なし（24時間稼働）
- 品質: TOEFL 100+レベル対応
- 一貫性: 全単語で統一フォーマット

---

**作成日**: 2025-07-03  
**戦略A更新**: 2025-07-03（セッション継続型処理詳細設計完了）  
**プロジェクト責任者**: りょうくん（TOEFL 100+目標）  
**技術サポート**: Claude Code（VPS: 160.251.167.39）  
**実装状況**: 戦略A実装準備完了、SessionManager実装待ち