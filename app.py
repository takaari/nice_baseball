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
    st.session_state.scoreboard = {"top": [""]*9, "bottom": [""]*9}
if "score" not in st.session_state:
    st.session_state.score = 0   # 現在の攻撃側の得点（1イニング中）
if "waiting_batter" not in st.session_state:
    st.session_state.waiting_batter = False  # これが二段階方式の鍵！
if "inning_started" not in st.session_state:
    st.session_state.inning_started = False



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


# --- ランナー進塁関数 ---
def advance_runners(bases_to_move):
    for i in range(2, -1, -1):
        if st.session_state.bases[i]:
            new_pos = i + bases_to_move
            if new_pos >= 3:
                st.session_state.score += 1
            else:
                st.session_state.bases[new_pos] = True
            st.session_state.bases[i] = False

    if bases_to_move >= 4:
        st.session_state.score += 1
    else:
        st.session_state.bases[bases_to_move - 1] = True


# ===============================
# ① 打席に立つ（結果は出さない）
# ===============================
if st.button("▶ 打席に立つ"):
    st.session_state.waiting_batter = True
    st.info("打者が打席に立ちました。『打つ』を押してください。")


# ===============================
# ② 打つ（このボタンで結果を決める）
# ===============================
if st.session_state.waiting_batter:

    if st.button("⚾ 打つ"):
        result = random.choices(batting, weights=weights, k=1)[0]
        st.write(f"結果：{result}")

        # --- 結果処理 ---
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

        # 次の打者を待つ状態へ戻す
        st.session_state.waiting_batter = False


# ---- 3アウトでチェンジ処理 ----
if st.session_state.outs >= 3:
    st.write("チェンジ！")

    # スコア反映
    if st.session_state.top:
        st.session_state.scoreboard["top"][st.session_state.inning - 1] = st.session_state.score
    else:
        st.session_state.scoreboard["bottom"][st.session_state.inning - 1] = st.session_state.score

    # 回の進行
    st.session_state.top = not st.session_state.top
    if st.session_state.top:
        st.session_state.inning += 1

    # 状態リセット
    st.session_state.outs = 0
    st.session_state.bases = [False, False, False]
    st.session_state.score = 0
    st.session_state.waiting_batter = False

    # ⭐ スコアボードを表示可能にする
    st.session_state.inning_started = True



# --- スコアボードを横並び表示 ---
st.markdown("### スコアボード")

innings = [str(i+1) for i in range(9)]
top_scores = st.session_state.scoreboard["top"]
bottom_scores = st.session_state.scoreboard["bottom"]

# ★ 空欄 "" は 0 とみなして合計
top_total = sum([s if isinstance(s, int) else 0 for s in top_scores])
bottom_total = sum([s if isinstance(s, int) else 0 for s in bottom_scores])

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

for inn in innings:
    html += f"<th>{inn}</th>"
html += "<th>R</th></tr>"

html += "<tr><td>表</td>"
for s in top_scores:
    html += f"<td>{s}</td>"
html += f"<td><b>{top_total}</b></td></tr>"

html += "<tr><td>裏</td>"
for s in bottom_scores:
    html += f"<td>{s}</td>"
html += f"<td><b>{bottom_total}</b></td></tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)
