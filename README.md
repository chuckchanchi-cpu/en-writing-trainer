# ✍️ en-writing-trainer — 英文寫作訓練（P.6 考試程度）

英文作文資料係**章節精華＋必考元素**。本 app 整合所有教過嘅寫作元素：訓練、提醒、AI 批改。

## 三大模式
| 模式 | 功能 |
|------|------|
| 📖 技巧操練 | 語法元素 MCQ（Similes／Reported Speech／Past Tense／-ed -ing／Connectives／Structure／5W1H），每題附「記得用」提醒 |
| 🧰 寫作工具箱 | 7 大寫作元素速查（規則＋例句＋提醒＋常見錯誤）＋ 考試 Checklist |
| ✍️ 寫作任務 | 寫短段落（80-120 字）→ AI 按 checklist 批改：元素檢查／文法修正／評語／升級示範／分數 |

## 寫作元素（必考）
Similes（as + adj + as）｜Reported Speech（told/ask + (not) to）｜Past Tense｜
-ed/-ing Adjectives｜Connectives（and/but/although/because/so + 順序詞）｜
Story Structure（四段式：setting→經過→結局教訓）｜5W1H 擴句

## 執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 測試
```bash
python3 _smoke_test.py
```

## AI 批改配置（Settings → Secrets）
```toml
OPENAI_API_KEY = "..."
OPENAI_MODEL_NAME = "qwen3.8-flash"
OPENAI_API_BASE = "https://api.silra.cn/v1"
```
