import os
import re
from datetime import datetime
from urllib.parse import quote

import altair as alt
import pandas as pd
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SB Soccer Offline Quality Team",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (Dark Theme) ───────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
/* ---- Global ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
/* ---- Hide default Streamlit chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
/* ---- App background (DARK) ---- */
.stApp {
    background-color: #0e1117;
    color: #fafafa;
}
/* ---- Sidebar (matches the dark main background) ---- */
[data-testid="stSidebar"] {
    background-color: #0e1117;
    border-right: 1px solid #2a2f3a;
    /* Keep the sidebar permanently fixed, visible, and at a constant width */
    min-width: 18rem !important;
    max-width: 18rem !important;
    width: 18rem !important;
    transform: none !important;
    visibility: visible !important;
}
[data-testid="stSidebar"] * {
    color: #CBD5E0 !important;
}
/* ---- Lock the sidebar open: hide every collapse / hide control ---- */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarHeader"] button,
button[kind="headerNoPadding"] {
    display: none !important;
}
/* Sidebar title */
.sidebar-brand {
    padding: 1rem 1.2rem 0.5rem;
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    line-height: 1.4;
    color: #FFFFFF !important;
    letter-spacing: -0.01em;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
}
.sidebar-brand span {
    display: block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #68A4C4 !important;
    margin-bottom: 0.3rem;
}
/* Section label in sidebar */
.sidebar-section-label {
    padding: 0 0.4rem;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7C8AA0 !important;
    margin: 0.6rem 0 0.4rem;
}
/* ---- Sidebar navigation buttons (look like nav links) ---- */
[data-testid="stSidebar"] .stButton button {
    background-color: transparent;
    border: none;
    color: #CBD5E0 !important;
    text-align: left;
    justify-content: flex-start;
    font-size: 0.9rem;
    font-weight: 400;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    width: 100%;
    transition: background 0.15s ease;
}
[data-testid="stSidebar"] .stButton button:hover {
    background-color: rgba(255,255,255,0.06);
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stButton button:focus {
    box-shadow: none !important;
    color: #FFFFFF !important;
}
/* ---- Sidebar expander (dropdown menus) ---- */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: none;
    background: transparent;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    font-size: 0.9rem;
    font-weight: 500;
    color: #CBD5E0 !important;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background-color: rgba(255,255,255,0.06);
}
/* ---- Main content area ---- */
.block-container {
    padding: 2.5rem 3rem 3rem !important;
    max-width: 980px;
}

/* ---- Light font colors for native Streamlit text ---- */
[data-testid="stHeading"],
[data-testid="stHeading"] *,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] blockquote,
[data-testid="stMarkdownContainer"] strong {
    color: #fafafa !important;
}
/* Blockquote (the "Note") accent */
[data-testid="stMarkdownContainer"] blockquote {
    border-left: 3px solid #68A4C4;
    padding-left: 1rem;
    color: #cbd5e0 !important;
}
/* Markdown tables on dark theme */
[data-testid="stMarkdownContainer"] table {
    border-collapse: collapse;
    width: 100%;
}
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td {
    border: 1px solid #2f3540 !important;
    padding: 0.55rem 0.9rem !important;
}
[data-testid="stMarkdownContainer"] th {
    background-color: #1c1f26 !important;
}

/* ---- Alert / message boxes (st.info / st.success / st.warning / st.error) ----
   Force PURE WHITE text inside these components so it stays readable against
   their colored backgrounds. */
[data-testid="stAlert"],
[data-testid="stAlert"] *,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] li,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] a,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] blockquote {
    color: #ffffff !important;
}

/* ---- Hero block (Overview page) ---- */
.hero {
    margin-bottom: 2rem;
    padding-bottom: 1.8rem;
    border-bottom: 2px solid #2a2f3a;
}
.hero .hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #68A4C4 !important;
    margin-bottom: 0.8rem;
}
.hero .hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.1rem;
    font-weight: 400;
    color: #fafafa !important;
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.hero .hero-desc {
    margin-top: 1.2rem;
    font-size: 1.08rem;
    line-height: 1.7;
    color: #b5c0cf !important;
    font-weight: 300;
    max-width: 720px;
}

/* ---- Page top bar (per-page standalone header) ---- */
.page-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #2a2f3a;
}
.page-header .eyebrow {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9aa6b5 !important;
    margin-bottom: 0.4rem;
}
.page-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    color: #fafafa !important;
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.page-header .subtitle {
    margin-top: 0.6rem;
    font-size: 0.95rem;
    color: #9aa6b5 !important;
    font-weight: 300;
}

/* ======================= UI polish (v2) ======================= */
:root {
    --bg:#0e1117; --surface:#151a23; --surface-2:#1b212c; --border:#262d3a;
    --border-soft:#1f2530; --text:#f4f6fa; --muted:#93a0b2; --muted-2:#6b778a;
    --accent:#68A4C4; --accent-soft:rgba(104,164,196,.14);
    --good:#6FCF97; --bad:#EB8C87; --warn:#F2C94C; --violet:#B58BD8;
    --radius:14px;
}
.block-container { max-width: 1240px !important; padding: 2.2rem 2.6rem 3rem !important; }

/* Active nav item (primary button in the sidebar) */
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: var(--accent-soft) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: inset 3px 0 0 var(--accent) !important;
    border: none !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] * { color:#ffffff !important; }

/* Main-area buttons */
.main .stButton button, [data-testid="stMain"] .stButton button {
    background: var(--surface); border: 1px solid var(--border); color: var(--text);
    border-radius: 10px; font-weight: 500; transition: all .15s ease;
}
[data-testid="stMain"] .stButton button:hover { border-color: var(--accent); color:#fff; }

/* Tabs → clean underline style */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: .25rem; border-bottom: 1px solid var(--border); margin-bottom: 1.2rem;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent; padding: .65rem 1.1rem; border-radius: 10px 10px 0 0;
    color: var(--muted) !important; font-weight: 500;
}
[data-testid="stTabs"] [data-baseweb="tab"] p { color: inherit !important; font-size: .95rem; }
[data-testid="stTabs"] [aria-selected="true"] { color: #ffffff !important; background: var(--surface); }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background-color: var(--accent) !important; height: 2px; }
[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

/* Inputs */
[data-baseweb="select"] > div, [data-baseweb="input"] > div {
    background: var(--surface) !important; border-color: var(--border) !important; border-radius: 10px !important;
}
[data-testid="stWidgetLabel"] p { color: var(--muted) !important; font-size: .78rem !important;
    font-weight: 600 !important; letter-spacing: .06em; text-transform: uppercase; }

/* Native metrics (other dashboards) as cards */
[data-testid="stMetric"] {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1rem 1.1rem;
}
[data-testid="stMetricLabel"] p { color: var(--muted) !important; font-size: .8rem !important; }

/* Expanders, dataframes, dividers */
[data-testid="stMain"] [data-testid="stExpander"] {
    background: var(--surface); border: 1px solid var(--border) !important; border-radius: var(--radius);
}
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
hr { border-color: var(--border) !important; }
[data-testid="stVegaLiteChart"] { background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: .9rem .9rem .4rem; }
[data-testid="stCaptionContainer"] p { color: var(--muted-2) !important; }

/* ---------- Tools Output components ---------- */
.to-head { display:flex; align-items:flex-end; justify-content:space-between; gap:1rem;
    margin: .2rem 0 1rem; flex-wrap: wrap; }
.to-head h3 { font-family:'DM Serif Display',serif; font-weight:400; font-size:1.6rem;
    margin:0; color:var(--text) !important; letter-spacing:-.01em; }
.to-head .src { color: var(--muted-2); font-size:.8rem; }
.to-head .src b { color: var(--muted); font-weight:500; }
.to-section { display:flex; align-items:center; gap:.6rem; margin: 1.6rem 0 .7rem; }
.to-section .t { font-size:.74rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
    color: var(--muted); }
.to-section .p { font-size:.78rem; color: var(--accent); background: var(--accent-soft);
    padding:.15rem .6rem; border-radius:999px; font-weight:600; }
.to-section .line { flex:1; height:1px; background: var(--border-soft); }
.to-grid { display:grid; gap:.8rem; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); }
.to-card { background: var(--surface); border:1px solid var(--border); border-radius: var(--radius);
    padding: 1rem 1.1rem .9rem; position:relative; overflow:hidden; }
.to-card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background: var(--c, var(--accent)); }
.to-card .l { font-size:.74rem; font-weight:600; letter-spacing:.06em; text-transform:uppercase; color: var(--muted); }
.to-card .v { font-size:1.9rem; font-weight:700; color: var(--text); margin:.25rem 0 .35rem;
    font-variant-numeric: tabular-nums; letter-spacing:-.02em; }
.to-card .f { display:flex; gap:.45rem; align-items:center; flex-wrap:wrap; font-size:.76rem; color: var(--muted-2); }
.to-chip { padding:.1rem .5rem; border-radius:999px; font-weight:600; font-size:.72rem; }
.to-chip.up-good, .to-chip.down-good { background: rgba(111,207,151,.13); color: var(--good); }
.to-chip.up-bad, .to-chip.down-bad { background: rgba(235,140,135,.13); color: var(--bad); }
.to-chip.flat { background: var(--surface-2); color: var(--muted); }
.to-rate { color: var(--muted); }
@media (max-width: 700px) { .block-container { padding: 1.2rem 1rem 2rem !important; } }
</style>
""", unsafe_allow_html=True)

# ── Navigation state ──────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Overview"


def go_to(page_name):
    st.session_state.page = page_name


def _nav_type(page_name):
    """Highlight the current page in the sidebar."""
    return "primary" if st.session_state.get("page") == page_name else "secondary"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # -- Company logo (top of sidebar) --
    # Safely render logo.png if it exists; never crash if the file is missing.
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
    except Exception:
        pass  # Logo is optional — ignore any image-loading error.

    st.markdown("""
    <div class="sidebar-brand">
        <span>Internal Portal</span>
        SB Soccer<br>Offline Quality Team
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)

    # -- Overview (main navigation item) --
    st.button("🏠  Overview", key="nav_overview",
              use_container_width=True, type=_nav_type("Overview"), on_click=go_to, args=("Overview",))

    # -- Team Productivity (live dashboard — top-level item) --
    st.button("📊  Team Productivity", key="nav_team_productivity",
              use_container_width=True, type=_nav_type("Team Productivity"), on_click=go_to, args=("Team Productivity",))

    # -- Customer Complaints (live dashboard — top-level item) --
    st.button("🗒️  Customer Complaints", key="nav_customer_complaints",
              use_container_width=True, type=_nav_type("Customer Complaints"), on_click=go_to, args=("Customer Complaints",))

    st.button("🎯  Quality Score", key="nav_quality_score",
              use_container_width=True, type=_nav_type("Quality Score"), on_click=go_to, args=("Quality Score",))

    st.button("🧰  Tools Output", key="nav_tools_output",
              use_container_width=True, type=_nav_type("Tools Output"), on_click=go_to, args=("Tools Output",))

    # -- "Review Processes" dropdown --
    with st.expander("🔍  Review Processes", expanded=True):
        st.button("A Review", key="nav_a_review",
                  use_container_width=True, type=_nav_type("A Review"), on_click=go_to, args=("A Review",))
        st.button("Hypercare Review", key="nav_hypercare_review",
                  use_container_width=True, type=_nav_type("Hypercare Review"), on_click=go_to, args=("Hypercare Review",))
        st.button("Player Review", key="nav_player_review",
                  use_container_width=True, type=_nav_type("Player Review"), on_click=go_to, args=("Player Review",))
        st.button("Sofascore Comparison Tool", key="nav_sofascore",
                  use_container_width=True, type=_nav_type("Sofascore Comparison Tool"), on_click=go_to, args=("Sofascore Comparison Tool",))

    # -- "Distribution Processes" dropdown --
    with st.expander("📦  Distribution Processes", expanded=True):
        st.button("Automated Match Extraction", key="nav_auto_extraction",
                  use_container_width=True, type=_nav_type("Automated Match Extraction"), on_click=go_to, args=("Automated Match Extraction",))
        st.button("Automated Match Distribution", key="nav_auto_distribution",
                  use_container_width=True, type=_nav_type("Automated Match Distribution"), on_click=go_to, args=("Automated Match Distribution",))

