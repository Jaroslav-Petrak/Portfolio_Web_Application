import streamlit as st
import pandas as pd
import datetime
import time
import json
import streamlit.components.v1 as components
import traceback
import requests



### CONFIGURATION OF THE TITLE FONTS ###
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
st.markdown(f'<div class="title-font">SALARY PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">for Fair Compensation</div>', unsafe_allow_html=True)

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



### BUTTONS ###

st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
        color: white !important;
        background-color: #ff5757 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        padding: 10px 30px !important;
        width: 100% !important;
        height: 50px !important;
        border: none !important;
        cursor: pointer;
        transition: background-color 0.3s ease !important;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: #e04e4e !important;
    }
    </style>
""", unsafe_allow_html=True)

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Predictor"

def set_section(section_name):
    st.session_state.selected_section = section_name

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("Predictor", key="btn_predictor", on_click=set_section, args=("Predictor",))
with col2:
    st.button("H-1B Salaries Report", key="btn_h1b_salaries_report", on_click=set_section, args=("H-1B Salaries Report",))
with col3:
    st.button("Description", key="btn_description", on_click=set_section, args=("Description",))



### PREDICTOR SECTION ###
if st.session_state.selected_section != "Description" and st.session_state.selected_section != "H-1B Salaries Report":
    st.title("Predictor")
    ### DATA FOR THE SEARCH BARS ###
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
        st.markdown("<h6 style='color: white; text-align: center;'>Company</h6>", unsafe_allow_html=True)
        selected_value_company = st.selectbox("", options = company_unique_values, index = max_company_unique_values-1, key = "company")
    with job_title_part:
        st.markdown("<h6 style='color: white; text-align: center;'>Job Title</h6>", unsafe_allow_html=True)
        selected_value_job_title = st.selectbox("", options = job_title_unique_values, index = max_job_title_unique_values-1, key = "job title")
    with branch_part:
        st.markdown("<h6 style='color: white; text-align: center;'>Branch</h6>", unsafe_allow_html=True)
        selected_value_branch = st.selectbox("", options = branch_unique_values, index = max_branch_unique_values-1, key = "branch")
    with location_part:
        st.markdown("<h6 style='color: white; text-align: center;'>Location</h6>", unsafe_allow_html=True)
        selected_value_location = st.selectbox("", options = location_unique_values, index = max_location_unique_values-1, key = "location")
    with submission_date_part:
        st.markdown("<h6 style='color: white; text-align: center;'>Submission Date</h6>", unsafe_allow_html=True)
        selected_submission_date = st.date_input("", datetime.date.today(), key = "submission_date")
    with starting_date_part:
        st.markdown("<h6 style='color: white; text-align: center;'>Start Date</h6>", unsafe_allow_html=True)
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
            time.sleep(1)

        if selected_value_company == "" or selected_value_job_title == "" or selected_value_location == "" or selected_value_branch == "":
            st.markdown(
                    """
                    <div style='margin-top: 30px; display: flex; justify-content: center;'>
                        <pre style='color: white; background-color: transparent; font-family: monospace; text-align: left; white-space: pre-wrap;'>
                        Choose at least one value in every parameter (company, job title, branch & location)!
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            

        elif selected_submission_date > selected_start_date:
            st.markdown(
                    """
                    <div style='margin-top: 30px; display: flex; justify-content: center;'>
                        <pre style='color: white; background-color: transparent; font-family: monospace; text-align: left; white-space: pre-wrap;'>
                        Choose submission day which is on the same day or prior to the start date!
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        else:
            data_from_user_input = {
                "EMPLOYER": selected_value_company,
                "JOB TITLE": selected_value_job_title,
                "LOCATION": selected_value_location,
                "SUBMIT DATE": selected_submission_date.strftime("%#m/%#d/%Y"),
                "START DATE": selected_start_date.strftime("%#m/%#d/%Y"),
                "BRANCH": selected_value_branch,
            }
            edited_input_data = json.dumps([data_from_user_input], indent=2)

            log_placeholder = st.empty()

            def update_logs(new_message):
                log_placeholder.markdown(
                    f"""
                    <div style='margin-top: 30px; display: flex; justify-content: center;'>
                        <pre style='color: white; background-color: transparent; font-family: monospace; text-align: left; white-space: pre-wrap;'>
                        {new_message}
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            try:
                update_logs("Getting to the endpoint of the ML Model...")
                scoring_uri = st.secrets["scoring_uri"]
                update_logs("Sending data for prediction...")
                headers = {"Content-Type": "application/json"}
                response = requests.post(scoring_uri, data=edited_input_data, headers=headers)
                response.raise_for_status()
                parsed_json_prediction = json.loads(response.text) 
                parsed_json_prediction = json.loads(parsed_json_prediction) 
                prediction_value = parsed_json_prediction["result"][0][0]
                clean_prediction = int(prediction_value)
                update_logs("Prediction calculated successfully.")

                st.text("")
                st.text("")

                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="background-color: #000000; padding: 30px; border-radius: 16px; width: 600px; color: white;">
                            <h2 style='text-align: center; margin-bottom: 20px;'>Result</h2>
                            <div style="display: flex; font-size: 24px; font-weight: bold; border-radius: 12px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.4); height: 80px;">
                                <div style="flex: 1; background-color: #ff5c5c; color: white; display: flex; align-items: center; justify-content: center;">
                                    Predicted Salary
                                </div>
                                <div style="flex: 1; background-color: white; color: black; display: flex; align-items: center; justify-content: center;">
                                    {clean_prediction} USD
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception:
                update_logs("An error occurred during prediction.")
                update_logs(traceback.format_exc())

### H-1B SALARIES DASHBOARD SECTION ###
if st.session_state.selected_section == "H-1B Salaries Report":
    dashboard_url = "https://lookerstudio.google.com/embed/reporting/263493b9-9aea-45df-85a8-e7e6a431bc72/page/tz6NF"
    components.iframe(dashboard_url, width=1600, height=1200, scrolling=True)

### DESCRIPTION SECTION ###
if st.session_state.selected_section == "Description":
    st.title("Description of the Project")
    st.markdown("""
                <div style='color: white;'>
                Predictor has been stemmed from <a href="https://h1bdata.info/index.php" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757;">H1B visa salary data</a>  in the USA. Positions with equivalent job titles have been collected in order to make a representative picture of the salaries. Model has been deployed as an endpoint on Azure Machine Learning. This project is part of the diploma thesis related to the degree of MSc. Applied Data Science & AI with the name Development of a Salary Predictor for Fair Compensation which covers the preprocessing of the data, model development, validation & deployment. Choose the company, job title, branch, location, submission date of the documents related to the work-related visa as well as starting date on the position & make a prediction of expected salary. Last update of the model has been done in May 2025.
                </div>
                """, unsafe_allow_html=True)
    st.text("")
    st.markdown("""
                <div style='color: white;'>
                H-1B Salaries Report has been built inside Google's Looker Studio which provides free reporting solution with embedding capability. Preprocessed data that has been used to train the machine learning model has been utilized inside the report to maintain consistency given the filtering during the cleaning & standardization of the underlying data.
                </div>
                """, unsafe_allow_html=True)
    st.text("")
    st.markdown("""
                <div style='color: white;'>
                Last update of the model has been done in May 2025.
                </div>
                """, unsafe_allow_html=True)



