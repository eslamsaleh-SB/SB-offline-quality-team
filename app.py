import os
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
/* ---- Sidebar expander ("Review Processes" dropdown) ---- */
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
    max-width: 1100px;
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

# ── Google Sheet data source ──────────────────────────────────────────────────
# CSV export of the 'Importrange' tab.
SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1LrQa1PBQEykOrCt7CaYBT-BrJvfJaU7pRTdyQgzqUE0/export?format=csv&gid=1474561682"
)

# Columns to keep (zero-indexed). Maps Google Sheet columns
# A, B, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, U, V.
MATCH_PROGRESS_COLUMNS = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 20]


@st.cache_data(ttl=300)  # cache for 5 minutes
def load_match_progress():
    """Load the Match Progress data from the Google Sheet CSV export,
    keeping only the requested columns and filling blanks with empty strings."""
    df = pd.read_csv(SHEET_CSV_URL, usecols=MATCH_PROGRESS_COLUMNS)
    df = df.fillna("")
    return df

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

    # -- Match Progress Tracker (main navigation item) --
    st.button("📊  Match Progress Tracker", key="nav_match_progress",
              use_container_width=True, on_click=go_to, args=("Match Progress Tracker",))

    # -- "Review Processes" dropdown containing the A Review page --
    with st.expander("🔍  Review Processes", expanded=True):
        st.button("A Review", key="nav_a_review",
                  use_container_width=True, on_click=go_to, args=("A Review",))

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

# ── Page: Match Progress Tracker (live Google Sheet data) ─────────────────────
elif page == "Match Progress Tracker":
    render_page_header(
        "Trackers",
        "Match Progress Tracker",
        "Live data synced from the team Google Sheet (refreshes every 5 minutes).",
    )

    try:
        df = load_match_progress()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(
            "Could not load the Match Progress data right now. "
            "Please make sure the Google Sheet is shared as 'Anyone with the link' "
            f"and try again.\n\nDetails: {e}"
        )

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