# ── Helper: standalone per-page header ────────────────────────────────────────
def render_page_header(eyebrow, title, subtitle=""):
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

# ── Live Scorecard data + dashboard (read straight from Google Sheets) ────────
_SHEET_ID = "1hHRnpri4jryPKzSR-h_obHCGzEckAd6OwP1ZhwSIiHo"
_SCORECARD_CSV = (
    "https://docs.google.com/spreadsheets/d/" + _SHEET_ID
    + "/gviz/tq?tqx=out:csv&sheet=Scorecard"
)
_MONTHS = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]
_SKIP_WORDS = {"date", "target", "total", "week", "wb", "year", "month", "day",
               "collected matches", "collected"}
_CAT_COLORS = ["#68A4C4", "#B58BD8", "#6FCF97", "#F2C94C", "#EB8C87", "#7FB3FF"]


def _to_num(value):
    """Turn a sheet cell like '1,076' or '' into a float."""
    if value is None:
        return 0.0
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    if cleaned in ("", "-", "."):
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _is_iso(value):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", str(value).strip()))


@st.cache_data(ttl=300, show_spinner=False)
def load_scorecard():
    """Read the Scorecard tab directly from Google Sheets and shape it.

    Cached for 5 minutes, so the page stays in sync with the sheet without
    re-downloading on every interaction. Nothing is hard-coded — every number
    comes from the live sheet.
    """
    raw = pd.read_csv(_SCORECARD_CSV, header=None, dtype=str, keep_default_na=False)
    grid = raw.values.tolist()

    # 1) Locate the row that holds the weekly (week-beginning) dates.
    date_row, best = -1, 0
    for i, row in enumerate(grid):
        hits = sum(1 for c in row if _is_iso(c))
        if hits > best:
            best, date_row = hits, i
    if date_row < 0 or best < 2:
        raise ValueError("Could not find the weekly date row in the Scorecard tab.")

    week_cols, week_dates = [], []
    for ci, val in enumerate(grid[date_row]):
        if _is_iso(val):
            week_cols.append(ci)
            week_dates.append(datetime.strptime(str(val).strip(), "%Y-%m-%d"))
    wset = set(week_cols)

    # 2) Detect category rows (Umbrella, Tornado, …); the "Total" row is skipped.
    cats = []
    for ri, row in enumerate(grid):
        if ri == date_row:
            continue
        weekly = [_to_num(row[c]) if c < len(row) else 0.0 for c in week_cols]
        total = sum(weekly)
        name = ""
        for k in (1, 0, 2, 3):  # prefer column B, then A, then C/D
            if k >= len(row) or k in wset:
                continue
            cell = str(row[k]).strip()
            if not cell or re.match(r"^[\d.,%\-]+$", cell) or cell.lower() in _SKIP_WORDS:
                continue
            name = cell
            break
        target = 0.0
        for k in range(min(4, len(row))):
            if k not in wset:
                target = max(target, _to_num(row[k]))
        if name and (total > 0 or target > 0):
            cats.append({"name": name, "target": target, "weekly": weekly, "total": total})
    if not cats:
        raise ValueError("No category rows found in the Scorecard tab.")

    # 3) Tidy table for charts + a per-month roll-up.
    records, mmap, order = [], {}, []
    for ci, d in enumerate(week_dates):
        key = (d.year, d.month)
        if key not in mmap:
            mmap[key] = {"name": _MONTHS[d.month - 1], "year": d.year, "month_idx": d.month - 1,
                         "weeks": [], "total": 0.0, "per_cat": {c["name"]: 0.0 for c in cats}}
            order.append(key)
        mo = mmap[key]
        week_total = 0.0
        for c in cats:
            v = c["weekly"][ci]
            week_total += v
            mo["per_cat"][c["name"]] += v
            records.append({"date": d, "month": _MONTHS[d.month - 1],
                            "month_idx": d.month - 1, "category": c["name"], "value": v})
        mo["weeks"].append({"date": d, "total": week_total})
        mo["total"] += week_total

    return {
        "categories": cats,
        "months": [mmap[k] for k in order],
        "long": pd.DataFrame(records),
        "total_collected": sum(c["total"] for c in cats),
        "total_target": sum(c["target"] for c in cats),
        "fetched_at": datetime.now(),
    }


def _auto_refresh(func):
    """Re-run just this section every 5 min, if this Streamlit build supports it."""
    frag = getattr(st, "fragment", None) or getattr(st, "experimental_fragment", None)
    if frag is None:
        return func
    try:
        return frag(run_every=300)(func)
    except Exception:
        try:
            return frag(func)
        except Exception:
            return func


def _color_scale(cats):
    return alt.Scale(domain=[c["name"] for c in cats], range=_CAT_COLORS[: len(cats)])


