import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Offline Quality Team",
    page_icon="📋",
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
/* ---- Sidebar (GRAY) ---- */
[data-testid="stSidebar"] {
    background-color: #262730;
    border-right: 1px solid #3a3f4b;
}
[data-testid="stSidebar"] * {
    color: #CBD5E0 !important;
}
/* Sidebar title */
.sidebar-brand {
    padding: 2rem 1.2rem 0.5rem;
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    line-height: 1.4;
    color: #FFFFFF !important;
    letter-spacing: -0.01em;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.4rem;
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
    padding: 0 1.2rem;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7C8AA0 !important;
    margin: 1rem 0 0.3rem;
}
/* Radio styling overrides */
[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 2px;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    padding: 0.45rem 1.2rem !important;
    border-radius: 6px;
    margin: 0 0.5rem !important;
    transition: background 0.15s ease;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"][aria-checked="true"] {
    background: rgba(104,164,196,0.18) !important;
    border-left: 3px solid #68A4C4;
}
[data-testid="stSidebar"] .stRadio label p {
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    color: #CBD5E0 !important;
}
[data-testid="stSidebar"] .stRadio label[aria-checked="true"] p {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}
/* ---- Main content area ---- */
.block-container {
    padding: 2.5rem 3rem 3rem !important;
    max-width: 860px;
}

/* ---- Light font colors for native Streamlit text ---- */
/* Headers (st.header / st.subheader / st.title) and markdown text/bullets */
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
/* Keep st.info / st.success / st.warning text DARK on their light boxes so they
   stay readable and visually distinct (blue vs green vs amber). The extra
   selectors give these higher specificity than the light-text rules above. */
[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] li,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] blockquote {
    color: #1a1d24 !important;
}

/* Page top bar */
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
/* Content card (dark) */
.content-card {
    background: #1c1f26;
    border: 1px solid #2f3540;
    border-radius: 10px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
}
.content-card h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #fafafa !important;
    margin: 0 0 0.9rem;
    font-weight: 400;
}
.content-card p {
    font-size: 0.925rem;
    line-height: 1.75;
    color: #c8cfda !important;
    margin-bottom: 0.9rem;
}
.content-card p:last-child { margin-bottom: 0; }
/* Info banner (custom HTML breadcrumb / welcome) */
.info-banner {
    background: rgba(104,164,196,0.12);
    border-left: 4px solid #68A4C4;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.4rem;
    font-size: 0.875rem;
    color: #cfe3f0 !important;
    margin-bottom: 1.5rem;
}
.info-banner strong { color: #ffffff !important; }
/* Home cards (dark) */
.home-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1.5rem;
}
.home-card {
    background: #1c1f26;
    border: 1px solid #2f3540;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
}
.home-card .icon { font-size: 1.5rem; margin-bottom: 0.6rem; }
.home-card h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: #fafafa !important;
    margin: 0 0 0.4rem;
    font-weight: 400;
}
.home-card p {
    font-size: 0.82rem;
    color: #9aa6b5 !important;
    margin: 0;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ── Content store ─────────────────────────────────────────────────────────────
# Replace the placeholder strings below with your real content.
# Each page is a list of cards; each card is (heading, [paragraph, paragraph, ...]).
LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
)
LOREM2 = (
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
    "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa "
    "qui officia deserunt mollit anim id est laborum."
)
LOREM3 = (
    "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis "
    "molestie pretium placerat, arcu purus aliquam erat, in accumsan odio magna vitae enim."
)

# ── Navigation structure ──────────────────────────────────────────────────────
nav_structure = {
    "🏠  Home": ["Overview"],
    "🔍  Review Process": ["A Review", "B Review", "Final Review"],
    "📁  Documents": ["Templates", "Reference Guides"],
    "⚙️  Team Settings": ["Contacts", "Escalation Policy"],
}

