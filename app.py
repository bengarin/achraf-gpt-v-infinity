import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from logic import analyze_chart_image
from csv_logic import analyze_candles_from_csv

st.set_page_config(page_title="ACHRAF GPT V∞", layout="centered")

st.title("🤖 ACHRAF GPT V∞")
st.markdown("### مساعد تداول ذكي: تحليل الشموع والصور")

# 📷 تحليل الصور
st.header("📷 تحليل صورة شارت")
uploaded_image = st.file_uploader("ارفع صورة شارت (PNG أو JPG)", type=["png", "jpg", "jpeg"], key="image")

if uploaded_image is not None:
    st.image(uploaded_image, caption="📊 الشارت المرفوع", use_column_width=True)
    st.markdown("#### 💡 التحليل الذكي:")
    result = analyze_chart_image(uploaded_image)
    st.success(result)

# 📄 تحليل ملف CSV
st.header("📄 تحليل بيانات شموع من ملف CSV")
uploaded_csv = st.file_uploader("ارفع ملف CSV فيه بيانات الشموع (OHLCV)", type=["csv"], key="csv")

if uploaded_csv is not None:
    try:
        df = pd.read_csv(uploaded_csv)
        st.dataframe(df.tail(10), use_container_width=True)
        st.markdown("#### 🧠 التحليل المبدئي:")
        result = analyze_candles_from_csv(uploaded_csv)
        st.success(result)
    except Exception as e:
        st.error(f"حدث خطأ في قراءة الملف: {str(e)}")