@_auto_refresh
def render_team_productivity():
    # -- Controls (handled before loading so Refresh takes effect immediately) --
    c1, c2, c3 = st.columns([2.2, 2.2, 1])
    period = c1.selectbox(
        "Filter by period",
        ["Full Year", "Q1 · Jan–Mar", "Q2 · Apr–Jun", "Q3 · Jul–Sep", "Q4 · Oct–Dec"],
        key="tp_period",
    )
    view = c2.radio("View", ["Monthly timeline", "By category"],
                    horizontal=True, key="tp_view")
    with c3:
        st.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            load_scorecard.clear()

    try:
        data = load_scorecard()
    except Exception as exc:  # noqa: BLE001
        st.error(
            "Couldn't read the **Scorecard** tab from Google Sheets. The sheet must be "
            "shared so anyone with the link can view it (Share → General access → "
            "Anyone with the link → Viewer)."
        )
        st.caption(f"Technical detail: {exc}")
        return

    cats = data["categories"]
    long = data["long"]
    total_collected = data["total_collected"]
    total_target = data["total_target"]
    overall = (total_collected / total_target * 100) if total_target else 0.0

    quarters = {"Q1 · Jan–Mar": [0, 1, 2], "Q2 · Apr–Jun": [3, 4, 5],
                "Q3 · Jul–Sep": [6, 7, 8], "Q4 · Oct–Dec": [9, 10, 11]}
    scope = quarters.get(period)
    months = data["months"] if scope is None else [m for m in data["months"] if m["month_idx"] in scope]
    fl = long if scope is None else long[long["month_idx"].isin(scope)]

    # -- Headline KPIs ---------------------------------------------------------
    m_tot = (fl.groupby(["month_idx", "month"])["value"].sum()
               .reset_index().sort_values("month_idx"))
    peak = m_tot.loc[m_tot["value"].idxmax()] if (not m_tot.empty and m_tot["value"].max() > 0) else None

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Overall progress", f"{overall:.0f}%" if overall >= 99.95 else f"{overall:.1f}%")
    k2.metric("Total matches", f"{int(total_collected):,}")
    k3.metric("Global target", f"{int(total_target):,}")
    k4.metric("Peak month", peak["month"] if peak is not None else "—",
              help=(f"{int(peak['value']):,} matches" if peak is not None else None))
    st.progress(min(1.0, (total_collected / total_target) if total_target else 0.0),
                text=f"{int(total_collected):,} of {int(total_target):,} matches collected "
                     f"· {len(cats)} categories ({', '.join(c['name'] for c in cats)})")
    st.caption(f"Live from the Scorecard tab · updated {data['fetched_at'].strftime('%b %d, %I:%M %p')}")
    st.divider()

    if view == "Monthly timeline":
        st.markdown("##### Monthly collections")
        st.altair_chart(
            alt.Chart(m_tot).mark_bar(color="#68A4C4", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(x=alt.X("month:N", sort=list(m_tot["month"]), title=None),
                    y=alt.Y("value:Q", title="Matches"),
                    tooltip=[alt.Tooltip("month:N", title="Month"),
                             alt.Tooltip("value:Q", title="Matches", format=",")])
            .properties(height=260),
            use_container_width=True,
        )

        st.markdown("##### Weekly trend by category")
        wk = fl.groupby(["date", "category"])["value"].sum().reset_index()
        st.altair_chart(
            alt.Chart(wk).mark_bar()
            .encode(x=alt.X("date:T", title=None),
                    y=alt.Y("value:Q", title="Matches", stack="zero"),
                    color=alt.Color("category:N", scale=_color_scale(cats),
                                    legend=alt.Legend(title=None, orient="top")),
                    tooltip=[alt.Tooltip("date:T", title="Week of"), "category",
                             alt.Tooltip("value:Q", title="Matches", format=",")])
            .properties(height=260),
            use_container_width=True,
        )

        st.markdown("##### Monthly gallery")
        if not months:
            st.info("No months in this period.")
        else:
            cols = st.columns(3)
            for i, mo in enumerate(months):
                with cols[i % 3]:
                    with st.container(border=True):
                        # Show only the weeks that actually have collections this month.
                        weeks_with_data = [w for w in mo["weeks"] if w["total"] > 0]
                        st.markdown(
                            f"**{mo['name']} {mo['year']}** &nbsp;"
                            f"<span style='color:#68A4C4;font-size:.8rem'>{len(weeks_with_data)} weeks</span>",
                            unsafe_allow_html=True,
                        )
                        st.metric("Total monthly collections", f"{int(mo['total']):,}")
                        if weeks_with_data:
                            wdf = pd.DataFrame([{"date": w["date"],
                                                 "day": w["date"].strftime("%d"),
                                                 "week": w["date"].strftime("%d %b"),
                                                 "matches": w["total"]} for w in weeks_with_data])
                            week_order = list(wdf.sort_values("date")["day"])
                            st.altair_chart(
                                alt.Chart(wdf).mark_bar(color="#68A4C4")
                                .encode(x=alt.X("day:N", sort=week_order, title=None,
                                                axis=alt.Axis(labelFontSize=9, labelAngle=0)),
                                        y=alt.Y("matches:Q", title=None),
                                        tooltip=[alt.Tooltip("week:N", title="Week of"),
                                                 alt.Tooltip("matches:Q", title="Matches", format=",")])
                                .properties(height=90),
                                use_container_width=True,
                            )
                            for c in cats:
                                v = mo["per_cat"][c["name"]]
                                pct = (v / mo["total"] * 100) if mo["total"] else 0
                                st.progress(min(1.0, v / mo["total"] if mo["total"] else 0),
                                            text=f"{c['name']}: {int(v):,} · {pct:.0f}%")
                        else:
                            st.caption("No collections recorded yet.")

        with st.expander("View the numbers as a table"):
            table = (fl.pivot_table(index="month", columns="category", values="value",
                                    aggfunc="sum").reindex([m["name"] for m in months]))
            if not table.empty:
                table["Total"] = table.sum(axis=1)
            st.dataframe(table.style.format("{:,.0f}"), use_container_width=True)

    else:  # By category
        st.markdown("##### Progress by category")
        for c in cats:
            pct = (c["total"] / c["target"] * 100) if c["target"] else 0
            st.markdown(f"**{c['name']}** — {int(c['total']):,} of {int(c['target']):,} ({pct:.0f}%)")
            st.progress(min(1.0, c["total"] / c["target"] if c["target"] else 0))

        st.markdown("##### Collected vs target")
        cmp_df = pd.DataFrame(
            [{"category": c["name"], "Collected": c["total"], "Target": c["target"]} for c in cats]
        ).melt("category", var_name="Measure", value_name="Matches")
        st.altair_chart(
            alt.Chart(cmp_df).mark_bar()
            .encode(x=alt.X("category:N", title=None),
                    y=alt.Y("Matches:Q"),
                    color=alt.Color("Measure:N",
                                    scale=alt.Scale(domain=["Collected", "Target"],
                                                    range=["#68A4C4", "#3a4a57"]),
                                    legend=alt.Legend(title=None, orient="top")),
                    xOffset="Measure:N",
                    tooltip=["category", "Measure", alt.Tooltip("Matches:Q", format=",")])
            .properties(height=300),
            use_container_width=True,
        )

        st.markdown("##### Monthly trend by category")
        trend = fl.groupby(["date", "category"])["value"].sum().reset_index()
        st.altair_chart(
            alt.Chart(trend).mark_line(point=True)
            .encode(x=alt.X("date:T", title=None),
                    y=alt.Y("value:Q", title="Matches"),
                    color=alt.Color("category:N", scale=_color_scale(cats),
                                    legend=alt.Legend(title=None, orient="top")),
                    tooltip=[alt.Tooltip("date:T", title="Week of"), "category",
                             alt.Tooltip("value:Q", title="Matches", format=",")])
            .properties(height=280),
            use_container_width=True,
        )


# ── Live Customer Complaints data + dashboard (read straight from Sheets) ─────
_COMPLAINTS_CSV = (
    "https://docs.google.com/spreadsheets/d/1bAif9RXwpopZuNx8f7-DgCPPOiMOrHAFpOyE0INM0SU"
    "/gviz/tq?tqx=out:csv&sheet=Customers%20Complaints"
)
# The gviz header row comes back partly blank, so we parse by fixed column index.
_C = {"id": 0, "app": 1, "match_id": 2, "ctype": 3, "issue": 4, "customer": 10,
      "validity": 11, "cdate": 12, "wb": 14, "month": 15, "frt": 19, "sla": 20,
      "qatl": 21, "reviewer": 23, "collector": 24, "responsible": 25, "match_name": 26}
_VALIDITY_COLORS = {"Valid": "#6FCF97", "Invalid": "#EB8C87",
                    "Duplicate": "#F2C94C", "Unspecified": "#6f7a8a"}
_APP_COLORS = {"Umbrella": "#B58BD8", "Tornado": "#68A4C4", "Unknown": "#6f7a8a"}


def _dur_hours(value):
    """Parse an 'H:MM:SS' duration into hours; guard broken values (e.g. negatives)."""
    s = str(value).strip()
    if not s or ":" not in s:
        return None
    parts = s.split(":")
    try:
        h, m = int(parts[0]), int(parts[1])
        sec = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        return None
    if h < 0 or h > 1000:  # the sheet occasionally holds corrupt cells
        return None
    return h + m / 60 + sec / 3600


@st.cache_data(ttl=300, show_spinner=False)
def load_complaints():
    """Read the raw 'Customers Complaints' tab and shape it into tidy rows.

    Cached for 5 minutes. Every figure is derived live from the sheet.
    """
    raw = pd.read_csv(_COMPLAINTS_CSV, header=None, dtype=str, keep_default_na=False)
    month_lookup = {m: i for i, m in enumerate(_MONTHS)}
    recs = []
    for row in raw.values.tolist():
        if len(row) <= _C["responsible"]:
            continue
        idv = str(row[_C["id"]]).strip()
        if not re.match(r"^\d+$", idv):  # data rows have a positive integer ID
            continue
        recs.append({
            "ID": int(idv),
            "App": row[_C["app"]].strip() or "Unknown",
            "Customer": row[_C["customer"]].strip() or "Unknown",
            "Validity": row[_C["validity"]].strip() or "Unspecified",
            "Complaint Type": row[_C["ctype"]].strip() or "Unknown",
            "Issue": row[_C["issue"]].strip() or "Unknown",
            "Month": row[_C["month"]].strip() or "Unknown",
            "Responsible": row[_C["responsible"]].strip() or "Unassigned",
            "Reviewer": row[_C["reviewer"]].strip(),
            "Collector": row[_C["collector"]].strip(),
            "frt_h": _dur_hours(row[_C["frt"]]),
            "sla_h": _dur_hours(row[_C["sla"]]),
        })
    df = pd.DataFrame(recs)
    if not df.empty:
        df["month_idx"] = df["Month"].map(month_lookup).fillna(99).astype(int)
    return {"df": df, "fetched_at": datetime.now()}


def _months_present(df):
    return [m for m in _MONTHS if m in set(df["Month"])]


def _count_chart(series, label, color="#68A4C4", horizontal=False):
    """Bar chart of category counts. Shows every value, whole-number axis,
    and full (untruncated) category labels."""
    cdf = series.value_counts().reset_index()
    cdf.columns = [label, "Complaints"]
    count_axis = alt.Axis(format="d", tickMinStep=1)        # 1, 2, 3 — no decimals
    base = alt.Chart(cdf)
    if horizontal:
        return base.mark_bar(color=color, cornerRadiusEnd=3).encode(
            y=alt.Y(f"{label}:N", sort="-x", title=None, axis=alt.Axis(labelLimit=360)),
            x=alt.X("Complaints:Q", title="Complaints", axis=count_axis),
            tooltip=[label, "Complaints"]).properties(height=max(160, 28 * len(cdf)))
    return base.mark_bar(color=color, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X(f"{label}:N", sort="-y", title=None, axis=alt.Axis(labelLimit=360, labelAngle=-40)),
        y=alt.Y("Complaints:Q", title="Complaints", axis=count_axis),
        tooltip=[label, "Complaints"]).properties(height=260)


@_auto_refresh
def render_customer_complaints():
    # -- Controls (before load, so Refresh applies immediately) ----------------
    c1, c2, c3, c4 = st.columns([2, 1.6, 2, 1])
    with c4:
        st.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True, key="cc_refresh"):
            load_complaints.clear()

    try:
        data = load_complaints()
    except Exception as exc:  # noqa: BLE001
        st.error(
            "Couldn't read the **Customers Complaints** tab from Google Sheets. The sheet "
            "must be shared so anyone with the link can view it."
        )
        st.caption(f"Technical detail: {exc}")
        return

    df = data["df"]
    if df.empty:
        st.info("No complaints found in the sheet yet.")
        return

    # Only classified complaints (Valid / Invalid) are analysed, so the total always
    # equals Valid + Invalid. Duplicates and any not-yet-classified rows are excluded.
    n_dup = int((df["Validity"] == "Duplicate").sum())
    n_unclassified = int((~df["Validity"].isin(["Valid", "Invalid", "Duplicate"])).sum())
    df = df[df["Validity"].isin(["Valid", "Invalid"])].copy()

    month_opts = ["All months"] + _months_present(df)
    period = c1.selectbox("Filter by month", month_opts, key="cc_month")
    validity_choice = c2.selectbox("Validity", ["All", "Valid", "Invalid"], key="cc_validity")
    view = c3.radio("View", ["Summary", "Breakdowns"], horizontal=True, key="cc_view")

    fm = df if period == "All months" else df[df["Month"] == period]
    fv = fm if validity_choice == "All" else fm[fm["Validity"] == validity_choice]

    # -- Headline KPIs ---------------------------------------------------------
    total = len(fm)
    valid = int((fm["Validity"] == "Valid").sum())
    invalid = int((fm["Validity"] == "Invalid").sum())
    valid_pct = (valid / total * 100) if total else 0
    avg_sla = fm["sla_h"].dropna().mean()
    avg_frt = fm["frt_h"].dropna().mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total complaints", f"{total:,}")
    k2.metric("Valid rate", f"{valid_pct:.0f}%")
    k3.metric("Valid", f"{valid:,}")
    k4.metric("Invalid", f"{invalid:,}")
    bits = [f"{fm['Customer'].nunique()} customers"]
    if pd.notna(avg_sla):
        bits.append(f"avg resolution {avg_sla:.1f}h")
    if pd.notna(avg_frt):
        bits.append(f"avg first response {avg_frt*60:.0f} min")
    if n_dup:
        bits.append(f"{n_dup} duplicates excluded")
    if n_unclassified:
        bits.append(f"{n_unclassified} unclassified excluded")
    st.progress(min(1.0, valid_pct / 100), text=" · ".join(bits))
    st.caption(f"Live from the Customers Complaints tab · updated "
               f"{data['fetched_at'].strftime('%b %d, %I:%M %p')}")
    st.divider()

    val_scale = alt.Scale(domain=list(_VALIDITY_COLORS), range=list(_VALIDITY_COLORS.values()))

    if view == "Summary":
        st.markdown("##### Complaints over time")
        mv = (fm.groupby(["month_idx", "Month", "Validity"]).size()
                .reset_index(name="Complaints").sort_values("month_idx"))
        order = [m for m in _MONTHS if m in set(mv["Month"])]
        st.altair_chart(
            alt.Chart(mv).mark_bar().encode(
                x=alt.X("Month:N", sort=order, title=None),
                y=alt.Y("Complaints:Q", stack="zero", title="Complaints",
                        axis=alt.Axis(format="d", tickMinStep=1)),
                color=alt.Color("Validity:N", scale=val_scale,
                                legend=alt.Legend(title=None, orient="top")),
                tooltip=["Month", "Validity", "Complaints"]).properties(height=260),
            use_container_width=True,
        )

        a, b = st.columns(2)
        with a:
            st.markdown("##### Validity breakdown")
            vc = fm["Validity"].value_counts().reset_index()
            vc.columns = ["Validity", "Complaints"]
            st.altair_chart(
                alt.Chart(vc).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                    x=alt.X("Validity:N", title=None, sort=["Valid", "Invalid"]),
                    y=alt.Y("Complaints:Q", title="Complaints",
                            axis=alt.Axis(format="d", tickMinStep=1)),
                    color=alt.Color("Validity:N", scale=val_scale, legend=None),
                    tooltip=["Validity", "Complaints"]).properties(height=240),
                use_container_width=True,
            )
        with b:
            st.markdown("##### Avg resolution time by month")
            ms = (fm.dropna(subset=["sla_h"]).groupby(["month_idx", "Month"])["sla_h"]
                    .mean().reset_index().sort_values("month_idx"))
            if ms.empty:
                st.caption("No resolution times recorded for this selection.")
            else:
                st.altair_chart(
                    alt.Chart(ms).mark_bar(color="#68A4C4", cornerRadiusTopLeft=3,
                                           cornerRadiusTopRight=3).encode(
                        x=alt.X("Month:N", sort=[m for m in _MONTHS if m in set(ms["Month"])],
                                title=None),
                        y=alt.Y("sla_h:Q", title="Avg hours"),
                        tooltip=["Month", alt.Tooltip("sla_h:Q", title="Avg hours",
                                                      format=".1f")]).properties(height=240),
                    use_container_width=True,
                )

    else:  # Breakdowns
        if validity_choice != "All":
            st.caption(f"Showing **{validity_choice}** complaints only.")
        if fv.empty:
            st.info("No complaints match this filter.")
        else:
            st.markdown("##### Complaints by customer")
            st.altair_chart(_count_chart(fv["Customer"], "Customer", horizontal=True),
                            use_container_width=True)

            a, b = st.columns(2)
            with a:
                st.markdown("##### By app")
                ac = fv["App"].value_counts().reset_index()
                ac.columns = ["App", "Complaints"]
                st.altair_chart(
                    alt.Chart(ac).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                        x=alt.X("App:N", title=None),
                        y=alt.Y("Complaints:Q", title="Complaints",
                                axis=alt.Axis(format="d", tickMinStep=1)),
                        color=alt.Color("App:N",
                                        scale=alt.Scale(domain=list(_APP_COLORS),
                                                        range=list(_APP_COLORS.values())),
                                        legend=None),
                        tooltip=["App", "Complaints"]).properties(height=240),
                    use_container_width=True,
                )
            with b:
                st.markdown("##### By complaint type")
                st.altair_chart(_count_chart(fv["Complaint Type"], "Complaint Type"),
                                use_container_width=True)

            st.markdown("##### Complaints by issue")
            st.altair_chart(_count_chart(fv["Issue"], "Issue", horizontal=True),
                            use_container_width=True)

            st.markdown("##### By responsible team")
            st.altair_chart(_count_chart(fv["Responsible"], "Responsible", color="#B58BD8"),
                            use_container_width=True)

    with st.expander("View the complaints as a table"):
        show = fv.sort_values("ID", ascending=False).copy()
        show["Resolution (h)"] = show["sla_h"].round(2)
        show = show[["ID", "Month", "Customer", "App", "Complaint Type", "Issue",
                     "Validity", "Resolution (h)", "Responsible"]]
        st.dataframe(show, use_container_width=True, hide_index=True)


