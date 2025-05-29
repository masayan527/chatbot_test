# chatbot_app.py
import streamlit as st
import requests
import joblib # モデルの読み込み用
from janome.tokenizer import Tokenizer # 日本語の単語分割用
from datetime import datetime # 時間・日付用

# --- 既存のOpenWeatherMap APIキーと天気関数 ---
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def get_weather(city_name):
    # ... (既存の天気関数と同じ) ...
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name + ",JP", # 都市名と国コード（日本）を指定
        "appid": OPENWEATHER_API_KEY,
        "units": "metric", # 温度を摂氏で取得
        "lang": "ja" # 日本語で情報を取得
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and data.get("main") and data.get("weather"):
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            city_display_name = data["name"]

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

# --- NLPモデルの読み込みと前処理関数 ---
# モデルはアプリ起動時に一度だけ読み込む
try:
    nlp_pipeline = joblib.load('intent_recognition_model.joblib')
    t = Tokenizer() # Janomeトークナイザーも初期化

    def tokenize_text_for_nlp(text):
        return ' '.join([token.surface for token in t.tokenize(text)])

except FileNotFoundError:
    st.error("NLPモデルファイル (intent_recognition_model.joblib) が見つかりません。"
             "先に train_nlp_model.py を実行してモデルを作成してください。")
    st.stop() # アプリの実行を停止
except Exception as e:
    st.error(f"NLPモデルの読み込み中にエラーが発生しました: {e}")
    st.stop()

# --- 地域名とAPI用の都市名のマッピング（これはエンティティ抽出の簡易版） ---
city_mapping = {
    "東京": "Tokyo",
    "大阪": "Osaka",
    "福岡": "Fukuoka",
    "札幌": "Sapporo",
    "名古屋": "Nagoya",
    "仙台": "Sendai",
    "広島": "Hiroshima",
    "沖縄": "Okinawa",
    "延岡": "Nobeoka",
    "nobeoka": "Nobeoka",
    "宮崎": "Miyazaki",
    "tokyo": "Tokyo", # ユーザーがローマ字で入力することも考慮
    # 必要に応じて他の都市も追加
}

# --- チャットボットのロジック（NLPを利用） ---
def simple_chatbot(text):
    # テキストを前処理してモデルに渡す
    tokenized_input = tokenize_text_for_nlp(text.lower()) # モデルは小文字化されたトークン済みテキストで学習

    # 意図を予測
    predicted_intent = nlp_pipeline.predict([tokenized_input])[0]

    # 予測された意図に基づいて応答を生成
    if predicted_intent == "greet":
        return "こんにちは！何かお手伝いできることはありますか？"
    
    elif predicted_intent == "get_weather":
        # 天気を聞く意図の場合、テキストから地域名を抽出（簡易版）
        found_region_key = None
        for region_key, api_city_name in city_mapping.items():
            if region_key.lower() in text.lower(): # ユーザーの入力テキストに地域名が含まれているか
                found_region_key = region_key
                break
        
        if found_region_key:
            return get_weather(city_mapping[found_region_key])
        else:
            return "どこの地域の天気ですか？（例: 東京の天気）"

    elif predicted_intent == "thank":
        return "どういたしまして！"
    
    elif predicted_intent == "goodbye":
        return "またお話ししましょう！"
    
    elif predicted_intent == "ask_capability":
        return "天気予報をお伝えしたり、簡単な会話ができます。他にはどんなことが知りたいですか？"
    
    elif predicted_intent == "get_time":
        now = datetime.now()
        return f"現在の時刻は {now.strftime('%H時%M分')} です。"
    
    elif predicted_intent == "get_date":
        today = datetime.today()
        return f"今日の {today.strftime('%Y年%m月%d日')} です。"
    
    else: # どの意図にも当てはまらなかった場合
        return "すみません、よくわかりません。別の質問をしてください。"

# --- StreamlitでのWebアプリ化 ---
st.title("ファイケムのアシスたん")

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