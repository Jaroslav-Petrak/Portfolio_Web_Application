import streamlit as st

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



profile_photo_part, divider_part, title_section_filler_part_1, title_part, title_section_filler_part_2 = st.columns([1.1, 0.1, 0.1, 4, 3])

with profile_photo_part:
    st.image("images/profile_picture.png", width=150)

with divider_part:
    st.markdown(
        """
        <div style="
            height: 150px;
            border-left: 4px solid white;
            margin: 0 auto;
        "></div>
        """,
        unsafe_allow_html=True
    )

with title_part:
    st.markdown(f'<div class="title-font">JAROSLAV PETRÁK</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-font">Data Scientist & Analyst</div>', unsafe_allow_html=True)


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
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Overview"

def set_section(section_name):
    st.session_state.selected_section = section_name

button_part_1, button_part_2, button_part_3, button_part_4 = st.columns([1, 1, 1, 1])
with button_part_1:
    st.button("Overview", key="btn_overview", on_click=set_section, args=("Overview",))
with button_part_2:
    st.button("Experience", key="btn_experience", on_click=set_section, args=("Experience",))
with button_part_3:
    st.button("Skills & Tools", key="btn_skills_and_tools", on_click=set_section, args=("Skills & Tools",))
with button_part_4:
    st.button("Certifications & Courses", key="btn_certifications_and_courses", on_click=set_section, args=("Certifications & Courses",))

st.markdown("""
            <style>
            /* More specific selectors to force override */
            button[kind="secondary"], button[kind="primary"] {
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

            button[kind="secondary"]:hover, button[kind="primary"]:hover {
                background-color: #e04e4e !important;
            }
            </style>
        """, unsafe_allow_html=True)
