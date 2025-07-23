#!/usr/bin/env python3
"""
Security+ 用語集をAnki用TSVファイルに変換するスクリプト
Gemini戦略に基づく最適化実装
"""

import re
import csv
import json
from datetime import datetime

# カテゴリ分類ルール（Gemini推奨）
CATEGORIES = {
    'cryptography': [
        '暗号化', '復号化', 'ハッシュ関数', 'デジタル署名', 'PKI', 'SSL/TLS',
        '量子暗号', 'ポストクォンタム暗号', '同形暗号', '暗号アジリティ',
        'ゼロ知識証明', '差分プライバシー'
    ],
    'network_security': [
        'VPN', 'ファイアウォール', 'IDS', 'IPS', '中間者攻撃', 'DDoS攻撃',
        'IoTセキュリティ', 'SSL/TLS'
    ],
    'access_control': [
        '認証', '認可', 'アカウンタビリティ', '多要素認証', 'シングルサインオン',
        'LDAP', 'RBAC', 'ACL', 'CIA'
    ],
    'threats_attacks': [
        'ソーシャルエンジニアリング', 'フィッシング', 'スピアフィッシング',
        'マルウェア', 'ランサムウェア', 'トロイの木馬', 'ルートキット',
        'ボットネット', 'SQLインジェクション', 'XSS', 'CSRF',
        'バッファオーバーフロー', '特権昇格', 'APT', 'ゼロデイ攻撃'
    ],
    'risk_compliance': [
        'リスクアセスメント', 'コンプライアンス', 'GDPR', 'HIPAA',
        'PCI DSS', 'ISO 27001', 'NIST', 'セキュリティガバナンス',
        'セキュリティポリシー', 'リスクレジスタ', 'KRI', 'KPI'
    ],
    'incident_response': [
        'インシデント対応', '災害復旧', '事業継続計画', 'SOC', 'SIEM',
        'SOAR', '脅威インテリジェンス', 'CTI', 'IOC', 'TTPs'
    ],
    'security_testing': [
        '脆弱性スキャン', 'ペネトレーションテスト', 'レッドチーム',
        'ブルーチーム', 'パープルチーム', 'ハニーポット', 'サンドボックス'
    ],
    'data_privacy': [
        'データ損失防止', 'データガバナンス', 'データプライバシー',
        'プライバシー影響評価', 'データ保護影響評価', '忘れられる権利',
        'データポータビリティ', 'データ最小化', 'データ匿名化', 'データ仮名化'
    ],
    'emerging_tech': [
        'クラウドセキュリティ', 'DevSecOps', 'セキュリティバイデザイン',
        'プライベート情報検索', 'フェデレーテッドラーニング', '秘密計算'
    ]
}

def categorize_term(term_key):
    """用語をカテゴリに分類"""
    for category, keywords in CATEGORIES.items():
        if any(keyword in term_key for keyword in keywords):
            return category
    return 'general'

def extract_abbreviation(term_raw):
    """正式名称から略称を抽出（例: Multi-Factor Authentication, MFA → MFA）"""
    # パターン1: (略称) 形式
    match = re.search(r'\(([A-Z]+[A-Za-z0-9]*)\)', term_raw)
    if match:
        return match.group(1)
    
    # パターン2: 略称, 正式名称 形式
    match = re.search(r'^([A-Z]{2,})', term_raw)
    if match:
        return match.group(1)
    
    # パターン3: 英語名から略称を推測
    words = re.findall(r'\b[A-Z][a-z]*', term_raw)
    if len(words) >= 2:
        return ''.join(word[0] for word in words[:3])
    
    return term_raw

def parse_term_line(line):
    """用語行を解析して構造化データに変換"""
    if ':' not in line:
        return None
    
    parts = line.split(':', 1)
    if len(parts) != 2:
        return None
    
    term_raw = parts[0].strip()
    definition = parts[1].strip()
    
    # 英語部分と日本語部分を分離
    japanese_match = re.search(r'（(.+?)）', term_raw)
    if japanese_match:
        english_term = term_raw.replace(japanese_match.group(0), '').strip()
        japanese_term = japanese_match.group(1)
    else:
        english_term = term_raw
        japanese_term = term_raw
    
    # 略称を抽出
    abbreviation = extract_abbreviation(english_term)
    
    # カテゴリを判定
    category = categorize_term(term_raw)
    
    return {
        'abbreviation': abbreviation,
        'english_term': english_term,
        'japanese_term': japanese_term,
        'definition': definition,
        'category': category,
        'priority': 'high' if abbreviation != english_term else 'medium'
    }

