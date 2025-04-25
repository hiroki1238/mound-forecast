import pandas as pd
from datetime import datetime

# CSV読み込み
df = pd.read_csv("data/yokoyama_log.csv")

# 日付をdatetime型に変換
df["date"] = pd.to_datetime(df["date"])

# days_since_last を初期化（空欄に）
df["days_since_last"] = None

# 前回登板日を記録
last_pitch_date = None

# 行ごとに処理
for i, row in df.iterrows():
    if last_pitch_date is not None:
        delta = (row["date"] - last_pitch_date).days
        df.at[i, "days_since_last"] = delta

    if row["relief_appearance"] == 1:
        last_pitch_date = row["date"]

# days_since_last を整数に（NaN以外）
df["days_since_last"] = pd.to_numeric(df["days_since_last"], errors="coerce").astype("Int64")

# 保存
df.to_csv("data/yokoyama_log_with_days.csv", index=False)
print("✅ days_since_last を追加したCSVを保存しました!")
