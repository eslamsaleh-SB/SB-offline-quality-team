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

    st.button("🎯  Quality Score", key="nav_quality_score",
              use_container_width=True, on_click=go_to, args=("Quality Score",))

    st.button("🧰  Tools Output", key="nav_tools_output",
              use_container_width=True, on_click=go_to, args=("Tools Output",))

    # -- "Review Processes" dropdown --
    with st.expander("🔍  Review Processes", expanded=True):
        st.button("A Review", key="nav_a_review",
                  use_container_width=True, on_click=go_to, args=("A Review",))
        st.button("Hypercare Review", key="nav_hypercare_review",
                  use_container_width=True, on_click=go_to, args=("Hypercare Review",))
        st.button("Player Review", key="nav_player_review",
                  use_container_width=True, on_click=go_to, args=("Player Review",))
        st.button("Sofascore Comparison Tool", key="nav_sofascore",
                  use_container_width=True, on_click=go_to, args=("Sofascore Comparison Tool",))

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


def _to_cards(title, agg, sel, cols, base):
    """One row of KPI cards for the selected period, with delta vs the previous one."""
    st.markdown(f"##### {title}")
    idx = list(agg.index)
    row = agg.loc[sel]
    prev = agg.loc[idx[idx.index(sel) - 1]] if idx.index(sel) > 0 else None
    boxes = st.columns(len(cols))
    for box, c in zip(boxes, cols):
        val = int(row[c])
        delta = None if prev is None else f"{val - int(prev[c]):+,}"
        is_err = c not in ("Matches", base)
        with box:
            st.metric(c, f"{val:,}", delta=delta,
                      delta_color="inverse" if is_err else "normal")
            if is_err and row[base]:
                st.caption(f"{val / row[base] * 100:.2f}% of reviewed")


def _to_chart(agg, metrics, match_col, fmt, height=300):
    a = agg.reset_index()
    pcol = a.columns[0]
    a["label"] = a[pcol].map(fmt)
    order = list(a["label"])
    long = a.melt(id_vars=["label"], value_vars=metrics, var_name="Metric", value_name="Count")
    bars = alt.Chart(long).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("label:N", sort=order, title=None, axis=alt.Axis(labelAngle=0, labelLimit=160)),
        xOffset=alt.XOffset("Metric:N", sort=metrics),
        y=alt.Y("Count:Q", title="Events", axis=alt.Axis(format="d")),
        color=alt.Color("Metric:N", scale=alt.Scale(domain=metrics, range=_CAT_COLORS[:len(metrics)]),
                        legend=alt.Legend(title=None, orient="top")),
        tooltip=[alt.Tooltip("label:N", title="Period"), "Metric",
                 alt.Tooltip("Count:Q", format=",")])
    chart = bars
    if match_col:
        line = alt.Chart(a).mark_line(point=True, color="#fafafa", strokeDash=[4, 3]).encode(
            x=alt.X("label:N", sort=order),
            y=alt.Y("Matches:Q", title="Matches (dashed)", axis=alt.Axis(format="d", orient="right")),
            tooltip=[alt.Tooltip("label:N", title="Period"), alt.Tooltip("Matches:Q", format=",")])
        chart = alt.layer(bars, line).resolve_scale(y="independent")
    st.altair_chart(chart.properties(height=height), use_container_width=True)


def _to_rates_table(agg, metrics, fmt):
    base = metrics[0]
    t = agg.copy()
    for m in metrics[1:]:
        t[f"{m} %"] = (t[m] / t[base].where(t[base] != 0) * 100).round(2)
    t.index = [fmt(i) for i in t.index]
    t = t.iloc[::-1]
    st.dataframe(t, use_container_width=True)


