import streamlit as st
import config.config

### CONFIGURATION OF THE TITLE FONTS ###
st.markdown(config.config.title_fonts, unsafe_allow_html=True)


st.markdown(f'<div class="title-font">SALARY PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">for Fair Compensation</div>', unsafe_allow_html=True)

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

company_part, position_part, location_part, submission_date_part, starting_date_part = st.columns([1, 1, 1, 1, 1])

with company_part:
    st.title("Company")

with position_part:
    st.title("Position")

with location_part:
    st.title("Location")

with submission_date_part:
    st.title("Submission Date")

with starting_date_part:
    st.title("Starting Date")

