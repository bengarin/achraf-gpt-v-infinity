
import pandas as pd

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["entry_signal"] = ""

    for i in range(2, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        prev2 = df.iloc[i - 2]

        # مثال بسيط: ظهور Pin Bar بعد شموع قوية
        body = abs(row["close"] - row["open"])
        wick_top = row["high"] - max(row["close"], row["open"])
        wick_bottom = min(row["close"], row["open"]) - row["low"]
        total_range = row["high"] - row["low"]

        is_pin_bar = (body < total_range * 0.3) and (
            wick_top > total_range * 0.6 or wick_bottom > total_range * 0.6
        )

        bullish_context = prev["close"] > prev["open"] and prev2["close"] > prev2["open"]
        bearish_context = prev["close"] < prev["open"] and prev2["close"] < prev2["open"]

        if is_pin_bar and wick_bottom > wick_top and bullish_context:
            df.at[i, "entry_signal"] = "🟢 Buy Signal (Pin Bar)"
        elif is_pin_bar and wick_top > wick_bottom and bearish_context:
            df.at[i, "entry_signal"] = "🔴 Sell Signal (Pin Bar)"

    return df
