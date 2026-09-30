from __future__ import annotations

from .attribute_analyzer import analyze_attributes
from .seo_analyzer import analyze_seo
from .similarity_analyzer import analyze_similarity


def analyze_quality(descriptions: list[str], keywords: str, attributes: list[str]) -> dict:
    per_description = []
    for text in descriptions:
        seo = analyze_seo(text, keywords)
        coverage = analyze_attributes(text, attributes)
        overall = round(seo["score"] * 0.55 + coverage["percentage"] * 0.45)
        per_description.append({"seo": seo, "attributes": coverage, "overall": overall})
    similarity = analyze_similarity(descriptions)
    differentiation = round((1 - similarity["average"]) * 100)
    overall = round(sum(item["overall"] for item in per_description) / 3 * 0.8 + differentiation * 0.2)
    return {"per_description": per_description, "similarity": similarity, "differentiation": differentiation, "overall": overall}
