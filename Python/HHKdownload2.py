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
# 「pip install Office365-REST-Python-Client --proxy=http://keith.asahi-kasei.co.jp:3128」SharePoint接続用ライブラリの追加（使っていない）
# 「pip install Office365 --proxy=http://keith.asahi-kasei.co.jp:3128」SharePoint接続用ライブラリの追加
import os
import pandas as pd
import glob
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
from msedge.selenium_tools import Edge, EdgeOptions 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ドライバーのオプションを設定
options = EdgeOptions()
options.use_chromium = True
options.add_argument('--headless=new') #ヘッドレスモード
# ドライバーを自動でインストール
path=EdgeChromiumDriverManager().install()
driver = Edge(path, options=options)
# 現在の日付から年度を取得
current_year = datetime.now().year
# 1~3月であれば-1年としている（年度：4月始まり）
if current_year >=1 and current_year<=3:
    current_year = current_year-1
# 最大の読み込み時間を設定 今回は最大60秒待機できるようにする
wait = WebDriverWait(driver=driver, timeout=60)

#ダウンロードフォルダ内に保存されている古い「HHK公開シート件名一覧.xls」を削除する（矢野追加分）
file_list = glob.glob(r"C:\Users\a1048554\Downloads\HHKシート公開件名一覧*xls")
for file in file_list:
    print("remove：{0}".format(file))
    os.remove(file)

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
time.sleep(10)

#Pandasに「HHKシート公開件名一覧.xls」を読み込ませる
read_file = pd.read_excel (r"C:\Users\a1048554\Downloads\HHKシート公開件名一覧.xls")

# 読み込んだエクセルファイルをCSVファイルに変換（変換する際に取得しておいた年度の数字をファイル名に追記している）
read_file.to_csv (r"C:\Users\a1048554\Downloads\\" + str(current_year) + "_HHK.csv", encoding='utf_8_sig', index = None, header=True)

# 矢野追加コード
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
import os

# SharePointのURL
site_url = "https://akgr01.sharepoint.com"

# 対象サイトへのアクセス（ID、パスワードを入力する）
ctx_auth = AuthenticationContext(site_url)
ctx_auth.acquire_token_for_user('ID', 'パスワード')
ctx = ClientContext(site_url, ctx_auth)

# コンテクスト情報の保存
web = ctx.web
ctx.load(web)
ctx.execute_query()

# アップロードしたいファイルの絶対パス
localfilepath = r"C:\Users\a1048554\Downloads\2023_HHK.csv"
filename = os.path.basename(localfilepath)
with open(localfilepath, 'rb') as content_file:
  file_content = content_file.read()
  
# アップロード先の情報取得
target_folder = ctx.web.get_folder_by_server_relative_url("https://akgr01.sharepoint.com/teams/AFC-RCC/PowerBI_Data?viewpath=%2Fteams%2FAFC%2DRCC%2FPowerBI%5FData")

# アップロード処理
target_file = target_folder.upload_file(filename, file_content)
ctx.execute_query()
