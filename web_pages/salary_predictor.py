import streamlit as st
import config.config
import pandas as pd
import datetime
import time
import json
from azureml.core.webservice import Webservice



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


df = pd.read_csv("data/source_for_search_bars.csv")
company_unique_values = sorted(df["EMPLOYER"].dropna().unique().tolist()) + [""]
job_title_unique_values = sorted(df["JOB TITLE"].dropna().unique().tolist()) + [""]
location_unique_values = sorted(df["LOCATION"].dropna().unique().tolist()) + [""]
branch_unique_values = sorted(df["BRANCH"].dropna().unique().tolist()) + [""]
max_company_unique_values = len(company_unique_values)
max_job_title_unique_values = len(job_title_unique_values)
max_location_unique_values = len(location_unique_values)
max_branch_unique_values = len(branch_unique_values)


st.markdown("""
<style>
    /* Hide the label container of all selectboxes */
    div[data-testid="stSelectbox"] > label {
        display: none;
        margin: 0;
        padding: 0;
    }

    /* Hide the label container of all date inputs */
    div[data-testid="stDateInput"] > label {
        display: none;
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)


company_part, job_title_part, branch_part, location_part, submission_date_part, starting_date_part = st.columns([1, 1, 1, 1, 1, 1])
with company_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Company</h3>", unsafe_allow_html=True)
    selected_value_company = st.selectbox("", options = company_unique_values, index = max_company_unique_values-1, key = "company")
with job_title_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Job Title</h3>", unsafe_allow_html=True)
    selected_value_job_title = st.selectbox("", options = job_title_unique_values, index = max_job_title_unique_values-1, key = "job title")
with branch_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Branch</h3>", unsafe_allow_html=True)
    selected_value_branch = st.selectbox("", options = branch_unique_values, index = max_branch_unique_values-1, key = "branch")
with location_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Location</h3>", unsafe_allow_html=True)
    selected_value_location = st.selectbox("", options = location_unique_values, index = max_location_unique_values-1, key = "location")
with submission_date_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Submission Date</h3>", unsafe_allow_html=True)
    selected_submission_date = st.date_input("", datetime.date.today(), key = "submission_date")
with starting_date_part:
    st.markdown("<h3 style='color: white; text-align: center;'>Start Date</h3>", unsafe_allow_html=True)
    selected_start_date = st.date_input("", datetime.date.today(), key = "start_date")


st.markdown("""
<style>
    /* Center the button container */
    div.stButton {
        text-align: center;
    }

    div.stButton > button {
        color: white !important;
        background-color: #ff5757 !important;
        border: none !important;
        width: 300px;
        height: 50px;
        font-size: 18px;
        border-radius: 8px;
        cursor: pointer;
    }

    div.stButton > button:hover {
        background-color: #e04e4e !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

clicked = st.button("Predict", key = "Predict")

if clicked:
    with st.spinner("Processing..."):
            time.sleep(2)
    if selected_value_company == "" or selected_value_job_title == "" or selected_value_location == "" or selected_value_branch == "":
        st.markdown("""
        <div style="background-color:#e04e4e; color: white; padding: 10px 20px; border-radius: 5px; text-align: center;">
            Choose at least one value in every parameter (company, job title, branch & location)!
        </div>
        """, unsafe_allow_html=True)
    elif selected_submission_date > selected_start_date:
        st.markdown("""
        <div style="background-color:#e04e4e; color: white; padding: 10px 20px; border-radius: 5px; text-align: center;">
            Choose submission day which is on the same day or prior to the start date!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color:#2ecc71; color: white; padding: 10px 20px; border-radius: 5px; text-align: center;">
            Form submitted successfully!
        </div>
        """, unsafe_allow_html=True)
        data = {
                "EMPLOYER": selected_value_company,
                "JOB TITLE": selected_value_job_title,
                "LOCATION": selected_value_location,
                "SUBMIT DATE": selected_submission_date.strftime("%#m/%#d/%Y"),
                "START DATE": selected_start_date.strftime("%#m/%#d/%Y"),
                "BRANCH": selected_value_branch,
                }
        json_data = json.dumps(data, indent=2)
        
        
        
        ################### TO BE CONTINUED!!!
        #endpoint = Webservice(workspace=workspace, name="salary-predictor")
        #prediction = endpoint.run(input_data=input_data)




