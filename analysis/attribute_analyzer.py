from __future__ import annotations


def analyze_attributes(text: str, attributes: list[str]) -> dict:
    known = [str(attribute).strip() for attribute in attributes if str(attribute).strip()]
    covered = [attribute for attribute in known if attribute.lower() in text.lower()]
    missing = [attribute for attribute in known if attribute not in covered]
    return {"covered": covered, "missing": missing, "percentage": round(len(covered) / len(known) * 100) if known else 100}
