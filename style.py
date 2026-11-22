import base64
from pathlib import Path

NAVY = "#0f2a5c"
BLUE = "#2f6fe4"
HERE = Path(__file__).parent


def to_uri(svg_str):
    return "data:image/svg+xml;base64," + base64.b64encode(svg_str.encode()).decode()


ICONS = {
    "logo_white": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 110">'
        '<polygon points="45,82 92,20 128,64 156,34 205,82" fill="none" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"/>'
        '<polygon points="92,20 75,44 92,37 106,46" fill="#7cc4fa"/>'
        '<path d="M35,94 Q85,84 130,94 T225,94" fill="none" stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>'
        '</svg>'
    ),
    "icon_info": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<circle cx="24" cy="24" r="20" fill="#2f6fe4"/>'
        '<circle cx="24" cy="15" r="2.6" fill="#ffffff"/>'
        '<rect x="21.5" y="21" width="5" height="14" rx="2.5" fill="#ffffff"/>'
        '</svg>'
    ),
    "icon_chart": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<rect x="6" y="26" width="8" height="16" rx="2" fill="#63b3ed"/>'
        '<rect x="20" y="18" width="8" height="24" rx="2" fill="#2f6fe4"/>'
        '<rect x="34" y="10" width="8" height="32" rx="2" fill="#0f2a5c"/>'
        '<path d="M8 20 L22 12 L38 6" fill="none" stroke="#e03131" stroke-width="3" stroke-linecap="round"/>'
        '</svg>'
    ),
    "icon_satellite": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<rect x="19" y="19" width="10" height="10" rx="2" transform="rotate(-45 24 24)" fill="#0f2a5c"/>'
        '<rect x="5" y="19" width="12" height="8" rx="1.5" transform="rotate(-45 11 23)" fill="#2f6fe4"/>'
        '<rect x="31" y="21" width="12" height="8" rx="1.5" transform="rotate(-45 37 25)" fill="#2f6fe4"/>'
        '<path d="M14 34 A10 10 0 0 0 24 44" fill="none" stroke="#63b3ed" stroke-width="3" stroke-linecap="round"/>'
        '</svg>'
    ),
    "icon_gauge": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<path d="M8 34 A16 16 0 1 1 40 34" fill="none" stroke="#c9dafa" stroke-width="6" stroke-linecap="round"/>'
        '<path d="M8 34 A16 16 0 0 1 34 14" fill="none" stroke="#2f6fe4" stroke-width="6" stroke-linecap="round"/>'
        '<line x1="24" y1="34" x2="32" y2="20" stroke="#e03131" stroke-width="3.5" stroke-linecap="round"/>'
        '<circle cx="24" cy="34" r="4" fill="#0f2a5c"/>'
        '</svg>'
    ),
    "icon_sliders": to_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<line x1="8" y1="14" x2="40" y2="14" stroke="#9dbfe6" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="18" cy="14" r="5" fill="#2f6fe4"/>'
        '<line x1="8" y1="24" x2="40" y2="24" stroke="#9dbfe6" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="30" cy="24" r="5" fill="#0f2a5c"/>'
        '<line x1="8" y1="34" x2="40" y2="34" stroke="#9dbfe6" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="22" cy="34" r="5" fill="#2f6fe4"/>'
        '</svg>'
    ),
}

S = 'fill="#d6e4ff" stroke="#2f6fe4" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"'
L = 'fill="none" stroke="#2f6fe4" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'

