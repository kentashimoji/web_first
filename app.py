import streamlit as st
import json

# --- 初期化 ---
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = ""

# --- データ読み込み ---
with open("questions.json", encoding="utf-8") as f:
    all_questions = json.load(f)

# --- カテゴリ選択 ---
categories = sorted(set(q["category"] for q in all_questions))
selected = st.selectbox("カテゴリを選択してください", categories)

if selected != st.session_state.selected_category:
    st.session_state.selected_category = selected
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.show_explanation = False
    st.experimental_rerun()

# --- 出題対象を絞り込み ---
questions = [q for q in all_questions if q["category"] == st.session_state.selected_category]
total = len(questions)

st.title("カテゴリ別クイズアプリ")

# --- 出題ロジック ---
if st.session_state.current < total:
    q = questions[st.session_state.current]
    st.subheader(f"Q{q['id']}：{q['question']}")

    for i, choice in enumerate(q["choices"]):
        if st.button(choice, key=f"{q['id']}_{choice}"):
            is_correct = (i == q["correct_index"])
            if is_correct:
                st.success("✅ 正解！")
                st.session_state.score += 1
            else:
                st.error("❌ 不正解")
            st.session_state.last_explanation = q["explanation"]
            st.session_state.show_explanation = True

# --- 解説表示と「次へ」ボタン ---
if st.session_state.show_explanation:
    st.info(f"📘 解説：{st.session_state.last_explanation}")
    if st.button("次の問題へ"):
        st.session_state.current += 1
        st.session_state.show_explanation = False
        st.experimental_rerun()

# --- 終了画面 ---
elif st.session_state.current >= total:
    rate = round((st.session_state.score / total) * 100)
    st.header("クイズ終了！")
    st.write(f"正答率：{rate}%（{st.session_state.score} / {total}）")
    if st.button("もう一度挑戦"):
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.show_explanation = False
        st.experimental_rerun()
