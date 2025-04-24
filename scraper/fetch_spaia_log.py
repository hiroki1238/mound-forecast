# 横山陸人の登板記録をSPAIAから取得

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 対象ページ
url = "https://spaia.jp/baseball/npb/player/1900083"

def fetch_with_selenium():
    # Chromeオプションの設定
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # ヘッドレスモードで実行
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    # WebDriverの初期化
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # ページにアクセス
        driver.get(url)

        # ページの読み込みを待機
        time.sleep(5)  # 動的コンテンツの読み込みを待つ

        # テーブルが表示されるまで待機
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))

        # ページのHTMLを取得
        html = driver.page_source

        # BeautifulSoupで解析
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    finally:
        driver.quit()

# メインの処理
try:
    print("ブラウザを起動してデータを取得中...")
    soup = fetch_with_selenium()

    # 表の部分（登板記録テーブル）を抽出
    tables = soup.find_all("table")

    target_table = None
    for table in tables:
        # テーブルのヘッダー部分を確認
        headers = table.find_all("th")
        header_text = " ".join([h.text.strip() for h in headers])
        if "日付" in header_text and "対戦チーム" in header_text:
            target_table = table
            break

    if not target_table:
        print("⛔ 登板記録テーブルが見つかりませんでした")
        print("ヒント: 見つかったテーブル数:", len(tables))
        if tables:
            print("最初のテーブルのテキスト:", tables[0].text[:100])  # デバッグ情報
        exit()

    # データ抽出
    data = []
    rows = target_table.find_all("tr")[1:]  # ヘッダー除く
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        if len(cols) < 6:
            continue
        date = cols[0]
        team = cols[2]
        is_home = 0 if "@" in cols[1] else 1
        innings = cols[4]
        pitches = cols[5]
        result = cols[3]

        data.append({
            "date": date,
            "opponent": team,
            "is_home": is_home,
            "innings": innings,
            "pitches": pitches,
            "result": result
        })

    # DataFrame化 & 保存
    df = pd.DataFrame(data)
    df.to_csv("data/yokoyama_spaia_log.csv", index=False, encoding="utf-8")
    print("✅ 登板記録をCSVに保存しました")

except Exception as e:
    print(f"⛔ エラーが発生しました: {str(e)}")
    exit()