SVG = {
    "lake": '<path d="M5 22c4-4 8-4 12 0s8 4 12 0 8-4 12 0" %s/><path d="M5 31c4-4 8-4 12 0s8 4 12 0 8-4 12 0" %s/><path d="M5 40c4-4 8-4 12 0s8 4 12 0 8-4 12 0" %s/><path d="M24 4v12M18 10l6-6 6 6" %s/>' % (L, L, L, L),
    "glacier": '<path d="M3 41 18 12l10 18 6-8 11 19Z" %s/><path d="M18 12l-6 11 6-3 4 4Z" fill="#fff" stroke="#2f6fe4" stroke-width="1.8" stroke-linejoin="round"/>' % S,
    "slope": '<path d="M4 41 24 7l20 34Z" %s/><path d="M24 7l-7 12 7-3 7 3Z" fill="#fff" stroke="#2f6fe4" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 41l8-14" %s stroke-dasharray="1 5"/>' % (S, L),
    "rain": '<path d="M13 30a8 8 0 0 1 1-16 11 11 0 0 1 21 3 7 7 0 0 1-1 13Z" %s/><path d="M15 36l-2 6M24 36l-2 6M33 36l-2 6" %s/>' % (S, L),
    "shield": '<path d="M24 4 41 10v14c0 10-7 16-17 20C14 40 7 34 7 24V10Z" %s/><path d="M15 24l6 6 12-13" %s/>' % (S, L),
    "houses": '<path d="M3 42V25l9-8 9 8v17Z" %s/><path d="M25 42V23l10-9 11 9v19Z" %s/><path d="M9 42V33h6v9M33 42V32h6v10" %s/>' % (S, S, L),
    "flask": '<path d="M18 5h12M20 5v14L8 40a3 3 0 0 0 3 4h26a3 3 0 0 0 3-4L28 19V5" fill="#d6e4ff" stroke="#0f2a5c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/><path d="M13 33h22" stroke="#0f2a5c" stroke-width="3" stroke-linecap="round"/>',
    "bulb": '<path d="M24 5a13 13 0 0 0-7 24v5h14v-5A13 13 0 0 0 24 5Z" fill="#fff" stroke="#0f2a5c" stroke-width="3" stroke-linejoin="round"/><path d="M18 40h12M20 44h8" stroke="#0f2a5c" stroke-width="3" stroke-linecap="round"/>',
    "thermo": '<path d="M20 8a4 4 0 0 1 8 0v20a9 9 0 1 1-8 0Z" fill="#fff" stroke="#0f2a5c" stroke-width="3" stroke-linejoin="round"/><circle cx="24" cy="35" r="5" fill="#e03131"/><path d="M24 14v21" stroke="#e03131" stroke-width="3.5" stroke-linecap="round"/>',
    "mountain": '<path d="M2 42 17 14l9 14 6-9 14 23Z" fill="#12306b"/><path d="M17 14l-5 9 5-3 4 4Z" fill="#fff"/><path d="M32 19l-4 7 4-2 3 3Z" fill="#fff"/>',
    "globe": '<circle cx="24" cy="24" r="19" fill="#2f6fe4" stroke="#0f2a5c" stroke-width="3"/><ellipse cx="24" cy="24" rx="8" ry="19" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M5 24h38M8 14h32M8 34h32M24 5v38" stroke="#fff" stroke-width="2.2" fill="none"/>',
}


def icon_img(name, h=40, extra=""):
    src = ICONS.get(name, "")
    return f'<img src="{src}" style="height:{h}px;{extra}">' if src else ""


def svg(name, size=24):
    return f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" style="flex:none">{SVG[name]}</svg>'


def landscape_svg(dark=True):
    if dark:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice">'
            '<defs>'
            '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d2a62"/><stop offset=".55" stop-color="#3b6db2"/><stop offset="1" stop-color="#a6cdf0"/></linearGradient>'
            '<linearGradient id="lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#45b8da"/><stop offset="1" stop-color="#0b4673"/></linearGradient>'
            '<linearGradient id="rock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6b8fc2"/><stop offset="1" stop-color="#1f3b6c"/></linearGradient>'
            '</defs>'
            '<rect width="1200" height="600" fill="url(#sky)"/>'
            '<polygon points="250,470 380,330 470,390 600,250 720,370 820,320 960,400 1200,340 1200,480 250,480" fill="#7ea3d4" opacity=".75"/>'
            '<polygon points="540,490 690,310 785,205 850,55 908,170 955,235 1015,212 1200,410 1200,490" fill="url(#rock)"/>'
            '<polygon points="850,55 908,170 955,235 905,305 862,215 842,130" fill="#1b3768" opacity=".55"/>'
            '<polygon points="850,55 792,195 826,168 852,222 884,160 908,170" fill="#f5f9ff"/>'
            '<polygon points="690,310 765,250 790,205 772,295" fill="#e3edff" opacity=".9"/>'
            '<polygon points="955,235 1015,212 1060,270 1000,300" fill="#e8f0ff" opacity=".85"/>'
            '<polygon points="740,320 905,308 1010,440 660,450" fill="#dcebfb" opacity=".92"/>'
            '<polygon points="780,330 850,322 880,400 760,410" fill="#c1d9f4" opacity=".7"/>'
            '<rect y="470" width="1200" height="130" fill="url(#lake)"/>'
            '<g stroke="#ffffff" stroke-opacity=".28" stroke-width="2">'
            '<line x1="520" y1="500" x2="760" y2="500"/><line x1="600" y1="525" x2="900" y2="525"/>'
            '<line x1="680" y1="552" x2="1000" y2="552"/><line x1="560" y1="578" x2="820" y2="578"/></g>'
            '<polygon points="880,600 1040,505 1200,525 1200,600" fill="#0a1c40"/>'
            '<polygon points="0,600 0,520 140,540 260,600" fill="#0a1c40"/>'
            "</svg>"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" preserveAspectRatio="xMaxYMax slice">'
        '<polygon points="0,420 0,300 180,190 300,270 470,110 640,260 760,170 930,290 1100,200 1200,260 1200,420" fill="#9dbfe6"/>'
        '<polygon points="470,110 415,185 460,165 495,210 525,168" fill="#ffffff"/>'
        '<polygon points="760,170 725,225 760,210 790,240" fill="#ffffff" opacity=".9"/>'
        '<polygon points="0,420 0,350 220,270 380,350 560,235 760,350 960,270 1200,360 1200,420" fill="#e7f0fc" opacity=".95"/>'
        "</svg>"
    )


