
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def export_analysis_to_pdf(df: pd.DataFrame, output_path="report.pdf"):
    df = df.tail(30)  # نأخذ آخر 30 شمعة فقط

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("📈 تقرير التحليل الذكي - ACHRAF GPT V∞", styles["Title"])
    elements.append(title)

    # تحديد الأعمدة التي تهمنا فقط
    columns_to_include = ["open", "high", "low", "close", "pattern", "liquidity_trap", "entry_signal"]
    data = [columns_to_include] + df[columns_to_include].fillna("").values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    doc.build(elements)
    return output_path
