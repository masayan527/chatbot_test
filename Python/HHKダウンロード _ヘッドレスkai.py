# pipでのインストール方法
# コマンドプロンプトを開いて
# pip install ライブラリ名 --proxy=http://keith.asahi-kasei.co.jp:3128
# 例：pip install os --proxy=http://keith.asahi-kasei.co.jp:3128
# ユーザー名部分（プログラム下部２ヶ所）をご自身の番号へ変更してください
# 本プログラムに必要なライブラリ
# os
# pandas
# glob
# time
# selenium
# datetime
import os
import pandas as pd
import glob
import time
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# EdgeOptionsオブジェクトを作成
options = EdgeOptions()
options.use_chromium = True

# Edge WebDriverのパスを指定して初期化
edge_driver_path = EdgeChromiumDriverManager().install()
driver = Edge(edge_driver_path, options=options)

# 以下はそのままのコード

# タイムアウト値を設定（10をお好みのタイムアウト値に置き換えてください）
options.set_capability('timeouts', {'pageLoad': 30000})

# ドライバーを自動でインストール
path=EdgeChromiumDriverManager().install()
# Edge WebDriverのパスを自動で取得
driver = Edge(EdgeChromiumDriverManager().install(), options=options)

# 現在の日付から年度を取得
current_year = datetime.now().year
# 1~3月であれば-1年としている（年度：4月始まり）
if current_year >=1 and current_year<=3:
    current_year = current_year-1
# 最大の読み込み時間を設定 今回は最大60秒待機できるようにする
wait = WebDriverWait(driver=driver, timeout=120)
# edgeブラウザでURL（HHKの公開件名進捗状況）を開く
driver.get('http://afccbof2.dc.asahi-kasei.co.jp/akway_new/doc/doc_open_list.php?type=4')
# 要素が全て検出できるまで待機する
wait.until(EC.presence_of_all_elements_located) 
# EXCEL出力ボタンの要素取得
element = driver.find_element("xpath","/html/body/table/tbody/tr[1]/td/form/table[2]/tbody/tr/td/input[2]")
# 取得した要素をクリック
element.click()
# ダウンロードが完了するまで待機（HHKシート公開件名一覧.xls.crdownloadのファイルが存在しなくなるまで１秒待機を繰り返す）
while glob.glob(r"C:\Users\a1048554\Downloads\HHKシート公開件名一覧.xls.crdownload") != []:
    # 待機時間設定
    time.sleep(1)    
# ループを抜けてすぐ次の処理をするとエラーになる確率が高いので一旦待機
time.sleep(5)
# ダウンロードフォルダ内のHHKシート公開件名一覧.xlsファイルを配列として取得
list_of_files = glob.glob(r"C:\Users\a1048554\Downloads\HHKシート公開件名一覧.xls")
# 取得した配列内のいちばん新しいファイルを取得
latest_file = max(list_of_files, key=os.path.getctime)
# 取得したいちばん新しいエクセルファイルをDataFrame＝Pandas(パンダス)で読込
read_file = pd.read_excel (latest_file)
# 読み込んだエクセルファイルをCSVファイルに変換（変換する際に取得しておいた年度の数字をファイル名に追記している）
read_file.to_csv (r"C:\Users\a1048554\Downloads\\" + str(current_year) + "_HHK.csv", encoding='utf_8_sig', index = None, header=True)