if st.session_state.selected_section != "Experience" and st.session_state.selected_section != "Skills & Tools" and st.session_state.selected_section != "Certifications & Courses":
    ### OVERVIEW SECTION ###
    main_content_overview_text_part, overview_filler_part ,main_content_overview_picture_part = st.columns([11,1,3], gap="small")
    ### TEXT PART OF THE OVERVIEW SECTION ###
    with main_content_overview_text_part:
        st.title("Overview")
        st.markdown("""
                    <div style='color: white;'>
                    Experienced Data Analyst with an educational background in Data Science & AI. Skilled in leveraging SQL, Excel & Power BI to drive insightful data analytics projects, particularly in HR & quality assurance domains. Proficient in developing & deploying machine learning models using popular libraries such as TensorFlow, XGBoost, CatBoost, LightGBM & Scikit-Learn. Experienced in deploying ML models on Azure Machine Learning & adept at data engineering tasks utilizing ETL tools like Azure Data Factory & Pentaho.
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE OVERVIEW SECTION ###    
    with main_content_overview_picture_part:
        st.image("images/profile_overview_icon.png", width=200)

    ### EDUCATION SECTION ###  
    main_content_education_text_part, education_filler_part, main_content_education_picture_part = st.columns([11, 1, 3], gap="small")
    ### PICTURE PART OF THE EDUCATION SECTION ###    
    with main_content_education_text_part:
        st.title("Education")
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.muvs.cvut.cz/en/prospective-students/master-of-science/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Czech Technical University in Prague (CTU)</a> - Project Management of Innovations (Ing./MSc.) - Current average 1.3 (A grade)
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.opit.com/courses/computer-science-master/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Open Institute of Technology (OPIT)</a> - Applied Data Science & AI (MSc.) - Total average 99%
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.muvs.cvut.cz/en/prospective-students/prospective-bachelor/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Czech Technical University in Prague (CTU)</a> - Economics & Management (Bc./BSc.) - Graduated with distinction with total average of 1.06 (nearly perfect A grade)
                    </div>
                    """, unsafe_allow_html=True)
    
    ### TEXT PART OF THE EDUCATION SECTION ###
    with main_content_education_picture_part:
        st.image("images/profile_education_icon.png", width=200)    
    
    ### LANGUAGES SECTION ###
    main_content_languages_text_part, languages_filler_part, main_content_languages_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE LANGUAGES SECTION ###
    with main_content_languages_text_part:
        st.title("Languages")
        st.markdown("""
                    <div style='color: white;'>
                    • <span style="text-decoration: none; color: #ff5757; font-weight: bold;">Czech</span> - Native
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/in/bc-jaroslav-petr%C3%A1k-7b9704264/details/certifications/1749917664315/single-media-viewer/?profileId=ACoAAEDjc30BZnSbgPlhIyAibehQFfGOTLWfijI" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">English</a> - CAE C1 certified
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/in/bc-jaroslav-petr%C3%A1k-7b9704264/details/certifications/1749919080218/single-media-viewer/?profileId=ACoAAEDjc30BZnSbgPlhIyAibehQFfGOTLWfijI" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">French</a> - DELF B1 certified
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE LANGUAGES SECTION ###    
    with main_content_languages_picture_part:
        st.image("images/profile_languages_icon.png", width=200)
if st.session_state.selected_section == "Experience":
    st.title("Experience")
    ### HR CONTROLLING DATA ANALYST SECTION ###
    main_content_position_1_text_part, position_1_filler_part, main_content_position_1_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE HR CONTROLLING DATA ANALYST SECTION ###
    with main_content_position_1_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        HR Controlling Data Analyst – <a href="https://www.cetin.cz/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">CETIN</a> (2024/04 – Now)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Development of data-driven reporting on training compliance, remuneration, benefits, equality, diversity & other HR metrics, achieving near-perfect legislative compliance, optimizing & prioritizing high-demand benefits, improving gender inclusivity for women by 6%
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • ML forecasting of HR cost metrics for planning purposes, resulting in 5% MAPE while forecasting of the training costs
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Creation of online Power BI course & led 8 Excel training sessions, enhancing internal analytical capabilities & reducing dependency on external data support of roughly 90 employees
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • Development of 2 Power Apps to streamline the employee benefits selection process, enabling 3,000 employees to make their selections efficiently
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Serving as system administrator for SAP SuccessFactors and the internal LMS, including development of customized reports within both platforms
                    </div>
                    """, unsafe_allow_html=True)          
    ### PICTURE PART OF THE HR CONTROLLING DATA ANALYST SECTION ###    
    with main_content_position_1_picture_part:
        st.image("images/experience_cetin_logo.png", width=200)

    st.text("")
    ### DATA ANALYST SUPPORT SECTION ###
    main_content_position_2_text_part, position_2_filler_part, main_content_position_2_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE DATA ANALYST SUPPORT SECTION ###
    with main_content_position_2_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        Data Analyst Support – <a href="https://www.cetin.cz/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">CETIN</a> (2023/06 – 2024/04)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Reporting about service quality assurance, contributing to maintaining lead times below thresholds specified in B2B contracts, resulting in performance 2-5% above the threshold on average
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Monitoring projects related to 7 report migrations, 1 data migration
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • Communication of feature engineering needs to the Data Engineers, ensuring swift delivery of necessary variables for reporting
                    </div>
                    """, unsafe_allow_html=True)   
    ### PICTURE PART OF THE DATA ANALYST SUPPORT SECTION ###    
    with main_content_position_2_picture_part:
        st.image("images/experience_cetin_logo.png", width=200)

    st.text("")
    ### HR TRAINEE SECTION ###
    main_content_position_3_text_part, position_3_filler_part, main_content_position_3_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE HR TRAINEE SECTION ###
    with main_content_position_3_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        HR Trainee – <a href="https://adastracorp.com/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Adastra</a> (2023/03 – 2023/04)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • IT recruitment related to Data Analytics & IT Project Management, handling a total of 75 telephone screenings & 3 in-person interviews
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Translation of a total of 7 company-internal directives from Czech to English
                    </div>
                    """, unsafe_allow_html=True)   
    ### PICTURE PART OF THE HR TRAINEE SECTION ###    
    with main_content_position_3_picture_part:
        st.image("images/experience_adastra_logo.png", width=200)

    st.text("")
    ### MARKETING TRAINEE SECTION ###
    main_content_position_4_text_part, position_4_filler_part, main_content_position_4_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE MARKETING TRAINEE SECTION ###
    with main_content_position_4_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        Marketing Trainee – <a href="https://www.cpihotels.com/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">CPI Hotels</a> (2022/09 – 2022/12)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Analysis of competitors, deriving insights about prices, quality, events, services from more than 20 local hotel providers
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Tracking voucher status in the database to estimate expected costs from active vouchers & savings from expired ones 
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • Editation of HTML codes for the modification of email marketing content
                    </div>
                    """, unsafe_allow_html=True)   
    ### PICTURE PART OF THE MARKETING TRAINEE SECTION ###    
    with main_content_position_4_picture_part:
        st.image("images/experience_cpi_hotels_logo.png", width=200)

if st.session_state.selected_section == "Skills & Tools":

    ### SKILLS SECTION ###
    main_content_skills_text_part, skills_filler_part, main_content_skills_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE SKILLS SECTION ###
    with main_content_skills_text_part:
        st.title("Skills")
        st.markdown("""
                    <div style='color: white;'>
                    • Report development
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • ML model development & deployment
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Presentation
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Project management
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Python website development
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE SKILLS SECTION ###    
    with main_content_skills_picture_part:
        st.image("images/profile_skills_icon.png", width=200)

    st.text("")
    ### PROGRAMMING LANGUAGES SECTION ###
    main_content_programming_languages_text_part, programming_languages_filler_part, main_content_programming_languages_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE PROGRAMMING LANGUAGES SECTION ###
    with main_content_programming_languages_text_part:
        st.title("Programming Languages")
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Python</b> - TensorFlow, Scikit-Learn, XGBoost, CatBoost, LightGBM, statsmodels, Pandas, NumPy, BeautifulSoup, Streamlit, Gradio, Matplotlib, Plotly, Seaborn
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>SQL</b>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>M</b>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Power fx</b>
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE PROGRAMMING LANGUAGES SECTION ###    
    with main_content_programming_languages_picture_part:
        st.image("images/profile_programming_languages_icon.png", width=200)

    st.text("")
    ### TOOLS SECTION ###
    main_content_tools_text_part, tools_filler_part, main_content_tools_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE TOOLS SECTION ###
    with main_content_tools_text_part:
        st.title("Tools")
        st.markdown("""
                    <div style='color: white;'>
                    • <b>General office tools</b> - MS Office Suite
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Visualization tools</b> - MS Power BI, Google Looker Studio, MS Excel 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Databases</b> - Azure SQL, MS SQL, MySQL, Snowflake, MS Access
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Code editors</b> - VSCode, JupyterLab, Google Colab 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>ETL tools</b> - Azure Data Factory, Pentaho 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <b>ML development & deployment</b> - Azure ML 
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Code versioning</b> - GitHub
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Project management</b> - Trello
                    </div>
                    """, unsafe_allow_html=True) 
        st.markdown("""
                    <div style='color: white;'>
                    • <b>App development tools</b> - MS Power Apps
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • <b>Automation</b> - Azure Automation, MS Power Automate
                    </div>
                    """, unsafe_allow_html=True)     
    ### PICTURE PART OF THE TOOLS SECTION ###    
    with main_content_tools_picture_part:
        st.image("images/profile_tools_icon.png", width=200)