# ── Quality Score Dashboard (live, read straight from Google Sheets) ──────────
_QS_SHEET_ID = "1meQNmgQTLq58yaC6TIz1zOrdm4ajkaynyK2WJdAvoaU"
_QS_BASE = ("https://docs.google.com/spreadsheets/d/" + _QS_SHEET_ID
            + "/gviz/tq?tqx=out:csv&sheet=")
_QS_WEEK_CSV = _QS_BASE + "Week%20Over%20Week%20Score"
_QS_MONTH_CSV = _QS_BASE + "Month%20Over%20Month%20Score"
# Sheet metric label -> short name used in the app.
_QS_METRIC_MAP = {
    "collector_score": "score",
    "errors": "errors",
    "collector_mod_event_count": "events",
}
_QS_COLORS = ["#68A4C4", "#B58BD8", "#6FCF97", "#F2C94C",
              "#EB8C87", "#7FB3FF", "#E0A458", "#9F8BD8"]
_QS_QUARTERS = {"Q1 · Jan–Mar": {1, 2, 3}, "Q2 · Apr–Jun": {4, 5, 6},
                "Q3 · Jul–Sep": {7, 8, 9}, "Q4 · Oct–Dec": {10, 11, 12}}


def _qs_parse_period(label, freq):
    """'4 January 2026' -> date (weekly) | 'January 2026' -> date (monthly)."""
    fmt = "%d %B %Y" if freq == "week" else "%B %Y"
    try:
        return datetime.strptime(str(label).strip(), fmt)
    except ValueError:
        return None


def _qs_shape(grid, freq):
    """Shape one tab's grid into tidy rows: module, metric, period, date, value."""
    hdr = -1
    for i, row in enumerate(grid):
        if row and str(row[0]).strip().lower() == "module":
            hdr = i
            break
    if hdr < 0:
        raise ValueError("Could not find the 'module' header row.")

    header = grid[hdr]
    pcols, plabels, pdates = [], [], []
    for ci in range(2, len(header)):
        lab = str(header[ci]).strip()
        d = _qs_parse_period(lab, freq) if lab else None
        if d is None:
            continue
        pcols.append(ci)
        plabels.append(lab)
        pdates.append(d)
    if not pcols:
        raise ValueError("No period columns found in the tab.")

    recs, last_module = [], ""
    for row in grid[hdr + 1:]:
        module = str(row[0]).strip() if len(row) > 0 else ""
        if module:
            last_module = module           # carry module across merged cells
        module = module or last_module
        metric = _QS_METRIC_MAP.get(str(row[1]).strip().lower() if len(row) > 1 else "")
        if not module or not metric:
            continue
        for j, ci in enumerate(pcols):
            cell = str(row[ci]).strip() if ci < len(row) else ""
            if cell == "":
                continue                   # no data for this module / period
            recs.append({"module": module, "metric": metric,
                         "period": plabels[j], "date": pdates[j],
                         "value": _to_num(cell)})
    return pd.DataFrame(recs)


@st.cache_data(ttl=300, show_spinner=False)
def load_quality_scores():
    """Read both tabs of the Quality Score Dashboard. Cached for 5 minutes."""
    week = _qs_shape(pd.read_csv(_QS_WEEK_CSV, header=None, dtype=str,
                                 keep_default_na=False).values.tolist(), "week")
    month = _qs_shape(pd.read_csv(_QS_MONTH_CSV, header=None, dtype=str,
                                  keep_default_na=False).values.tolist(), "month")
    return {"week": week, "month": month, "fetched_at": datetime.now()}


def _qs_weighted_score(slice_df):
    """Overall score for a slice = 1 - errors/events (matches collector_score)."""
    errs = slice_df.loc[slice_df["metric"] == "errors", "value"].sum()
    evts = slice_df.loc[slice_df["metric"] == "events", "value"].sum()
    if evts <= 0:
        sc = slice_df.loc[slice_df["metric"] == "score", "value"]
        return (sc.mean() if not sc.empty else 0.0), errs, evts
    return (1 - errs / evts) * 100, errs, evts


@_auto_refresh
def render_quality_score():
    # -- Controls (before load, so Refresh applies immediately) ----------------
    c1, c2, c3 = st.columns([1.5, 3, 1])
    freq_label = c1.radio("Granularity", ["Weekly", "Monthly"],
                          horizontal=True, key="qs_freq")
    with c3:
        st.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True, key="qs_refresh"):
            load_quality_scores.clear()

    try:
        data = load_quality_scores()
    except Exception as exc:  # noqa: BLE001
        st.error(
            "Couldn't read the **Quality Score Dashboard** from Google Sheets. The sheet "
            "must be shared so anyone with the link can view it."
        )
        st.caption(f"Technical detail: {exc}")
        return

    freq = "week" if freq_label == "Weekly" else "month"
    df = data[freq]
    if df.empty:
        st.info("No quality-score data found in the sheet yet.")
        return

    periods = (df[["date", "period"]].drop_duplicates()
               .sort_values("date").reset_index(drop=True))
    plist = list(periods["period"])

    # -- Period filter: a week range, or a quarter for months ------------------
    if freq == "week":
        if len(plist) >= 2:
            start, end = c2.select_slider("Week range", options=plist,
                                          value=(plist[0], plist[-1]), key="qs_week_range")
        else:
            start = end = plist[0]
        d0 = periods.loc[periods["period"] == start, "date"].iloc[0]
        d1 = periods.loc[periods["period"] == end, "date"].iloc[0]
        period_mask = df["date"].between(min(d0, d1), max(d0, d1))
        period_note = f"{start} → {end}"
    else:
        present_q = [q for q, mset in _QS_QUARTERS.items()
                     if any(d.month in mset for d in periods["date"])]
        # Full range, a whole quarter, or a single specific month.
        choice = c2.selectbox("Period", ["Full range"] + present_q + plist,
                              key="qs_month_period")
        if choice == "Full range":
            period_mask = pd.Series(True, index=df.index)
            period_note = f"{plist[0]} → {plist[-1]}"
        elif choice in _QS_QUARTERS:
            period_mask = df["date"].dt.month.isin(_QS_QUARTERS[choice])
            period_note = choice
        else:
            period_mask = df["period"] == choice
            period_note = choice

    fdf = df[period_mask].copy()
    if fdf.empty:
        st.info("No data for the selected period.")
        return

    # -- Plotting helpers: one axis label per period, short week/month labels --
    modules = sorted(df["module"].unique())
    fmt_short = "%d %b" if freq == "week" else "%b %Y"
    fdf["plabel"] = fdf["date"].dt.strftime(fmt_short)
    period_order = list(fdf.sort_values("date")["plabel"].unique())
    x_period = alt.X("plabel:N", sort=period_order, title=None,
                     axis=alt.Axis(labelAngle=-40 if freq == "week" else 0))
    color_enc = alt.Color("module:N",
                          scale=alt.Scale(domain=modules, range=_QS_COLORS[: len(modules)]),
                          legend=alt.Legend(title=None, orient="top"))

    # -- Headline KPIs ---------------------------------------------------------
    ov_score, ov_errs, ov_evts = _qs_weighted_score(fdf)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Overall quality score", f"{ov_score:.2f}%")
    k2.metric("Total errors", f"{int(ov_errs):,}")
    k3.metric("Events reviewed", f"{int(ov_evts):,}")
    k4.metric("Modules tracked", f"{fdf['module'].nunique()}")
    st.caption(f"Showing {freq_label.lower()} data · {period_note} · "
               f"updated {data['fetched_at'].strftime('%d %b %Y, %H:%M')}")

    # -- Per-module score cards (score big; total errors in brackets under) ----
    st.markdown("##### Score by module")
    card_mods = [m for m in modules if m in set(fdf["module"])]
    ncol = 4
    for i in range(0, len(card_mods), ncol):
        cols = st.columns(ncol)
        for col, m in zip(cols, card_mods[i:i + ncol]):
            msl = fdf[fdf["module"] == m]
            sc, er, _ev = _qs_weighted_score(msl)
            sline = msl[msl["metric"] == "score"].sort_values("date")
            delta = (f"{sline['value'].iloc[-1] - sline['value'].iloc[0]:+.2f} pts"
                     if len(sline) >= 2 else None)
            with col.container(border=True):
                st.metric(m.capitalize(), f"{sc:.2f}%", delta=delta)
                st.markdown(
                    f"<div style='color:#9aa6b5;font-size:.85rem;margin-top:-.5rem'>"
                    f"({int(er):,} total errors)</div>", unsafe_allow_html=True)

    # -- Tabbed views ----------------------------------------------------------
    tab_trend, tab_rank, tab_err, tab_detail, tab_table = st.tabs(
        ["Score trend", "Ranking", "Errors & volume", "Module detail", "Data table"])

    with tab_trend:
        sel_t = st.multiselect("Modules", card_mods, default=card_mods, key="qs_trend_mods")
        sc_df = fdf[(fdf["metric"] == "score") & (fdf["module"].isin(sel_t))]
        if sc_df.empty:
            st.info("Pick at least one module to see the trend.")
        else:
            line = (alt.Chart(sc_df).mark_line(point=True)
                    .encode(x=x_period,
                            y=alt.Y("value:Q", title="Score (%)",
                                    scale=alt.Scale(zero=False)),
                            color=color_enc,
                            tooltip=["module", alt.Tooltip("period:N", title="Period"),
                                     alt.Tooltip("value:Q", title="Score", format=".2f")])
                    .properties(height=360))
            st.altair_chart(line, use_container_width=True)
            st.caption("Each line is a module's collector_score over the selected periods.")

    with tab_rank:
        rrecs = []
        for m in card_mods:
            s, e, _v = _qs_weighted_score(fdf[fdf["module"] == m])
            rrecs.append({"module": m, "score": s, "errors": e})
        rdf = pd.DataFrame(rrecs)
        bar = (alt.Chart(rdf).mark_bar(cornerRadiusEnd=3)
               .encode(y=alt.Y("module:N", sort="x", title=None),
                       x=alt.X("score:Q", title="Score (%)", scale=alt.Scale(zero=False)),
                       color=color_enc,
                       tooltip=["module", alt.Tooltip("score:Q", title="Score", format=".2f"),
                                alt.Tooltip("errors:Q", title="Errors", format=",")])
               .properties(height=max(160, 42 * len(rdf))))
        st.altair_chart(bar, use_container_width=True)
        st.caption("Lowest score first — these modules need the most attention.")

    with tab_err:
        sel_e = st.multiselect("Modules", card_mods, default=card_mods, key="qs_err_mods")
        er_df = fdf[(fdf["metric"] == "errors") & (fdf["module"].isin(sel_e))]
        if er_df.empty:
            st.info("Pick at least one module to see errors.")
        else:
            err_chart = (alt.Chart(er_df).mark_bar()
                         .encode(x=x_period,
                                 y=alt.Y("value:Q", title="Errors", stack="zero"),
                                 color=color_enc,
                                 tooltip=["module", alt.Tooltip("period:N", title="Period"),
                                          alt.Tooltip("value:Q", title="Errors", format=",")])
                         .properties(height=300))
            st.altair_chart(err_chart, use_container_width=True)
        ev_df = (fdf[(fdf["metric"] == "events") & (fdf["module"].isin(sel_e))]
                 .groupby("module", as_index=False)["value"].sum())
        if not ev_df.empty:
            vol = (alt.Chart(ev_df).mark_bar(cornerRadiusEnd=3)
                   .encode(y=alt.Y("module:N", sort="-x", title=None),
                           x=alt.X("value:Q", title="Events reviewed"),
                           color=color_enc,
                           tooltip=["module", alt.Tooltip("value:Q", title="Events", format=",")])
                   .properties(height=max(160, 42 * len(ev_df))))
            st.markdown("**Volume reviewed per module**")
            st.altair_chart(vol, use_container_width=True)

    with tab_detail:
        m = st.selectbox("Module", card_mods, key="qs_detail_mod")
        msl = fdf[fdf["module"] == m]
        sc, er, ev = _qs_weighted_score(msl)
        d1, d2, d3 = st.columns(3)
        d1.metric("Score", f"{sc:.2f}%")
        d2.metric("Total errors", f"{int(er):,}")
        d3.metric("Events reviewed", f"{int(ev):,}")
        sc_one = msl[msl["metric"] == "score"]
        if not sc_one.empty:
            sline = (alt.Chart(sc_one).mark_area(opacity=0.25, line={"color": _QS_COLORS[0]},
                                                 color=_QS_COLORS[0])
                     .encode(x=x_period,
                             y=alt.Y("value:Q", title="Score (%)", scale=alt.Scale(zero=False)),
                             tooltip=[alt.Tooltip("period:N", title="Period"),
                                      alt.Tooltip("value:Q", title="Score", format=".2f")])
                     .properties(height=240))
            st.altair_chart(sline, use_container_width=True)
        er_one = msl[msl["metric"] == "errors"]
        if not er_one.empty:
            ebar = (alt.Chart(er_one).mark_bar(color="#EB8C87")
                    .encode(x=x_period,
                            y=alt.Y("value:Q", title="Errors"),
                            tooltip=[alt.Tooltip("period:N", title="Period"),
                                     alt.Tooltip("value:Q", title="Errors", format=",")])
                    .properties(height=200))
            st.altair_chart(ebar, use_container_width=True)

    with tab_table:
        sc_df = fdf[fdf["metric"] == "score"]
        if sc_df.empty:
            st.info("No score rows for this selection.")
        else:
            piv = (sc_df.pivot_table(index="period", columns="module",
                                     values="value", aggfunc="mean", sort=False))
            order = list(periods.loc[periods["period"].isin(piv.index), "period"])
            piv = piv.reindex(order)
            disp = piv.copy()
            for c in disp.columns:
                disp[c] = disp[c].map(lambda v: f"{v:.2f}%" if pd.notna(v) else "—")
            st.dataframe(disp, use_container_width=True)
            st.caption("collector_score (%) by module and period.")


