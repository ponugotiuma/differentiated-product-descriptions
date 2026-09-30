from __future__ import annotations

import math
import re
from collections import Counter


def _vector(text: str) -> Counter:
    return Counter(re.findall(r"[a-z0-9]+", text.lower()))


def _cosine(first: Counter, second: Counter) -> float:
    keys = set(first) | set(second)
    numerator = sum(first[key] * second[key] for key in keys)
    denominator = math.sqrt(sum(value * value for value in first.values()) * sum(value * value for value in second.values()))
    return round(numerator / denominator, 3) if denominator else 0.0


def analyze_similarity(descriptions: list[str]) -> dict:
    values = {"1-2": _cosine(_vector(descriptions[0]), _vector(descriptions[1])), "1-3": _cosine(_vector(descriptions[0]), _vector(descriptions[2])), "2-3": _cosine(_vector(descriptions[1]), _vector(descriptions[2]))}
    average = sum(values.values()) / len(values)
    return {"method": "Local TF-IDF-style token cosine fallback (not an embedding measurement)", "scores": values, "average": round(average, 3), "warning": average >= 0.72}
