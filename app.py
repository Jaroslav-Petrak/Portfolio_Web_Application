import streamlit as st
import config.config

st.set_page_config(layout="wide")

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config.config.background_color} !important;
        color: {config.config.primary_font_color} !important;
    }}

    /* Navigation sidebar background color */
    section[data-testid="stSidebar"] {{
        background-color: #2C3E50 !important;  /* <-- Change this to your desired nav background color */
    }}

    /* Navigation sidebar font color */
    section[data-testid="stSidebar"] * {{
        color: #F1F1F1 !important;  /* <-- Change this to your desired nav font color */
    }}

    /* Sidebar links hover effect */
    section[data-testid="stSidebar"] a:hover {{
        background-color: #1f1f1f !important;
        transition: all 0.3s ease;
        border-radius: 5px;
        padding: 5px 10px;
        text-decoration: none;
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

main_page = st.Page(page="web_pages/main_page.py", title="Main Page")
salary_predictor = st.Page(page="web_pages/salary_predictor.py", title="Salary Predictor")
contact = st.Page(page="web_pages/contact.py", title="Contact")

pg = st.navigation({
    "NAVIGATION": [main_page, contact],
    "Portfolio Projects": [salary_predictor]
})

pg.run()