# ── Tools Output (Player Review App · Sofascore · WhoScored Validation) ──────
# Every section reads a Google Sheet as public CSV (same pattern as the other
# live dashboards). Sheets must be shared "anyone with the link can view".
# The Apps Scripts (apps_script/1_PlayerReview.gs, 2_Sofascore.gs, 3_WhoScored.gs)
# write the tabs PR_Summary / Sofa_Summary / WS_Summary. The site reads them with a
# Google service account (the sheets are shared with its e-mail as Viewer).
# Config lives in .streamlit/secrets.toml — see apps_script/README.md.
_TO_WEEKS_DEFAULT = 6
_TO_SHEET_KEYS = {"PR_Summary": "pr_sheet_id", "Sofa_Summary": "sofa_sheet_id",
                  "WS_Summary": "ws_sheet_id"}


def _to_secrets():
    try:
        return st.secrets
    except Exception:  # noqa: BLE001 — no secrets.toml
        return {}


_TO_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "service account.json")


_TO_HUB_SHEET_ID = "1npyRK-hWRVC1rie9MNDP2cHs17zUMMW8qLJUAGpMMYA"   # "Tools Documentation"


def _to_sheet_ids():
    ids = {k: _TO_HUB_SHEET_ID for k in _TO_SHEET_KEYS.values()}
    s = _to_secrets()
    if "tools_output" in s:
        ids.update({k: v for k, v in dict(s["tools_output"]).items() if v})
    return ids


def _to_configured():
    has_key = "gcp_service_account" in _to_secrets() or os.path.exists(_TO_KEY_FILE)
    return has_key and bool(_to_sheet_ids())


@st.cache_resource(show_spinner=False)
def _to_client():
    import gspread
    s = _to_secrets()
    if "gcp_service_account" in s:
        return gspread.service_account_from_dict(dict(s["gcp_service_account"]))
    return gspread.service_account(filename=_TO_KEY_FILE)


def _to_read(tab):
    sheet_id = _to_sheet_ids().get(_TO_SHEET_KEYS[tab], "")
    if not sheet_id:
        raise RuntimeError(f"{_TO_SHEET_KEYS[tab]} is missing in secrets.toml [tools_output]")
    values = _to_client().open_by_key(sheet_id).worksheet(tab).get_all_values()
    if not values:
        return pd.DataFrame()
    df = pd.DataFrame(values[1:], columns=[str(c).strip().lower() for c in values[0]])
    return df


