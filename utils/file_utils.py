from __future__ import annotations

import io
import uuid
from pathlib import Path
from PIL import Image, UnidentifiedImageError

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
ALLOWED_TYPES = {"png", "jpg", "jpeg", "webp"}


def save_uploaded_image(uploaded_file) -> tuple[str, Image.Image]:
    suffix = Path(uploaded_file.name).suffix.lower().lstrip(".")
    if suffix not in ALLOWED_TYPES:
        raise ValueError("Unsupported image type. Use PNG, JPG, JPEG, or WEBP.")
    try:
        image = Image.open(io.BytesIO(uploaded_file.getvalue())).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc
    image.thumbnail((1600, 1600))
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{uuid.uuid4().hex}.jpg"
    image.save(path, format="JPEG", quality=88, optimize=True)
    return str(path), image
