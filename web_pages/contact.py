import streamlit as st
import base64

st.markdown("""
                        <style>
                        .title-font {
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                            font-size: 48px;
                            font-weight: bold;
                            color: #ffffff;
                        }
                        .subtitle-font {
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                            font-size: 48px;
                            color: #f88181;
                        }
                        </style>
                    """, unsafe_allow_html=True)
st.markdown(f'<div class="title-font">CONTACT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">Information</div>', unsafe_allow_html=True)

### FIRST DIVISION LINE ###
st.markdown("""
        <hr style="
            border: none;
            height: 4px;
            background-color: white;
            margin: 10px 0;
            box-shadow: none;
            opacity: 1;
        ">
    """, unsafe_allow_html=True)

### CREATION OF 2 SEPARATE COLUMNS FOR LINKED & EMAIL ###
linkedin_icon_part, email_icon_part, filler_part = st.columns([2, 2, 14], gap="small")


def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string

### LINKEDIN PART ###
with linkedin_icon_part:
    linked_icon_base64 = img_to_base64("images/linkedin_icon.png")
    html_code_linkedin_icon = f"""
    <a href="https://www.linkedin.com/in/bc-jaroslav-petr%C3%A1k-7b9704264/" target="_blank" style="display:inline-block;">
        <img src="data:image/png;base64,{linked_icon_base64}" width="100" style="vertical-align:middle;">
    </a>
    """
    st.markdown(html_code_linkedin_icon, unsafe_allow_html=True)

### EMAIL PART ###
with email_icon_part:
    email_icon_base64 = img_to_base64("images/email_icon.png")
    html_code_email_icon = f"""
    <a href="mailto:jaro.p.main@gmail.com" target="_blank" style="display:inline-block;">
        <img src="data:image/png;base64,{email_icon_base64}" width="80" style="vertical-align:middle;">
    </a>
    """
    st.markdown(html_code_email_icon, unsafe_allow_html=True)