def _add_periods(df, col):
    """Add date / week (starts Sunday) / month columns from a date column."""
    df = df.copy()
    df["date"] = pd.to_datetime(df[col], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.normalize()
    df["week"] = df["date"] - pd.to_timedelta((df["date"].dt.weekday + 1) % 7, unit="D")
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


@st.cache_data(ttl=300, show_spinner=False)
def load_pr_output():
    raw = _to_read("PR_Summary")
    df = pd.DataFrame({
        "Matches": raw["matches"].map(_to_num),
        "Events Reviewed": raw["events_reviewed"].map(_to_num),
        "Collector Wrong": raw["collector_wrong"].map(_to_num),
        "Both Wrong": raw["both_wrong"].map(_to_num),
        "completion_date": raw["completion_date"].str.strip(),
    })
    return {"df": _add_periods(df, "completion_date"), "fetched_at": datetime.now()}


@st.cache_data(ttl=300, show_spinner=False)
def load_sofa_output():
    raw = _to_read("Sofa_Summary")
    df = pd.DataFrame({
        "Matches": raw["matches"].map(_to_num),
        "Events Reviewed": raw["events_reviewed"].map(_to_num),
        "SB Wrong": raw["sb_wrong"].map(_to_num),
        "Both Wrong": raw["both_wrong"].map(_to_num),
        "completion_date": raw["completion_date"].str.strip(),
    })
    return {"df": _add_periods(df, "completion_date"), "fetched_at": datetime.now()}


@st.cache_data(ttl=300, show_spinner=False)
def load_ws_output():
    raw = _to_read("WS_Summary")
    df = pd.DataFrame({
        "Competition": raw["competition"].str.strip().replace("", "Unknown"),
        "Event": raw["event"].str.strip().replace(_WS_EVENT_NAMES).replace("", "Unknown"),
        "Events Reviewed": raw["events_reviewed"].map(_to_num),
        "Missing": raw["missing"].map(_to_num),
        "Already Added": raw["already_added"].map(_to_num),
        "WS Wrong": raw["ws_wrong"].map(_to_num),
        "completion_date": raw["completion_date"].str.strip(),
    })
    return {"df": _add_periods(df, "completion_date"), "fetched_at": datetime.now()}


def _wk_label(ts):
    return f"{ts.strftime('%b %d')} – {(ts + pd.Timedelta(days=6)).strftime('%b %d')}"


def _mo_label(ts):
    return ts.strftime("%b %Y")


def _to_agg(df, by, metrics, match_col):
    g = df.groupby(by)
    out = g[metrics].sum()
    if match_col:   # daily rows already hold the match count → sum it
        out.insert(0, "Matches", g[match_col].sum())
    return out.sort_index()


# ═══════════════════════ Tools Output — executive report UI ═══════════════════════
_TO_COLORS = {
    "Matches": "#94A3B8", "Events Reviewed": "#3B82F6", "Correct": "#10B981",
    "Collector Wrong": "#F43F5E", "SB Wrong": "#F43F5E", "WS Wrong": "#F43F5E",
    "Both Wrong": "#F59E0B", "Missing": "#8B5CF6", "Already Added": "#14B8A6", "Other": "#475569",
}
_TO_CSS = """
<style>
.xr-hero{background:linear-gradient(135deg,#0f1b33 0%,#111827 55%,#0b1220 100%);
  border:1px solid #1e2a44;border-radius:20px;padding:26px 28px;margin:6px 0 18px;position:relative;overflow:hidden}
.xr-hero:after{content:"";position:absolute;right:-80px;top:-80px;width:260px;height:260px;border-radius:50%;
  background:radial-gradient(circle,rgba(59,130,246,.18),transparent 70%)}
.xr-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.xr-kicker{font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#60A5FA}
.xr-title{font-family:'DM Serif Display',serif;font-size:34px;line-height:1.1;color:#F8FAFC;margin:6px 0 4px}
.xr-sub{font-size:13px;color:#94A3B8}
.xr-period{background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.35);color:#BFDBFE;
  padding:6px 14px;border-radius:999px;font-size:13px;font-weight:600;white-space:nowrap}
.xr-body{display:grid;grid-template-columns:220px 1fr;gap:22px;margin-top:22px;align-items:center}
@media(max-width:900px){.xr-body{grid-template-columns:1fr}}
.xr-ring{display:flex;flex-direction:column;align-items:center;justify-content:center}
.xr-ring .cap{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#94A3B8;margin-top:8px;font-weight:700}
.xr-ring .dl{font-size:12px;margin-top:4px}
.xr-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.xr-kpi{background:rgba(15,23,42,.65);border:1px solid #1f2a40;border-radius:14px;padding:14px 16px 10px}
.xr-kpi .l{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:#94A3B8}
.xr-kpi .dot{width:8px;height:8px;border-radius:50%}
.xr-kpi .v{font-size:30px;font-weight:700;color:#F8FAFC;letter-spacing:-.02em;margin:6px 0 2px;
  font-variant-numeric:tabular-nums}
.xr-kpi .r{font-size:12px;color:#CBD5E1;min-height:16px}
.xr-kpi .row{display:flex;justify-content:space-between;align-items:flex-end;gap:6px;margin-top:6px}
.xr-chip{font-size:11px;font-weight:700;padding:3px 8px;border-radius:999px;white-space:nowrap}
.xr-good{background:rgba(16,185,129,.15);color:#34D399}.xr-bad{background:rgba(244,63,94,.15);color:#FB7185}
.xr-flat{background:#1e293b;color:#94A3B8}
.xr-ins{background:#0f172a;border:1px solid #1e293b;border-left:4px solid #3B82F6;border-radius:14px;
  padding:16px 20px;margin:0 0 20px}
.xr-ins h4{margin:0 0 8px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#60A5FA!important}
.xr-ins ul{margin:0;padding-left:18px}.xr-ins li{color:#E2E8F0!important;font-size:14px;line-height:1.7}
.xr-h{display:flex;align-items:baseline;gap:10px;margin:26px 0 10px}
.xr-h b{font-size:18px;color:#F8FAFC;font-weight:700}.xr-h span{font-size:12px;color:#64748B}
.xr-tbl{width:100%;border-collapse:separate;border-spacing:0;background:#0f172a;border:1px solid #1e293b;
  border-radius:14px;overflow:hidden;font-size:13px}
.xr-tbl th{background:#111c33!important;color:#94A3B8!important;font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;text-align:left;padding:10px 12px!important;border:none!important}
.xr-tbl td{padding:9px 12px!important;border:none!important;border-top:1px solid #1e293b!important;color:#E2E8F0!important;
  font-variant-numeric:tabular-nums}
.xr-bar{height:8px;border-radius:6px;background:#1e293b;overflow:hidden;display:flex;min-width:120px}
.xr-bar i{display:block;height:100%}
.xr-pct{font-weight:700}
</style>
"""


def _to_color(m):
    return _TO_COLORS.get(m, "#3B82F6")


def _to_spark(vals, color, w=120, h=34):
    vals = [float(v) for v in vals]
    if len(vals) < 2:
        return ""
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1
    pts = [(i * (w - 4) / (len(vals) - 1) + 2, h - 4 - (v - lo) / rng * (h - 8)) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"2,{h} " + line + f" {w - 2},{h}"
    lx, ly = pts[-1]
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<polygon points="{area}" fill="{color}" opacity=".14"/>'
            f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3" fill="{color}"/></svg>')


def _to_ring(pct, label, delta_html):
    pct = max(0.0, min(100.0, pct))
    r, c = 62, 2 * 3.14159 * 62
    color = "#10B981" if pct >= 97 else "#F59E0B" if pct >= 93 else "#F43F5E"
    return (f'<div class="xr-ring"><svg width="160" height="160" viewBox="0 0 160 160">'
            f'<circle cx="80" cy="80" r="{r}" stroke="#1e293b" stroke-width="12" fill="none"/>'
            f'<circle cx="80" cy="80" r="{r}" stroke="{color}" stroke-width="12" fill="none" '
            f'stroke-linecap="round" stroke-dasharray="{c * pct / 100:.1f} {c:.1f}" transform="rotate(-90 80 80)"/>'
            f'<text x="80" y="78" text-anchor="middle" fill="#F8FAFC" font-size="30" font-weight="700">{pct:.1f}%</text>'
            f'<text x="80" y="100" text-anchor="middle" fill="#94A3B8" font-size="11">of events correct</text></svg>'
            f'<div class="cap">{label}</div><div class="dl">{delta_html}</div></div>')


def _to_chip(d, is_err, fmt="{:+,}", unit=""):
    if d == 0 or d != d:
        return '<span class="xr-chip xr-flat">no change</span>'
    good = (d < 0) if is_err else (d > 0)
    arrow = "▲" if d > 0 else "▼"
    txt = fmt.format(abs(d)).lstrip("+")
    return f'<span class="xr-chip {"xr-good" if good else "xr-bad"}">{arrow} {txt}{unit}</span>'


def _to_style(chart, height):
    return (chart.properties(height=height, background="transparent")
            .configure_view(strokeWidth=0)
            .configure_axis(labelColor="#94A3B8", titleColor="#64748B", gridColor="#1e293b",
                            domain=False, ticks=False, labelFontSize=11, titleFontSize=11,
                            titleFontWeight="normal", labelPadding=6)
            .configure_legend(labelColor="#CBD5E1", labelFontSize=12, symbolType="circle",
                              orient="top", title=None, padding=0, offset=12, columnPadding=18))


def _to_trend(agg, cfg, fmt, height=340):
    """Volume bars (with labels) + error-rate lines (with % labels)."""
    base_m, errs = cfg["metrics"][0], cfg["errors"]
    a = agg.reset_index()
    a["Period"] = a[a.columns[0]].map(fmt)
    order = list(a["Period"])
    x = alt.X("Period:N", sort=order, title=None, axis=alt.Axis(labelAngle=0, labelLimit=150))
    bars = alt.Chart(a).mark_bar(color="#1d4ed8", opacity=.55, cornerRadiusTopLeft=6,
                                 cornerRadiusTopRight=6, size=34).encode(
        x=x, y=alt.Y(f"{base_m}:Q", title=base_m, axis=alt.Axis(format="~s", tickCount=4)),
        tooltip=["Period", alt.Tooltip(f"{base_m}:Q", format=",")])
    bar_lbl = bars.mark_text(dy=-8, color="#93C5FD", fontSize=11, fontWeight="bold").encode(
        text=alt.Text(f"{base_m}:Q", format=",.0f"))
    rate = a[["Period"] + errs].copy()
    for e in errs:
        rate[e] = (a[e] / a[base_m].where(a[base_m] != 0) * 100).round(2)
    rl = rate.melt(id_vars=["Period"], var_name="Rate", value_name="pct")
    rl["Rate"] = rl["Rate"] + " %"
    dom = [e + " %" for e in errs]
    col = alt.Color("Rate:N", sort=dom, scale=alt.Scale(domain=dom, range=[_to_color(e) for e in errs]))
    ry = alt.Y("pct:Q", title="Error rate (%)", axis=alt.Axis(orient="right", grid=False, format=".1f"))
    lines = alt.Chart(rl).mark_line(strokeWidth=2.6, point=alt.OverlayMarkDef(size=60, filled=True)).encode(
        x=x, y=ry, color=col, tooltip=["Period", "Rate", alt.Tooltip("pct:Q", format=".2f", title="%")])
    line_lbl = alt.Chart(rl).mark_text(dy=-12, fontSize=11, fontWeight="bold").encode(
        x=x, y=ry, color=alt.Color("Rate:N", sort=dom, legend=None,
                                   scale=alt.Scale(domain=dom, range=[_to_color(e) for e in errs])),
        text=alt.Text("pct:Q", format=".1f"))
    chart = alt.layer(bars + bar_lbl, lines + line_lbl).resolve_scale(y="independent", color="independent")
    st.altair_chart(_to_style(chart, height), use_container_width=True)


def _to_volume(agg, cfg, fmt, height=300):
    """Grouped bars of every metric, each bar labelled."""
    metrics = cfg["metrics"]
    a = agg.reset_index()
    a["Period"] = a[a.columns[0]].map(fmt)
    order = list(a["Period"])
    long = a.melt(id_vars=["Period"], value_vars=metrics, var_name="Metric", value_name="Count")
    enc = dict(x=alt.X("Period:N", sort=order, title=None, axis=alt.Axis(labelAngle=0, labelLimit=150)),
               xOffset=alt.XOffset("Metric:N", sort=metrics),
               y=alt.Y("Count:Q", title="Events", scale=alt.Scale(type="symlog"),
                       axis=alt.Axis(format="~s", tickCount=4)))
    color = alt.Color("Metric:N", sort=metrics,
                      scale=alt.Scale(domain=metrics, range=[_to_color(m) for m in metrics]))
    bars = alt.Chart(long).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        **enc, color=color, tooltip=["Period", "Metric", alt.Tooltip("Count:Q", format=",")])
    lbl = alt.Chart(long).mark_text(dy=-7, fontSize=10, color="#CBD5E1").encode(
        **enc, detail="Metric:N", text=alt.Text("Count:Q", format="~s"))
    st.altair_chart(_to_style(bars + lbl, height), use_container_width=True)


def _to_insights(agg, sel, cfg, unit):
    idx = list(agg.index)
    pos = idx.index(sel)
    if pos == 0:
        return []
    cur, prev = agg.loc[sel], agg.loc[idx[pos - 1]]
    base = cfg["metrics"][0]
    out = []
    if prev[base]:
        ch = (cur[base] - prev[base]) / prev[base] * 100
        out.append(f"<b>{base}</b> {'up' if ch >= 0 else 'down'} <b>{abs(ch):.1f}%</b> vs previous "
                   f"{unit} ({int(prev[base]):,} → {int(cur[base]):,}).")
    for e in cfg["errors"]:
        if cur[base] and prev[base]:
            r1, r0 = cur[e] / cur[base] * 100, prev[e] / prev[base] * 100
            d = r1 - r0
            word = "improved" if d < 0 else "worsened" if d > 0 else "held steady"
            out.append(f"<b>{e}</b> rate {word}: <b>{r1:.2f}%</b> ({d:+.2f} pts).")
    if "Matches" in cur and prev.get("Matches", 0):
        out.append(f"<b>{int(cur['Matches']):,}</b> matches reviewed "
                   f"({int(cur['Matches'] - prev['Matches']):+,} vs previous {unit}).")
    return out


def _to_hdr(title, note=""):
    st.markdown(f'<div class="xr-h"><b>{title}</b><span>{note}</span></div>', unsafe_allow_html=True)


def _render_tool_output(df, key, cfg):
    """Executive report: hero (score + KPIs + sparklines) → insights → trends → detail."""
    if df.empty:
        st.info("No reviewed data for this selection yet.")
        return
    metrics, errs, match = cfg["metrics"], cfg["errors"], cfg.get("match")
    match_col = "Matches" if match else None
    wk = _to_agg(df, "week", metrics, match_col)
    mo = _to_agg(df, "month", metrics, match_col)

    c1, c2, c3 = st.columns([1, 1.3, 2.2])
    gran = c1.radio("View by", ["Week", "Month"], horizontal=True, key=f"{key}_gran")
    agg, fmt, unit = (wk, _wk_label, "week") if gran == "Week" else (mo, _mo_label, "month")
    sel = c2.selectbox(gran, list(agg.index)[::-1], format_func=fmt, key=f"{key}_{gran}_sel")

    row = agg.loc[sel]
    idx = list(agg.index)
    pos = idx.index(sel)
    prev = agg.loc[idx[pos - 1]] if pos > 0 else None
    hist = agg.iloc[max(0, pos - 7):pos + 1]
    base = metrics[0]

    # ── Hero ──────────────────────────────────────────────
    kpis = []
    for m in (["Matches"] if match else []) + metrics:
        val = int(row[m])
        is_err = m in errs
        chip = _to_chip(val - int(prev[m]), is_err) if prev is not None else ""
        rate = (f"{val / row[base] * 100:.2f}% of reviewed" if is_err and row[base] else "&nbsp;")
        kpis.append(f'<div class="xr-kpi"><div class="l"><span class="dot" style="background:{_to_color(m)}"></span>{m}</div>'
                    f'<div class="v">{val:,}</div><div class="r">{rate}</div>'
                    f'<div class="row">{chip}{_to_spark(hist[m].tolist(), _to_color(m))}</div></div>')
    ring = ""
    if cfg.get("score") and row[base]:
        score = 100 - row[errs].sum() / row[base] * 100
        dl = ""
        if prev is not None and prev[base]:
            ps = 100 - prev[errs].sum() / prev[base] * 100
            dl = _to_chip(round(score - ps, 2), False, "{:+.2f}", " pts")
        ring = _to_ring(score, cfg["score"], dl)
    body_cls = "xr-body" if ring else "xr-body\" style=\"grid-template-columns:1fr"
    st.markdown(
        f'<div class="xr-hero"><div class="xr-top"><div><div class="xr-kicker">{cfg["kicker"]}</div>'
        f'<div class="xr-title">{cfg["title"]}</div><div class="xr-sub">{cfg["source"]}</div></div>'
        f'<div class="xr-period">{gran} · {fmt(sel)}</div></div>'
        f'<div class="{body_cls}">{ring}<div class="xr-kpis">{"".join(kpis)}</div></div></div>',
        unsafe_allow_html=True)

    ins = _to_insights(agg, sel, cfg, unit)
    if ins:
        st.markdown('<div class="xr-ins"><h4>Key insights</h4><ul>' +
                    "".join(f"<li>{i}</li>" for i in ins) + "</ul></div>", unsafe_allow_html=True)

    # ── Trends ────────────────────────────────────────────
    _to_hdr("Volume & error rate — weekly", "bars = events reviewed · lines = error rate %")
    weeks = list(wk.index)
    wk_view = wk
    if len(weeks) > 1:
        rng = st.select_slider("Weeks shown (default: last 6)", options=weeks,
                               value=(weeks[max(0, len(weeks) - _TO_WEEKS_DEFAULT)], weeks[-1]),
                               format_func=_wk_label, key=f"{key}_wrange")
        wk_view = wk.loc[rng[0]:rng[1]]
    _to_trend(wk_view, cfg, _wk_label)

    _to_hdr("Volume & error rate — monthly")
    _to_trend(mo, cfg, _mo_label)

    _to_hdr("Every metric — monthly", "log scale so small counts stay visible")
    _to_volume(mo, cfg, _mo_label)

    with st.expander("📋  Full numbers & rates"):
        t1, t2 = st.tabs(["Weekly", "Monthly"])
        for tab, a, f in ((t1, wk, _wk_label), (t2, mo, _mo_label)):
            with tab:
                t = a.copy()
                for e in errs:
                    t[f"{e} %"] = (t[e] / t[base].where(t[base] != 0) * 100).round(2)
                t.index = [f(i) for i in t.index]
                t.index.name = "Period"
                st.dataframe(t.iloc[::-1], use_container_width=True,
                             column_config={c: st.column_config.NumberColumn(format="%.2f%%")
                                            for c in t.columns if c.endswith("%")})


def _to_header_bar(loader, key, fetched_at):
    c1, c2 = st.columns([6, 1])
    c1.caption(f"Live from Google Sheets · weeks run Sunday → Saturday by collection completion "
               f"date · updated {fetched_at.strftime('%b %d, %I:%M %p')}")
    if c2.button("↻ Refresh", key=f"{key}_refresh", use_container_width=True):
        loader.clear()
        st.rerun()


def _to_load(loader, label):
    try:
        return loader()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Couldn't read the **{label}** tab. Make sure the script has run and the sheet "
                 "is shared with the service account's e-mail (Viewer).")
        st.caption(f"Technical detail: {exc}")
        return None


def _to_not_connected():
    if _to_configured():
        return False
    st.info("Tools Output isn't connected yet. Add the service account to Streamlit Secrets.")
    return True


