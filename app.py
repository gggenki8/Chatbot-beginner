import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

#ページ設定
st.set_page_config(page_title="AI チャットボット", page_icon="🤖")

st.title("🤖 AI チャットボット")

#サイドバー設定
with st.sidebar:
    st.header("設定")
    system_prompt = st.text_area(
        "AIの役割設定", 
        value="あなたは親切なアシスタントです。日本語で答えてください。",
        height=100
    )
    if st.button("会話をリセット"):
        st.session_state.messages = []

# 会話履歴に初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去の会話を表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ユーザー入力
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーのメッセージを表示.保存
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAIに送信
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages_to_send = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_to_send
            )
            ai_reply = response.choices[0].message.content
            st.write(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})