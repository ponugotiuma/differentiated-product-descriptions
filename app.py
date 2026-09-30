from __future__ import annotations

import os
from html import escape
from pathlib import Path

import streamlit as st
from PIL import Image

from ai.gemini_service import generate_descriptions
from analysis.quality_analyzer import analyze_quality
from database.database import (
    add_description,
    create_product,
    dashboard_stats,
    get_product,
    init_db,
    list_products,
    save_quality,
    save_review,
)
from utils.export_utils import content_csv, content_json
from utils.file_utils import save_uploaded_image

st.set_page_config(page_title="Differentiated Product Descriptions", page_icon="✦", layout="wide")
init_db()


def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #17252b; --muted: #52646a; --paper: #fff4e8; --line: #dbe4df; --mint: #d7f3df; --teal: #0e6261; --coral: #f26b5b; --gold: #f4bd4f; --deep-teal: #102f35; --dark-coral: #c94d40; --surface: #ffffff; --surface-warm: #fffaf5; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    [data-testid="stAppViewContainer"] *, [data-testid="stMainBlockContainer"] * { color: var(--ink); }
    h1, h2, h3 { color: var(--ink); font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    [data-testid="stAppViewContainer"] { background: #fff4e8; }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }
    [data-testid="stMainBlockContainer"] { animation: page-in .55s ease both; }
    [data-testid="stSidebar"] { background: var(--deep-teal); border-right: 1px solid #28545a; }
    [data-testid="stSidebar"] * { color: #edf8f2; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label { color: #91b8b1; font-size: 11px; font-weight: 700; letter-spacing: 1.3px; text-transform: uppercase; }
    [data-testid="stSidebar"] [role="radiogroup"] { gap: 7px; }
    [data-testid="stSidebar"] [role="radio"] { border-radius: 10px; padding: 9px 10px; transition: background .2s ease, transform .2s ease; }
    [data-testid="stSidebar"] [role="radio"]:hover { background: #1c4a4e; transform: translateX(4px); }
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"] { background: #f4bd4f; color: #173238; box-shadow: 0 8px 18px #071c20aa; }
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"] * { color: #173238; }
    .brand { padding: 10px 0 25px; position: relative; }
    .brand:after { background: var(--coral); border-radius: 50%; content: ''; height: 7px; position: absolute; right: 8px; top: 18px; width: 7px; animation: blink 2.2s infinite; }
    .brand-mark { color: var(--gold); font-size: 42px; line-height: .8; font-weight: 700; text-shadow: 0 0 22px #f4bd4f88; }
    .brand-name { color: white; font: 700 18px 'Space Grotesk'; line-height: 1.1; margin-top: 10px; }
    .eyebrow { color: var(--coral); font-size: 12px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
    .hero { background: linear-gradient(118deg, #103f45 0%, #176b67 58%, #0d514f 100%); border: 0; border-radius: 14px; box-shadow: 0 18px 40px #14545026; color: white; overflow: hidden; padding: 30px; position: relative; margin-bottom: 28px; }
    .hero:before, .hero:after { border: 1px solid #f4bd4f55; border-radius: 50%; content: ''; position: absolute; pointer-events: none; }
    .hero:before { height: 220px; right: -55px; top: -115px; width: 220px; }
    .hero:after { height: 130px; right: 35px; top: -62px; width: 130px; }
    .hero h1 { color: #ffffff !important; font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.02; margin: 8px 0 10px; max-width: 690px; position: relative; }
    .hero p { color: #c6e7dd !important; font-size: 16px; line-height: 1.55; margin: 0; max-width: 710px; position: relative; }
    .hero .eyebrow { color: var(--gold) !important; position: relative; }
    .metric-label { color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; }
    .metric-value { color: var(--teal); font: 700 31px 'Space Grotesk'; margin-top: 4px; }
    [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 11px; padding: 14px 16px; box-shadow: 0 6px 15px #234a3c0c; transition: transform .2s ease, box-shadow .2s ease; }
    [data-testid="stMetric"] *, [data-testid="stVerticalBlockBorderWrapper"] * { color: var(--ink); }
    [data-testid="stTextInput"] label, [data-testid="stTextArea"] label, [data-testid="stSelectbox"] label, [data-testid="stFileUploader"] label, [data-testid="stRadio"] label { color: var(--ink) !important; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] [data-baseweb="select"] *, [data-testid="stFileUploader"] section, [data-testid="stFileUploader"] section * { color: var(--ink) !important; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] [data-baseweb="select"] > div, [data-testid="stFileUploader"] section { background: #ffffff !important; border-color: var(--line) !important; color: #000000 !important; }
    [data-testid="stFileUploader"] button, [data-testid="stFileUploader"] button * { background: #ffffff !important; border-color: var(--line) !important; color: #000000 !important; }
    [data-testid="stBaseButton-secondary"], button[kind="secondary"] { background: #ffffff !important; border: 1px solid var(--line) !important; color: #000000 !important; }
    [data-testid="stBaseButton-secondary"] *, button[kind="secondary"] * { color: #000000 !important; }
    [data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color: var(--muted) !important; opacity: 1; }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
    [data-testid="stAlert"] *, [data-testid="stInfo"] *, [data-testid="stWarning"] *, [data-testid="stSuccess"] *, [data-testid="stError"] * { color: var(--ink) !important; }
    [data-testid="stCodeBlock"] * { color: #edf8f2 !important; }
    [data-testid="stMetric"]:hover { box-shadow: 0 12px 24px #234a3c1c; transform: translateY(-4px); }
    [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, var(--teal), #61b99b, var(--gold)); background-size: 200% 100%; animation: shimmer 2.8s linear infinite; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: #ffffffd9; border-color: var(--line); border-radius: 12px; box-shadow: 0 7px 18px #234a3c0a; transition: transform .2s ease, box-shadow .2s ease; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: 0 14px 26px #234a3c16; transform: translateY(-3px); }
    .status-pill { display: inline-block; padding: 5px 11px; border-radius: 999px; font-size: 12px; font-weight: 700; background: var(--mint); color: #287057 !important; }
    .warning-box { background: #fff6df; border-left: 4px solid var(--gold); padding: 10px 14px; color: #72521d !important; }
    .products-table { background: #ffffff; border: 1px solid var(--line); border-radius: 8px; color: #000000; overflow: hidden; width: 100%; }
    .products-table table { border-collapse: collapse; color: #000000; width: 100%; }
    .products-table th { background: #ffffff; border-bottom: 1px solid var(--line); color: #000000; font-size: 12px; font-weight: 600; padding: 10px 9px; text-align: left; }
    .products-table td { background: #ffffff; border-bottom: 1px solid #edf1ee; color: #000000; font-size: 13px; padding: 10px 9px; }
    .products-table tr:last-child td { border-bottom: 0; }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus, [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within { border-color: var(--teal) !important; box-shadow: 0 0 0 1px var(--teal) !important; }
    [data-testid="stBaseButton-primary"], button[kind="primary"] { background: var(--coral) !important; border: 0 !important; box-shadow: 0 7px 0 var(--dark-coral) !important; color: #fff !important; transition: transform .15s ease, box-shadow .15s ease; }
    [data-testid="stBaseButton-primary"] *, button[kind="primary"] * { color: #fff !important; }
    [data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover { background: var(--dark-coral) !important; box-shadow: 0 4px 0 #a63f35 !important; transform: translateY(3px); }
    @keyframes page-in { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes blink { 0%, 100% { opacity: .35; transform: scale(.8); } 50% { opacity: 1; transform: scale(1.15); } }
    @keyframes shimmer { to { background-position: -200% 0; } }
    @media (max-width: 720px) { .hero { padding: 23px; } .hero h1 { font-size: 2.2rem; } [data-testid="stMetric"] { padding: 11px; } }
    </style>
    """, unsafe_allow_html=True)


def product_attributes(product_analysis: dict) -> list[str]:
    raw = product_analysis.get("attributes", [])
    return [str(item) for item in raw] if isinstance(raw, list) else []


def quality_cards(result: dict) -> None:
    cols = st.columns(4)
    labels = [("Overall", result["overall"]), ("SEO", round(sum(item["seo"]["score"] for item in result["per_description"]) / 3)), ("Coverage", round(sum(item["attributes"]["percentage"] for item in result["per_description"]) / 3)), ("Differentiation", result["differentiation"])]
    for column, (label, value) in zip(cols, labels):
        with column:
            st.markdown(f'<div class="metric-label">{label}</div><div class="metric-value">{value}%</div>', unsafe_allow_html=True)


def render_analysis(product: dict) -> None:
    quality = product.get("quality", [])
    if not quality:
        st.info("Quality analysis will appear after generation.")
        return
    latest = quality[-3:]
    similarity = __import__("json").loads(latest[-1]["similarity_scores"])
    quality_cards({"overall": product["quality_score"], "differentiation": round((1 - similarity["average"]) * 100), "per_description": [{"seo": {"score": item["seo_score"]}, "attributes": {"percentage": item["attribute_coverage"]}} for item in latest]})
    st.subheader("Per-description quality")
    for index, item in enumerate(latest, 1):
        cols = st.columns([1, 1, 2])
        cols[0].metric(f"Description {index} SEO", f"{item['seo_score']:.0f}%")
        cols[1].metric("Attribute coverage", f"{item['attribute_coverage']:.0f}%")
        cols[2].progress(min(float(item["overall_score"]) / 100, 1), text=f"Overall {item['overall_score']:.0f}%")
    if latest:
        st.subheader("Semantic similarity")
        st.caption("Transparent local fallback: token cosine similarity, not an embedding API measurement.")
        cols = st.columns(3)
        for column, (pair, score) in zip(cols, similarity["scores"].items()):
            column.metric(pair, f"{score:.3f}")
        if similarity.get("warning"):
            st.warning("These descriptions may be too similar. Consider editing their angle or structure.")


def dashboard() -> None:
    stats = dashboard_stats()
    st.markdown('<div class="hero"><div class="eyebrow">Content operations / overview</div><h1>Product content, with a quality gate.</h1><p>Turn one product input into differentiated, reviewable content that is ready for a human decision.</p></div>', unsafe_allow_html=True)
    cols = st.columns(5)
    metrics = [("Products processed", stats["products"]), ("Descriptions generated", stats["descriptions"]), ("Pending reviews", stats["pending"]), ("Approved", stats["approved"]), ("Average quality", f"{stats['average']:.0f}%")]
    for column, (label, value) in zip(cols, metrics):
        column.markdown(f'<div class="metric-label">{label}</div><div class="metric-value">{value}</div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Recent products")
    products = list_products()[:8]
    if products:
        rows = "".join(
            f"<tr><td>{escape(str(product['id']))}</td><td>{escape(product['name'])}</td>"
            f"<td>{escape(product['category'])}</td><td>{escape(product['status'])}</td>"
            f"<td>{product['quality_score']:.0f}%</td><td>{escape(product['created_at'][:10])}</td></tr>"
            for product in products
        )
        st.markdown(
            '<div class="products-table"><table><thead><tr>'
            '<th>ID</th><th>Product</th><th>Category</th><th>Status</th>'
            '<th>Quality</th><th>Processed</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No products yet. Start with a product image and a few known facts.")
    if st.button("Create Product Description", type="primary"):
        st.session_state.next_page = "Create Product"
        st.rerun()


def create_product_page() -> None:
    st.markdown('<div class="eyebrow">01 / input</div>', unsafe_allow_html=True)
    st.title("Create product")
    st.caption("Give the model the facts you know. It will keep visible observations and user-provided information separate from unsupported claims.")
    left, right = st.columns([1.05, 1])
    with left:
        name = st.text_input("Product name *", placeholder="e.g. Alpine Trail Bottle")
        category = st.text_input("Product category", placeholder="e.g. Drinkware")
        info = st.text_area("Additional product information", placeholder="Known color, use case, included items, or other verified details.", height=120)
        keywords = st.text_input("Target SEO keywords", placeholder="Separate keywords with commas")
        brand = st.text_input("Optional brand information")
    with right:
        uploaded = st.file_uploader("Product image *", type=["png", "jpg", "jpeg", "webp"])
        if uploaded:
            try:
                st.image(uploaded, caption="Image preview", use_container_width=True)
            except Exception:
                st.error("That image could not be previewed.")
    if st.button("Generate 3 Descriptions", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Product name is required.")
        elif not uploaded:
            st.error("Product image is required.")
        else:
            try:
                image_path, _ = save_uploaded_image(uploaded)
                with st.spinner("Analyzing the product and building three distinct approaches..."):
                    result, is_demo = generate_descriptions(image_path, name, category or "Product", info, keywords, brand)
                    product_id = create_product({"name": name.strip(), "category": category.strip() or "Uncategorized", "image_path": image_path, "additional_info": info, "target_keywords": keywords, "brand_info": brand, "product_analysis": result.get("product_analysis", {})})
                    descriptions = [result["description_1"].strip(), result["description_2"].strip(), result["description_3"].strip()]
                    attributes = product_attributes(result.get("product_analysis", {})) + [item.strip() for item in info.split(",") if item.strip()]
                    quality = analyze_quality(descriptions, keywords, attributes)
                    ids = [add_description(product_id, label, text, quality["per_description"][index]["seo"]["score"], quality["per_description"][index]["attributes"]["percentage"]) for index, (label, text) in enumerate(zip(["SEO-focused", "Customer-benefit", "Marketplace"], descriptions))]
                    save_quality(product_id, quality, ids)
                    st.session_state.current_product_id = product_id
                    st.session_state.next_page = "Generated Descriptions"
                if is_demo:
                    st.info("Demo Mode: generated content uses realistic local sample output. Set DEMO_MODE=false for Gemini.")
                st.rerun()
            except (ValueError, RuntimeError, OSError) as exc:
                st.error(str(exc))


def generated_page() -> None:
    product = get_product(st.session_state.get("current_product_id", 0))
    st.markdown('<div class="eyebrow">02 / generated content</div>', unsafe_allow_html=True)
    st.title("Generated descriptions")
    if not product:
        st.info("Generate a product first, or open one from Product History.")
        return
    st.caption(f"{product['name']} / {product['category']}")
    for index, description in enumerate(product["descriptions"], 1):
        with st.container(border=True):
            st.subheader(f"Description {index}  ·  {description['description_type']}")
            st.write(description["description_text"])
    st.success("Exactly three descriptions are stored for human comparison and review.")


def quality_page() -> None:
    st.markdown('<div class="eyebrow">03 / quality gate</div>', unsafe_allow_html=True)
    st.title("Quality analysis")
    product = get_product(st.session_state.get("current_product_id", 0))
    if product:
        render_analysis(product)
    else:
        st.info("Generate or select a product to inspect its quality analysis.")


def review_page() -> None:
    st.markdown('<div class="eyebrow">04 / human decision</div>', unsafe_allow_html=True)
    st.title("Human review")
    product = get_product(st.session_state.get("current_product_id", 0))
    if not product:
        st.info("Generate or select a product to review.")
        return
    options = [f"Description {index + 1} · {item['description_type']}" for index, item in enumerate(product["descriptions"])]
    selected = st.radio("Choose the working version", options, horizontal=True)
    selected_index = options.index(selected)
    edited = st.text_area("Edit before approval", value=product["descriptions"][selected_index]["description_text"], height=180)
    cols = st.columns(2)
    with cols[0]:
        if st.button("Approve selected description", type="primary", use_container_width=True):
            if not edited.strip():
                st.error("The final description cannot be empty.")
            else:
                save_review(product["id"], product["descriptions"][selected_index]["id"], edited.strip(), "Approved")
                st.success("Approved description saved.")
                st.rerun()
    with cols[1]:
        if st.button("Reject and keep in review", use_container_width=True):
            save_review(product["id"], product["descriptions"][selected_index]["id"], edited.strip(), "Rejected")
            st.warning("Product remains available for another review.")
    if product.get("review") and product["review"]["review_status"] == "Approved":
        st.divider()
        st.subheader("Final approved content")
        final_text = product["review"]["edited_text"]
        st.code(final_text, language=None)
        st.download_button("Download TXT", final_text, file_name=f"{product['name']}.txt")
        st.download_button("Download JSON", content_json(product, final_text), file_name=f"{product['name']}.json", mime="application/json")
        st.download_button("Download CSV", content_csv(product, final_text), file_name=f"{product['name']}.csv", mime="text/csv")


def history_page() -> None:
    st.markdown('<div class="eyebrow">05 / archive</div>', unsafe_allow_html=True)
    st.title("Product history")
    products = list_products()
    statuses = ["All"] + sorted({p["status"] for p in products})
    categories = ["All"] + sorted({p["category"] for p in products})
    left, right = st.columns(2)
    status = left.selectbox("Filter by status", statuses)
    category = right.selectbox("Filter by category", categories)
    filtered = list_products(status, category)
    if not filtered:
        st.info("No products match these filters.")
        return
    for item in filtered:
        with st.container(border=True):
            cols = st.columns([3, 2, 1, 1])
            cols[0].markdown(f"**{item['name']}**  \n{item['category']} · {item['created_at'][:10]}")
            cols[1].markdown(f'<span class="status-pill">{item["status"]}</span>', unsafe_allow_html=True)
            cols[2].metric("Quality", f"{item['quality_score']:.0f}%")
            if cols[3].button("Open", key=f"open-{item['id']}"):
                st.session_state.current_product_id = item["id"]
                st.session_state.next_page = "Generated Descriptions"
                st.rerun()


def main() -> None:
    inject_css()
    pages = ["Dashboard", "Create Product", "Generated Descriptions", "Quality Analysis", "Human Review", "Product History"]
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "next_page" in st.session_state:
        st.session_state.page = st.session_state.pop("next_page")
    with st.sidebar:
        st.markdown('<div class="brand"><div class="brand-mark">✦</div><div class="brand-name">Differentiated<br>Product Descriptions</div></div>', unsafe_allow_html=True)
        page = st.radio("Workspace", pages, key="page")
    {"Dashboard": dashboard, "Create Product": create_product_page, "Generated Descriptions": generated_page, "Quality Analysis": quality_page, "Human Review": review_page, "Product History": history_page}[page]()


if __name__ == "__main__":
    main()
