from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .prompts import SYSTEM_PROMPT


def load_env() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"'))


def demo_result(name: str, category: str, info: str, keywords: str, brand: str) -> dict[str, Any]:
    facts = [item.strip() for item in [name, category, info, brand] if item.strip()]
    fact_line = ", ".join(facts)
    keyword_phrase = keywords.strip() or name
    return {"product_analysis": {"attributes": facts, "visible_facts": ["Product is shown in the uploaded image"], "user_facts": facts, "unsupported_facts": []}, "description_1": f"Discover {name}, a {category.lower()} designed around the details shoppers search for. Featuring {keyword_phrase}, it presents a clear, fact-grounded choice for your catalog. {info}".strip(), "description_2": f"Make room for {name} in your everyday routine. Its {category.lower()} profile and the provided details ({fact_line}) give customers a straightforward way to understand what makes it useful, without overpromising.", "description_3": f"{name} | {category}\nKey details: {info or 'See product image for appearance.'}\nSearch terms: {keyword_phrase}"}


def generate_descriptions(image_path: str, name: str, category: str, info: str, keywords: str, brand: str) -> tuple[dict[str, Any], bool]:
    load_env()
    demo = os.getenv("DEMO_MODE", "true").lower() in {"1", "true", "yes", "on"}
    if demo:
        return demo_result(name, category, info, keywords, brand), True
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env or enable DEMO_MODE=true.")
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        image_bytes = Path(image_path).read_bytes()
        prompt = f"""{SYSTEM_PROMPT}\n\nProduct name: {name}\nCategory: {category}\nAdditional information: {info}\nTarget SEO keywords: {keywords}\nBrand information: {brand}"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"), prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.4),
        )
        data = json.loads(response.text)
        required = ["product_analysis", "description_1", "description_2", "description_3"]
        if any(not data.get(key) for key in required):
            raise ValueError("Gemini returned incomplete content.")
        return data, False
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned malformed JSON. Please try again.") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc
