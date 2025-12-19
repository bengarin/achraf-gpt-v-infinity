import csv
from collections import Counter
from statistics import mean
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def analyze_for_report(path="decision_log.csv", window=10):
    with open(path, mode="r", encoding="utf-8") as file:
        reader = list(csv.DictReader(file))
        if not reader:
            return None

        recent = reader[-window:]
        scores = [int(r["score"]) for r in recent]
        qualities = [r["quality"] for r in recent]
        warnings_all = []
        for r in recent:
            if r["warnings"]:
                warnings_all += r["warnings"].split("; ")

        total = len(recent)
        avg_score = round(mean(scores), 2)
        good_pct = round(qualities.count("Good Decision") / total * 100)
        clean_pct = round(sum(1 for r in recent if not r["warnings"]) / total * 100)
        common_warning = Counter(warnings_all).most_common(1)[0] if warnings_all else ("None", 0)

        mind_score = 0
        mind_score += (good_pct / 100) * 40
        mind_score += (clean_pct / 100) * 30
        mind_score += 20 if common_warning[1] <= 2 else 0
        mind_score += 10 if scores[-1] > scores[0] else 0
        mind_score -= 20 if common_warning[1] > 3 else 0
        mind_score -= 15 if qualities.count("Bad Decision") >= 2 else 0
        mind_score = round(max(0, min(100, mind_score)), 2)

        summary = {
            "total": total,
            "avg_score": avg_score,
            "good_pct": good_pct,
            "clean_pct": clean_pct,
            "common_warning": common_warning,
            "mind_score": mind_score
        }
        return summary

def generate_pdf_report(output_path="trading_mind_report.pdf"):
    data = analyze_for_report()
    if not data:
        print("❌ لا يوجد بيانات لإنشاء تقرير.")
        return

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    flow = []

    title = "🧠 ACHRAF GPT V∞ – تقرير الذكاء التداولي"
    flow.append(Paragraph(title, styles["Title"]))
    flow.append(Spacer(1, 20))

    flow.append(Paragraph(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    flow.append(Paragraph(f"👤 المتداول: Achraf Bengarin", styles["Normal"]))
    flow.append(Spacer(1, 15))

    flow.append(Paragraph(f"🔢 عدد الصفقات الأخيرة: {data['total']}", styles["Normal"]))
    flow.append(Paragraph(f"📈 متوسط التقييم العام: {data['avg_score']}/100", styles["Normal"]))
    flow.append(Paragraph(f"✅ نسبة القرارات الجيدة: {data['good_pct']}%", styles["Normal"]))
    flow.append(Paragraph(f"🔒 نسبة بدون تحذيرات: {data['clean_pct']}%", styles["Normal"]))
    flow.append(Paragraph(f"⚠️ أكثر تحذير تكرر: {data['common_warning'][0]} ({data['common_warning'][1]} مرات)", styles["Normal"]))
    flow.append(Paragraph(f"🧠 MindScore العام: {data['mind_score']} / 100", styles["Normal"]))
    flow.append(Spacer(1, 20))

    # توصية ذكية حسب النتيجة
    if data["mind_score"] >= 80:
        comment = "أداء ممتاز! استمر في الانضباط."
    elif data["mind_score"] >= 60:
        comment = "جيد، لكن تحتاج للمزيد من الصبر والتركيز."
    else:
        comment = "تنبيه! تكرار أخطاء كثيرة – راجع أسلوبك فورًا."

    flow.append(Paragraph("📌 توصية النظام:", styles["Heading3"]))
    flow.append(Paragraph(comment, styles["Normal"]))

    doc.build(flow)
    print("✅ تم إنشاء التقرير بنجاح:", output_path)