_PR_CFG = dict(kicker="Tools Output · Collection quality", title="Player Review App",
               source="Player Review drive · Resolved folders",
               metrics=["Events Reviewed", "Collector Wrong", "Both Wrong"],
               errors=["Collector Wrong", "Both Wrong"], match=True, score="Collector accuracy")
_SOFA_CFG = dict(kicker="Tools Output · Data comparison", title="Sofascore",
                 source="Archive Data/Resolved + New Resolved",
                 metrics=["Events Reviewed", "SB Wrong", "Both Wrong"],
                 errors=["SB Wrong", "Both Wrong"], match=True, score="SB accuracy")
_WS_EVENT_NAMES = {"Pass": "through_ball", "TakeOn": "Dribble", "Take_On": "Dribble"}
_WS_METRICS = ["Events Reviewed", "Missing", "Already Added", "WS Wrong"]
_WS_CFG = dict(kicker="Tools Output · Validation", title="WhoScored Validation",
               source="WhoScored sheet · Through-balls (reviewed rows)",
               metrics=_WS_METRICS, errors=["Missing", "Already Added", "WS Wrong"], match=False)


@_auto_refresh
def render_pr_output():
    if _to_not_connected():
        return
    data = _to_load(load_pr_output, "PR_Summary")
    if data is None:
        return
    _to_header_bar(load_pr_output, "pr", data["fetched_at"])
    _render_tool_output(data["df"], "pr", _PR_CFG)


@_auto_refresh
def render_sofa_output():
    if _to_not_connected():
        return
    data = _to_load(load_sofa_output, "Sofa_Summary")
    if data is None:
        return
    _to_header_bar(load_sofa_output, "sofa", data["fetched_at"])
    _render_tool_output(data["df"], "sofa", _SOFA_CFG)


def _ws_rank_table(t, dim):
    """HTML ranking table with labelled composition bars."""
    res = _WS_METRICS[1:]
    rows = []
    for name, r in t.iterrows():
        tot = r["Events Reviewed"] or 1
        segs = "".join(f'<i style="width:{r[m] / tot * 100:.2f}%;background:{_to_color(m)}"></i>' for m in res)
        cells = "".join(f'<td><span class="xr-pct" style="color:{_to_color(m)}">{r[m] / tot * 100:.1f}%</span>'
                        f' <span style="color:#64748B">({int(r[m]):,})</span></td>' for m in res)
        rows.append(f"<tr><td><b>{name}</b></td><td>{int(r['Events Reviewed']):,}</td>{cells}"
                    f'<td><div class="xr-bar">{segs}</div></td></tr>')
    head = "".join(f"<th>{m}</th>" for m in res)
    st.markdown(f'<table class="xr-tbl"><tr><th>{dim}</th><th>Reviewed</th>{head}<th>Mix</th></tr>'
                f'{"".join(rows)}</table>', unsafe_allow_html=True)


def _ws_breakdown(df, dim, key):
    c1, c2, _sp = st.columns([1.3, 1.3, 1.6])
    scope = c1.radio("Period", ["Week", "Month", "All time"], horizontal=True, key=f"{key}_scope")
    sub, pill = df, "All time"
    if scope == "Week":
        opts = sorted(df["week"].unique(), reverse=True)
        sel = c2.selectbox("Week", opts, format_func=lambda t: _wk_label(pd.Timestamp(t)), key=f"{key}_bw")
        sub, pill = df[df["week"] == sel], _wk_label(pd.Timestamp(sel))
    elif scope == "Month":
        opts = sorted(df["month"].unique(), reverse=True)
        sel = c2.selectbox("Month", opts, format_func=lambda t: _mo_label(pd.Timestamp(t)), key=f"{key}_bm")
        sub, pill = df[df["month"] == sel], _mo_label(pd.Timestamp(sel))
    t = sub.groupby(dim)[_WS_METRICS].sum().sort_values("Events Reviewed", ascending=False)
    if t.empty:
        st.info("Nothing reviewed in this period.")
        return
    tot = t.sum()
    base_tot = tot["Events Reviewed"] or 1
    kpis = ""
    for m in _WS_METRICS:
        rate = "" if m == "Events Reviewed" else f"{tot[m] / base_tot * 100:.2f}% of reviewed"
        kpis += (f'<div class="xr-kpi"><div class="l"><span class="dot" style="background:{_to_color(m)}">'
                 f'</span>{m}</div><div class="v">{int(tot[m]):,}</div><div class="r">{rate}</div></div>')
    st.markdown(f'<div class="xr-hero"><div class="xr-top"><div><div class="xr-kicker">WhoScored · comparison</div>'
                f'<div class="xr-title">By {dim.lower()}</div><div class="xr-sub">{len(t)} {dim.lower()}s reviewed'
                f'</div></div><div class="xr-period">{pill}</div></div>'
                f'<div class="xr-body" style="grid-template-columns:1fr"><div class="xr-kpis">{kpis}</div></div></div>',
                unsafe_allow_html=True)

    _to_hdr(f"Result mix by {dim.lower()}", "share of reviewed events · labels show %")
    res = _WS_METRICS[1:]
    p = t[res].div(t["Events Reviewed"].where(t["Events Reviewed"] != 0), axis=0).mul(100).round(1)
    long = p.reset_index().melt(id_vars=[dim], var_name="Result", value_name="pct")
    y = alt.Y(f"{dim}:N", sort=list(t.index), title=None, axis=alt.Axis(labelLimit=240))
    color = alt.Color("Result:N", sort=res, scale=alt.Scale(domain=res, range=[_to_color(m) for m in res]))
    bars = alt.Chart(long).mark_bar(height=20).encode(
        y=y, x=alt.X("pct:Q", stack="zero", title="% of reviewed", scale=alt.Scale(domain=[0, 100])),
        color=color, order=alt.Order("Result:N"),
        tooltip=[dim, "Result", alt.Tooltip("pct:Q", format=".1f", title="%")])
    lbl = alt.Chart(long).transform_filter("datum.pct >= 6").mark_text(
        color="#0b1220", fontSize=11, fontWeight="bold", dx=-4, align="right").encode(
        y=y, x=alt.X("pct:Q", stack="zero"), order=alt.Order("Result:N"),
        detail="Result:N", text=alt.Text("pct:Q", format=".0f"))
    st.altair_chart(_to_style(bars + lbl, max(200, 34 * len(t))), use_container_width=True)

    _to_hdr("Ranking", "sorted by events reviewed")
    _ws_rank_table(t, dim)


@_auto_refresh
def render_ws_output():
    if _to_not_connected():
        return
    data = _to_load(load_ws_output, "WS_Summary")
    if data is None:
        return
    df = data["df"]
    _to_header_bar(load_ws_output, "ws", data["fetched_at"])
    t1, t2, t3 = st.tabs(["Overview", "By Event", "By Competition"])
    with t1:
        _render_tool_output(df, "ws_all", _WS_CFG)
    with t2:
        ev = st.selectbox("Event", ["All events (compare)"] + sorted(df["Event"].unique()), key="ws_ev")
        if ev.startswith("All events"):
            _ws_breakdown(df, "Event", "ws_evb")
        else:
            _render_tool_output(df[df["Event"] == ev], f"ws_ev_{ev}",
                                dict(_WS_CFG, title=f"WhoScored · {ev}"))
    with t3:
        comp = st.selectbox("Competition", ["All competitions (compare)"] + sorted(df["Competition"].unique()),
                            key="ws_comp")
        if comp.startswith("All competitions"):
            _ws_breakdown(df, "Competition", "ws_cb")
        else:
            _render_tool_output(df[df["Competition"] == comp], f"ws_c_{comp}",
                                dict(_WS_CFG, title=f"WhoScored · {comp}"))


# ── Page Router ───────────────────────────────────────────────────────────────
page = st.session_state.page

# ── Page: Overview (main landing page) ────────────────────────────────────────
if page == "Overview":
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Internal Portal</div>
        <h1 class="hero-title">SB Soccer Offline Quality Team</h1>
        <p class="hero-desc">
            Welcome to the central hub for the SB Soccer Offline Quality Team. This portal is
            designed to streamline our workflows, housing all official Processes, documentation,
            and Match Progress trackers in one accessible location.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Page: A Review (standalone header + native Streamlit components) ──────────
elif page == "A Review":
    render_page_header(
        "Review Process",
        "A Review Process",
        "Reviewing match facts to deliver data to the customer with zero errors.",
    )

    st.info(
        "This process is applied to **100% of the matches** collected during the "
        "Collection phase. Its primary purpose is to review match facts, ensuring that "
        "data is delivered to the customer with **zero errors** regarding these specific events."
    )

    st.subheader("Match Distribution Priority")
    st.markdown(
        "Matches are distributed based on priority. **Customer** matches are assigned first, "
        "followed by **Opponent**, **Trial**, and **Academy** ad hoc games. After that, "
        "lower-priority matches are handled (P1, P2, and other priority levels)."
    )

    st.subheader("Events Reviewed")
    st.markdown("The following events are meticulously reviewed in this process:")
    st.markdown(
        """
- Starting XI (formation, starting players, and bench)
- Tactical shifts
- Goals
- Assists
- Cards
- Substitutions
- Fouls (including offsides)
- Free kicks
- Corner kicks and the subsequent event
- Errors
- Freeze frame shots
- Pressures before shots
- Player on/off
- Injury stoppages
"""
    )
    st.markdown(
        "> **Note:** For all the above, the event details, player, location, and "
        "event extras are reviewed."
    )

    st.subheader("Freeze Frame Shots (Specific Review)")
    st.markdown("For freeze frame shots specifically, the following elements are reviewed:")
    st.markdown(
        """
- Shooter
- Blocker
- Goalkeeper extras
- Goal location
- Player positions in the frame
- Shot impact
"""
    )

    st.subheader("Quality & Performance Tracking")
    st.success(
        "All corrections and updates are displayed in a **dashboard** to evaluate each "
        "collector's performance and generate a **quality score** for each collector per match."
    )

# ── Page: Hypercare Review (standalone header + native Streamlit components) ──
elif page == "Hypercare Review":
    render_page_header(
        "Review Process",
        "Hypercare Review Process",
        "Heightened scrutiny for customers requiring additional attention.",
    )

    st.markdown(
        "This specialized review type is applied to matches involving customers who have "
        "previously experienced issues, thereby requiring **additional attention for a "
        "designated period**. A dynamic list of prioritized teams is strictly maintained and "
        "updated based on current circumstances."
    )

    st.subheader("How Teams Are Added")
    st.markdown(
        """
- **Internal Decisions:** Based on quality monitoring and internal team evaluations.
- **Customer Requests:** Direct requests from the clients to ensure heightened scrutiny.
"""
    )

    st.subheader("Review Scope")
    st.markdown("_Varies based on customer requirements:_")
    st.markdown(
        """
- **Full Match Review:** Reviewing the entire 90-minute match data.
- **Player-Specific Review:** Auditing all data related to a single, specific player.
- **Pressure Events Audit:** Reviewing Pressure events to identify, correct, or add missing instances.
- **Zero-Post-Edit Matches:** Reviewing matches for customers who strictly require zero modifications after the initial collection process is finalized.
"""
    )

    st.warning(
        "**Resource Allocation Note:** Only the most experienced collectors and reviewers are "
        "assigned to Hypercare matches to guarantee the highest possible data quality and precision."
    )

