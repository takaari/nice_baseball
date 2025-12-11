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
if "last_result_icon" not in st.session_state:
    st.session_state.last_result_icon = ""  # ← 追加（画像表示用）
if "change_flag" not in st.session_state:
    st.session_state.change_flag = False



# --- UI ---
st.title("⚾ ナイスベースボール")

half = "表" if st.session_state.top else "裏"
st.subheader(f"{st.session_state.inning}回{half}")


import base64

# 画像ファイルを Base64 に変換
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ---------------------------------------------------------
# ⭐ ランナー画像 ＋ 結果アイコン or チェンジ表示
# ---------------------------------------------------------
key = "".join(["1" if b else "0" for b in st.session_state.bases])
runner_img_path = f"images/base_{key}.jpg"
runner_base64 = img_to_base64(runner_img_path)

overlay_html = ""

# --- チェンジ時の中央テキスト表示 ---
if st.session_state.change_flag:
    overlay_html = """
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 80px;
            font-weight: bold;
            color: red;
            font-family: 'Arial Rounded MT Bold', 'Hiragino Maru Gothic Pro', 'Yu Gothic', sans-serif;
            text-shadow: 3px 3px 6px #00000088;
        ">
            チェンジ
        </div>
    """

# --- 打撃結果アイコン表示 ---
elif st.session_state.last_result_icon:
    result_img_path = f"images/{st.session_state.last_result_icon}"
    result_base64 = img_to_base64(result_img_path)

    overlay_html = f"""
        <img src="data:image/png;base64,{result_base64}"
            style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 180px;
            ">
    """


# --- HTML 全体を合体 ---
html_code = f"""
<div style="position: relative; display: inline-block;">
    <img src="data:image/jpeg;base64,{runner_base64}" width="400">
    {overlay_html}
</div>
"""

st.components.v1.html(html_code, height=450)

# ---------------------------------------------------------


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
        st.session_state.change_flag = False
        st.session_state.waiting_batter = True
        
        st.session_state.last_result_icon = ""  # ← 結果アイコンを消す
        
        st.rerun()
        


# ===============================
# ② 打つ
# ===============================
if st.session_state.waiting_batter:
    if st.button("⚾ 打つ"):

        result = random.choices(batting, weights=weights, k=1)[0]

        # メッセージ保存
        if result == "out":
            st.session_state.last_message = "アウト！"
            st.session_state.last_result_icon = "OUT.png"
        elif result == "hit":
            st.session_state.last_message = "ヒット！"
            st.session_state.last_result_icon = "1BH.png"
        elif result == "two_base":
            st.session_state.last_message = "ツーベースヒット！"
            st.session_state.last_result_icon = "2BH.png"
        elif result == "three_base":
            st.session_state.last_message = "スリーベースヒット！"
            st.session_state.last_result_icon = "3BH.png"
        elif result == "home_run":
            st.session_state.last_message = "ホームラン！！"
            st.session_state.last_result_icon = "HR.png"

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


# --- 打撃結果を表示（テキスト） ---
# if st.session_state.last_message:
#    st.info(st.session_state.last_message)


# ---- 3アウトでチェンジ処理 ----
if st.session_state.outs >= 3:
#    st.write("チェンジ！")
    st.session_state.change_flag = True


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
    st.session_state.last_result_icon = ""  # ← 画像もクリア


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

