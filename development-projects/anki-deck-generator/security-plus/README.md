# 🔥 Security+ Anki デッキ - "be perfect" キャンペーン成果

## 📊 デッキ概要
- **総用語数**: 108語（100%処理成功）
- **生成日**: 2025-07-23 16:18:16
- **対象試験**: CompTIA Security+ (SY0-601/701)
- **設計方針**: 略称優先、実務例重視、カテゴリ分類

## 📁 ファイル構成
```
security-plus/
├── raw_terms.txt                 # 原文用語リスト
├── process_terms.py             # 処理スクリプト
├── security_plus_deck.tsv       # 生データTSV
├── Security_Plus_Deck_Final.tsv # Anki用最終ファイル ⭐
└── README.md                    # このファイル
```

## 🎯 カテゴリ別内訳
- **脅威・攻撃** (threats_attacks): 15語
- **暗号化** (cryptography): 13語  
- **リスク・コンプライアンス** (risk_compliance): 12語
- **データプライバシー** (data_privacy): 10語
- **インシデント対応** (incident_response): 10語
- **アクセス制御** (access_control): 9語
- **ネットワークセキュリティ** (network_security): 7語
- **セキュリティテスト** (security_testing): 7語
- **新興技術** (emerging_tech): 6語
- **一般** (general): 19語

## 🚀 Ankiインポート手順

### 1. ファイル準備
```bash
# 最終ファイルをローカルにダウンロード
scp conoha-server:~/.pg/development-projects/anki-deck-generator/security-plus/Security_Plus_Deck_Final.tsv ./
```

### 2. Ankiインポート
1. Anki起動
2. `ファイル` → `インポート`
3. `Security_Plus_Deck_Final.tsv` を選択
4. 設定:
   - **フィールドの区切り**: タブ
   - **HTMLを許可**: ✅ チェック
   - **デッキ**: "Security+ 2025" (新規作成)
   - **ノートタイプ**: Basic

### 3. 学習設定推奨値
- **新規カード/日**: 10-20枚
- **復習上限**: 200枚
- **学習ステップ**: 1分 10分
- **再学習ステップ**: 10分
- **卒業間隔**: 1日
- **簡単間隔**: 4日

## 🎨 カード表示例

**Front面**: `PKI`

**Back面**:
```
Public Key Infrastructure
正式名称: Public Key Infrastructure
定義: 公開鍵暗号方式を利用した認証基盤
実例: デジタル証明書の発行・管理、WebサーバーのSSL証明書
カテゴリ: cryptography
```

## 💡 学習戦略 (Gemini推奨)

### Phase 1: 基礎定着 (1-2週間)
- 略称 → 正式名称の暗記
- 基本定義の理解
- カテゴリ別グループ学習

### Phase 2: 実践強化 (2-3週間)  
- 実務例の詳細理解
- カテゴリ間の関連性把握
- 混合問題での応用

### Phase 3: 試験対策 (1-2週間)
- 高速レビュー
- 弱点分野の集中学習
- 実際の試験形式での練習

## 📈 進捗追跡
- Anki統計機能で毎日進捗確認
- 苦手カテゴリの特定・強化
- 7日間の復習率90%以上を目標

## 🔗 関連リソース
- [CompTIA Security+ 公式サイト](https://www.comptia.org/certifications/security)
- [NIST サイバーセキュリティフレームワーク](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

---

**作成者**: Claude Code + りょうくん  
**最適化**: Gemini 3AI協議システム  
**品質方針**: "be perfect" キャンペーン 🔥