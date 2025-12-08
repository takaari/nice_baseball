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
    st.session_state.top = True
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = {"top": [""]*9, "bottom": [""]*9}
if "score" not in st.session_state:
    st.session_state.score = 0
if "waiting_batter" not in st.session_state:
    st.session_state.waiting_batter = False
if "inning_started" not in st.session_state:
    st.session_state.inning_started = False
if "last_message" not in st.session_state:
    st.session_state.last_message = ""


# --- UI ---
st.title("⚾ ナイスベースボール")

half = "表" if st.session_state.top else "裏"
st.subheader(f"{st.session_state.inning}回{half}")


# -----------------------------------
# ⭐ ランナー画像の表示（追加）
# -----------------------------------
key = "".join(["1" if b else "0" for b in st.session_state.bases])
img_path = f"images/base_{key}.jpg"
st.image(img_path, width=400)
# -----------------------------------


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
# ① 打席に立つ
# ===============================
if not st.session_state.waiting_batter:
    if st.button("▶ 打席に立つ"):
        st.session_state.waiting_batter = True
        st.rerun()


# ===============================
# ② 打つ
# ===============================
if st.session_state.waiting_batter:
    if st.button("⚾ 打つ"):

        result = random.choices(batting, weights=weights, k=1)[0]

        # メッセージ保存（画面に出す用）
        if result == "out":
            st.session_state.last_message = "アウト！"
        elif result == "hit":
            st.session_state.last_message = "ヒット！"
        elif result == "two_base":
            st.session_state.last_message = "ツーベースヒット！"
        elif result == "three_base":
            st.session_state.last_message = "スリーベースヒット！"
        elif result == "home_run":
            st.session_state.last_message = "ホームラン！！"

        # 結果処理
        if result == "out":
            st.session_state.outs += 1
        else:
            if result == "hit":
                advance_runners(1)
            elif result == "two_base":
                advance_runners(2)
            elif result == "three_base":
                advance_runners(3)
            elif result == "home_run":
                advance_runners(4)

        st.session_state.waiting_batter = False
        st.rerun()


# --- 打撃結果を表示 ---
if st.session_state.last_message:
    st.info(st.session_state.last_message)


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
    st.session_state.last_message = ""


# --- スコアボード ---
st.markdown("### スコアボード")

innings = [str(i+1) for i in range(9)]
top_scores = st.session_state.scoreboard["top"]
bottom_scores = st.session_state.scoreboard["bottom"]

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
