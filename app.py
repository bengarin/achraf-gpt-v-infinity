
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from patterns import detect_candle_patterns
from liquidity import detect_liquidity_traps
from signals import generate_signals

st.set_page_config(page_title="📊 Dashboard - ACHRAF GPT V∞", layout="wide")

st.title("🧠 Dashboard لإدارة الصفقات - ACHRAF GPT V∞")

uploaded_file = st.file_uploader("📂 ارفع ملف CSV لعرض الصفقات", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # التحليل الذكي
    df = detect_candle_patterns(df)
    df = detect_liquidity_traps(df)
    df = generate_signals(df)

    # عرض جدول متفاعل
    st.subheader("📋 جدول التحليل الكامل")
    selected_cols = st.multiselect("🎯 اختر الأعمدة التي ترغب في عرضها:", df.columns.tolist(), default=["open", "high", "low", "close", "pattern", "liquidity_trap", "entry_signal"])
    st.dataframe(df[selected_cols].tail(30), use_container_width=True)

    # رسم بياني تفاعلي
    st.subheader("📈 الشموع مع الإشارات الفنية")
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'], high=df['high'],
        low=df['low'], close=df['close'],
        name="Candles"
    )])

    # إضافة إشارات شراء/بيع
    for i, row in df.iterrows():
        if "Buy" in str(row.get("entry_signal", "")):
            fig.add_trace(go.Scatter(x=[i], y=[row["low"]], mode="markers", marker=dict(color="green", size=10), name="Buy"))
        elif "Sell" in str(row.get("entry_signal", "")):
            fig.add_trace(go.Scatter(x=[i], y=[row["high"]], mode="markers", marker=dict(color="red", size=10), name="Sell"))

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 الرجاء رفع ملف CSV أولًا لعرض Dashboard.")
