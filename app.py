# Verification copy — compile check only. Safe to delete.
import os
import streamlit as st

st.info(
    "This process is applied to **100% of the matches** collected during the "
    "Collection phase. Its primary purpose is to review match facts, ensuring that "
    "data is delivered to the customer with **zero errors** regarding these specific events."
)

with st.sidebar:
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
    except Exception:
        pass

st.success(
    "All corrections and updates are displayed in a **dashboard** to evaluate each "
    "collector's performance and generate a **quality score** for each collector per match."
)
