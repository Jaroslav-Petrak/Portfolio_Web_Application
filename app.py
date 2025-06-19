import streamlit as st
import base64

st.set_page_config(layout="wide")
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img_base64 = get_base64_image("images/background.png")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #2C3E50 !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: #F1F1F1 !important;
    }}

    section[data-testid="stSidebar"] a:hover {{
        background-color: #1f1f1f !important;
        transition: all 0.3s ease;
        border-radius: 5px;
        padding: 5px 10px;
        text-decoration: none;
    }}

    header[data-testid="stHeader"] {{
        background-color: #1f1f1f !important;
    }}

    header[data-testid="stHeader"] * {{
        color: #ffffff !important;
    }}

    footer {{
        visibility: hidden;
    }}
    </style>
""", unsafe_allow_html=True)

main_page = st.Page(page="web_pages/main_page.py", title="Main Page")
salary_predictor_and_report = st.Page(page="web_pages/salary_predictor_and_report.py", title="Salary Predictor & Report")
chatbot = st.Page(page="web_pages/chatbot.py", title="Chatbot")
contact = st.Page(page="web_pages/contact.py", title="Contact")

pg = st.navigation({
    "NAVIGATION": [main_page, contact, chatbot],
    "Portfolio Projects": [salary_predictor_and_report]
})
pg.run()
