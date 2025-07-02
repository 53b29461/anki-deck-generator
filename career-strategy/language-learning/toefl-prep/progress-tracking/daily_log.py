#!/usr/bin/env python3
"""
TOEFL学習進捗記録システム
Gemini×Claude×ChatGPT統合戦略による学習管理
"""

import json
import datetime
from pathlib import Path

class TOEFLProgressTracker:
    def __init__(self):
        self.data_file = Path(__file__).parent / "progress_data.json"
        self.load_data()
    
    def load_data(self):
        """進捗データを読み込み"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {"daily_records": [], "vocab_progress": {}, "mock_tests": []}
    
    def save_data(self):
        """進捗データを保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def log_daily_study(self, vocab_count=0, reading_time=0, listening_time=0, 
                       speaking_time=0, writing_time=0, notes=""):
        """日次学習記録"""
        today = datetime.date.today().isoformat()
        record = {
            "date": today,
            "vocab_count": vocab_count,
            "time_breakdown": {
                "reading": reading_time,
                "listening": listening_time,
                "speaking": speaking_time,  
                "writing": writing_time,
                "total": reading_time + listening_time + speaking_time + writing_time
            },
            "notes": notes
        }
        self.data["daily_records"].append(record)
        self.save_data()
        print(f"✅ {today}の学習記録を保存しました")
        print(f"📚 語彙: {vocab_count}語, ⏱️  総学習時間: {record['time_breakdown']['total']}分")
    
    def update_vocab_progress(self, rank, completion_percentage):
        """語彙進捗更新"""
        self.data["vocab_progress"][f"rank_{rank}"] = {
            "completion": completion_percentage,
            "updated_date": datetime.date.today().isoformat()
        }
        self.save_data()
        print(f"📖 TOEFL3800 Rank{rank}: {completion_percentage}%完了")
    
    def add_mock_test(self, reading_score, listening_score, speaking_score, writing_score, notes=""):
        """模試結果記録"""
        total_score = reading_score + listening_score + speaking_score + writing_score
        mock_record = {
            "date": datetime.date.today().isoformat(),
            "scores": {
                "reading": reading_score,
                "listening": listening_score,
                "speaking": speaking_score,
                "writing": writing_score,
                "total": total_score
            },
            "notes": notes
        }
        self.data["mock_tests"].append(mock_record)
        self.save_data()
        print(f"🎯 模試結果記録: R{reading_score} L{listening_score} S{speaking_score} W{writing_score} (合計{total_score})")
    
    def show_progress_summary(self):
        """進捗サマリー表示"""
        print("=" * 50)
        print("🚀 TOEFL学習進捗サマリー")
        print("=" * 50)
        
        # 語彙進捗
        print("📚 語彙進捗 (TOEFL3800):")
        for rank, data in self.data["vocab_progress"].items():
            print(f"  {rank.replace('_', ' ').title()}: {data['completion']}%")
        
        # 最近の学習記録
        if self.data["daily_records"]:
            recent = self.data["daily_records"][-7:]  # 直近7日間
            total_time = sum([r["time_breakdown"]["total"] for r in recent])
            print(f"📊 直近7日間の学習時間: {total_time}分")
        
        # 模試結果推移
        if self.data["mock_tests"]:
            print("🎯 模試結果推移:")
            for test in self.data["mock_tests"][-3:]:  # 直近3回
                score = test["scores"]
                print(f"  {test['date']}: 合計{score['total']}点 (R{score['reading']} L{score['listening']} S{score['speaking']} W{score['writing']})")

if __name__ == "__main__":
    import sys
    tracker = TOEFLProgressTracker()
    
    if len(sys.argv) == 1:
        tracker.show_progress_summary()
    elif sys.argv[1] == "log":
        # 使用例: python daily_log.py log 50 30 15 20 15 "Rank3単語50語、Reading精読"
        if len(sys.argv) >= 7:
            vocab, reading, listening, speaking, writing = map(int, sys.argv[2:7])
            notes = sys.argv[7] if len(sys.argv) > 7 else ""
            tracker.log_daily_study(vocab, reading, listening, speaking, writing, notes)
        else:
            print("使用法: python daily_log.py log <語彙数> <Reading分> <Listening分> <Speaking分> <Writing分> [メモ]")
    elif sys.argv[1] == "vocab":
        # 使用例: python daily_log.py vocab 3 85
        if len(sys.argv) >= 4:
            rank, percentage = int(sys.argv[2]), int(sys.argv[3])
            tracker.update_vocab_progress(rank, percentage)
        else:
            print("使用法: python daily_log.py vocab <ランク> <完了率%>")
    elif sys.argv[1] == "mock":
        # 使用例: python daily_log.py mock 25 23 18 22 "初回模試"
        if len(sys.argv) >= 6:
            r, l, s, w = map(int, sys.argv[2:6])
            notes = sys.argv[6] if len(sys.argv) > 6 else ""
            tracker.add_mock_test(r, l, s, w, notes)
        else:
            print("使用法: python daily_log.py mock <R> <L> <S> <W> [メモ]")