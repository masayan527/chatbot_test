def simple_chatbot(text):
    text = text.lower() # 入力を小文字に変換

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

# チャットボットとの会話
while True:
    user_input = input("あなた: ")
    if user_input.lower() == "終了":
        print("チャットボット: 会話を終了します。")
        break
    response = simple_chatbot(user_input)
    print(f"チャットボット: {response}")
    