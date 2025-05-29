# chatbot_app.py
import streamlit as st
import requests # 新しく追加するライブラリ

# OpenWeatherMapのAPIキーをここに設定してください
# 絶対にGitHubなどの公開リポジトリに直接書き込まないでください！
# 環境変数やStreamlit Secretsを使うのがベストですが、今回はテスト用に直接書きます。
# 実際には st.secrets["OPENWEATHER_API_KEY"] のように使います。
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"] # 例: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 天気予報を取得する関数
def get_weather(city_name):
    # 日本語の都市名に対応させるため、OpenWeatherMapのAPIは都市名と国コードを指定
    # ただし、都市名だけでの検索は複数の候補が出てくる場合があるので、
    # より厳密には緯度経度を使う方が良いですが、今回は簡易版として都市名で検索
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name + ",JP", # 都市名と国コード（日本）を指定
        "appid": OPENWEATHER_API_KEY,
        "units": "metric", # 温度を摂氏で取得
        "lang": "ja" # 日本語で情報を取得
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        data = response.json()

        if data and data.get("main") and data.get("weather"):
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            city_display_name = data["name"] # APIが認識した都市名（日本語化される場合がある）

            return (
                f"{city_display_name} の天気は {weather_description} です。\n"
                f"現在の気温は {temperature:.1f}℃ で、体感温度は {feels_like:.1f}℃ です。"
            )
        else:
            return f"{city_name} の天気情報を取得できませんでした。都市名が正しいか確認してください。"
    except requests.exceptions.RequestException as e:
        return f"天気情報の取得中にエラーが発生しました: {e}"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"


# あなたのチャットボットのロジックを修正
def simple_chatbot(text):
    text = text.lower()

    if "こんにちは" in text or "こんばんは" in text:
        return "こんにちは！何かお手伝いできることはありますか？"
    elif "天気" in text:
        # 地域名を抽出するための簡易的なロジック
        # 例：「東京の天気」「大阪の天気」「福岡の天気」
        regions = ["東京", "大阪", "福岡", "札幌", "名古屋", "仙台", "広島", "沖縄", "Nobeoka", "延岡","宮崎"] # よくある地域名を追加
        
        found_region = None
        for region in regions:
            if region.lower() in text:
                found_region = region
                break
        
        if found_region:
            return get_weather(found_region)
        else:
            return "どこの地域の天気ですか？（例: 東京の天気）"
            
    elif "ありがとう" in text:
        return "どういたしまして！"
    elif "さようなら" in text:
        return "またお話ししましょう！"
    else:
        return "すみません、よくわかりません。別の質問をしてください。"

# --- StreamlitでのWebアプリ化 ---

st.title("簡易チャットボット")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ここにメッセージを入力してください..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = simple_chatbot(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)