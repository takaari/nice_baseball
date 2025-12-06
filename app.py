import streamlit as st
import random

# --- セッションステート初期化 ---
if "outs" not in st.session_state:
    st.session_state.outs = 0
if "bases" not in st.session_state:
    st.session_state.bases = [False, False, False]   # 1,2,3塁
if "inning" not in st.session_state:
    st.session_state.inning = 1
if "top" not in st.session_state:
    st.session_state.top = True  # True = 表, False = 裏
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = {"top": [0]*9, "bottom": [0]*9}
if "score" not in st.session_state:
    st.session_state.score = 0   # 現在の攻撃側の得点（1イニング中）


# --- UI ---
st.title("⚾ ナイスベースボール")

half = "表" if st.session_state.top else "裏"
st.subheader(f"{st.session_state.inning}回{half}")

st.write("塁:", st.session_state.bases)
st.write("アウト:", st.session_state.outs)
st.write("現在のイニング得点:", st.session_state.score)

# --- バッティング確率 ---
batting = ["hit", "two_base", "three_base", "home_run", "out"]
weights = [0.25, 0.1, 0.03, 0.07, 0.55]


# --- ランナー進塁関数（重要） ---
def advance_runners(bases_to_move):
    # ランナーを後ろから処理（上書き防止）
    for i in range(2, -1, -1):
        if st.session_state.bases[i]:
            new_pos = i + bases_to_move
            if new_pos >= 3:
                # 得点
                st.session_state.score += 1
            else:
                st.session_state.bases[new_pos] = True
            st.session_state.bases[i] = False

    # 打者の処理
    if bases_to_move >= 4:   # ホームラン
        st.session_state.score += 1
    else:
        st.session_state.bases[bases_to_move - 1] = True


# --- 打席 ---
if st.button("▶ 打席に立つ"):

    result = random.choices(batting, weights=weights, k=1)[0]
    st.write(f"結果：{result}")

    if result == "out":
        st.session_state.outs += 1
        st.write("アウト！")
    else:
        if result == "hit":
            advance_runners(1)
        elif result == "two_base":
            advance_runners(2)
        elif result == "three_base":
            advance_runners(3)
        elif result == "home_run":
            advance_runners(4)


# ---- 3アウトでチェンジ処理 ----
if st.session_state.outs >= 3:
    st.write("チェンジ！")

    # スコアをスコアボードへ
    if st.session_state.top:
        st.session_state.scoreboard["top"][st.session_state.inning - 1] = st.session_state.score
    else:
        st.session_state.scoreboard["bottom"][st.session_state.inning - 1] = st.session_state.score

    # 回の進行
    st.session_state.top = not st.session_state.top
    if st.session_state.top:   # 裏 → 表に戻ったらイニング+1
        st.session_state.inning += 1

    # 状態リセット
    st.session_state.outs = 0
    st.session_state.bases = [False, False, False]
    st.session_state.score = 0


# --- スコアボードを横並び表示 ---
st.markdown("### スコアボード")

innings = [str(i+1) for i in range(9)]
top_scores = st.session_state.scoreboard["top"]
bottom_scores = st.session_state.scoreboard["bottom"]

# 合計（R）
top_total = sum(top_scores)
bottom_total = sum(bottom_scores)

html = """
<style>
table {
    border-collapse: collapse;
    width: 100%;
    font-size: 20px;
}
th, td {
    border: 1px solid #444;
    padding: 6px 10px;
    text-align: center;
}
th {
    background-color: #eee;
}
</style>

<table>
    <tr>
        <th>回</th>
"""

# 回の番号を横に並べる
for inn in innings:
    html += f"<th>{inn}</th>"

# R 列
html += "<th>R</th></tr>"

# 表
html += "<tr><td>表</td>"
for s in top_scores:
    html += f"<td>{s}</td>"
html += f"<td><b>{top_total}</b></td></tr>"

# 裏
html += "<tr><td>裏</td>"
for s in bottom_scores:
    html += f"<td>{s}</td>"
html += f"<td><b>{bottom_total}</b></td></tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)
