import streamlit as st
import config.config

st.set_page_config(layout="wide")

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config.config.background_color} !important;
        color: {config.config.primary_font_color} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {config.config.navigation_background_color} !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {config.config.navigation_font_color} !important;
    }}

    header[data-testid="stHeader"] {{
        background-color: {config.config.background_color} !important;
    }}

    header[data-testid="stHeader"] * {{
        color: {config.config.primary_font_color} !important;
    }}

    footer {{
        visibility: hidden;
    }}
    </style>
""", unsafe_allow_html=True)

### WHITE FONT OF TEXT IN NAVIGATION PANEL###
st.markdown("""
    <style>
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] a:hover {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Selected navigation link background in sidebar */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background-color: #1f1f1f !important;
        color: white !important;          /* keep text visible */
        border-radius: 8px;               /* optional rounded corners */
    }
    </style>
""", unsafe_allow_html=True)



main_page = st.Page(page="web_pages/main_page.py", title="Main Page")
salary_predictor = st.Page(page="web_pages/salary_predictor.py", title="Salary Predictor")
contact = st.Page(page="web_pages/contact.py", title="Contact")

pg = st.navigation({
    "NAVIGATION": [main_page, contact],
    "Portfolio Projects": [salary_predictor]
})

pg.run()
