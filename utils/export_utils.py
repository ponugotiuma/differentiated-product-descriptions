from __future__ import annotations

import csv
import io
import json


def content_json(product: dict, description: str) -> str:
    return json.dumps({"product": product["name"], "category": product["category"], "description": description, "status": product["status"]}, indent=2)


def content_csv(product: dict, description: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["product_id", "product_name", "category", "status", "description"])
    writer.writerow([product["id"], product["name"], product["category"], product["status"], description])
    return output.getvalue()
