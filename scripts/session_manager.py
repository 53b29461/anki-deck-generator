#!/usr/bin/env python3
"""
セッション管理システム
- 進捗追跡・復元
- セッション間引き継ぎ
- 品質管理・バックアップ
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SessionManager:
    def __init__(self, project_root: str = ".."):
        self.project_root = project_root
        self.progress_dir = os.path.join(project_root, "data", "progress")
        self.progress_file = os.path.join(self.progress_dir, "session_progress.json")
        self.session_logs_dir = os.path.join(self.progress_dir, "session_logs")
        
        # 進捗データをロード
        self.progress_data = self.load_progress()
    
    def load_progress(self) -> Dict:
        """進捗データを読み込み"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # デフォルトの進捗データ
            return self._create_default_progress()
    
    def save_progress(self) -> None:
        """進捗データを保存"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Progress saved: {self.progress_file}")
    
    def get_next_batch(self, batch_size: int = 100) -> Tuple[int, int, List[str]]:
        """次に処理するバッチの単語リストを取得"""
        current_start = self.progress_data["current_status"]["current_batch_start"]
        current_end = min(current_start + batch_size - 1, 
                         self.progress_data["project_info"]["total_words"])
        
        # TOEFL 3800 ファイルから単語を抽出
        words = self._extract_words_from_range(current_start, current_end)
        
        return current_start, current_end, words
    
    def _extract_words_from_range(self, start: int, end: int) -> List[str]:
        """指定範囲の単語をTOEFLファイルから抽出"""
        input_file = os.path.join(self.project_root, "data", "input", "toefl3800__rank3.txt")
        words = []
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # 指定範囲の単語を抽出（1-based indexing）
        for i in range(start - 1, min(end, len(lines))):
            if i < len(lines):
                parts = lines[i].split('\t')
                if len(parts) >= 4:
                    word = parts[3]  # 英単語は4列目
                    words.append(word)
        
        return words
    
    def update_progress(self, word: str, position: int) -> None:
        """単語処理完了時の進捗更新"""
        # 完了語彙リストに追加
        if word not in self.progress_data["completed_words_list"]:
            self.progress_data["completed_words_list"].append(word)
        
        # 統計更新
        self.progress_data["current_status"]["completed_words"] = len(
            self.progress_data["completed_words_list"]
        )
        self.progress_data["current_status"]["last_processed_word"] = word
        
        # 5語ごとに中間保存
        if position % 5 == 0:
            self.save_progress()
            print(f"📊 Progress update: {position} words processed")
    
    def start_new_session(self, batch_size: int = 100) -> Dict:
        """新しいセッションを開始"""
        current_session = self.progress_data["current_status"]["current_session"]
        start, end, words = self.get_next_batch(batch_size)
        
        session_info = {
            "session_id": current_session,
            "date": datetime.now().isoformat(),
            "word_range": f"{start}-{end}",
            "target_words": words,
            "estimated_count": len(words),
            "status": "in_progress"
        }
        
        # セッションログ作成
        self._create_session_log(session_info)
        
        print(f"🚀 Session {current_session} started")
        print(f"📝 Processing words {start}-{end} ({len(words)} words)")
        print(f"📋 First 5 words: {words[:5]}")
        
        return session_info
    
    def complete_session(self, words_processed: int) -> None:
        """セッション完了処理"""
        current_session = self.progress_data["current_status"]["current_session"]
        
        # セッション履歴に追加
        session_record = {
            "session_id": current_session,
            "date": datetime.now().isoformat(),
            "words_processed": words_processed,
            "word_range": f"{self.progress_data['current_status']['current_batch_start']}-{self.progress_data['current_status']['current_batch_end']}",
            "status": "completed",
            "notes": f"Processed {words_processed} words successfully"
        }
        
        self.progress_data["session_history"].append(session_record)
        
        # 次セッションの準備
        self.progress_data["current_status"]["current_session"] += 1
        self.progress_data["current_status"]["current_batch_start"] = self.progress_data["current_status"]["current_batch_end"] + 1
        self.progress_data["current_status"]["current_batch_end"] = min(
            self.progress_data["current_status"]["current_batch_start"] + 99,
            self.progress_data["project_info"]["total_words"]
        )
        
        self.save_progress()
        print(f"✅ Session {current_session} completed")
        print(f"📊 Total progress: {self.progress_data['current_status']['completed_words']}/{self.progress_data['project_info']['total_words']} words")
    
    def _create_session_log(self, session_info: Dict) -> None:
        """セッションログファイル作成"""
        log_file = os.path.join(self.session_logs_dir, f"session_{session_info['session_id']:03d}.log")
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"# Session {session_info['session_id']} Log\n")
            f.write(f"Date: {session_info['date']}\n")
            f.write(f"Word Range: {session_info['word_range']}\n")
            f.write(f"Target Count: {session_info['estimated_count']}\n")
            f.write(f"Status: {session_info['status']}\n\n")
            f.write("## Target Words:\n")
            for i, word in enumerate(session_info['target_words'], 1):
                f.write(f"{i:3d}. {word}\n")
    
    def create_handoff_document(self) -> None:
        """セッション引き継ぎドキュメント作成"""
        handoff_file = os.path.join(self.project_root, "session_handoff", "current_session_state.md")
        
        status = self.progress_data["current_status"]
        
        content = f"""# Session Handoff Document
Generated: {datetime.now().isoformat()}

## Current Progress
- **Total Words**: {self.progress_data['project_info']['total_words']}
- **Completed**: {status['completed_words']} words
- **Current Session**: {status['current_session']}
- **Next Batch**: Words {status['current_batch_start']}-{status['current_batch_end']}
- **Last Processed**: {status['last_processed_word']}

## Recently Completed Words
{chr(10).join(f"- {word}" for word in self.progress_data['completed_words_list'][-5:])}

## Next Session Plan
- **Words to Process**: {status['current_batch_end'] - status['current_batch_start'] + 1}
- **Priority**: High
- **Strategy**: Claude Code direct generation
- **Expected Output**: Enhanced TSV with CSS styling

## Quality Standards
- Definition: Natural Japanese, multiple meanings if applicable
- Examples: 3 practical sentences, TOEFL-appropriate
- Etymology: Historical accuracy + memory techniques
- Format: HTML/CSS consistent with existing 8 words

## File Locations
- Progress: `data/progress/session_progress.json`
- Output: `data/output/claude-code/enhanced_deck_v2.tsv`
- CSS: `data/output/claude-code/card_template.css`
- Main Script: `scripts/enhanced_anki_processor.py`
"""
        
        with open(handoff_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📋 Handoff document created: {handoff_file}")
    
    def _create_default_progress(self) -> Dict:
        """デフォルト進捗データ作成"""
        return {
            "project_info": {
                "name": "TOEFL 3800 Rank3 Anki Deck Generator",
                "strategy": "Session-based Claude Code Processing",
                "start_date": datetime.now().isoformat(),
                "total_words": 1159
            },
            "current_status": {
                "completed_words": 0,
                "current_session": 1,
                "current_batch_start": 1,
                "current_batch_end": 100,
                "last_processed_word": "",
                "session_strategy": "claude-code-direct"
            },
            "completed_words_list": [],
            "session_history": [],
            "quality_metrics": {
                "avg_definition_length": 0,
                "avg_examples_count": 3,
                "etymology_completion_rate": 0,
                "css_html_consistency": 100,
                "anki_import_success_rate": 100
            },
            "next_session_plan": {
                "session_id": 1,
                "target_word_range": "1-100", 
                "estimated_words": 100,
                "priority": "high",
                "notes": "Begin systematic processing"
            }
        }

if __name__ == "__main__":
    # テスト実行
    manager = SessionManager()
    
    # 現在の進捗表示
    print("📊 Current Progress:")
    print(f"Completed: {manager.progress_data['current_status']['completed_words']} words")
    print(f"Next batch: {manager.progress_data['current_status']['current_batch_start']}-{manager.progress_data['current_status']['current_batch_end']}")
    
    # 次バッチの単語取得テスト
    start, end, words = manager.get_next_batch(10)  # テスト用に10語
    print(f"\n🎯 Next 10 words ({start}-{end}):")
    for i, word in enumerate(words, start):
        print(f"{i:3d}. {word}")
    
    # 引き継ぎドキュメント作成
    manager.create_handoff_document()