#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_smoke_test.py — en-writing-trainer 冒煙測試"""
import ast
import json
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
fail = 0
src = open("app.py", encoding="utf-8").read()
try:
    ast.parse(src)
    print("✅ app.py syntax OK")
except SyntaxError as e:
    print(f"❌ syntax error: {e}")
    fail += 1

# 工具箱元素齊全
for tid in ["simile", "rspeech", "past", "eding", "connect", "structure", "expand"]:
    if f'"id": "{tid}"' in src:
        print(f"✅ tool {tid} 有")
    else:
        print(f"❌ tool {tid} 缺")
        fail += 1

# writing_bank.json 題庫完整性
with open("writing_bank.json", encoding="utf-8") as f:
    QB = json.load(f)
assert len(QB) >= 10, f"應該至少 10 個 topic，實際 {len(QB)}"
total = 0
for k, v in QB.items():
    qs = v["questions"]
    total += len(qs)
    for item in qs:
        assert len(item) == 5, f"{k}: tuple len != 5"
        typ, q, ans, opts, hint = item
        assert isinstance(opts, list) and len(opts) == 4, f"{k}: 選項唔夠 4 個"
        assert ans in opts, f"{k}: 答案唔喺選項入面: {ans} | {opts}"
        assert q and ans and hint, f"{k}: 空欄位"
        assert len(opts) == len(set(opts)), f"{k}: 重複選項: {opts}"
    print(f"✅ {v['name']}: {len(qs)} 題")
print(f"✅ QUESTION_BANK total: {total} 題, {len(QB)} topics")

# 作文任務齊（至少 5 個：fiona/diary/free/helping/chef）
for tid in ["fiona", "diary", "free", "helping", "chef"]:
    if f'"id": "{tid}"' in src:
        print(f"✅ task {tid} 有")
    else:
        print(f"❌ task {tid} 缺")
        fail += 1

print("done" if fail == 0 else f"FAILED ({fail})")
sys.exit(1 if fail else 0)
