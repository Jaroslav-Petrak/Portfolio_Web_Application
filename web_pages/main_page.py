import streamlit as st
import config.config

### CONFIGURATION OF THE TITLE FONTS ###
st.markdown(config.config.title_fonts, unsafe_allow_html=True)

profile_photo_part, title_part = st.columns([1, 7])
with profile_photo_part:
    st.image("images/profile_picture.png",width = 150)
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
                    Experienced Data Analyst with educational background in Data Science & Artificial Intelligence. I have worked on projects related to data analytics in HR & quality assurance with the use of SQL, Excel & Power BI. I have worked with ML models with the libraries such as TensorFlow, XGBoost, CatBoost, LightGBM, Scikit-Learn, Pandas & Numpy. I am familiar with ML model deployments in Azure Machine Learning. I have also worked with ETL tools such as Azure Data Factory & Pentaho related to Data Engineering.
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
                    • Czech Technical University in Prague (CTU) - Project Management of Innovations (Ing./MSc.)
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Open Institute of Technology (OPIT) - Applied Data Science & AI (MSc.)
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Czech Technical University in Prague (CTU) - Economics & Management (Bc./BSc.)
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
                    • Czech - Native
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • English - CAE C1 certified
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • French - DELF B1 certified
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
                        HR Controlling Data Analyst – CETIN (2024/04 – Now)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Creation of reports about training & remuneration
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • ML forecasting HR metrics for planning purposes
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Excel & Power BI training of employees
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • Power Apps development for the benefit selection
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Administration of SAP SuccessFactors & internal LMS
                    </div>
                    """, unsafe_allow_html=True)          
    ### PICTURE PART OF THE HR CONTROLLING DATA ANALYST SECTION ###    
    with main_content_position_1_picture_part:
        st.image("images/experience_cetin_logo.png", width=200)

    ### DATA ANALYST SUPPORT SECTION ###
    main_content_position_2_text_part, position_2_filler_part, main_content_position_2_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE DATA ANALYST SUPPORT SECTION ###
    with main_content_position_2_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        Data Analyst Support – CETIN (2023/06 – 2024/04)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Creation of reports about service quality assurance
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Monitoring projects related to report & data migrations
                    </div>
                    """, unsafe_allow_html=True)   
    ### PICTURE PART OF THE DATA ANALYST SUPPORT SECTION ###    
    with main_content_position_2_picture_part:
        st.image("images/experience_cetin_logo.png", width=200)

    ### HR TRAINEE SECTION ###
    main_content_position_3_text_part, position_3_filler_part, main_content_position_3_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE HR TRAINEE SECTION ###
    with main_content_position_3_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        HR Trainee – Adastra (2023/03 – 2023/04)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • IT recruitment (data analytics & project management)
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Translation of directives from Czech to English
                    </div>
                    """, unsafe_allow_html=True)   
    ### PICTURE PART OF THE HR TRAINEE SECTION ###    
    with main_content_position_3_picture_part:
        st.image("images/experience_adastra_logo.png", width=200)

    ### MARKETING TRAINEE SECTION ###
    main_content_position_4_text_part, position_4_filler_part, main_content_position_4_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE MARKETING TRAINEE SECTION ###
    with main_content_position_4_text_part:        
        st.markdown("""
                    <div style='color: white; font-size: 20px; font-weight: bold;'>
                        Marketing Trainee – CPI Hotels (2022/09 – 2022/12)
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    <div style='color: white;'>
                    • Analysis of competition
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Work with internal database of vouchers
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • Editing HTML codes
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

    ### PROGRAMMING LANGUAGES SECTION ###
    main_content_programming_languages_text_part, programming_languages_filler_part, main_content_programming_languages_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE PROGRAMMING LANGUAGES SECTION ###
    with main_content_programming_languages_text_part:
        st.title("Programming Languages")
        st.markdown("""
                    <div style='color: white;'>
                    • Python
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • SQL
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • M
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Power fx
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE PROGRAMMING LANGUAGES SECTION ###    
    with main_content_programming_languages_picture_part:
        st.image("images/profile_programming_languages_icon.png", width=200)

    ### TOOLS SECTION ###
    main_content_tools_text_part, tools_filler_part, main_content_tools_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE TOOLS SECTION ###
    with main_content_tools_text_part:
        st.title("Tools")
        st.markdown("""
                    <div style='color: white;'>
                    • General office tools - MS Office Suite
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Visualization tools - Power BI, Excel 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Databases - MS SQL, MySQL, Snowflake, MS Access
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Code editors - VSCode, JupyterLab, Google Colab 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • ETL tools - Azure Data Factory, Pentaho 
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • ML development & deployment - Azure ML 
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • Code versioning - GitHub
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • Project management - Trello
                    </div>
                    """, unsafe_allow_html=True) 
        st.markdown("""
                    <div style='color: white;'>
                    • App development tools - Power Apps
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • Automation - Azure Automation, Power Automate
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
                    • English CAE C1
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • French DELF B1
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Mathematics +
                    </div>
                    """, unsafe_allow_html=True)
    ### PICTURE PART OF THE COURSES SECTION ###    
    with main_content_certifications_picture_part:
        st.image("images/profile_certifications_icon.png", width=200)

    ### COURSES SECTION ###
    main_content_courses_text_part, courses_filler_part, main_content_courses_picture_part = st.columns([11, 1, 3], gap="small")
    ### TEXT PART OF THE COURSES SECTION ###
    with main_content_courses_text_part:
        st.title("Courses")
        st.markdown("""
                    <div style='color: white;'>
                    • Machine Learning Explainability
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • LangChain for Generative AI
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • DP-100 Azure Data Scientist Associate Exam Guide
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Pentaho for ETL & Data Integration
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Ultimate Azure Data Factory
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <div style='color: white;'>
                    • Deep Learning: RNN in Python
                    </div>
                    """, unsafe_allow_html=True)    
        st.markdown("""
                    <div style='color: white;'>
                    • Microsoft Applied Skills: Canvas Power Apps
                    </div>
                    """, unsafe_allow_html=True)   
        st.markdown("""
                    <div style='color: white;'>
                    • Deep Learning with Python & Keras
                    </div>
                    """, unsafe_allow_html=True) 
        st.markdown("""
                    <div style='color: white;'>
                    • Snowflake Decoded
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • Python for Data Science & ML Bootcamp
                    </div>
                    """, unsafe_allow_html=True)     
        st.markdown("""
                    <div style='color: white;'>
                    • Power BI Essential Training
                    </div>
                    """, unsafe_allow_html=True)  
        st.markdown("""
                    <div style='color: white;'>
                    • SQL Essential Training
                    </div>
                    """, unsafe_allow_html=True)  
    ### PICTURE PART OF THE COURSES SECTION ###    
    with main_content_courses_picture_part:
        st.image("images/profile_courses_icon.png", width=200)