def photo_or_svg(photo_names, dark=True):
    for n in photo_names:
        p = HERE / n
        if not p.exists():
            p = HERE / "assets" / n
        if p.exists():
            mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
            return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode(), True
    return to_uri(landscape_svg(dark)), False


def get_css(page):
    bottom_mountains = ""
    if page == "What-If Simulator":
        bottom_mountains = (
            ".stApp::after{content:'';position:fixed;right:0;bottom:0;width:75%;height:260px;"
            f"background:url({to_uri(landscape_svg(False))}) right bottom / cover no-repeat;opacity:.75;pointer-events:none;z-index:0;}}"
        )

    raw_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label, .stApp button,
.stApp input, div[data-testid="stMarkdownContainer"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display:none !important; visibility:hidden; }
header[data-testid="stHeader"] { background: transparent; height: 0; }

.stApp { background: linear-gradient(135deg,#c2d7f8 0%,#dbe8fc 50%,#c6d9f7 100%); color:__NAVY__; color-scheme: light; }
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp p,.stApp label { color:__NAVY__; }
.block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 1340px; position: relative; z-index: 1; }
__BOTTOM__

section[data-testid="stSidebar"] { background: linear-gradient(180deg,#10285a 0%,#0a1b40 100%);}
section[data-testid="stSidebar"] > div { padding-top: 0.5rem; }
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] { display:none; }
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .4rem; }
section[data-testid="stSidebar"] * { color:#ffffff !important; }
section[data-testid="stSidebar"] button {
    width: 100%; background: transparent !important; border: none !important; box-shadow: none !important;
    justify-content: flex-start !important; text-align: left !important;
    border-radius: 12px !important; padding: .62rem 1rem !important; min-height: 46px;
}
section[data-testid="stSidebar"] button > div { justify-content: flex-start !important; gap: 12px; }
section[data-testid="stSidebar"] button p { font-size: 15px; font-weight: 500; margin: 0; }
section[data-testid="stSidebar"] button:hover { background: rgba(255,255,255,.09) !important; }
section[data-testid="stSidebar"] button[kind="primary"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] { background: #2d5cc8 !important; }
section[data-testid="stSidebar"] button[kind="primary"] p,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p { font-weight: 700; }
.sb-logo { display:flex; justify-content:center; padding: 18px 0 30px 0; }

.gwcard, div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .cardmark),
div[data-testid="stVerticalBlock"]:has(> div.element-container .cardmark) {
    background: rgba(255,255,255,.58); border: 1px solid rgba(255,255,255,.9); border-radius: 22px;
    box-shadow: 0 10px 28px rgba(30,64,130,.12); padding: 22px 26px; box-sizing: border-box;
}
div[data-testid="stElementContainer"]:has(.cardmark), div.element-container:has(.cardmark) { display:none; }
.card-title { font-size: 19px; font-weight: 700; color: __NAVY__; margin-bottom: 8px; }
.page-title { display:flex; align-items:center; gap:14px; font-size: clamp(22px, 3vw, 32px); font-weight: 800; color: __NAVY__; margin: 0 0 8px 0; line-height:1.1; flex-wrap: wrap; }
.subtitle { font-size: 16px; color: __NAVY__; margin: 0 0 18px 0; }

div[data-testid="stSelectbox"] div[role="group"], div[data-baseweb="select"] > div,
div[data-testid="stPopover"] > div > button {
    background: rgba(255,255,255,.92) !important; border: 1px solid #c9dafa !important;
    border-radius: 999px !important; min-height: 44px; color: __NAVY__ !important; font-weight: 600 !important;
}
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] > div > div {
    background: rgba(255,255,255,.92) !important; border: 1px solid #c9dafa !important;
    border-radius: 12px !important; color: __NAVY__ !important; font-weight: 700 !important;
}
div[data-testid="stNumberInput"] input {
    color: __BLUE__ !important; -webkit-text-fill-color: __BLUE__ !important;
    font-weight: 800 !important; font-size: 16px !important;
}
div[data-testid="stNumberInput"] button {
    background: rgba(230,239,255,.8) !important; color: __NAVY__ !important; border: none !important;
}
div[data-testid="stPopover"] > div > button * { color: __NAVY__ !important; font-weight: 600 !important; }
div[data-testid="stSelectbox"] input, div[data-testid="stSelectbox"] [role="combobox"] { color: __NAVY__ !important; -webkit-text-fill-color: __NAVY__ !important; font-weight: 600; }
div[data-testid="stSelectbox"] button svg, div[data-testid="stSelectbox"] svg { fill: __NAVY__ !important; color: __NAVY__ !important; }
div[data-testid="stSelectboxVirtualDropdown"], div[data-baseweb="popover"] ul { background:#ffffff !important; border-radius: 14px; }
div[data-testid="stSelectboxVirtualDropdown"] *, div[data-baseweb="popover"] li { color: __NAVY__ !important; }
div[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover, div[data-testid="stSelectboxVirtualDropdown"] [aria-selected="true"] { background:#e6efff !important; }

div[data-testid="stExpander"] details {
    background: rgba(255,255,255,.62) !important;
    border: 1px solid rgba(255,255,255,.92) !important;
    border-radius: 18px !important;
    overflow: hidden;
}
div[data-testid="stExpander"] summary {
    background: rgba(255,255,255,.82) !important;
    color: __NAVY__ !important;
    padding: 12px 18px !important;
    border-radius: 18px !important;
}
div[data-testid="stExpander"] summary *, div[data-testid="stExpander"] summary svg {
    color: __NAVY__ !important;
    fill: __NAVY__ !important;
    font-weight: 700 !important;
}

.hero { border-radius: 26px; min-height: 500px; height: calc(100vh - 90px); padding: clamp(32px, 6vw, 80px) clamp(24px, 5vw, 64px); position: relative; overflow: hidden; box-shadow: 0 14px 34px rgba(15,42,92,.25); display:flex; flex-direction:column; justify-content:center; align-items:flex-start; }
.hero h1 { color:#fff !important; font-size: clamp(36px, 6vw, 64px); font-weight: 800; margin: 0 0 8px 0; letter-spacing:-1px; }
.hero .tag { color:#fff !important; font-style: italic; font-size: clamp(18px, 2.5vw, 26px); margin: 0 0 26px 0; }
.hero .desc { color:#e6efff !important; font-size: clamp(15px, 1.8vw, 17px); max-width: 450px; line-height: 1.6; margin-bottom: 30px; }
.hero a.cta { display:inline-block; background:#3b82f6; color:#fff !important; text-decoration:none; font-weight:600; padding: 13px 26px; border-radius: 999px; font-size: 15px; box-shadow: 0 6px 16px rgba(30,80,200,.4); }

.donut { width: 190px; height: 190px; max-width: 100%; border-radius: 50%; margin: 6px auto 10px auto; display:flex; align-items:center; justify-content:center; }
.donut-in { width: 136px; height: 136px; border-radius: 50%; background: __NAVY__; display:flex; align-items:baseline; justify-content:center; padding-top: 42px; box-sizing: border-box; }
.donut-in b { color:#fff !important; font-size: 48px; font-weight: 800; line-height: 1; }
.donut-in small { color:#fff !important; font-size: 22px; font-weight: 600; }
.risk-label { text-align:center; font-weight: 700; font-size: 18px; display:flex; justify-content:center; align-items:center; gap: 8px; }
.fbar { display:flex; align-items:center; gap: 8px; margin: 12px 0; font-size: 13.5px; font-weight: 600; flex-wrap: nowrap; }
.fbar .nm { width: 178px; white-space: nowrap; display:flex; align-items:center; gap: 7px; flex-shrink: 0; }
.fbar .track { flex:1; min-width: 65px; height: 8px; border-radius: 99px; background:#c9dafa; overflow:hidden; }
.fbar .fill { height:100%; border-radius: 99px; background: __BLUE__; }
.fbar .pc { width: 42px; text-align:right; font-weight: 700; flex-shrink: 0; }
.banner { display:flex; align-items:center; gap: 14px; background: rgba(196,219,252,.85); border-radius: 18px; padding: 16px 22px; font-size: 15px; margin-top: 14px; flex-wrap: wrap; }
iframe { border-radius: 22px; width: 100% !important; }

.sim-head { display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px; flex-wrap: wrap; gap: 8px; }
.sim-head .l { display:flex; align-items:center; gap: 10px; font-size: clamp(16px, 2vw, 19px); font-weight: 700; }
.sim-head .val { font-size: clamp(22px, 2.5vw, 30px); font-weight: 800; color: __BLUE__; }
div[data-testid="stSlider"] [role="group"], div[data-testid="stSlider"] div[data-baseweb="slider"] { filter: hue-rotate(224deg) saturate(1.25); }
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"], div[data-testid="stSlider"] [data-testid="stSliderTickBar"], div[data-testid="stSlider"] [data-testid="stTickBar"] { display:none !important; }
.ticks { position: relative; height: 20px; font-size: 13px; color: __NAVY__; margin-top: -2px; }
.ticks span { position:absolute; top:0; color: __NAVY__; }
div[data-testid="stMainBlockContainer"] button[data-testid="stBaseButton-primary"], main button[kind="primary"] {
    background: __BLUE__ !important; border: none !important; color:#fff !important; border-radius: 12px !important;
    padding: .65rem 2.8rem !important; font-weight: 700; max-width: 340px !important; margin: 0 auto !important;
    box-shadow: 0 8px 18px rgba(47,111,228,.35) !important; }
div[data-testid="stMainBlockContainer"] button[data-testid="stBaseButton-primary"] * { color:#fff !important; }
div[data-testid="stMainBlockContainer"] div[data-testid="stElementContainer"]:has(button[data-testid="stBaseButton-primary"]) { display:flex; justify-content:center; width:100% !important; }
.big-score { font-size: clamp(54px, 6vw, 78px); font-weight: 800; line-height: 1; margin: 10px 0 14px 0; }
.pill { display:inline-flex; align-items:center; gap: 8px; padding: 8px 18px; border-radius: 999px; font-weight: 700; font-size: 15px; }
.pts { font-size: 14px; margin-top: 14px; line-height: 1.7; }
.insight-row { display:flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
.insight-row .txt { flex: 1; min-width: 240px; font-size: 15px; line-height: 1.6; }
.insight-row .pic { width: 250px; flex-grow: 1; max-width: 100%; min-height: 120px; border-radius: 16px; background-size: cover; background-position: center; }

.about-top { position:relative; border-radius: 22px; padding: 10px 0 24px 0; }
.about-top p { max-width: 65%; font-size: 16px; line-height: 1.7; }
.steps { display:flex; align-items:center; justify-content: space-between; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
.step { text-align:center; font-size: 14px; font-weight: 600; flex: 1; min-width: 120px; line-height: 1.5; }
.step .ico { height: 68px; display:flex; align-items:center; justify-content:center; margin-bottom: 8px; }
.step small { font-weight: 400; font-size: 13px; }
.arrow { font-size: 28px; color: #8ea9dc; margin-bottom: 36px; }
.fgrid { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; }
.fcell { background: rgba(255,255,255,.78); border-radius: 18px; padding: 22px 8px; text-align:center; font-weight: 600; font-size: 15px; line-height: 1.5; display:flex; flex-direction:column; align-items:center; gap: 10px; }
.safer { border-radius: 22px; padding: 40px 24px; text-align:center; color:#fff; min-height: 360px;
         background: linear-gradient(180deg,#143574 0%,#1f4f9e 55%,#86aee0 100%); box-shadow: 0 10px 28px rgba(30,64,130,.22); }
.safer h3 { color:#fff !important; font-size: clamp(20px, 2.5vw, 26px); font-weight: 800; margin: 18px 0 18px 0; line-height: 1.25; }
.safer p { color:#e3edff !important; font-size: 16px; margin: 6px 0; }

@media (max-width: 992px) {
    .block-container { padding: 1rem 1rem 2.5rem 1rem; }
    .about-top p { max-width: 100%; }
    .hero { height: auto; min-height: 420px; }
    .arrow { display: none; }
}
@media (max-width: 600px) {
    .gwcard { padding: 16px 14px; border-radius: 16px; }
    .fbar { flex-wrap: wrap; }
    .fbar .nm { width: 100%; font-size: 13px; }
    .donut { width: 165px; height: 165px; }
    .donut-in { width: 118px; height: 118px; padding-top: 34px; }
    .donut-in b { font-size: 40px; }
}
</style>
"""
    return raw_css.replace("__NAVY__", NAVY).replace("__BLUE__", BLUE).replace("__BOTTOM__", bottom_mountains)