# csv_logic.py - تحليل بيانات الشموع من ملف CSV

import pandas as pd

def analyze_candles_from_csv(file):
    """
    تحليل مبدئي لبيانات الشموع من ملف CSV.
    يفحص الاتجاهات، حجم التداول، ونماذج أساسية.
    """
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return f"❌ خطأ في قراءة الملف: {str(e)}"

    if not all(col in df.columns for col in ["open", "high", "low", "close", "volume"]):
        return "❌ الملف لا يحتوي على الأعمدة الأساسية (open, high, low, close, volume)."

    avg_volume = df["volume"].mean()
    last_close = df["close"].iloc[-1]
    first_open = df["open"].iloc[0]
    direction = "صعودي" if last_close > first_open else "هبوطي"

    result = (
        f"✅ تم قراءة {len(df)} شمعة بنجاح.\n"
        f"🔁 الاتجاه العام: {direction}\n"
        f"📊 متوسط الحجم: {int(avg_volume)}\n"
        f"📍 أول سعر فتح: {first_open:.2f}\n"
        f"📍 آخر سعر إغلاق: {last_close:.2f}"
    )
    return result
