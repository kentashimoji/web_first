import streamlit as st
import json

# --- 初期化 ---
if "page" not in st.session_state:
    st.session_state.page = "home"
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

categories = sorted(set(q["category"] for q in all_questions))

# --- トップページ ---
if st.session_state.page == "home":
    st.title("🧠 カテゴリ別クイズアプリ")
    st.write("挑戦したいカテゴリを選んでください👇")

    for cat in categories:
        if st.button(f"▶ {cat}クイズを始める", key=cat):
            st.session_state.selected_category = cat
            st.session_state.page = "quiz"
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.show_explanation = False
            st.rerun()

# --- クイズページ ---
elif st.session_state.page == "quiz":
    questions = [q for q in all_questions if q["category"] == st.session_state.selected_category]
    total = len(questions)

    st.title(f"📚 {st.session_state.selected_category}クイズ")

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

    if st.session_state.show_explanation:
        st.markdown(st.session_state.last_explanation)
        if st.button("次の問題へ"):
            st.session_state.current += 1
            st.session_state.show_explanation = False
            st.rerun()

    elif st.session_state.current >= total:
        rate = round((st.session_state.score / total) * 100)
        st.header("🎉 クイズ終了！")
        st.write(f"正答率：{rate}%（{st.session_state.score} / {total}）")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 もう一度挑戦"):
                st.session_state.current = 0
                st.session_state.score = 0
                st.session_state.show_explanation = False
                st.rerun()
        with col2:
            if st.button("🏠 トップに戻る"):
                st.session_state.page = "home"
                st.rerun()
