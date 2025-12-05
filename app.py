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

batting = ["hit", "two_base", "three_base", "home_run", "out"]
weights = [0.1, 0.1, 0.1, 0.1, 0.6]


# -------------------------
# ランナーを進める関数
# -------------------------
def advance_runners(hit_type):
    bases = st.session_state.bases
    runs = 0

    # アウト
    if hit_type == "out":
        st.session_state.outs += 1
        st.session_state.message = "アウト！"
        return

    # ホームラン
    if hit_type == "home_run":
        runs = sum(bases) + 1   # ランナー + バッター
        st.session_state.bases = [False, False, False]  # 塁を空にする
        st.session_state.runs += runs
        st.session_state.message = f"ホームラン！ {runs} 点入りました！"
        return

    # 単打・二塁打・三塁打
    shift = {"hit": 1, "two_base": 2, "three_base": 3}[hit_type]

    # 新しい塁情報を作る
    new_bases = [False, False, False]

    # ランナーを後ろから動かす（3塁 → 2塁 → 1塁）
    for i in reversed(range(3)):
        if bases[i]:
            new_position = i + shift
            if new_position >= 3:
                runs += 1   # 返ってきた
            else:
                new_bases[new_position] = True

    # バッターの位置
    if shift == 1:
        new_bases[0] = True
    elif shift == 2:
        new_bases[1] = True
    elif shift == 3:
        new_bases[2] = True

    st.session_state.bases = new_bases
    st.session_state.runs += runs
    st.session_state.message = f"{hit_type}！ {runs} 点入りました。"


# -------------------------
# 打席ボタン
# -------------------------
if st.button("▶ 打席に立つ"):
    result = random.choices(batting, weights=weights, k=1)[0]
    st.write(f"結果：{result}")

# -------------------------
# 状況表示
# -------------------------
st.subheader("◆ 現在の状況")

col1, col2 = st.columns(2)

with col1:
    st.write(f"アウト：{st.session_state.outs} / 3")
    st.write(f"得点：{st.session_state.runs}")

with col2:
    st.write("塁状況（True = ランナーあり）：")
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