# Page content definitions: page name -> list of (heading, [paragraphs])
# NOTE: "A Review" is rendered with native Streamlit components in the router
# below (not from this dict), so it is intentionally not listed here.
PAGE_CONTENT = {
    "B Review": [
        ("B Review", [LOREM, LOREM2]),
        ("Guidelines", [LOREM3]),
    ],
    "Final Review": [
        ("Final Review", [LOREM, LOREM3]),
        ("Sign-off Checklist", [LOREM2]),
    ],
    "Templates": [
        ("Available Templates", [LOREM, LOREM2]),
    ],
    "Reference Guides": [
        ("Reference Guides", [LOREM3, LOREM]),
    ],
    "Contacts": [
        ("Team Contacts", [LOREM, LOREM2]),
    ],
    "Escalation Policy": [
        ("Escalation Policy", [LOREM2, LOREM3]),
    ],
}

# Breadcrumb section labels shown in the info banner per page
PAGE_BREADCRUMB = {
    "A Review": "🔍 <strong>Section:</strong> Review Process › A Review",
    "B Review": "🔍 <strong>Section:</strong> Review Process › B Review",
    "Final Review": "🔍 <strong>Section:</strong> Review Process › Final Review",
    "Templates": "📁 <strong>Section:</strong> Documents › Templates",
    "Reference Guides": "📁 <strong>Section:</strong> Documents › Reference Guides",
    "Contacts": "⚙️ <strong>Section:</strong> Team Settings › Contacts",
    "Escalation Policy": "⚙️ <strong>Section:</strong> Team Settings › Escalation Policy",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span>Internal Docs</span>
        Offline Quality Team<br>Processes &amp; Documents
    </div>
    """, unsafe_allow_html=True)

    # Flatten nav structure into radio options
    page_options = []
    for section, pages in nav_structure.items():
        for page in pages:
            page_options.append(f"  {page}")  # slight indent for sub-items

    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)
    selected_page = st.radio(
        "nav",
        options=page_options,
        index=0,
        label_visibility="collapsed",
    )

# ── Helper: render a content card ─────────────────────────────────────────────
def placeholder_card(heading, body_paras):
    paras = "".join(f"<p>{p}</p>" for p in body_paras)
    st.markdown(f"""
    <div class="content-card">
        <h2>{heading}</h2>
        {paras}
    </div>
    """, unsafe_allow_html=True)

# ── Page Router ───────────────────────────────────────────────────────────────
page = selected_page.strip()

# ── Main header (always shown) ────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="eyebrow">Offline Quality Team</div>
    <h1>Processes &amp; Documents</h1>
    <div class="subtitle">Internal reference hub — use the sidebar to navigate sections.</div>
</div>
""", unsafe_allow_html=True)

# ── Page: Home / Overview ─────────────────────────────────────────────────────
if page == "Overview":
    st.markdown("""
    <div class="info-banner">
        👋 Welcome! Select a section from the sidebar to view guidelines, templates, or team processes.
    </div>
    <div class="home-grid">
        <div class="home-card">
            <div class="icon">🔍</div>
            <h3>Review Process</h3>
            <p>Step-by-step guidelines for A, B, and Final reviews.</p>
        </div>
        <div class="home-card">
            <div class="icon">📁</div>
            <h3>Documents</h3>
            <p>Download templates and browse reference guides.</p>
        </div>
        <div class="home-card">
            <div class="icon">⚙️</div>
            <h3>Team Settings</h3>
            <p>Contacts, escalation paths, and on-call policies.</p>
        </div>
        <div class="home-card">
            <div class="icon">📝</div>
            <h3>Quick Edit</h3>
            <p>Replace the placeholder text in PAGE_CONTENT with your real content.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page: A Review (native Streamlit components) ──────────────────────────────
elif page == "A Review":
    st.markdown(
        '<div class="info-banner">🔍 <strong>Section:</strong> Review Process › A Review</div>',
        unsafe_allow_html=True,
    )

    st.header("A Review Process")

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

# ── All other pages (data-driven) ─────────────────────────────────────────────
elif page in PAGE_CONTENT:
    breadcrumb = PAGE_BREADCRUMB.get(page, "")
    if breadcrumb:
        st.markdown(f'<div class="info-banner">{breadcrumb}</div>', unsafe_allow_html=True)
    for heading, paras in PAGE_CONTENT[page]:
        placeholder_card(heading, paras)