def _render_tool_output(df, key, metrics, match_col=None):
    """Cards (week + month), weekly chart with week-range filter, monthly chart."""
    if df.empty:
        st.info("No reviewed data for this selection yet.")
        return
    cols = (["Matches"] if match_col else []) + metrics
    wk = _to_agg(df, "week", metrics, match_col)
    mo = _to_agg(df, "month", metrics, match_col)

    c1, c2 = st.columns(2)
    weeks_desc = list(wk.index)[::-1]
    months_desc = list(mo.index)[::-1]
    sel_w = c1.selectbox("Week (Sun – Sat)", weeks_desc, format_func=_wk_label, key=f"{key}_wsel")
    sel_m = c2.selectbox("Month", months_desc, format_func=_mo_label, key=f"{key}_msel")

    _to_cards(f"Week · {_wk_label(sel_w)}", wk, sel_w, cols, metrics[0])
    _to_cards(f"Month · {_mo_label(sel_m)}", mo, sel_m, cols, metrics[0])
    st.divider()

    st.markdown("##### Weekly trend")
    weeks = list(wk.index)
    if len(weeks) > 1:
        start_default = weeks[max(0, len(weeks) - _TO_WEEKS_DEFAULT)]
        rng = st.select_slider("Weeks shown (default: last 6)", options=weeks,
                               value=(start_default, weeks[-1]), format_func=_wk_label,
                               key=f"{key}_wrange")
        wk_view = wk.loc[rng[0]:rng[1]]
    else:
        wk_view = wk
    _to_chart(wk_view, metrics, match_col, _wk_label)

    st.markdown("##### Monthly trend")
    _to_chart(mo, metrics, match_col, _mo_label)

    with st.expander("Numbers & rates"):
        st.markdown("**Weekly**")
        _to_rates_table(wk, metrics, _wk_label)
        st.markdown("**Monthly**")
        _to_rates_table(mo, metrics, _mo_label)


def _to_refresh(key, loader):
    if st.button("🔄 Refresh", key=f"{key}_refresh"):
        loader.clear()


def _to_load(loader, label):
    try:
        return loader()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Couldn't read the **{label}** tab. Make sure the script has run and the sheet "
                 "is shared with the service account's e-mail (Viewer).")
        st.caption(f"Technical detail: {exc}")
        return None


@_auto_refresh
def render_pr_output():
    if not _to_configured():
        st.info("Tools Output isn't connected yet. Add the service account and sheet IDs to "
                "`.streamlit/secrets.toml` (see `apps_script/README.md`).")
        return
    _to_refresh("pr", load_pr_output)
    data = _to_load(load_pr_output, "PR_Summary")
    if data is None:
        return
    st.caption(f"Source: Player Review drive (Resolved folders) · week = collection completion date · "
               f"updated {data['fetched_at'].strftime('%b %d, %I:%M %p')}")
    _render_tool_output(data["df"], "pr", ["Events Reviewed", "Collector Wrong", "Both Wrong"],
                        match_col="Matches")


@_auto_refresh
def render_sofa_output():
    if not _to_configured():
        st.info("Tools Output isn't connected yet. Add the service account and sheet IDs to "
                "`.streamlit/secrets.toml` (see `apps_script/README.md`).")
        return
    _to_refresh("sofa", load_sofa_output)
    data = _to_load(load_sofa_output, "Sofa_Summary")
    if data is None:
        return
    st.caption(f"Source: resolved batches (Archive/Resolved + New Resolved) · week = "
               f"collection completion date · updated {data['fetched_at'].strftime('%b %d, %I:%M %p')}")
    _render_tool_output(data["df"], "sofa", ["Events Reviewed", "SB Wrong", "Both Wrong"],
                        match_col="Matches")


_WS_EVENT_NAMES = {"Pass": "through_ball", "TakeOn": "Dribble", "Take_On": "Dribble"}
_WS_METRICS = ["Events Reviewed", "Missing", "Already Added", "WS Wrong"]


