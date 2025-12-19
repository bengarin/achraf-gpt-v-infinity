import csv
from collections import Counter
from statistics import mean

def compute_mind_score(path="decision_log.csv", window=10):
    with open(path, mode="r", encoding="utf-8") as file:
        reader = list(csv.DictReader(file))
        if not reader:
            print("⚠️ لا يوجد بيانات لتقييم السلوك.")
            return

        # نأخذ آخر N صفقة فقط
        recent = reader[-window:]

        scores = [int(row["score"]) for row in recent]
        qualities = [row["quality"] for row in recent]
        all_warnings = []
        for row in recent:
            if row["warnings"]:
                all_warnings += row["warnings"].split("; ")

        # الحسابات
        total = len(recent)
        good_pct = qualities.count("Good Decision") / total * 100
        clean_pct = sum(1 for r in recent if not r["warnings"]) / total * 100
        warning_counts = Counter(all_warnings)
        most_common_warning = warning_counts.most_common(1)[0] if warning_counts else ("None", 0)

        # mind score
        score = 0
        score += (good_pct / 100) * 40
        score += (clean_pct / 100) * 30
        if most_common_warning[1] <= 2:
            score += 20
        if scores[-1] > scores[0]:
            score += 10
        if most_common_warning[1] > 3:
            score -= 20
        if qualities.count("Bad Decision") >= 2:
            score -= 15

        final_score = round(max(0, min(100, score)), 2)

        # 🧠 تقرير بشري
        print("🧠 MindScore:", final_score, "/100")
        print("📈 نسبة القرارات الجيدة:", round(good_pct), "%")
        print("🔒 نسبة القرارات بدون تحذيرات:", round(clean_pct), "%")
        print("⚠️ أكثر خطأ متكرر:", most_common_warning[0], f"({most_common_warning[1]} مرات)")

        if most_common_warning[1] > 3:
            print("🚨 تنبيه: هذا الخطأ يتكرر بشكل مقلق. راجع أسلوب دخولك.")

        if final_score >= 80:
            print("✅ أداء ذهني ممتاز! استمر بنفس الانضباط.")
        elif final_score >= 60:
            print("⚠️ جيد لكن يمكن تحسين الانضباط أكثر.")
        else:
            print("❌ الأداء الذهني ضعيف. أوقف التداول وراجع قراراتك.")
