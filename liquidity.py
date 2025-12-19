
import pandas as pd

def detect_liquidity_traps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["liquidity_trap"] = ""

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        # شروط بسيطة لاكتشاف فخ سيولة: ذيل طويل مقابل الاتجاه العام + اختراق كاذب للقمة أو القاع
        long_upper_wick = (row["high"] - max(row["close"], row["open"])) > (row["high"] - row["low"]) * 0.6
        long_lower_wick = (min(row["close"], row["open"]) - row["low"]) > (row["high"] - row["low"]) * 0.6

        fakeout_high = row["high"] > prev["high"] and row["close"] < prev["close"]
        fakeout_low = row["low"] < prev["low"] and row["close"] > prev["close"]

        if long_upper_wick and fakeout_high:
            df.at[i, "liquidity_trap"] = "🔴 Stop Hunt (High)"
        elif long_lower_wick and fakeout_low:
            df.at[i, "liquidity_trap"] = "🟢 Stop Hunt (Low)"

    return df
