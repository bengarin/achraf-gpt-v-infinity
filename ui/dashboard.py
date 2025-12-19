import streamlit as st
import pandas as pd
from collections import Counter
from statistics import mean
import altair as alt
from app.logic import evaluate_trade_decision
# ==========================================
# تحميل البيانات من ملف سجل التداول
# ==========================================
@st.cache_data
def load_data(path="decision_log.csv"):
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        st.warning("⚠️ لم يتم العثور على ملف decision_log.csv.")
        return pd.DataFrame()

# ==========================================
# حساب MindScore من آخر 10 قرارات
# ==========================================
def compute_mindscore(df):
    if df.empty:
        return 0, {}, {}

    recent = df.tail(10)
    scores = recent["score"].tolist()
    qualities = recent["quality"].tolist()
    warnings_all = "; ".join(recent["warnings"].dropna().tolist()).split("; ")
    warnings_all = [w.strip() for w in warnings_all if w.strip()]

    total = len(recent)
    good_pct = qualities.count("Good Decision") / total * 100
    clean_pct = sum(1 for w in recent["warnings"] if not isinstance(w, str) or w.strip() == "") / total * 100
    warning_counts = Counter(warnings_all)

    score = 0
    score += (good_pct / 100) * 40
    score += (clean_pct / 100) * 30
    score += 20 if warning_counts.most_common(1)[0][1] <= 2 else 0
    score += 10 if scores[-1] > scores[0] else 0
    score -= 20 if warning_counts.most_common(1)[0][1] > 3 else 0
    score -= 15 if qualities.count("Bad Decision") >= 2 else 0
    score = round(max(0, min(100, score)), 2)

    return score, warning_counts, {"good_pct": good_pct, "clean_pct": clean_pct}

# ==========================================
# حساب تطور MindScore عبر الزمن (رسم بياني)
# ==========================================
def compute_mindscore_series(df, window=5):
    """حساب MindScore عبر الزمن على دفعات."""
    if len(df) < window:
        return pd.DataFrame()

    scores = []
    for i in range(window, len(df)+1):
        subset = df.iloc[i-window:i]
        score, _, _ = compute_mindscore(subset)
        scores.append({"index": i, "mind_score": score})
    return pd.DataFrame(scores)

# ==========================================
# واجهة Streamlit
# ==========================================
st.set_page_config(page_title="ACHRAF GPT V∞ Dashboard", layout="centered")
st.title("📊 ACHRAF GPT V∞ – لوحة الذكاء التداولي")
st.markdown("تحليل فوري لسلوكك التداولي بناءً على سجل القرارات")

# تحميل البيانات
df = load_data()

if not df.empty:
    st.subheader("🔢 عدد الصفقات:")
    st.metric(label="Total Trades", value=len(df))

    st.subheader("🧠 MindScore:")
    mind_score, warnings, stats = compute_mindscore(df)
    st.metric(label="MindScore", value=f"{mind_score}/100")

    st.subheader("📈 تحليل الأداء:")
    st.write(f"✅ قرارات جيدة: {round(stats['good_pct'])}%")
    st.write(f"🔒 بدون تحذيرات: {round(stats['clean_pct'])}%")

    st.subheader("⚠️ أكثر التحذيرات تكرارًا:")
    if warnings:
        for warn, count in warnings.most_common(3):
            st.write(f"- {warn}: {count} مرات")
    else:
        st.write("لا يوجد تحذيرات متكررة.")

    # الرسم البياني لتطور MindScore
    st.subheader("📉 تطوّر MindScore عبر الزمن:")
    score_data = compute_mindscore_series(df)
    if not score_data.empty:
        chart = alt.Chart(score_data).mark_line(point=True).encode(
            x=alt.X('index', title='رقم الصفقة'),
            y=alt.Y('mind_score', title='MindScore'),
            tooltip=["index", "mind_score"]
        ).properties(width=600, height=300)
        st.altair_chart(chart)
    else:
        st.info("🔍 لا يوجد بيانات كافية للرسم البياني (تحتاج على الأقل 5 صفقات).")

    # عرض سجل القرارات بالكامل
    with st.expander("📄 عرض سجل كامل للقرارات"):
        st.dataframe(df)

else:
    st.info("📭 لا توجد بيانات متاحة حالياً.")
