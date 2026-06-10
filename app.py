import os
import streamlit as st
import streamlit.components.v1 as components

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
        "Live collection performance, pulled directly from the Scorecard tab in Google Sheets. Auto-refreshes every 5 minutes.",
    )

    # The dashboard is a self-contained HTML/CSS/JS component. It fetches the
    # Scorecard tab live (client-side) every time the page loads, so the numbers
    # stay in sync with the sheet automatically — nothing is hard-coded here.
    _dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "scorecard_dashboard.html")
    try:
        with open(_dashboard_path, "r", encoding="utf-8") as _f:
            _dashboard_html = _f.read()
        components.html(_dashboard_html, height=2000, scrolling=True)
    except FileNotFoundError:
        st.error(
            "Could not find **scorecard_dashboard.html** next to `app.py`. "
            "Make sure the dashboard file sits in the same folder as app.py."
        )