def generate_practical_examples(term_data):
    """実務例を生成（Security+試験対策重視）"""
    examples = {
        'PKI': 'デジタル証明書の発行・管理、WebサーバーのSSL証明書',
        'VPN': 'リモートワーク時の安全な企業ネットワーク接続',
        'MFA': '銀行ATM（カード＋PIN）、クラウドサービス（パスワード＋SMS）',
        'ACL': 'ルーター設定、ファイルサーバーのアクセス権限',
        'IDS': 'ネットワーク監視、不正侵入の検知・ログ記録',
        'DDoS攻撃': 'ボットネットによる大量アクセスでサーバーダウン',
        'SIEM': 'セキュリティログの収集・分析・可視化プラットフォーム',
        'GDPR': 'EU居住者の個人データ処理に関する同意取得・削除権',
    }
    
    abbr = term_data['abbreviation']
    if abbr in examples:
        return examples[abbr]
    
    # カテゴリベースのデフォルト例
    category_examples = {
        'cryptography': '暗号化通信、データ保護、認証システム',
        'network_security': 'ファイアウォール設定、トラフィック監視',
        'access_control': 'ユーザー権限管理、認証システム',
        'threats_attacks': 'サイバー攻撃の手法、セキュリティ対策',
        'risk_compliance': '規制遵守、リスク管理プロセス',
        'incident_response': 'セキュリティインシデント対応手順',
        'security_testing': 'セキュリティ評価、脆弱性検査',
        'data_privacy': '個人情報保護、プライバシー対策',
        'emerging_tech': '最新技術、将来のセキュリティ',
    }
    
    return category_examples.get(term_data['category'], 'セキュリティ関連技術・概念')

def process_security_terms():
    """Security+用語集を処理してTSV生成"""
    print("🔥 Security+ Anki デッキ生成開始 - 'be perfect'キャンペーン実行中")
    
    # 用語リストを読み込み
    with open('raw_terms.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    processed_terms = []
    stats = {'total': 0, 'processed': 0, 'categories': {}}
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('Security+'):
            continue
            
        stats['total'] += 1
        term_data = parse_term_line(line)
        
        if term_data:
            # 実務例を追加
            term_data['practical_example'] = generate_practical_examples(term_data)
            processed_terms.append(term_data)
            stats['processed'] += 1
            
            # カテゴリ統計
            category = term_data['category']
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            print(f"✅ 処理完了: {term_data['abbreviation']} ({category})")
        else:
            print(f"⚠️  解析失敗: {line[:50]}...")
    
    # TSV出力（Anki互換）
    output_file = 'security_plus_deck.tsv'
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        
        # ヘッダー
        writer.writerow([
            'Front', 'Japanese', 'English_Full', 'Definition', 
            'Practical_Example', 'Category', 'Priority'
        ])
        
        # データ行（優先度順にソート）
        sorted_terms = sorted(processed_terms, 
                            key=lambda x: (x['priority'] == 'medium', x['category'], x['abbreviation']))
        
        for term in sorted_terms:
            writer.writerow([
                term['abbreviation'],
                term['japanese_term'],
                term['english_term'],
                term['definition'],
                term['practical_example'],
                term['category'],
                term['priority']
            ])
    
    # 統計レポート
    print(f"\n📊 処理統計:")
    print(f"  総用語数: {stats['total']}")
    print(f"  処理成功: {stats['processed']}")
    print(f"  成功率: {stats['processed']/stats['total']*100:.1f}%")
    print(f"\n📁 カテゴリ別内訳:")
    for category, count in sorted(stats['categories'].items()):
        print(f"  {category}: {count}語")
    
    print(f"\n🎯 出力ファイル: {output_file}")
    print(f"📅 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🔥 'be perfect'キャンペーン: 最高品質のSecurity+デッキが完成！")
    
    return output_file, stats

if __name__ == "__main__":
    process_security_terms()