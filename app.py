import streamlit as st
import random

# -------------------
# 初期化
# -------------------
if "on_base" not in st.session_state:
    st.session_state.on_base = [False, False, False]  # 1,2,3 塁
if "waiting_batter" not in st.session_state:
    st.session_state.waiting_batter = False  # 打者が打つのを待っているか
if "outs" not in st.session_state:
    st.session_state.outs = 0

batting = ["hit", "two_base", "three_base", "home_run", "out"]
weights = [0.1, 0.1, 0.1, 0.1, 0.6]

# -------------------
# UI
# -------------------
st.title("野球シミュレーター（二段階方式）")

# 現在の塁状況を表示
st.write("### 塁状況")
st.write(f"1塁: {st.session_state.on_base[0]}")
st.write(f"2塁: {st.session_state.on_base[1]}")
st.write(f"3塁: {st.session_state.on_base[2]}")
st.write(f"アウト: {st.session_state.outs}")

# -------------------
# 打席に立つ（ステップ1）
# -------------------
if st.button("▶ 打席に立つ"):
    st.session_state.waiting_batter = True
    st.success("打者が打席に立ちました！『打つ』ボタンで結果を決めてください。")

# -------------------
# 打つ（ステップ2）
# -------------------
if st.session_state.waiting_batter:

    if st.button("⚾ 打つ"):
        result = random.choices(batting, weights=weights, k=1)[0]
        st.write(f"結果：**{result}**")

        # ▼ 結果処理 ▼
        if result == "out":
            st.session_state.outs += 1

        else:
            # --- ランナー進塁処理 ---
            if result == "hit":  # 単打
                if st.session_state.on_base[2]:  # 3塁ランナーがホームへ
                    st.session_state.on_base[2] = False
                if st.session_state.on_base[1]:
                    st.session_state.on_base[2] = True
                    st.session_state.on_base[1] = False
                if st.session_state.on_base[0]:
                    st.session_state.on_base[1] = True
                st.session_state.on_base[0] = True  # 打者が1塁へ

            elif result == "two_base":
                st.session_state.on_base = [
                    False,
                    True,
                    st.session_state.on_base[0] or st.session_state.on_base[1] or st.session_state.on_base[2]
                ]

            elif result == "three_base":
                st.session_state.on_base = [
                    False,
                    False,
                    True
                ]

            elif result == "home_run":
                st.write("ホームラン！ランナーと打者が全て生還します。")
                st.session_state.on_base = [False, False, False]

        # 打者処理終了
        st.session_state.waiting_batter = False


