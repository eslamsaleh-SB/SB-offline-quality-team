import os
import re
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

# ── Navigation state ──────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Overview"


def go_to(page_name):
    st.session_state.page = page_name

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
              use_container_width=True, on_click=go_to, args=("Overview",))

    # -- Team Productivity (live dashboard — top-level item) --
    st.button("📊  Team Productivity", key="nav_team_productivity",
              use_container_width=True, on_click=go_to, args=("Team Productivity",))

    # -- Customer Complaints (live dashboard — top-level item) --
    st.button("🗒️  Customer Complaints", key="nav_customer_complaints",
              use_container_width=True, on_click=go_to, args=("Customer Complaints",))

    # -- "Review Processes" dropdown --
    with st.expander("🔍  Review Processes", expanded=True):
        st.button("A Review", key="nav_a_review",
                  use_container_width=True, on_click=go_to, args=("A Review",))
        st.button("Hypercare Review", key="nav_hypercare_review",
                  use_container_width=True, on_click=go_to, args=("Hypercare Review",))

    # -- "Distribution Processes" dropdown --
    with st.expander("📦  Distribution Processes", expanded=True):
        st.button("Automated Match Extraction", key="nav_auto_extraction",
                  use_container_width=True, on_click=go_to, args=("Automated Match Extraction",))
        st.button("Automated Match Distribution", key="nav_auto_distribution",
                  use_container_width=True, on_click=go_to, args=("Automated Match Distribution",))

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
                        st.markdown(
                            f"**{mo['name']} {mo['year']}** &nbsp;"
                            f"<span style='color:#68A4C4;font-size:.8rem'>{len(mo['weeks'])} weeks</span>",
                            unsafe_allow_html=True,
                        )
                        st.metric("Total monthly collections", f"{int(mo['total']):,}")
                        if mo["total"] > 0:
                            wdf = pd.DataFrame([{"date": w["date"],
                                                 "week": w["date"].strftime("%d %b"),
                                                 "matches": w["total"]} for w in mo["weeks"]])
                            st.altair_chart(
                                alt.Chart(wdf).mark_bar(color="#68A4C4")
                                .encode(x=alt.X("date:T", title=None,
                                                axis=alt.Axis(format="%d", labelFontSize=9)),
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
