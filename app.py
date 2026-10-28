#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✍️ English Writing Trainer — 英文寫作訓練（P.6 考試程度）

作文資料係章節精華（必考元素）：Similes、Reported Speech、Past Tense、
-ed/-ing Adjectives、Connectives、Story Structure、5W1H 擴句。

三種模式：
  📖 技巧操練 — 語法元素 MCQ（附「記得用」提醒）
  🧰 寫作工具箱 — 所有教過嘅寫作元素速查（寫作前提醒清單）
  ✍️ 寫作任務 — 寫短段落（80-120 字）→ AI 按 checklist 批改＋評語
"""

import os
import json
import re
import random
import requests
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "writing_bank.json"), encoding="utf-8") as f:
    QUESTION_BANK = json.load(f)

st.set_page_config(page_title="✍️ 英文寫作訓練", page_icon="✍️", layout="wide")

# 將 Streamlit Secrets 注入環境變數
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k in st.secrets.keys():
        os.environ[k] = str(st.secrets[k])

def get_api_config():
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "qwen3.8-flash")
    if not base:
        silra_url = os.environ.get("SILRA_API_URL", "")
        if silra_url:
            base = silra_url.replace("/chat/completions", "").rstrip("/")
    if not base:
        base = "https://api.silra.cn/v1"
    return base, key, model

def silra_chat(messages, max_tokens=2000):
    base, key, model = get_api_config()
    if not key:
        return None
    try:
        resp = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.5},
            timeout=120,
        )
        try:
            return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            body = (resp.text or "").strip()[:200]
            st.error(f"❌ API 回應格式錯誤（HTTP {resp.status_code}）：{body or '（空回應）'}")
            st.caption("💡 常見原因：API key 無效／API 地址或模型名稱唔啱（Settings → Secrets）")
            return None
    except Exception as e:
        st.error(f"❌ 連接出錯：{e}")
        return None

# ===== 寫作元素工具箱（章節精華＝必考）=====
TOOLS = [
    {
        "id": "simile",
        "name": "🌈 Similes 明喻（as + adjective + as）",
        "rule": "用 'as + 形容詞原形 + as' 比較兩樣事物，令描述生動。",
        "examples": [
            "as smooth as silk（光滑如絲）", "as gentle as a lamb（溫順如羔羊）", "as wise as an owl（聰明如貓頭鷹）",
            "as happy as a lark（快樂如百靈鳥）", "as cunning as a fox（狡猾如狐狸）", "as light as a feather（輕如羽毛）",
            "as busy as a bee（忙碌如蜜蜂）", "as brave as a lion（勇敢如獅子）", "as slow as a snail（慢如蝸牛）",
            "as pretty as a flower（靚如花）", "as sweet as honey（甜如蜜）", "as wicked as a devil（惡如魔鬼）",
        ],
        "remind": "✏️ 寫作提醒：至少用一個 simile！中間用形容詞原形（as better as ❌）。",
        "mistake": "⚠️ 常見錯誤：比較級入 simile（as happier ❌）；配對錯範疇（as smooth as cotton ❌→silk）",
    },
    {
        "id": "rspeech",
        "name": "💬 Reported Speech 間接引語",
        "rule": "命令句：tell + 人 + to + 原形；Please…：ask + 人 + to + 原形；否定：not to + 原形；代詞要轉（my→her、me→him）。",
        "examples": [
            "\"Take it.\" → He told me to take it.",
            "\"Please stay.\" → They asked me to stay.",
            "\"Don't escape.\" → The witch told Fiona not to escape.",
            "\"Please try my apple.\" → The witch asked Snow White to try her apple.",
        ],
        "remind": "✏️ 寫作提醒：故事有對白時，嘗試用 reported speech 轉述至少一句。",
        "mistake": "⚠️ 常見錯誤：to 後面用咗過去式（to took ❌）；否定寫 to not / don't to ❌",
    },
    {
        "id": "past",
        "name": "📜 Past Tense 敘事過去式",
        "rule": "故事用過去式寫：be → was/were；動詞 → 過去式（go→went, take→took, see→saw）。",
        "examples": [
            "There **was** a beautiful princess called Fiona.",
            "One day, a witch **came** to the palace and **saw** the princess.",
            "The king **told** the prince to help.",
        ],
        "remind": "✏️ 寫作提醒：全篇敘事用過去式；檢查每個動詞！",
        "mistake": "⚠️ 常見錯誤：敘事中途轉咗現在式；不規則動詞寫錯（draw→drew ❌drawed）",
    },
    {
        "id": "eding",
        "name": "😊 -ed / -ing Adjectives",
        "rule": "-ed 描述自己感受（人）；-ing 描述令人有感受嘅事物。",
        "examples": [
            "The children were **excited**. / The ride was **exciting**.",
            "Fiona was **frightened**. / The witch was **frightening**.",
            "We were **amazed** by the magic. / The magic was **amazing**.",
        ],
        "remind": "✏️ 寫作提醒：描寫感受用 -ed（I was surprised），描寫事物用 -ing（a surprising ending）。",
        "mistake": "⚠️ 常見錯誤：It is excited ❌（應 exciting）；I am amazing ❌（應 amazed）",
    },
    {
        "id": "connect",
        "name": "🔗 Connectives 連接詞與順序詞",
        "rule": "and/but/although/because/so 連接句子；first/next/then/after that/finally 排序。",
        "examples": [
            "She was tired, **but** she kept running.",
            "**Although** he was poor, he was happy.（although ≠ but 連用）",
            "**First**, the princess danced. **Next**, the witch came. **Finally**, the prince saved her.",
        ],
        "remind": "✏️ 寫作提醒：用至少 2 個連接詞/順序詞令故事流暢。",
        "mistake": "⚠️ 常見錯誤：although 同 but 連用；because 同 so 連用",
    },
    {
        "id": "structure",
        "name": "🏗️ Story Structure 故事結構（四段式）",
        "rule": "第 1 段：setting（time and place）＋ characters；第 2-3 段：事件經過（起因→發展）；第 4 段：結局＋教訓（positive thinking）。",
        "examples": [
            "Once upon a time, there was a beautiful princess called Fiona.",
            "\"Help! Help!\" shouted Fiona.（對白標點：引號＋驚嘆號）",
            "We learnt that we should be thankful.（正面結局）",
        ],
        "remind": "✏️ 寫作提醒：四段式＋首段有 setting/characters＋結尾有教訓句。",
        "mistake": "⚠️ 常見錯誤：漏 setting；結局冇正面思想；對白冇標點",
    },
    {
        "id": "expand",
        "name": "✏️ 5W1H 擴句",
        "rule": "用 Who/What/When/Where/Why/How 擴寫句子，令內容豐富。",
        "examples": [
            "The princess is pretty. → The princess is as pretty as a flower.",
            "He ran. → He ran quickly because the witch was chasing him.",
        ],
        "remind": "✏️ 寫作提醒：短句要擴寫（加原因、時間、地點、感受）。",
        "mistake": "⚠️ 常見錯誤：句子太短太乾；擴寫後文法出錯",
    },
]

DRILLS = [
    ("Complete: Her eyes are as shiny as _____.", ["stars", "a rose", "honey", "silk"], "stars", "simile", "as shiny as stars ✏️ 寫作記住用一個 simile！"),
    ("Complete: Fiona was as gentle as _____.", ["a lamb", "a lion", "a toad", "a snail"], "a lamb", "simile", "as gentle as a lamb（溫順如羔羊）"),
    ("The witch told Fiona not to escape. This is an example of _____.", ["reported speech", "past tense", "a simile", "5W1H"], "reported speech", "rspeech", "⚠️ reported speech 否定 = told + 人 + not to + 原形"),
    ("Which is correct?", ["The witch told Fiona not to escape.", "The witch told Fiona to not escape.", "The witch said Fiona not escape.", "The witch told Fiona don't escape."], "The witch told Fiona not to escape.", "rspeech", "否定命令固定：not to + 原形"),
    ("Which sentence uses the past tense correctly?", ["There was a princess called Fiona.", "There is a princess called Fiona.", "There were a princess called Fiona.", "There be a princess called Fiona."], "There was a princess called Fiona.", "past", "故事敘事用過去式（was/were）"),
    ("The children were _____ by the magic show.", ["amazed", "amazing", "amaze", "amazement"], "amazed", "eding", "人用 -ed（感到驚嘆）；事物用 -ing"),
    ("The magic show was _____.", ["amazing", "amazed", "amaze", "amazement"], "amazing", "eding", "事物用 -ing（令人驚嘆）"),
    ("_____ the witch was wicked, the princess was kind.", ["Although", "But", "Because", "So"], "Although", "connect", "⚠️ although 唔可以同 but 連用"),
    ("Which connective shows sequence?", ["First", "Because", "But", "Although"], "First", "connect", "順序詞：first/next/then/finally"),
    ("The 1st paragraph of a story must include _____.", ["the setting and the characters", "the ending", "the lesson", "the dialogue marks"], "the setting and the characters", "structure", "首段要有 setting（time and place）＋characters"),
    ("Which ending promotes positive thinking?", ["We learnt that we should be thankful.", "The witch was wicked.", "Fiona was pretty.", "Once upon a time..."], "We learnt that we should be thankful.", "structure", "結局教訓句＝正面思想（checklist 要求）"),
    ("Expand using a simile: The princess is pretty.", ["The princess is as pretty as a flower.", "The princess is pretty like flower.", "The princess is as prettier as a flower.", "The princess pretty as a flower."], "The princess is as pretty as a flower.", "expand", "擴句用 as + 形容詞原形 + as"),
    ("Which sentence uses dialogue punctuation correctly?", ['"Help! Help!" shouted Fiona.', '"Help! Help!" shouted Fiona.', 'Help! Help! shouted Fiona.', '"Help! Help!" Shouted Fiona.'], '"Help! Help!" shouted Fiona.', "structure", "對白：引號＋驚嘆號；「shouted」細寫"),
    ("Which is the correct expansion of 'He ran'?", ["He ran quickly because the witch was chasing him.", "He ran.", "He run quickly because witch chase him.", "He ran quick because the witch chased him."], "He ran quickly because the witch was chasing him.", "expand", "5W1H 擴句：加原因、方式、時態一致"),
    ("The story should be written mainly in _____.", ["the past tense", "the present tense", "the future tense", "the imperative"], "the past tense", "past", "敘事故事用過去式（checklist 第 3 點）"),
]

TASKS = [
    {
        "id": "fiona",
        "name": "👸 Fiona 公主故事（四段式）",
        "prompt": (
            "Once upon a time, there was a beautiful princess called Fiona. One day, a witch came to the palace. "
            "She saw the princess…\n\n請續寫呢個故事（80-120 字，四段式）：\n"
            "第 1 段：setting＋characters｜第 2-3 段：巫婆捉走公主（用 reported speech 寫對白）→ 魔法藥丸換臉\n"
            "第 4 段：結局＋教訓（positive thinking）"
        ),
        "must": ["過去式敘事", "至少 1 個 simile（as + adj + as）", "至少 1 句 reported speech（told/ask + (not) to）", "對白用正確標點", "結局有正面教訓", "四段式", "80-120 字"],
    },
    {
        "id": "diary",
        "name": "📓 Diary Entry 日記",
        "prompt": (
            "You are Helen. Last Saturday afternoon, you ran into your friend on your way to choir practice. "
            "You went to a snack shop together. Write a diary entry about what happened.（80-120 字）"
        ),
        "must": ["日記格式（日期、Dear Diary）", "過去式敘事", "至少 1 個 simile", "至少 1 個 connective（and/but/because/so）", "感受描寫（-ed 形容詞）", "80-120 字"],
    },
    {
        "id": "free",
        "name": "🌟 自由題（自訂主題）",
        "prompt": "自選一個主題寫一段短文（80-120 字），例如：難忘的一天／我的寵物／一次冒險。請用晒下面嘅寫作元素！",
        "must": ["過去式敘事", "至少 1 個 simile", "至少 1 個 connective", "5W1H 擴句（原因/時間/地點）", "正面結尾", "80-120 字"],
    },
    {
        "id": "helping",
        "name": "🤝 A Helping Hand（賣旗經歷）",
        "prompt": (
            "Last Saturday, you sold flags with your classmates to raise money for charity. Write a short story about this experience.（80-120 字，三段式）\n"
            "第 1 段：setting（時間地點＋人物）｜第 2 段：賣旗經過（用 5W1H：when/where/how/why）＋一句對白\n"
            "第 3 段：感受＋教訓（positive thinking）"
        ),
        "must": ["過去式敘事", "5W1H 擴句（when/where/how/why）", "形容詞（kind-hearted, generous）", "至少 1 個連接詞", "正面結尾", "80-120 字"],
    },
    {
        "id": "chef",
        "name": "👨‍🍳 A Day with the Super Chef（煮食日記）",
        "prompt": (
            "Yesterday, you tried to make chocolate cookies with your family. Write a diary entry about it.（80-120 字，三段式）\n"
            "第 1 段：setting｜第 2 段：整餅步驟（用 first/next/then/finally）＋一句對話（正確標點）\n"
            "第 3 段：感受＋教訓（I would keep trying!）"
        ),
        "must": ["日記格式（日期、Dear Diary）", "過去式敘事", "連接詞（first/next/then/finally）", "對白標點（驚嘆號）", "正面思維結尾", "80-120 字"],
    },
]

def ai_review(task, text):
    must = "；".join(task["must"])
    prompt = (
        "你是小六英文寫作老師。請批改以下英文短文（P.6 程度）。\n"
        f"任務：{task['name']}\n要求元素：{must}\n\n學生作文：\n{text}\n\n"
        "請按以下格式用書面語廣東話回覆：\n"
        "【元素檢查】逐項列出要求元素 ✅/❌（有用到就✅）\n"
        "【文法修正】列出文法/拼寫錯誤（原句 → 改正）\n"
        "【評語】2-3 句總評（做得好嘅地方＋要改善嘅地方）\n"
        "【升級示範】揀 1-2 句改寫成更好嘅版本（用上教過嘅元素）\n"
        "【分數】滿分 10 分"
    )
    return silra_chat([{"role": "user", "content": prompt}], max_tokens=2000)

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ 模式")
    mode = st.radio("揀模式", ["📖 技巧操練", "🧰 寫作工具箱", "✍️ 寫作任務（AI 批改）"], key="wr_mode")

st.title("✍️ 英文寫作訓練")
st.caption("P.6 考試寫作 — 章節精華元素（Similes／Reported Speech／Past Tense／-ed -ing／Connectives／Story Structure／5W1H）")

def _norm_en(s):
    """正規化：去首尾空白、細寫、去標點、收斂空白，用嚟寬鬆比對答案"""
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = re.sub(r"[.,!?;:'\"()\[\]]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _match_option(ans, opts):
    """模糊比對答案同選項：①A/B/C/D 代號對應 ②正規化一致 ③單向包含（選項完整喺答案入面、≥4 字元）"""
    na = _norm_en(ans)
    if not na:
        return None
    if na.upper() in ("A", "B", "C", "D") and len(opts) == 4:
        return opts["ABCD".index(na.upper())]
    for o in opts:
        if _norm_en(o) == na:
            return o
    for o in opts:
        no = _norm_en(o)
        if len(na) >= 4 and len(no) >= 4 and no in na:
            return o
    return None

def ai_generate_drills(topics, count):
    """✨ AI 生成新題：按所選寫作元素生成英文文法題（同教材題一致嘅 5 元組格式）"""
    base, key, model = get_api_config()
    if not key:
        st.error("⚠️ 未偵測到 API key — 請設定 OPENAI_API_KEY（app Settings → Secrets）")
        return []
    topic_desc = "；".join(QUESTION_BANK[t]["name"] for t in topics)
    prompt = (
        "You are an experienced Primary 6 English teacher in Hong Kong. "
        f"Create grammar questions about these writing elements: {topic_desc}\n\n"
        "Requirements:\n"
        "1. Multiple-choice only: 1 correct + 3 plausible distractors (same category, commonly confused).\n"
        "2. Question text in English; hint and trap in Traditional Chinese (書面語) explaining the grammar rule and the common mistake.\n"
        "3. \"answer\" must be EXACTLY one of the 4 options (no A/B/C/D prefix, no extra words).\n"
        "4. The answer must NOT appear inside the question text (use a blank _____ ).\n"
        "5. SINGLE-CORRECT-ANSWER RULE: exactly one correct option per question.\n"
        "6. Only use the textbook writing elements listed above — do not invent new grammar rules.\n"
        "7. Vary the answers across the set: avoid repeating the same answer word.\n\n"
        "Output ONLY a JSON array, nothing else:\n"
        '[{"question":"...","options":["...","...","...","..."],"answer":"...","hint":"...","trap":"..."}]'
    )
    out = silra_chat([{"role": "user", "content": prompt}], max_tokens=3000)
    if not out:
        return []
    m = re.search(r"\[.*\]", out, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    valid = []
    for item in data:
        if not isinstance(item, dict):
            continue
        q = str(item.get("question") or "").strip()
        opts = [str(o).strip() for o in (item.get("options") or []) if str(o).strip()]
        ans = str(item.get("answer") or "").strip()
        hint = str(item.get("hint") or "").strip()
        trap = str(item.get("trap") or "").strip()
        if len(opts) != 4 or not q:
            continue
        matched = _match_option(ans, opts)
        if matched is None:
            continue
        # 答案唔准漏喺題目（whole-word + 忽略大小寫）
        if re.search(r"(?<![A-Za-z])" + re.escape(matched) + r"(?![A-Za-z])", q, re.IGNORECASE):
            continue
        # 統一 5 元組格式 [q, opts, ans, tid, hint]（同教材題一致，避免解包 ValueError）
        valid.append([q, opts, matched, "ai", hint + ("｜" + trap if trap else "")])
    # 答案多樣性（唔夠數用剩低題目補足，保證出足 count 題）
    n_distinct = len({v[2] for v in valid})
    max_repeat = max(1, -(-count // n_distinct)) if n_distinct else 1
    used = {}
    out_q = []
    rest_q = []
    for v in valid:
        if len(out_q) >= count:
            break
        a = v[2]
        if used.get(a, 0) < max_repeat:
            used[a] = used.get(a, 0) + 1
            out_q.append(v)
        else:
            rest_q.append(v)
    for v in rest_q:
        if len(out_q) >= count:
            break
        out_q.append(v)
    return out_q[:count]

def build_drill_round(topics, count):
    """由所選 topic 題庫 + 常設 DRILLS 抽題（題庫題目格式：["mc", q, ans, opts, hint]）"""
    pool = []
    for t in topics:
        for item in QUESTION_BANK[t]["questions"]:
            _, q, ans, opts, hint = item
            pool.append([q, list(opts), ans, t, hint])
    pool += DRILLS
    random.shuffle(pool)
    return pool[:count]

if mode == "📖 技巧操練":
    if "wr_q" not in st.session_state:
        st.session_state.wr_q = []
        st.session_state.wr_checked = False
    if "wr_topics" not in st.session_state:
        st.session_state.wr_topics = list(QUESTION_BANK.keys())[:6]
    st.markdown("**揀 Topic（可多選；常設「綜合操練題」會自動加入）：**")
    topics = st.multiselect(
        "Topic",
        list(QUESTION_BANK.keys()),
        format_func=lambda k: QUESTION_BANK[k]["name"],
        default=list(QUESTION_BANK.keys())[:6],
        key="wr_topics",
        label_visibility="collapsed",
    )
    count = st.slider("每輪題數", 5, 20, 10, key="wr_count")
    gen_mode = st.radio("生成模式", ["📖 教材原題（即時）", "✨ AI 生成新題"], key="wr_genmode")
    if st.button("🎲 生成操練題", type="primary"):
        if not topics:
            st.warning("⚠️ 請揀至少一個 Topic")
        elif gen_mode.startswith("✨"):
            with st.spinner("✨ AI 生成緊新題…（約 10–30 秒）"):
                qs_ai = ai_generate_drills(topics, count)
            if qs_ai:
                # AI 唔夠數 → 用教材題補足，保證出夠要求題數
                if len(qs_ai) < count:
                    extra = [q for q in build_drill_round(topics, count * 2)
                             if q[0] not in {x[0] for x in qs_ai}]
                    qs_ai = qs_ai + extra
                st.session_state.wr_q = qs_ai[:count]
                st.session_state.wr_checked = False
                st.rerun()
            else:
                st.error("❌ AI 生成唔到合格題目 — 再試一次？")
        else:
            st.session_state.wr_q = build_drill_round(topics, count)
            st.session_state.wr_checked = False
            st.rerun()
    qs = st.session_state.wr_q
    if not qs:
        st.info("👈 揀 Topic → 㩒「生成操練題」開始！每題附「記得用」提醒。")
    else:
        for i, (q, opts, ans, tid, hint) in enumerate(qs):
            st.markdown(f"**{i+1}.** {q}")
            st.radio(" ", opts, key=f"wr_a{i}", index=None, label_visibility="collapsed")
        if not st.session_state.wr_checked:
            if st.button("✅ 檢查答案", type="primary"):
                st.session_state.wr_checked = True
                st.rerun()
        else:
            correct = 0
            for i, (q, opts, ans, tid, hint) in enumerate(qs):
                user = st.session_state.get(f"wr_a{i}")
                ok = user == ans
                if ok:
                    correct += 1
                    st.success(f"**{i+1}.** ✅ {user}")
                else:
                    st.error(f"**{i+1}.** ❌ 你答：「{user or '（未作答）'}」　正確答案：**{ans}**")
                st.caption(f"💡 {hint}")
            st.metric("🏆 得分", f"{correct} / {len(qs)}")

elif mode == "🧰 寫作工具箱":
    st.subheader("🧰 寫作元素速查（寫作前睇一次）")
    for t in TOOLS:
        with st.expander(t["name"]):
            st.markdown(f"**規則：** {t['rule']}")
            for e in t["examples"]:
                st.markdown(f"- {e}")
            st.info(t["remind"])
            st.caption(t["mistake"])
    st.subheader("✅ 考試寫作 Checklist")
    for item in ["四段式（4 paragraphs）", "首段：setting（time and place）＋ characters", "全篇過去式", "對白標點正確（\"Help!\" shouted Fiona.）",
                 "用 reported speech 轉述對白", "用 simile 'as + adj + as'", "結局正面思想（We learnt that…）", "80-120 字"]:
        st.checkbox(item, key=f"ck_{item}")

else:  # ✍️ 寫作任務
    task_names = [t["name"] for t in TASKS]
    choice = st.selectbox("揀寫作任務", task_names, key="wr_task")
    task = next(t for t in TASKS if t["name"] == choice)
    st.subheader(task["name"])
    st.markdown(task["prompt"])
    st.markdown("**📋 必用元素：** " + "｜".join(task["must"]))
    text = st.text_area("✍️ 你嘅作文：", height=220, placeholder="Write your story here...（80-120 words）")
    wc = len([w for w in re.findall(r"[A-Za-z']+", text)])
    st.caption(f"字數：{wc}（目標 80-120）")
    if st.button("🤖 AI 批改", type="primary"):
        if wc < 20:
            st.warning("⚠️ 作文字數太少，寫長少少先批改（建議 80 字以上）")
        else:
            with st.spinner("🤖 AI 批改緊…"):
                out = ai_review(task, text)
            if out:
                st.subheader("📝 批改結果")
                st.markdown(out)