# ── Page: Player Review (standalone header + native Streamlit components) ─────
elif page == "Player Review":
    render_page_header(
        "Review Process",
        "Player Review App",
        "Compare collector work vs reviewer work, then correct the data.",
    )

    st.info(
        "The **Player Review App** compares the collector's work with the reviewer's work. "
        "The reviewer tags the players, the two datasets are compared to identify which side "
        "is correct and which is incorrect, and the data is then corrected in the application."
    )

    st.subheader("Process Steps")

    st.markdown("**1. CSV Download**")
    st.markdown(
        "The reviewer receives a CSV file through the website "
        "[http://195.7.4.251:5015/](http://195.7.4.251:5015/). "
        "The reviewer enters the **Match ID** and downloads the CSV file."
    )

    st.markdown("**2. CSV Import and Player Tagging**")
    st.markdown(
        "The CSV contains the match data. However, when the reviewer imports the CSV into the "
        "application, the data appears **without player IDs**. The reviewer then adds the players "
        "to the events."
    )

    st.markdown("**3. Finish Match and Upload**")
    st.markdown(
        "Once the reviewer completes the tagging, they click **Finish Match**. The file is then "
        "uploaded to **Google Drive**."
    )

    st.markdown("**4. Data Comparison**")
    st.markdown(
        "The next stage compares the collector's data with the reviewer's data. "
        "The comparison includes four possible actions:"
    )
    st.markdown(
        """
- Collector Right
- Collector Wrong
- Both Are Wrong
- Off-Camera
"""
    )

    st.markdown("**5. Data Correction**")
    st.markdown(
        "Once the reviewer completes the comparison, they correct the data in the "
        "**production application**."
    )

    st.subheader("Next Development Phase")
    st.success(
        "The next phase is to enable corrections directly through a **product tool** added to the "
        "application. This will allow the fixing process to be performed by importing the CSV into "
        "the application, **without the current manual correction process**."
    )

# ── Page: Sofascore Comparison Tool (standalone header + native components) ───
elif page == "Sofascore Comparison Tool":
    render_page_header(
        "Review Process",
        "Sofascore Comparison Tool",
        "An extra QA layer that flags discrepancies between Sofascore and our data.",
    )

    st.info(
        "The **Sofascore Comparison Tool** compares Sofascore event data against our internal "
        "data to surface discrepancies. It acts as an **additional quality-assurance layer** in "
        "the daily review of completed matches, helping validate accuracy and confirm no "
        "important events were missed."
    )

    st.subheader("How the Tool Works")
    st.markdown("Every event is compared and sorted into one of two groups:")

    c1, c2 = st.columns(2)
    with c1:
        st.success(
            "**✅ Matched Events**\n\n"
            "Exist in **both** Sofascore and our data — confirms the event was collected and "
            "recorded correctly."
        )
    with c2:
        st.warning(
            "**⚠️ Unmatched Events**\n\n"
            "Exist in **one** dataset only. Every unmatched event is reviewed manually to decide "
            "if it was missed, recorded incorrectly, or differs due to provider methodology."
        )
    st.markdown(
        "> When the review confirms our data is wrong, corrections are applied so the database "
        "stays accurate and complete."
    )

    st.subheader("Daily Quality Assurance Process")
    st.markdown(
        "Run as part of the daily QA workflow on the day's processed matches, the tool verifies:"
    )
    st.markdown(
        """
- No important events were missed.
- All collected events were recorded accurately.
- Any discrepancies are caught and resolved as early as possible.
"""
    )

    st.subheader("League Coverage")
    st.markdown("Sofascore availability varies by competition, giving three coverage tiers:")
    cov1, cov2, cov3 = st.columns(3)
    cov1.metric("Full A Review", "All events")
    cov2.metric("Facts-Only", "Fact events")
    cov3.metric("No Data", "No comparison")
    st.caption(
        "Full A Review = complete comparison. Facts-Only = limited to fact events. "
        "No Data = no Sofascore data, so the tool cannot compare."
    )

    st.subheader("Benefits")
    st.markdown(
        """
- Daily validation of completed matches.
- Early detection of missing or incorrect events.
- Improved overall data accuracy.
- Faster identification and correction of discrepancies.
- Higher confidence in data quality and completeness.
"""
    )

    st.subheader("Expected Outcome")
    st.success(
        "Built into the daily review, the tool lets the team continuously monitor data quality, "
        "quickly spot discrepancies, and keep the database as accurate and complete as possible — "
        "strengthening the QA workflow and keeping data standards consistent across all matches."
    )

# ── Page: Automated Match Extraction (Distribution Processes) ─────────────────
elif page == "Automated Match Extraction":
    render_page_header(
        "Distribution Process",
        "Automated Match Extraction Process",
        "From manual tracking to a fully automated bot solution.",
    )

    st.markdown(
        "This document explains the evolution of our match distribution workflow, highlighting "
        "the transition from a manual tracking method to a **fully automated bot solution**."
    )

    # -- Side-by-side comparison: old vs new --
    col1, col2 = st.columns(2)

    with col1:
        st.error("**Previous Manual Process**")
        st.markdown(
            """
- Received a Tableau email every 15 minutes with PDF attachments of completed matches.
- Team Leaders manually opened emails and reviewed PDFs.
- Extracted Match IDs manually and added them to the tracking sheet.
- Manually checked for duplicate entries to avoid errors.
- **Time Consumption:** Required 3–5 minutes every 15 minutes, creating a continuous manual workload throughout the entire shift.
"""
        )

    with col2:
        st.success("**Current Automated Process**")
        st.markdown(
            """
- An automated bot accesses the Tableau email every 15 minutes.
- Downloads, reads PDFs, and extracts Match IDs automatically.
- Adds matches directly to the tracking sheet.
- Automatically handles duplicate checks before adding any match.
- Records the exact date and timestamp for each added match.
"""
        )

    # -- Team Leader responsibility (below the columns) --
    st.info(
        "**Current Team Leader Responsibility:** No continuous manual work is required. "
        "At the end of each shift, the Team Leader only performs a quick **5-minute validation "
        "check** against Tableau to ensure no completed matches were missed by the bot."
    )

    # -- Improvement summary (bottom) --
    st.subheader("Key Improvements")
    st.markdown(
        """
- Significant reduction in manual workload and elimination of repetitive tasks.
- Reduced risk of duplicate entries.
- Faster and more consistent match distribution updates.
- Better tracking through automated timestamps.
"""
    )

    st.subheader("Time Efficiency Comparison")
    st.markdown(
        """
| Process | Manual Effort |
| --- | --- |
| Previous Process | 3–5 minutes every 15 minutes |
| Current Process | ~5 minutes every 8-hour shift |
"""
    )

# ── Page: Automated Match Distribution (Distribution Processes) ───────────────
elif page == "Automated Match Distribution":
    render_page_header(
        "Distribution Process",
        "Automated Match Distribution Process",
        "From a communication-heavy workflow to a streamlined, automated system.",
    )

    st.markdown(
        "This document explains the transition from a manual, communication-heavy match "
        "distribution process to a streamlined, automated system utilizing **Google Forms "
        "and bots**."
    )

    # -- Side-by-side comparison: old vs new --
    col1, col2 = st.columns(2)

    with col1:
        st.error("**Previous Manual Process**")
        st.markdown(
            """
- Reviewers contacted the Team Leader via WhatsApp to request a match.
- Team Leader manually checked the distribution sheet and prioritized matches (Customer > Opponent > Trial > Academy > P1/P2/Other).
- Manually assigned the appropriate match to the reviewer.
- **Challenges:** Continuous WhatsApp interruptions, distractions for Team Leaders, and distribution speed relied entirely on TL availability.
- **Time Consumption:** Up to 5 minutes per request.
"""
        )

    with col2:
        st.success("**Current Automated Process**")
        st.markdown(
            """
- Reviewer submits a request via Google Form using their HR code.
- The bot reads the HR code, checks the sheet, and auto-assigns based on strict priority logic (Customer > Opponent > Trial > Academy > P1/P2/Other). **Tie-breaker:** First added to the sheet.
- The match is automatically added to the reviewer's sheet with an exact date/time stamp.
- The form tracking sheet is automatically updated to confirm distribution.
- **Time Consumption:** Less than 1 minute with minimal TL involvement.
"""
        )

    # -- Exceptions & scenarios (below the columns) --
    st.warning(
        "**Excluded Matches (Manual Assignment):** Hypercare matches and high-priority games "
        "requiring top-tier reviewers are intentionally excluded from the bot and are still "
        "distributed manually by Team Leaders."
    )
    st.info(
        "**No Match Scenario:** If the distribution sheet is empty, the bot updates the form "
        "response to indicate no matches are available. The reviewer then contacts the TL for "
        "alternative tasks."
    )

    # -- Improvement summary --
    st.subheader("Key Improvements")
    st.markdown(
        """
- Significant reduction in communication overhead and TL distractions.
- Faster match assignment and consistent prioritization logic.
- Automated tracking for distribution history and timestamps.
"""
    )

    st.subheader("Time Efficiency Comparison")
    st.markdown(
        """
| Process | Manual Effort |
| --- | --- |
| Previous Process | Up to 5 minutes + continuous communication |
| Current Process | < 1 minute (Zero TL involvement) |
"""
    )

    # -- Future improvements --
    with st.expander("🚀  Future Improvements (Next Phase)", expanded=False):
        st.markdown(
            """
- Automating the distribution of Hypercare and high-priority matches using advanced conditions.
- Enhancing assignment logic based on individual reviewer performance and qualification metrics.
"""
        )

    # -- Code update log + simple, non-technical summary --
    st.subheader("Code Updated — 9 June 2026")
    st.markdown("**Simple Summary**")
    st.markdown("In plain terms, here is exactly what happens when a reviewer submits a request:")
    st.markdown(
        """
1. **The reviewer submits the form.** They enter their HR code and send the request — no need to message the Team Leader anymore.
2. **The system identifies them.** It looks up the HR code to confirm who the reviewer is and whether they are on the Live team or an Offline team.
3. **It checks their shift time.** The request is compared against the reviewer's scheduled shift:
   - **Too early?** If they ask before their shift is allowed to start, they receive an "Early Start" message telling them the exact time they may begin. No match is given yet.
   - **On time?** If they are within their shift window, the request proceeds normally.
   - **Late finish?** If they ask well after their shift has ended, they still get served, but the request is marked with the amount of delay for tracking.
4. **It finds work by priority.** The system goes through the task types in order of importance and gives the reviewer the first available match. If two matches are equally important, the one that has been waiting longest is assigned first.
5. **If the top option is empty, it keeps looking.** When the highest-priority task has nothing available, the system moves down the list until it finds work. Once something is assigned, the remaining lower-priority options are simply noted as already handled.
6. **If nothing is available anywhere,** the reviewer is told there are no matches to distribute, and the Team Leader is notified so they can provide another task.
7. **Some matches stay manual.** Hypercare and other high-priority games are deliberately left out of the automatic process and are still assigned by Team Leaders.
8. **Requests are handled one at a time.** If several people submit at the same moment, the requests line up and are processed in order, so nothing is lost and no match is given to two people.
"""
    )

# ── Page: Team Productivity (live dashboard) ──────────────────────────────────
elif page == "Team Productivity":
    render_page_header(
        "Performance",
        "Team Productivity",
        "Live collection performance, read straight from the Scorecard tab in Google "
        "Sheets. Refreshes automatically every 5 minutes.",
    )
    render_team_productivity()

# ── Page: Customer Complaints (live dashboard) ────────────────────────────────
elif page == "Customer Complaints":
    render_page_header(
        "Quality",
        "Customer Complaints",
        "Live analysis of customer complaints, read straight from the Complaints sheet "
        "in Google Sheets. Refreshes automatically every 5 minutes.",
    )
    render_customer_complaints()

# ── Page: Quality Score (live dashboard) ──────────────────────────────────────
elif page == "Quality Score":
    render_page_header(
        "Quality",
        "Quality Score",
        "Live collector quality scores by module, read straight from the Quality Score "
        "Dashboard in Google Sheets. Refreshes automatically every 5 minutes.",
    )
    render_quality_score()

# ── Page: Tools Output (live dashboards for the review tools) ─────────────────
elif page == "Tools Output":
    st.markdown(_TO_CSS, unsafe_allow_html=True)
    render_page_header(
        "Executive report",
        "Tools Output",
        "Quality results from the Player Review App, Sofascore comparison and WhoScored "
        "validation — live, refreshed every 5 minutes.",
    )
    _pr_tab, _sofa_tab, _ws_tab = st.tabs(["Player Review App", "Sofascore", "WhoScored Validation"])
    with _pr_tab:
        render_pr_output()
    with _sofa_tab:
        render_sofa_output()
    with _ws_tab:
        render_ws_output()
