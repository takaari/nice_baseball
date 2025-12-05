import streamlit as st
import random

# --- ここにバッティング確率をセット ---
batting = ["hit", "two_base", "three_base", "home_run", "out"]
weights = [0.1, 0.1, 0.1, 0.1, 0.6]

# --- セッションステート初期化 ---
if "outs" not in st.session_state:
    st.session_state.outs = 0
if "bases" not in st.session_state:
    st.session_state.bases = [False, False, False]
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("⚾ シンプル野球ゲーム")

# --- ボタンを押して打席に立つ ---
if st.button("▶ 打席に立つ"):
    # ★ ここに weights版を組み込む ★
    result = random.choices(batting, weights=weights, k=1)[0]
    st.write(f"結果：{result}")

    # ---- ここから先は進塁処理・アウト処理など ----
    if result == "out":
        st.session_state.outs += 1
        st.write("アウトになりました！")
    else:
        # hit 二塁打 三塁打 本塁打で進塁処理
        if result == "hit":
            bases_to_move = 1
        elif result == "two_base":
            bases_to_move = 2
        elif result == "three_base":
            bases_to_move = 3
        elif result == "home_run":
            bases_to_move = 4

        # ---- 進塁処理（あなたが作ったもの） ----
        for i in range(2, -1, -1):
            if st.session_state.bases[i]:
                new_pos = i + bases_to_move
                if new_pos >= 3:
                    st.session_state.score += 1
                else:
                    st.session_state.bases[new_pos] = True
                st.session_state.bases[i] = False

        # バッターを塁に置く
        if bases_to_move >= 4:
            st.session_state.score += 1
        else:
            st.session_state.bases[bases_to_move - 1] = True

# --- 状態表示 ---
st.write("塁の状態：", st.session_state.bases)
st.write("アウト：", st.session_state.outs)
st.write("得点：", st.session_state.score)

# --- 3アウトならチェンジ ---
if st.session_state.outs >= 3:
    st.write("チェンジ！")
    st.session_state.outs = 0
    st.session_state.bases = [False, False, False]



