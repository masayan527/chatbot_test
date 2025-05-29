import streamlit as st

# 以前作成したチャットボットの関数
def simple_chatbot(text):
    text = text.lower()
    if "こんにちは" in text or "こんばんは" in text:
        return "こんにちは！何かお手伝いできることはありますか？"
    elif "天気" in text:
        return "今日の天気は晴れです！"
    elif "ありがとう" in text:
        return "どういたしまして！"
    elif "さようなら" in text:
        return "またお話ししましょう！"
    else:
        return "すみません、よくわかりません。別の質問をしてください。"

st.title("ファインケムのアシスたん")

# セッションステートにメッセージ履歴を保存（会話を記憶するため）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け取る
if prompt := st.chat_input("何か質問してください..."):
    # ユーザーのメッセージを履歴に追加して表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # チャットボットの応答を生成
    response = simple_chatbot(prompt)

    # チャットボットの応答を履歴に追加して表示
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)