def _ws_breakdown(df, dim, key):
    """Table + stacked bar of a dimension (Event / Competition) for a chosen period."""
    c1, c2 = st.columns([1, 2])
    scope = c1.radio("Period", ["Week", "Month", "All time"], horizontal=True, key=f"{key}_scope")
    sub = df
    if scope == "Week":
        opts = sorted(df["week"].unique(), reverse=True)
        sel = c2.selectbox("Week", opts, format_func=lambda t: _wk_label(pd.Timestamp(t)),
                           key=f"{key}_bw")
        sub = df[df["week"] == sel]
    elif scope == "Month":
        opts = sorted(df["month"].unique(), reverse=True)
        sel = c2.selectbox("Month", opts, format_func=lambda t: _mo_label(pd.Timestamp(t)),
                           key=f"{key}_bm")
        sub = df[df["month"] == sel]
    t = sub.groupby(dim)[_WS_METRICS].sum().sort_values("Events Reviewed", ascending=False)
    if t.empty:
        st.info("Nothing reviewed in this period.")
        return
    long = t[_WS_METRICS[1:]].reset_index().melt(id_vars=[dim], var_name="Result", value_name="Events")
    st.altair_chart(
        alt.Chart(long).mark_bar().encode(
            y=alt.Y(f"{dim}:N", sort=list(t.index), title=None, axis=alt.Axis(labelLimit=260)),
            x=alt.X("Events:Q", stack="zero", axis=alt.Axis(format="d")),
            color=alt.Color("Result:N", scale=alt.Scale(domain=_WS_METRICS[1:],
                                                        range=_CAT_COLORS[1:4]),
                            legend=alt.Legend(title=None, orient="top")),
            tooltip=[dim, "Result", alt.Tooltip("Events:Q", format=",")])
        .properties(height=max(180, 30 * len(t))),
        use_container_width=True,
    )
    out = t.copy()
    for m in _WS_METRICS[1:]:
        out[f"{m} %"] = (out[m] / out["Events Reviewed"] * 100).round(2)
    st.dataframe(out, use_container_width=True)


@_auto_refresh
def render_ws_output():
    if not _to_configured():
        st.info("Tools Output isn't connected yet. Add the service account and sheet IDs to "
                "`.streamlit/secrets.toml` (see `apps_script/README.md`).")
        return
    _to_refresh("ws", load_ws_output)
    data = _to_load(load_ws_output, "WS_Summary")
    if data is None:
        return
    df = data["df"]
    st.caption(f"Source: WhoScored sheet (Through-balls, reviewed rows) · week = "
               f"collection completion date · updated {data['fetched_at'].strftime('%b %d, %I:%M %p')}")
    t1, t2, t3 = st.tabs(["Overview", "By Event", "By Competition"])
    with t1:
        _render_tool_output(df, "ws_all", _WS_METRICS)
    with t2:
        ev = st.selectbox("Event", ["All events"] + sorted(df["Event"].unique()), key="ws_ev")
        if ev == "All events":
            _ws_breakdown(df, "Event", "ws_evb")
        else:
            _render_tool_output(df[df["Event"] == ev], f"ws_ev_{ev}", _WS_METRICS)
    with t3:
        comp = st.selectbox("Competition", ["All competitions"] + sorted(df["Competition"].unique()),
                            key="ws_comp")
        if comp == "All competitions":
            _ws_breakdown(df, "Competition", "ws_cb")
        else:
            _render_tool_output(df[df["Competition"] == comp], f"ws_c_{comp}", _WS_METRICS)


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
    render_page_header(
        "Tools",
        "Tools Output",
        "Review output from the Player Review App, the Sofascore comparison tool and "
        "WhoScored validation. Weeks run Sunday to Saturday. Refreshes every 5 minutes.",
    )
    _pr_tab, _sofa_tab, _ws_tab = st.tabs(["Player Review App", "Sofascore", "WhoScored Validation"])
    with _pr_tab:
        render_pr_output()
    with _sofa_tab:
        render_sofa_output()
    with _ws_tab:
        render_ws_output()
