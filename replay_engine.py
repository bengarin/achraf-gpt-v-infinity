import csv
from collections import Counter
from statistics import mean

def analyze_decision_log(path="decision_log.csv"):
    decisions = []
    warnings_all = []
    reasons_all = []

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            decisions.append({
                "score": int(row["score"]),
                "quality": row["quality"]
            })
            warnings_all += row["warnings"].split("; ") if row["warnings"] else []
            reasons_all += row["reasons"].split("; ") if row["reasons"] else []

    if not decisions:
        print("⚠️ No decisions found in log.")
        return

    # إحصائيات
    total = len(decisions)
    avg_score = round(mean([d["score"] for d in decisions]), 2)
    qualities = Counter([d["quality"] for d in decisions])
    common_warnings = Counter(warnings_all).most_common(3)
    common_reasons = Counter(reasons_all).most_common(3)

    # عرض التقرير
    print(f"📊 عدد الصفقات المسجلة: {total}")
    print(f"🔢 متوسط التقييم العام: {avg_score}/100")
    print("📈 تصنيف القرارات:")
    for quality, count in qualities.items():
        print(f"  - {quality}: {count} ({round((count/total)*100)}%)")
    print("⚠️ أكثر التحذيرات تكرارًا:")
    for w, n in common_warnings:
        print(f"  - {w} ({n} مرات)")
    print("✅ أكثر الأسباب تكرارًا:")
    for r, n in common_reasons:
        print(f"  - {r} ({n} مرات)")
