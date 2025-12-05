import streamlit as st
import random

st.title("⚾ 野球シミュレーター（1 打席ごと）")

# -------------------------
# セッション状態の初期化
# -------------------------
if "outs" not in st.session_state:
    st.session_state.outs = 0
if "runs" not in st.session_state:
    st.session_state.runs = 0
if "bases" not in st.session_state:
    st.session_state.bases = [False, False, False]  # 1,2,3塁
if "message" not in st.session_state:
    st.session_state.message = ""

batting = ["hit", "two_base", "three_base", "home_run", "out", "out", "out", "out", "out", "out", "out", "out", "out", "out", "out"]


# -------------------------
# ランナーを進める関数
# -------------------------
def advance_runners(hit_type):
    bases = st.session_state.bases
    runs = 0

    if hit_type == "out":
        st.session_state.outs += 1
        st.session_state.message = "アウト！"
        return

    # ホームラン
    if hit_type == "home_run":
        runs = sum(bases) + 1  # ランナー分 + バッター
        st.session_state.bases = [False, False, False]
        st.session_state.message = f"ホームラン！{runs} 点入りました！"
        st.session_state.runs += runs
        return

    # 単打・二塁打・三塁打用の進塁処理
    shift = {"hit": 1, "two_base": 2, "three_base": 3}[hit_type]

    for _ in range(shift):
        # 三塁ランナーが返る
        if bases[2]:
            runs += 1
        # 進塁
        bases = [False] + bases[:2]

    st.session_state.bases = bases
    st.session_state.runs += runs
    st.session_state.message = f"{hit_type}！ {runs} 点追加されました。"


# -------------------------
# 打席ボタン
# -------------------------
if st.button("▶ 打席を実行する"):
    result = random.choice(batting)
    advance_runners(result)

# -------------------------
# 状況表示
# -------------------------
st.subheader("◆ 現在の状況")

col1, col2 = st.columns(2)

with col1:
    st.write(f"アウト：{st.session_state.outs} / 3")
    st.write(f"得点：{st.session_state.runs}")

with col2:
    st.write("塁状況：")
    st.write(f"1塁：{st.session_state.bases[0]}")
    st.write(f"2塁：{st.session_state.bases[1]}")
    st.write(f"3塁：{st.session_state.bases[2]}")

st.write("**結果：**", st.session_state.message)

# -------------------------
# チェンジ処理
# -------------------------
if st.session_state.outs >= 3:
    st.warning("チェンジ！3アウトになりました。リセットしてください。")

# リセットボタン
if st.button("🔄 リセット"):
    st.session_state.outs = 0
    st.session_state.runs = 0
    st.session_state.bases = [False, False, False]
    st.session_state.message = "リセットしました！"
