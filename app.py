import base64
import html
import json
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "business.json"
LOGO_IMAGE_PATH = "assets/651fa53d-7fd1-4663-8600-aba5389a5bca.png"
PRODUCT_250G_SIZE_LABEL = "250 g"
PRODUCT_500G_SIZE_LABEL = "500 g"
PRODUCT_1KG_SIZE_LABEL = "1 kg"
LOOSE_TEA_IMAGE_PATHS = {
    PRODUCT_250G_SIZE_LABEL: "assets/6cc32f61-1971-49cd-9962-55ca04232192.png",
    PRODUCT_500G_SIZE_LABEL: "assets/cd822b57-ac2f-40b7-ad87-d434f32afe0b.png",
    PRODUCT_1KG_SIZE_LABEL: "assets/4e101546-ebb5-4381-8d29-f7a360030067.png",
}
LAMSA_TEA_IMAGE_PATH = "assets/bdc8f3c0-9962-4796-8b6a-ffc29437e487.png"
MASALA_TEA_IMAGE_PATH = "assets/094c11e2-a39c-4b8e-949b-e66d416e0534.png"


def load_business_data() -> dict:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def local_background_css(image_path: str) -> str:
    path = BASE_DIR / image_path
    if not path.exists():
        return (
            "linear-gradient(90deg, rgba(250,245,234,.96) 0%, rgba(250,245,234,.72) 38%, "
            "rgba(33,77,54,.28) 100%), "
            "linear-gradient(120deg, #eef1d3 0%, #adbd61 40%, #365d37 100%)"
        )

    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        "linear-gradient(90deg, rgba(250,245,234,.94) 0%, rgba(250,245,234,.72) 39%, "
        "rgba(18,39,27,.12) 68%), "
        f"url('data:{mime};base64,{encoded}')"
    )


def local_image_src(image_path: str) -> str:
    path = BASE_DIR / image_path
    if not path.exists():
        return ""

    mime_by_suffix = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    mime = mime_by_suffix.get(path.suffix.lower(), "image/png")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def product_pack_html(
    name: str,
    image_class: str,
    pack_class: str,
    size_label: str,
    prefer_image: bool = True,
) -> str:
    image_src = local_image_src(LOOSE_TEA_IMAGE_PATHS.get(size_label, ""))
    if prefer_image and image_src:
        return (
            f'<img class="{image_class}" src="{image_src}" '
            f'alt="{safe(name)} {safe(size_label)} tea packet">'
        )

    return (
        f'<div class="{pack_class}">'
        "<small>Assam Tea Company</small>"
        f"<strong>{safe(name)}<br>Black Tea</strong>"
        "</div>"
    )


def safe(text: str) -> str:
    return html.escape(text)


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("/", "-")