if st.session_state.selected_section == "Certifications & Courses":
    ### CERTIFICATIONS SECTION ###
    main_content_certifications_text_part, certifications_filler_part, main_content_certifications_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE COURSES SECTION ###
    with main_content_certifications_text_part:
        st.title("Certifications")
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/in/bc-jaroslav-petr%C3%A1k-7b9704264/details/certifications/1749917664315/single-media-viewer/?profileId=ACoAAEDjc30BZnSbgPlhIyAibehQFfGOTLWfijI" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">English</a> - CAE C1
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/in/bc-jaroslav-petr%C3%A1k-7b9704264/details/certifications/1749919080218/single-media-viewer/?profileId=ACoAAEDjc30BZnSbgPlhIyAibehQFfGOTLWfijI" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">French</a> - DELF B1
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <span style="text-decoration: none; color: #ff5757; font-weight: bold;">Mathematics +</span>
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE COURSES SECTION ###    
    with main_content_certifications_picture_part:
        st.image("images/profile_certifications_icon.png", width=200)

    st.text("")
    ### COURSES SECTION ###
    main_content_courses_text_part, courses_filler_part, main_content_courses_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE COURSES SECTION ###
    with main_content_courses_text_part:
        st.title("Courses")
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.kaggle.com/learn/certification/jaroslavpetrk/machine-learning-explainability" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Machine Learning Explainability</a> - 2025/03
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-3b00b5e2-8553-4d20-af9f-07767013f444/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">LangChain for Generative AI: Using OpenAI LLMs in Python</a> - 2025/02
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-1d33734e-bfe2-4647-8e55-68dcc319aff8/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">DP-100 Azure Data Scientist Associate Complete Exam Guide</a> - 2025/01
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-2d533184-b618-4f5b-8954-997a820fc1f0/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Pentaho for ETL & Data Integration Masterclass 2025 - PDI 9</a> - 2025/01
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-fdc5571d-61d5-4762-963c-1bed892735ad/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Ultimate Azure Data Factory: Cloud Data Engineering</a> - 2025/01
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-64d70f8b-328f-40d9-9fdb-d3c6c7d95c6c/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Deep Learning: Recurrent Neural Networks in Python</a> - 2024/08
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-2c06bced-042e-496e-ab18-102d43c70615/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Microsoft Applied Skills: Create Canvas Apps with Power Apps</a> - 2024/08
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-331abbf8-f43c-48a0-ab92-6c82a0c28e71/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Deep Learning with Python & Keras</a> - 2024/07
                    </div>
                    """, unsafe_allow_html=True) 
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-e7fe9bf3-8757-4ef1-8540-4ee9fcb37a98/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Snowflake Decoded - Master the Fundamental Concepts</a> - 2024/04
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.udemy.com/certificate/UC-1e138c43-7582-4f48-b125-49cb5216f9b2/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Python for Data Science & Machine Learning Bootcamp</a> - 2023/08
                    </div>
                    """, unsafe_allow_html=True)     
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/learning/certificates/64dc916bc7a5b085739400705b35e84276b8f15fec188be79281781342360afe" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">Power BI Essential Training</a> - 2023/04
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • <a href="https://www.linkedin.com/learning/certificates/f9289ed9626c4aa51b8e66b1ad789ceee44b8fbd39f6c91440c364972e8b72e6" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #ff5757; font-weight: bold;">SQL Essential Training</a> - 2023/04
                    </div>
                    """, unsafe_allow_html=True)  
    ### PICTURE PART OF THE COURSES SECTION ###    
    with main_content_courses_picture_part:
        st.image("images/profile_courses_icon.png", width=200)






