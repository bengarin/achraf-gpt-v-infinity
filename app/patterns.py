
import pandas as pd

def detect_candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect basic candlestick patterns and add a new column `pattern` to the dataframe.
    Patterns: Hammer, Inverted Hammer, Bullish Engulfing, Bearish Engulfing, Doji, Shooting Star, Pin Bar
    """
    df = df.copy()
    df["pattern"] = ""

    for i in range(1, len(df)):
        o, h, l, c = df.loc[i, ["open", "high", "low", "close"]]
        prev_o, prev_c = df.loc[i-1, ["open", "close"]]
        body = abs(c - o)
        range_ = h - l

        # DOJI
        if body <= 0.1 * range_:
            df.loc[i, "pattern"] = "Doji"

        # HAMMER
        elif body > 0 and (h - max(c, o)) <= 0.1 * range_ and (min(c, o) - l) >= 2 * body:
            df.loc[i, "pattern"] = "Hammer"

        # INVERTED HAMMER / SHOOTING STAR
        elif body > 0 and (min(c, o) - l) <= 0.1 * range_ and (h - max(c, o)) >= 2 * body:
            df.loc[i, "pattern"] = "Inverted Hammer"

        # BULLISH ENGULFING
        elif prev_c < prev_o and c > o and c > prev_o and o < prev_c:
            df.loc[i, "pattern"] = "Bullish Engulfing"

        # BEARISH ENGULFING
        elif prev_c > prev_o and c < o and o > prev_c and c < prev_o:
            df.loc[i, "pattern"] = "Bearish Engulfing"

        # PIN BAR
        upper_wick = h - max(c, o)
        lower_wick = min(c, o) - l
        if body <= 0.3 * range_ and (upper_wick >= 2 * body or lower_wick >= 2 * body):
            df.loc[i, "pattern"] += " Pin Bar"

    return df
