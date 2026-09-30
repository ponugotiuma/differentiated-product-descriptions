from __future__ import annotations

import re


def analyze_seo(text: str, keywords: str) -> dict:
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    target = [word.strip().lower() for word in keywords.split(",") if word.strip()]
    detected = [keyword for keyword in target if keyword in text.lower()]
    missing = [keyword for keyword in target if keyword not in detected]
    length_score = 100 if 40 <= len(words) <= 180 else max(40, 100 - abs(len(words) - 100) // 2)
    keyword_score = 100 if not target else round(len(detected) / len(target) * 100)
    structure_score = 100 if len(text.strip()) >= 40 else 45
    score = round(length_score * 0.35 + keyword_score * 0.4 + structure_score * 0.25)
    suggestions = []
    if missing: suggestions.append("Consider adding: " + ", ".join(missing))
    if len(words) < 40: suggestions.append("Add useful, fact-grounded detail for stronger search context.")
    return {"score": min(score, 100), "detected": detected, "missing": missing, "suggestions": suggestions}
