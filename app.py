import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ACHRAF GPT V∞", layout="centered")
st.title("📊 ACHRAF GPT V∞")

st.markdown("مساعد ذكي لتحليل الشارتات واكتشاف النماذج الفنية.")

model = st.selectbox("اختر نوع النموذج لتحليله", ["اختراق كاذب", "فخ سيولة", "اختراق مؤكد"])

def show_chart(data, level, label):
    fig, ax = plt.subplots()
    ax.plot(data, label="السعر")
    ax.axhline(y=level, color='red', linestyle='--', label=label)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

if model == "اختراق كاذب":
    data = np.concatenate([
        np.linspace(1.1150, 1.1195, 20),
        np.linspace(1.1195, 1.1215, 5),
        np.linspace(1.1215, 1.1180, 10),
        np.linspace(1.1180, 1.1160, 5)
    ])
    show_chart(data, 1.1200, "مستوى المقاومة")
    st.warning("❌ هذا اختراق كاذب. لا ينصح بالدخول.")

elif model == "فخ سيولة":
    data = np.concatenate([
        np.linspace(1.2980, 1.3000, 15),
        np.linspace(1.3000, 1.3030, 3),
        np.linspace(1.3030, 1.2985, 6),
        np.linspace(1.2985, 1.2960, 6)
    ])
    show_chart(data, 1.3000, "منطقة سيولة")
    st.warning("🪤 فخ سيولة. تجنب الدخول.")

elif model == "اختراق مؤكد":
    data = np.concatenate([
        np.linspace(1.2450, 1.2495, 15),
        np.linspace(1.2495, 1.2525, 5),
        np.linspace(1.2525, 1.2500, 5),
        np.linspace(1.2500, 1.2560, 10)
    ])
    show_chart(data, 1.2500, "مستوى الاختراق")
    st.success("✅ اختراق مؤكد. فرصة جيدة للدخول.")