def query_value(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def add_item_to_bag(item: dict) -> None:
    if "bag_items" not in st.session_state:
        st.session_state.bag_items = []
    st.session_state.bag_items.append(item)


data = load_business_data()
hero = data["hero"]
PAGE_SLUGS = {
    "Home": "home",
    "Products": "products",
    "About Us": "about",
    "Checkout": "checkout",
}
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
current_page = st.session_state.current_page
if current_page not in PAGE_SLUGS.values():
    current_page = "home"
    st.session_state.current_page = "home"
if query_value("product"):
    current_page = "products"
    st.session_state.current_page = "products"
page_titles = {
    "home": "Home",
    "products": "Products",
    "about": "About Us",
    "checkout": "Checkout",
}

st.set_page_config(
    page_title=f"{data['company_name']} | {page_titles[current_page]}",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

background = local_background_css(hero["image_path"])

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, header, footer {{visibility: hidden;}}
    .stApp {{ background: #FAF5EA; color: #302A22; }}
    .block-container {{
        max-width: 100%;
        padding: 0;
        font-family: 'Inter', Arial, sans-serif;
    }}
    .announcement {{
        background: #214D36;
        color: #FAF5EA;
        height: 42px;
        overflow: hidden;
        display: flex;
        align-items: center;
        white-space: nowrap;
        letter-spacing: .05em;
        font-size: .86rem;
        font-weight: 500;
    }}
    .announcement-track {{
        min-width: max-content;
        animation: tea-scroll 27s linear infinite;
    }}
    .announcement-track span {{ padding: 0 2.2rem; }}
    @keyframes tea-scroll {{
        from {{ transform: translateX(0); }}
        to {{ transform: translateX(-50%); }}
    }}
    .nav {{
        height: 86px;
        padding: 0 clamp(1.3rem, 6vw, 5.5rem);
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(250, 245, 234, .97);
        border-bottom: 1px solid #E8DDBF;
    }}
    .brand {{ display: flex; align-items: center; gap: .82rem; }}
    .logo {{
        width: 82px; height: 82px;
        border-radius: 0;
        display: block;
        object-fit: contain;
        background: transparent;
    }}
    .logo-fallback {{
        width: 49px; height: 49px;
        border-radius: 50%;
        display: grid; place-items: center;
        color: #FAF5EA;
        background: #214D36;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 1.45rem; font-weight: 700;
    }}
    .brand-name {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-weight: 700; font-size: clamp(1.5rem, 2vw, 1.8rem);
        color: #173A28;
    }}
    .brand-strip {{
        padding: .75rem 0 .7rem clamp(1.3rem, 6vw, 5.5rem);
        background: rgba(250, 245, 234, .97);
        border-bottom: 1px solid #E8DDBF;
        min-height: 100px;
    }}
    .brand-strip .brand-name {{
        font-size: clamp(1.55rem, 2.2vw, 2rem);
    }}
    .links {{ display: flex; align-items: center; gap: clamp(1.1rem, 3vw, 2.8rem); }}
    .links a {{
        text-decoration: none; color: #42392E;
        font-size: .96rem; font-weight: 500;
    }}
    .links .active {{ color: #214D36; font-weight: 700; border-bottom: 2px solid #B58B3B; padding-bottom: .35rem; }}
    [data-testid="stBaseButton-pills"] {{
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        color: #42392E !important;
        font-weight: 600 !important;
        padding: .35rem .75rem !important;
    }}
    [data-testid="stBaseButton-pillsActive"] {{
        border: 0 !important;
        border-bottom: 2px solid #B58B3B !important;
        border-radius: 0 !important;
        background: transparent !important;
        color: #214D36 !important;
        font-weight: 800 !important;
        padding: .35rem .75rem !important;
    }}
    .page-hero {{
        padding: clamp(3.3rem, 7vw, 5.5rem) clamp(1.3rem, 7vw, 6.2rem);
        background:
            linear-gradient(90deg, rgba(250,245,234,.95), rgba(250,245,234,.8)),
            linear-gradient(120deg, #F2E8D3 0%, #D6C183 58%, #214D36 100%);
    }}
    .page-hero-inner {{
        max-width: 900px;
    }}
    .page-hero h1 {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2.8rem, 5vw, 4.25rem);
        line-height: 1.04;
        color: #173A28;
        margin: 0 0 1rem;
    }}
    .page-hero p {{
        color: #5D503F;
        font-size: 1.08rem;
        line-height: 1.75;
        max-width: 680px;
        margin: 0;
    }}
    .hero {{
        min-height: min(660px, calc(100vh - 128px));
        padding: clamp(3.5rem, 8vw, 6.8rem) clamp(1.3rem, 7vw, 6.2rem);
        display: flex; align-items: center;
        background-image: {background};
        background-position: center;
        background-size: cover;
    }}
    .hero-content {{ max-width: 575px; }}
    .eyebrow {{
        text-transform: uppercase; letter-spacing: .18em;
        color: #826527; font-size: .77rem; font-weight: 700; margin-bottom: 1.1rem;
    }}
    h1.hero-title {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(3rem, 5vw, 4.4rem);
        line-height: 1.02; margin: 0 0 1.15rem;
        color: #183D2B; font-weight: 700;
    }}
    .hero-line {{
        color: #4A4032; font-size: clamp(1rem, 1.4vw, 1.14rem);
        letter-spacing: .04em; margin-bottom: 2.25rem;
    }}
    .cta {{
        display: inline-block; background: #214D36; color: #FAF5EA !important;
        border-radius: 999px; padding: .95rem 2.15rem;
        text-decoration: none; font-weight: 600;
        box-shadow: 0 10px 22px rgba(33,77,54,.2);
    }}
    .section {{
        padding: clamp(3.4rem, 6vw, 5.2rem) clamp(1.3rem, 7vw, 6.2rem);
    }}
    .cream {{ background: #FAF5EA; }}
    .soft {{ background: #F2E8D3; }}
    .section-heading {{
        text-align: center; max-width: 700px; margin: 0 auto 2.6rem;
    }}
    .kicker {{
        color: #98742E; text-transform: uppercase; font-weight: 700;
        letter-spacing: .17em; font-size: .74rem; margin-bottom: .7rem;
    }}
    .section-heading h2 {{
        color: #173A28; font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2.2rem, 3vw, 2.8rem); margin: 0 0 .65rem;
    }}
    .section-heading p {{ color: #665A49; margin: 0; line-height: 1.7; }}
    .cards {{
        display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1.35rem; max-width: 1180px; margin: 0 auto;
    }}
    .review {{
        background: #FFFDF7; border: 1px solid #E9DDBD; border-radius: 18px;
        padding: 1.7rem 1.65rem; min-height: 166px;
    }}
    .stars {{ color: #B58B3B; letter-spacing: .18rem; font-size: .84rem; }}
    .review .quote {{ color: #453C30; line-height: 1.67; margin: 1rem 0 1.2rem; }}
    .review .person {{ font-weight: 600; color: #214D36; font-size: .93rem; }}
    .review .sample {{ color: #847762; font-size: .8rem; margin-left: .35rem; }}
    .benefit {{
        text-align: center; padding: 1.7rem 1.35rem;
    }}
    .benefit-icon {{
        margin: 0 auto 1.15rem; width: 54px; height: 54px; border-radius: 50%;
        background: #E7D7AF; color: #214D36; display: grid; place-items: center;
        font-size: 1.42rem;
    }}
    .benefit h3 {{
        font-family: 'Cormorant Garamond', Georgia, serif; color: #173A28;
        font-size: 1.7rem; margin: 0 0 .55rem;
    }}
    .benefit p {{ color: #665A49; line-height: 1.7; margin: 0; }}
    .feature {{
        max-width: 1180px; margin: 0 auto; border-radius: 22px;
        display: grid; grid-template-columns: .88fr 1.12fr; overflow: hidden;
        background: #214D36; color: #FAF5EA;
    }}
    .packet {{
        min-height: 265px; background: #DFC995;
        display: grid; place-items: center;
    }}
    .packet-shape {{
        width: 150px; height: 198px; border-radius: 8px;
        background: #F9F1DE; color: #214D36; display: flex; flex-direction: column;
        align-items: center; justify-content: center; box-shadow: 0 16px 27px rgba(0,0,0,.13);
        text-align: center; padding: 1rem;
    }}
    .packet-shape strong {{ font-family: 'Cormorant Garamond'; font-size: 1.45rem; line-height: 1.05; }}
    .packet-shape span {{ font-size: .68rem; margin-top: .75rem; letter-spacing: .12em; }}
    .feature-copy {{ padding: clamp(2rem, 5vw, 3.2rem); }}
    .feature-copy h2 {{
        font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.55rem;
        margin: .35rem 0 .8rem; color: #FAF5EA;
    }}
    .feature-copy p {{ color: #EEE2C9; max-width: 490px; line-height: 1.7; }}
    .feature-note {{ font-size: .87rem; color: #CDB781 !important; }}
    .product-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1.35rem;
        max-width: 1180px;
        margin: 0 auto;
    }}
    .shop-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 2.1rem;
        max-width: 1180px;
        margin: 0 auto;
    }}
    .shop-card {{
        display: block;
        background: #FFFDF7;
        border: 1px solid #EEE5D1;
        text-decoration: none;
        color: #302A22;
        padding-bottom: 2rem;
        transition: transform .18s ease, box-shadow .18s ease;
    }}
    .shop-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 18px 38px rgba(33,77,54,.12);
    }}
    .shop-image {{
        min-height: 420px;
        display: grid;
        place-items: center;
        background: transparent;
        position: relative;
        overflow: hidden;
    }}
    .stock-tag {{
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(48,42,34,.62);
        color: #FFFFFF;
        padding: .45rem .9rem;
        font-size: .95rem;
    }}
    .shop-pack {{
        width: min(290px, 72%);
        min-height: 205px;
        border-radius: 16px;
        background: linear-gradient(160deg, #214D36 0%, #173A28 60%, #E06625 60%, #F2A23A 100%);
        color: #FAF5EA;
        box-shadow: 0 22px 34px rgba(0,0,0,.16);
        border: 7px solid #F9F1DE;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 1.65rem;
    }}
    .shop-pack small {{
        color: #F4D999;
        text-transform: uppercase;
        letter-spacing: .15em;
        font-weight: 800;
        margin-bottom: .8rem;
    }}
    .shop-pack strong {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: .95;
    }}
    .shop-product-image {{
        width: min(560px, 98%);
        max-height: 410px;
        object-fit: contain;
        display: block;
    }}
    .shop-info {{
        text-align: center;
        padding: 2rem 1.4rem 0;
    }}
    .shop-weight {{
        color: #7B7064;
        font-size: 1.35rem;
        margin-bottom: 1.25rem;
    }}
    .shop-info h3 {{
        color: #302A22;
        font-family: 'Inter', Arial, sans-serif;
        font-size: clamp(1.65rem, 3vw, 2.05rem);
        line-height: 1.2;
        margin: 0 0 1rem;
    }}
    .shop-rating {{
        color: #302A22;
        margin-bottom: 1.35rem;
        font-size: 1rem;
    }}
    .shop-rating span {{
        color: #F1B739;
        font-size: 1.35rem;
        letter-spacing: .08em;
        vertical-align: middle;
    }}
    .shop-price {{
        font-size: clamp(2rem, 4vw, 2.7rem);
        font-weight: 400;
        margin-bottom: 1.65rem;
    }}
    .product-select-note {{
        text-align: center;
        color: #214D36;
        font-size: .95rem;
        font-weight: 700;
        margin-top: -1.15rem;
        margin-bottom: 1.35rem;
    }}
    .back-link {{
        display: inline-block;
        color: #214D36 !important;
        font-weight: 700;
        text-decoration: none;
        margin-bottom: 1.3rem;
    }}
    .product-detail-list {{
        display: grid;
        gap: 2rem;
        max-width: 1180px;
        margin: 0 auto;
    }}
    .product-detail {{
        display: grid;
        grid-template-columns: .95fr 1.05fr;
        gap: clamp(2rem, 5vw, 4rem);
        align-items: center;
        background: #FFFDF7;
        border: 1px solid #E9DDBD;
        border-radius: 26px;
        padding: clamp(1.4rem, 4vw, 2.4rem);
        box-shadow: 0 18px 42px rgba(33,77,54,.09);
    }}
    .product-visual {{
        min-height: 610px;
        border-radius: 0;
        background: transparent;
        display: grid;
        align-items: center;
        justify-items: start;
        overflow: visible;
    }}
    .mock-pack {{
        width: min(330px, 74%);
        min-height: 250px;
        border-radius: 18px;
        background: linear-gradient(160deg, #214D36 0%, #173A28 58%, #C08B2C 58%, #E7B753 100%);
        color: #FAF5EA;
        box-shadow: 0 24px 42px rgba(0,0,0,.2);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2rem;
        border: 8px solid #F9F1DE;
    }}
    .mock-pack small {{
        color: #F4D999;
        text-transform: uppercase;
        letter-spacing: .16em;
        font-weight: 800;
        margin-bottom: 1rem;
    }}
    .mock-pack strong {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2.2rem, 4vw, 3.6rem);
        line-height: .95;
    }}
    .mock-pack span {{
        margin-top: 1rem;
        letter-spacing: .12em;
        font-size: .82rem;
    }}
    .detail-product-image {{
        width: min(720px, 100%);
        max-height: 600px;
        object-fit: contain;
        display: block;
    }}
    .product-info .brand-line {{
        color: #E06625;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }}
    .product-info h2 {{
        color: #302A22;
        font-family: 'Inter', Arial, sans-serif;
        font-size: clamp(2.5rem, 5vw, 4.2rem);
        font-weight: 400;
        line-height: 1.12;
        margin: 0 0 1.25rem;
    }}
    .from-price {{
        color: #302A22;
        font-size: clamp(2rem, 3vw, 2.9rem);
        margin: 0 0 1.15rem;
        font-weight: 400;
    }}
    .product-desc {{
        color: #5D503F;
        font-size: 1.04rem;
        line-height: 1.7;
        max-width: 620px;
        margin-bottom: 1.15rem;
    }}
    .review-line {{
        color: #4B4135;
        display: flex;
        align-items: center;
        gap: .65rem;
        margin: 1rem 0 1.55rem;
        font-size: .98rem;
    }}
    .review-stars {{
        color: #F1B739;
        letter-spacing: .08em;
        font-size: 1.35rem;
    }}
    .size-picker {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: .75rem;
        margin: 0 0 1.35rem;
    }}
    .size-option {{
        display: block;
        border: 2px solid #E06625;
        border-radius: 10px;
        padding: .8rem .75rem;
        text-align: center;
        background: #FFFDF7;
        color: #302A22 !important;
        text-decoration: none;
    }}
    .size-option.active {{
        background: #E06625;
        color: #FFFFFF !important;
    }}
    .size-option.active span {{
        color: #FFFFFF;
    }}
    .size-option span {{
        display: block;
        color: #E06625;
        font-weight: 800;
        margin-top: .2rem;
    }}
    .selected-summary {{
        background: #F7EDD7;
        border-radius: 12px;
        color: #302A22;
        padding: .95rem 1rem;
        margin: 0 0 1rem;
        font-weight: 700;
    }}
    .commerce-row {{
        display: grid;
        grid-template-columns: 180px 1fr;
        gap: .9rem;
        margin-bottom: .9rem;
    }}
    .quantity-box {{
        border: 2px solid #E06625;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        min-height: 58px;
        overflow: hidden;
        color: #E06625;
        font-size: 1.35rem;
        text-align: center;
        align-items: center;
    }}
    .quantity-box a, .quantity-box span {{
        min-height: 58px;
        display: grid;
        place-items: center;
        color: #E06625;
        text-decoration: none;
    }}
    .quantity-box a {{
        background: #F9B38E;
        color: #FFFDF7 !important;
    }}
    .quantity-box span {{
        background: #FFFDF7;
    }}
    .quantity-box span:first-child, .quantity-box span:last-child {{
        background: #F9B38E;
        color: #FFFDF7;
        height: 100%;
        display: grid;
        place-items: center;
    }}
    .cart-button {{
        display: grid;
        place-items: center;
        border: 2px solid #E06625;
        border-radius: 8px;
        color: #E06625 !important;
        text-decoration: none;
        font-size: 1.25rem;
        font-weight: 600;
    }}
    .primary-buy {{
        display: grid;
        place-items: center;
        min-height: 60px;
        border-radius: 8px;
        background: #214D36;
        color: #FAF5EA !important;
        text-decoration: none;
        font-size: 1.25rem;
        font-weight: 700;
    }}
    .stButton > button {{
        border-radius: 8px;
        min-height: 48px;
        border: 1px solid #E1D2B2;
        color: #214D36;
        background: #FFFDF7;
        font-weight: 700;
    }}
    .stButton > button:hover {{
        border-color: #214D36;
        color: #214D36;
        background: #F7EDD7;
    }}
    .product-card {{
        background: #FFFDF7;
        border: 1px solid #E9DDBD;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 12px 26px rgba(33,77,54,.08);
    }}
    .tea-card {{
        padding: 1.4rem;
        display: flex;
        flex-direction: column;
        min-height: 100%;
    }}
    .tea-card-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: .9rem;
    }}
    .tea-badge {{
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: #214D36;
        color: #FAF5EA;
        display: grid;
        place-items: center;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-weight: 700;
        font-size: 1.18rem;
        flex: 0 0 auto;
    }}
    .product-pack {{
        min-height: 230px;
        background:
            radial-gradient(circle at 50% 28%, rgba(255,255,255,.5), transparent 35%),
            linear-gradient(140deg, #E7D7AF, #B99246);
        display: grid;
        place-items: center;
    }}
    .product-pouch {{
        width: 136px;
        height: 174px;
        border-radius: 10px 10px 16px 16px;
        background: #214D36;
        color: #FAF5EA;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 16px 26px rgba(0,0,0,.16);
        border: 5px solid #F7EDD7;
    }}
    .product-pouch strong {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 2rem;
        line-height: 1;
    }}
    .product-pouch span {{
        margin-top: .8rem;
        font-size: .72rem;
        letter-spacing: .14em;
        color: #E7D7AF;
    }}
    .product-body {{ padding: 1.55rem; }}
    .product-body h3, .tea-card h3 {{
        margin: 0 0 .65rem;
        color: #173A28;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 1.8rem;
    }}
    .product-body p, .tea-card p {{ color: #665A49; line-height: 1.65; margin: 0 0 1rem; }}
    .price-list {{
        display: grid;
        gap: .62rem;
        margin-top: auto;
    }}
    .price-row {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
        background: #F7EDD7;
        border-radius: 999px;
        padding: .62rem .82rem;
        font-size: .92rem;
    }}
    .price-row span:first-child {{ color: #665A49; font-weight: 600; }}
    .price-row span:last-child {{ color: #214D36; font-weight: 800; }}
    .product-meta {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        border-top: 1px solid #E9DDBD;
        padding-top: 1rem;
        color: #4A4032;
        font-size: .9rem;
    }}
    .product-price {{ color: #214D36; font-weight: 700; }}
    .simple-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1.1rem;
        max-width: 980px;
        margin: 0 auto;
    }}
    .simple-card {{
        background: #FFFDF7;
        border: 1px solid #E9DDBD;
        border-radius: 18px;
        padding: 1.35rem;
        display: grid;
        grid-template-columns: 1fr auto;
        gap: .75rem 1rem;
        align-items: start;
    }}
    .simple-product-image-wrap {{
        grid-column: 1 / -1;
        min-height: 260px;
        display: grid;
        place-items: center;
        margin: -.25rem -.25rem .7rem;
    }}
    .simple-product-image {{
        width: min(320px, 92%);
        max-height: 260px;
        object-fit: contain;
        display: block;
    }}
    .simple-card h3 {{
        margin: 0;
        color: #173A28;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 1.65rem;
    }}
    .simple-card p {{
        grid-column: 1 / -1;
        color: #665A49;
        line-height: 1.65;
        margin: 0;
    }}
    .simple-price {{
        background: #214D36;
        color: #FAF5EA;
        border-radius: 999px;
        padding: .55rem .85rem;
        font-weight: 700;
        white-space: nowrap;
    }}
    .quality-list {{
        max-width: 980px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
    }}
    .quality-pill {{
        background: #FFFDF7;
        border: 1px solid #E9DDBD;
        border-radius: 999px;
        padding: .9rem 1rem;
        text-align: center;
        color: #214D36;
        font-weight: 600;
    }}
    .about-story {{
        max-width: 1180px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: .95fr 1.05fr;
        gap: clamp(2rem, 5vw, 4rem);
        align-items: center;
    }}
    .about-visual {{
        min-height: 510px;
        display: grid;
        place-items: center;
    }}
    .about-visual img {{
        width: min(560px, 100%);
        max-height: 500px;
        object-fit: contain;
        display: block;
    }}
    .about-copy h2 {{
        color: #173A28;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2.5rem, 4vw, 3.5rem);
        line-height: 1.08;
        margin: 0 0 1rem;
    }}
    .about-copy p {{
        color: #5D503F;
        line-height: 1.8;
        margin: 0 0 1rem;
        font-size: 1.03rem;
    }}
    .about-values {{
        max-width: 1180px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1.1rem;
    }}
    .about-value {{
        background: #FFFDF7;
        border: 1px solid #E9DDBD;
        padding: 1.45rem;
    }}
    .about-value h3 {{
        color: #173A28;
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 1.65rem;
        margin: 0 0 .65rem;
    }}
    .about-value p {{
        color: #665A49;
        line-height: 1.65;
        margin: 0;
    }}
    .about-promise {{
        max-width: 1180px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1.05fr .95fr;
        gap: clamp(2rem, 5vw, 4rem);
        align-items: center;
    }}
    .about-promise-list {{
        display: grid;
        gap: .9rem;
        margin-top: 1.3rem;
    }}
    .about-promise-list div {{
        background: #F7EDD7;
        border-left: 4px solid #B58B3B;
        padding: .95rem 1.1rem;
        color: #42392E;
        font-weight: 600;
    }}
    .order-panel {{
        max-width: 900px;
        margin: 0 auto;
        background: #214D36;
        color: #FAF5EA;
        border-radius: 22px;
        padding: clamp(2rem, 5vw, 3.2rem);
        text-align: center;
    }}
    .order-panel h2 {{
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: clamp(2.2rem, 3vw, 2.8rem);
        margin: 0 0 .65rem;
    }}
    .order-panel p {{ color: #EEE2C9; line-height: 1.7; margin: 0 0 1.6rem; }}
    .footer {{
        background: #173A28; color: #EBDFC5; padding: 2.1rem clamp(1.3rem, 7vw, 6.2rem);
        display: flex; justify-content: space-between; gap: 1rem; align-items: center;
    }}
    .footer strong {{ font-family: 'Cormorant Garamond'; font-size: 1.55rem; color: #FAF5EA; }}
    .footer p {{ margin: .32rem 0 0; font-size: .88rem; }}
    .footer-links {{ font-size: .88rem; opacity: .9; }}
    @media (max-width: 760px) {{
        .nav {{ height: auto; padding-top: 1rem; padding-bottom: 1rem; display: block; }}
        .brand-strip {{ padding: 1rem 1.3rem; }}
        .links {{ margin-top: 1rem; gap: 1rem; overflow-x: auto; padding-bottom: .35rem; }}
        .hero {{ min-height: 540px; }}
        .cards, .feature, .product-grid, .quality-list, .simple-grid, .shop-grid, .product-detail, .about-story, .about-values, .about-promise {{ grid-template-columns: 1fr; }}
        .product-visual {{ min-height: 310px; }}
        .about-visual {{ min-height: 320px; }}
        .commerce-row, .size-picker {{ grid-template-columns: 1fr; }}
        .simple-card {{ grid-template-columns: 1fr; }}
        .footer {{ display: block; }}
        .footer-links {{ margin-top: 1rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

announcement = safe(data["announcement"])


def render_header(active_page: str) -> None:
    logo_src = local_image_src(LOGO_IMAGE_PATH)
    logo_html = (
        f'<img class="logo" src="{logo_src}" alt="{safe(data["company_name"])} logo">'
        if logo_src
        else '<div class="logo-fallback">AT</div>'
    )
    brand_col, _, nav_col = st.columns([1.2, 0.8, 1.4], vertical_alignment="center")
    with brand_col:
        st.markdown(
            f"""
            <div class="brand-strip">
                <div class="brand">
                    {logo_html}
                    <div class="brand-name">{safe(data["company_name"])}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    active_label = next(
        item for item in data["navigation"] if PAGE_SLUGS[item] == active_page
    )
    with nav_col:
        chosen = st.pills(
            "Navigation",
            data["navigation"],
            default=active_label,
            label_visibility="collapsed",
            key=f"nav_pills_{active_page}",
            width="stretch",
        )
    chosen_page = PAGE_SLUGS[chosen]
    if chosen_page != st.session_state.current_page:
        if query_value("product"):
            st.query_params.clear()
        st.session_state.current_page = chosen_page
        st.rerun()


def render_announcement() -> None:
    st.markdown(
        f"""
        <div class="announcement">
            <div class="announcement-track">
                <span>{announcement}</span><span>{announcement}</span>
                <span>{announcement}</span><span>{announcement}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    footer_links = "&nbsp;&nbsp; | &nbsp;&nbsp;".join(
        safe(item) for item in data["navigation"] if item != "Home"
    )
    st.markdown(
        f"""
        <footer class="footer">
            <div>
                <strong>{safe(data["company_name"])}</strong>
                <p>{safe(data["footer_text"])}</p>
            </div>
            <div class="footer-links">{footer_links}</div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    render_header("home")
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">Black Loose Tea Packets</div>
                <h1 class="hero-title">{safe(hero["headline"])}</h1>
                <p class="hero-line">{safe(hero["supporting_line"])}</p>
                <a class="cta" href="#featured-tea">{safe(hero["button_label"])}</a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_announcement()

    reviews = "".join(
        f"""
        <article class="review">
            <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <p class="quote">"{safe(review['quote'])}"</p>
            <span class="person">{safe(review['author'])}</span>
            <span class="sample">(sample feedback)</span>
        </article>
        """
        for review in data["testimonials"]
    )
    st.markdown(
        f"""
        <section class="section cream">
            <div class="section-heading">
                <div class="kicker">Customer Feedback</div>
                <h2>Tea moments our customers enjoy</h2>
                <p>Temporary sample reviews for layout preview. We will replace these with genuine customer words before launch.</p>
            </div>
            <div class="cards">{reviews}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    icons = ["&#10022;", "&#9832;", "&#10003;"]
    benefits = "".join(
        f"""
        <article class="benefit">
            <div class="benefit-icon">{icons[index]}</div>
            <h3>{safe(benefit['title'])}</h3>
            <p>{safe(benefit['description'])}</p>
        </article>
        """
        for index, benefit in enumerate(data["benefits"])
    )
    featured = data["featured_product"]
    st.markdown(
        f"""
        <section class="section soft">
            <div class="section-heading">
                <div class="kicker">Why Choose Our Tea</div>
                <h2>A richer everyday cup</h2>
            </div>
            <div class="cards">{benefits}</div>
        </section>
        <section class="section cream" id="featured-tea">
            <div class="feature">
                <div class="packet">
                    <div class="packet-shape">
                        <strong>Assam<br>Tea</strong>
                        <span>BLACK LOOSE TEA</span>
                    </div>
                </div>
                <div class="feature-copy">
                    <div class="kicker">Featured Tea</div>
                    <h2>{safe(featured["name"])}</h2>
                    <p>{safe(featured["description"])}</p>
                    <p class="feature-note">{safe(featured["sizes_note"])}</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


def render_products() -> None:
    products_page = data["products_page"]
    tea_by_slug = {
        slugify(category["name"]): category
        for category in products_page["tea_categories"]
    }
    requested_product_slug = query_value("product")
    if "selected_product_slug" not in st.session_state:
        st.session_state.selected_product_slug = ""
    if (
        requested_product_slug in tea_by_slug
        and requested_product_slug != st.session_state.selected_product_slug
    ):
        st.session_state.selected_product_slug = requested_product_slug
        st.session_state.selected_size = products_page["size_labels"][0]
        st.session_state.selected_qty = 1
    if st.session_state.selected_product_slug not in tea_by_slug:
        st.session_state.selected_product_slug = ""
    if "selected_size" not in st.session_state:
        st.session_state.selected_size = products_page["size_labels"][0]
    if st.session_state.selected_size not in products_page["size_labels"]:
        st.session_state.selected_size = products_page["size_labels"][0]
    if "selected_qty" not in st.session_state:
        st.session_state.selected_qty = 1
    st.session_state.selected_qty = max(1, min(int(st.session_state.selected_qty), 99))

    render_header("products")
    st.markdown(
        f"""
        <section class="page-hero">
            <div class="page-hero-inner">
                <div class="kicker">Products</div>
                <h1>{safe(products_page["headline"])}</h1>
                <p>{safe(products_page["intro"])}</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_announcement()

    if st.session_state.selected_product_slug:
        category = tea_by_slug[st.session_state.selected_product_slug]
        detail_name = safe(category["name"])
        detail_pack = product_pack_html(
            category["name"],
            "detail-product-image",
            "mock-pack",
            st.session_state.selected_size,
        )
        st.markdown(
            f"""
            <section class="section cream" style="padding-bottom:1.5rem;">
            """,
            unsafe_allow_html=True,
        )
        if st.button("← Back to all products", key="back_to_products"):
            st.session_state.selected_product_slug = ""
            st.query_params.clear()
            st.rerun()

        image_col, info_col = st.columns([1.15, 1], gap="large")
        with image_col:
            st.markdown(
                f"""
                <div class="product-visual">
                    {detail_pack}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info_col:
            selected_price = category["prices"][st.session_state.selected_size]
            st.markdown(
                f"""
                <div class="product-info">
                    <div class="brand-line">Assam Tea Company</div>
                    <h2>{detail_name} Black Loose Tea</h2>
                    <div class="from-price">{safe(selected_price)}</div>
                    <p class="product-desc">{safe(category["description"])}</p>
                    <div class="review-line">
                        <span class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
                        <span>Sample customer reviews</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            size = st.radio(
                "Choose packet size",
                products_page["size_labels"],
                horizontal=True,
                key="selected_size",
            )
            st.number_input(
                "Quantity",
                min_value=1,
                max_value=99,
                step=1,
                key="selected_qty",
            )
            st.markdown(
                f"""
                <div class="selected-summary">
                    Selected: {detail_name} · {safe(size)} · {safe(category["prices"][size])} each · Qty {st.session_state.selected_qty}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Add to bag", key="add_to_bag", use_container_width=True):
                add_item_to_bag({
                    "product": category["name"],
                    "size": size,
                    "price": category["prices"][size],
                    "quantity": st.session_state.selected_qty,
                })
                st.session_state.current_page = "checkout"
                st.rerun()

        st.markdown("</section>", unsafe_allow_html=True)
        render_footer()
        return

    def add_direct_product_to_bag(product: dict, quantity: int = 1) -> None:
        add_item_to_bag({
            "product": product["name"],
            "size": product.get("size", "Standard packet"),
            "price": product["price"],
            "quantity": quantity,
        })
        st.session_state.current_page = "checkout"
        st.rerun()

    st.markdown(
        f"""
        <section class="section cream">
            <div class="section-heading">
                <div class="kicker">Black Loose Tea</div>
                <h2>{safe(products_page["loose_tea_heading"])}</h2>
                <p>{safe(products_page["loose_tea_intro"])}</p>
            </div>
            <div class="product-select-note">Click a product to choose packet size and quantity.</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    rows = [
        products_page["tea_categories"][index:index + 2]
        for index in range(0, len(products_page["tea_categories"]), 2)
    ]
    for row_index, row in enumerate(rows):
        columns = st.columns(2)
        for column, category in zip(columns, row):
            category_slug = slugify(category["name"])
            shop_pack = product_pack_html(
                category["name"],
                "shop-product-image",
                "shop-pack",
                products_page["size_labels"][0],
            )
            with column:
                st.markdown(
                    f"""
                    <a class="shop-card" href="?product={category_slug}" target="_self" aria-label="View {safe(category["name"])} Black Loose Tea">
                        <div class="shop-image">
                            <div class="stock-tag">In stock</div>
                            {shop_pack}
                        </div>
                        <div class="shop-info">
                            <div class="shop-weight">250 g to 1 kg</div>
                            <h3>{safe(category["name"])} Black Loose Tea</h3>
                            <div class="shop-rating"><span>&#9733;&#9733;&#9733;&#9733;&#9733;</span> Sample reviews</div>
                            <div class="shop-price">From {safe(category["prices"][products_page["size_labels"][0]])}</div>
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        f"""
        <section class="section soft">
            <div class="section-heading">
                <div class="kicker">Special Products</div>
                <h2>Tea add-ons and flavored tea</h2>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    special_columns = st.columns(2)
    special_product_images = {
        "Masala Tea Mix": MASALA_TEA_IMAGE_PATH,
        "Lamsa Tea": LAMSA_TEA_IMAGE_PATH,
    }
    for column, product in zip(special_columns, products_page["special_products"]):
        product_image_src = local_image_src(
            special_product_images.get(product["name"], "")
        )
        product_image_html = (
            f'<div class="simple-product-image-wrap">'
            f'<img class="simple-product-image" src="{product_image_src}" alt="{safe(product["name"])}">'
            "</div>"
            if product_image_src
            else ""
        )
        with column:
            st.markdown(
                f"""
                <article class="simple-card">
                    {product_image_html}
                    <h3>{safe(product["name"])}</h3>
                    <span class="simple-price">{safe(product["price"])}</span>
                    <p>{safe(product["description"])}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Add {product['name']} to bag", key=f"special_{slugify(product['name'])}", use_container_width=True):
                add_direct_product_to_bag(product)

    st.markdown(
        """
        <section class="section cream">
            <div class="section-heading">
                <div class="kicker">Sugar</div>
                <h2>Sugar products</h2>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    sugar_columns = st.columns(max(1, len(products_page["sugar_products"])))
    for column, product in zip(sugar_columns, products_page["sugar_products"]):
        with column:
            st.markdown(
                f"""
                <article class="simple-card">
                    <h3>{safe(product["name"])}</h3>
                    <span class="simple-price">{safe(product["price"])}</span>
                    <p>{safe(product["description"])}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Add {product['name']} to bag", key=f"sugar_{slugify(product['name'])}", use_container_width=True):
                add_direct_product_to_bag(product)

    st.markdown(
        """
        <section class="section soft">
            <div class="section-heading">
                <div class="kicker">Wholesale / Bulk Orders</div>
                <h2>Whole bags for larger needs</h2>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    bulk_columns = st.columns(2)
    for column, product in zip(bulk_columns, products_page["bulk_products"]):
        with column:
            st.markdown(
                f"""
                <article class="simple-card">
                    <h3>{safe(product["name"])}</h3>
                    <span class="simple-price">{safe(product["price"])}</span>
                    <p>{safe(product["description"])}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Add {product['name']} to bag", key=f"bulk_{slugify(product['name'])}", use_container_width=True):
                add_direct_product_to_bag(product)

    st.markdown(
        f"""
        <section class="section cream">
                <div class="order-panel">
                    <h2>Want to place an order?</h2>
                    <p>{safe(products_page["order_note"])}</p>
                    <p>Choose a product above and click Add to bag to continue to checkout.</p>
                </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


def render_about() -> None:
    render_header("about")
    about_image = local_image_src(LOOSE_TEA_IMAGE_PATHS[PRODUCT_1KG_SIZE_LABEL])
    logo_src = local_image_src(LOGO_IMAGE_PATH)
    st.markdown(
        f"""
        <section class="page-hero">
            <div class="page-hero-inner">
                <div class="kicker">About Us</div>
                <h1>Fresh Assam tea for everyday cups.</h1>
                <p>Assam Tea Company brings strong, aromatic black loose tea and everyday tea products to families, shops, offices, and regular tea lovers.</p>
            </div>
        </section>
        <section class="section cream">
            <div class="about-story">
                <div class="about-visual">
                    <img src="{about_image}" alt="Assam Tea Company loose tea packet">
                </div>
                <div class="about-copy">
                    <div class="kicker">Our Story</div>
                    <h2>Built around the daily tea break.</h2>
                    <p>We believe a good cup of tea should be strong, fresh, and dependable. Our products are selected and packed for customers who want rich color, full flavor, and a satisfying brew at home or work.</p>
                    <p>From regular loose tea packets to premium choices, flavored tea, tea masala, and bulk options, our catalog is designed for practical everyday needs.</p>
                </div>
            </div>
        </section>
        <section class="section soft">
            <div class="section-heading">
                <div class="kicker">What We Care About</div>
                <h2>Simple promises, carefully kept.</h2>
                <p>Our focus is clear: freshness, strong taste, and reliable service for every customer.</p>
            </div>
            <div class="about-values">
                <article class="about-value">
                    <h3>Fresh Packing</h3>
                    <p>Tea is packed with care so the aroma and flavor stay ready for each cup.</p>
                </article>
                <article class="about-value">
                    <h3>Strong Flavor</h3>
                    <p>Our black loose tea options are made for customers who enjoy a bold, satisfying brew.</p>
                </article>
                <article class="about-value">
                    <h3>Everyday Value</h3>
                    <p>Multiple packet sizes and price ranges make it easy to choose what fits your home or business.</p>
                </article>
            </div>
        </section>
        <section class="section cream">
            <div class="about-promise">
                <div class="about-copy">
                    <div class="kicker">Our Products</div>
                    <h2>Tea choices for every need.</h2>
                    <p>Customers can choose from Regular, Regular Plus, Premium, Premium Plus, and Super Premium black loose tea, with packet sizes from 250 g to 1 kg.</p>
                    <div class="about-promise-list">
                        <div>Loose tea packets for families and daily tea drinkers</div>
                        <div>Tea masala and flavored tea for variety</div>
                        <div>Bulk tea and sugar options for larger orders</div>
                    </div>
                </div>
                <div class="about-visual">
                    <img src="{logo_src}" alt="{safe(data["company_name"])} logo">
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


def render_checkout() -> None:
    render_header("checkout")
    bag_items = st.session_state.get("bag_items", [])
    st.markdown(
        """
        <section class="page-hero">
            <div class="page-hero-inner">
                <div class="kicker">Checkout</div>
                <h1>Review your bag</h1>
                <p>Confirm your selected item and share customer details to prepare the order.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if not bag_items:
        st.markdown(
            """
            <section class="section cream">
                <div class="order-panel">
                    <h2>Your bag is empty</h2>
                    <p>Go to Products and add a tea packet to start checkout.</p>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Go to Products", key="checkout_to_products"):
            st.session_state.current_page = "products"
            st.rerun()
        render_footer()
        return

    st.markdown('<section class="section cream">', unsafe_allow_html=True)
    item_col, form_col = st.columns([1, 1], gap="large")
    with item_col:
        st.markdown("### Bag items")
        for index, item in enumerate(bag_items, start=1):
            st.markdown(
                f"""
                <div class="selected-summary">
                    <strong>{index}. {safe(item["product"])}</strong><br>
                    Size: {safe(item["size"])}<br>
                    Price: {safe(item["price"])} each<br>
                    Quantity: {item["quantity"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("Add more products", key="edit_bag_item"):
            st.session_state.current_page = "products"
            st.rerun()
        if st.button("Clear bag", key="clear_bag"):
            st.session_state.bag_items = []
            st.rerun()
    with form_col:
        st.text_input("Customer name", key="checkout_name")
        st.text_input("Phone number", key="checkout_phone")
        st.text_area("Order notes", key="checkout_notes")
        st.button("Submit order request", key="submit_order_request", use_container_width=True)
    st.markdown("</section>", unsafe_allow_html=True)
    render_footer()


if current_page == "products":
    render_products()
elif current_page == "checkout":
    render_checkout()
elif current_page == "about":
    render_about()
else:
    render_home()
