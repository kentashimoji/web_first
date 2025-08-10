import streamlit as st
import json

# --- 初期化 ---
for key, value in {
    "page": "home",
    "selected_category": None,
    "current": 0,
    "score": 0,
    "show_explanation": False,
    "last_explanation": "",
    "show_more": False,
    "answered": False,
    "is_correct": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- データ読み込み ---
with open("questions.json", encoding="utf-8") as f:
    all_questions = json.load(f)

categories = sorted(set(q["category"] for q in all_questions))

# --- トップページ ---
if st.session_state.page == "home":
    st.title("🧠 カテゴリ別クイズアプリ")
    st.write("挑戦したいカテゴリを選んでください👇")

    for cat in categories:
        if st.button(f"▶ {cat}クイズを始める", key=f"start_{cat}"):
            st.session_state.selected_category = cat
            st.session_state.page = "quiz"
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.show_explanation = False
            st.session_state.show_more = False
            st.session_state.answered = False
            st.rerun()

# --- クイズページ ---
elif st.session_state.page == "quiz":
    questions = [q for q in all_questions if q["category"] == st.session_state.selected_category]
    total = len(questions)

    st.title(f"📚 {st.session_state.selected_category}クイズ")

    if st.session_state.current < total:
        q = questions[st.session_state.current]
        st.subheader(f"Q{q['id']}：{q['question']}")

        # 選択肢ボタン
        for i, choice in enumerate(q["choices"]):
            if st.button(choice, key=f"{q['id']}_choice_{i}"):
                st.session_state.answered = True
                st.session_state.is_correct = (i == q["correct_index"])
                st.session_state.last_explanation = q["explanation"]
                st.session_state.show_explanation = True
                if st.session_state.is_correct:
                    st.session_state.score += 1
                st.session_state.show_more = False
                st.rerun()

        # 正誤表示と解説
        if st.session_state.show_explanation:
            if st.session_state.answered:
                if st.session_state.is_correct:
                    st.success("✅ 正解！")
                else:
                    st.error("❌ 不正解")
                st.session_state.answered = False  # 表示は1回だけ

            st.markdown(st.session_state.last_explanation)

            if st.button("📖 One More", key=f"more_{q['id']}"):
                st.session_state.show_more = True
                st.rerun()

            if st.session_state.show_more:
                if "explanation2" in q and q["explanation2"]:
                    st.markdown(q["explanation2"], unsafe_allow_html=True)
                else:
                    st.info("補足説明はありません。")

        # 次の問題へ
        if st.button("次の問題へ", key=f"next_{q['id']}"):
            st.session_state.current += 1
            st.session_state.show_explanation = False
            st.session_state.show_more = False
            st.session_state.answered = False
            st.rerun()

    else:
        # 結果表示
        rate = round((st.session_state.score / total) * 100)
        st.header("🎉 クイズ終了！")
        st.write(f"正答率：{rate}%（{st.session_state.score} / {total}）")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 もう一度挑戦", key="retry"):
                st.session_state.current = 0
                st.session_state.score = 0
                st.session_state.show_explanation = False
                st.session_state.show_more = False
                st.session_state.answered = False
                st.rerun()
        with col2:
            if st.button("🏠 トップに戻る", key="back_home"):
                st.session_state.page = "home"
                st.rerun()
