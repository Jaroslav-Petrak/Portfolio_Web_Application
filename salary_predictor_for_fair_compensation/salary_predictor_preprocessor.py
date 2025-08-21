import pandas as pd
import numpy as np
from rapidfuzz import process
import calendar
import re
import tensorflow as tf
from sklearn.model_selection import train_test_split

def preprocessing_pipeline(df, mode = "inference"):
  #############################################
  # SENIORITY MAPPING #########################
  #############################################
  def encoded_seniority(job_title):
      title = job_title.lower()
      if "vice president" in title or "vp" in title:
          return 7
      elif "director" in title:
          return 6
      elif "manager" in title and not "project manager" in title and not "account manager" in title and not "product manager" in title:
          return 5
      elif "lead" in title:
          return 4
      elif "senior" in title:
          return 3
      elif "junior" in title:
          return 1
      else:
          return 2
  df["SENIORITY"] = df["JOB TITLE"].apply(encoded_seniority)
  ############################################
  # POSITION MAPPING #########################
  ############################################
  def get_position(job_title):
    title = job_title.lower()
    
    ### IT ###
    if "data analyst" in title or "data analytics" in title:
      return "Data Analyst"
    elif "data engineer" in title or "data engineering" in title:
      return "Data Engineer"
    elif "data scientist" in title or "data science" in title:
      return "Data Scientist"
    elif "machine learning engineer" in title or "machine learning engineering" in title:
      return "Machine Learning Engineer"
    elif "ai engineer" in title or "ai engineering" in title:
      return "AI Engineer"
    elif "data architect" in title or "data architecture" in title:
      return "Data Architect"
    elif "software engineer" in title or "software engineering" in title:
      return "Software Engineer"
    elif "software developer" in title or "software development" in title:
      return "Software Developer"
    elif "devops" in title:
      return "DevOps Engineer"
    elif "systems analyst" in title or "systems analysis" in title:
      return "Systems Analyst"
    elif "developer advocate" in title:
      return "Developer Advocate"
    elif "front end developer" in title or "front-end developer" in title or "front end development" in title or "front-end development" in title:
      return "Front-End Developer"
    elif "back end developer" in title or "back-end developer" in title or "back end development" in title or "back-end development" in title:
      return "Back-End Developer"
    elif "full stack developer" in title or "full stack development" in title:
      return "Full-Stack Developer"
    elif "android developer" in title or "android development" in title:
      return "Android Developer"
    elif "ios developer" in title or "ios development" in title:
      return "iOS Developer"
    elif "cloud engineer" in title or "cloud engineering" in title:
      return "Cloud Engineer"
    elif "qa engineer" in title or "qa engineering" in title:
      return "QA Engineer"
    elif "security engineer" in title:
      return "Security Engineer"
    elif "security analy" in title:
      return "Security Analyst"
    elif "security architect" in title:
      return "Security Architect"
    elif "security administrat" in title:
      return "Security Administrator"
    elif "incident respon" in title:
      return "Incident Responder"
    elif "cyber security" in title:
      return "Cyber Security Specialist"
    
    ### FINANCE & ACCOUNTING ###
    elif "cost accountant" in title or "cost accounting" in title:
      return "Cost Accountant"
    elif "project accountant" in title or "project accounting" in title:
      return "Project Accountant"
    elif "tax accountant" in title or "tax accounting" in title:
      return "Tax Accountant"
    elif "revenue accountant" in title or "revenue accounting" in title:
      return "Revenue Accountant"
    elif "payroll accountant" in title or "payroll accounting" in title:
      return "Payroll Accountant"
    elif "accounts receivable" in title:
      return "Accounts Receivable Accountant"
    elif "accounts payable" in title:
      return "Accounts Payable Accountant"
    elif "fund accountant" in title or "fund accounting" in title:
      return "Fund Accountant"
    elif title == "junior accountant" or title == "accountant" or title == "senior accountant" or title == "lead accountant" or title == "accounting manager" or title == "director of accounting" or title == "vice president, accounting":
      return "Accountant"
    elif "financial analyst" in title or "financial analytics" in title:
      return "Financial Analyst"
    elif "financial specialist" in title or "financial manager" in title or "director of finance" in title or "vice president, finance" in title:
      return "Financial Specialist"

    ### SALES ###
    elif "account management" in title or "account manager" in title:
      return "Account Manager"
    elif "client relation" in title:
      return "Client Relationship Specialist"
    elif "business development" in title:
      return "Business Development Specialist"
    elif "sales" in title:
      return "Sales Specialist"
    elif "account executive" in title:
      return "Account Executive"
    
    ### R&D ###
    elif "r&d engineer" in title:
      return "R&D Engineer"
    elif "r&d specialist" in title or title == "r&d manager" or title == "director of r&d" or title == "vice president, r&d":
      return "R&D Specialist"
    elif "research analy" in title:
      return "Research Analyst"
    elif "research scientist" in title or "research science" in title:
      return "Research Scientist"
    elif "formulation scientist" in title or "formulation science" in title:
      return "Formulation Scientist"
    elif "prototype engineer" in title:
      return "Prototype Engineer"
    elif "clinical research" in title:
      return "Clinical Research Associate"
    elif "design engineer" in title:
      return "Design Engineer"
    elif "lab specialist" in title or "lab manager" in title or "director of labs" in title or "vice president, labs" in title:
      return "Lab Specialist"
    elif "innovation" in title:
      return "Innovation Specialist"
    
    ### PRODUCT & PROJECT MANAGEMENT ###
    elif "project analy" in title:
      return "Project Analyst"
    elif "process analyst" in title or "process excellence" in title:
      return "Process Analyst" 
    elif "scrum master" in title:
      return "Scrum Master"

    ### HR ###
    elif "recruit" in title:
      return "Recruiter"
    elif "hr business partner" in title:
      return "HR Business Partner"
    elif "learning and development" in title:
      return "Learning and Development Specialist"
    elif "employee relations" in title:
      return "Employee Relations Specialist"
    elif "compensation and benefits" in title or "compensations and benefits" in title:
      return "Compensation and Benefits Specialist"
    elif "hris" in title:
      return "HRIS Specialist"
    elif "diversity and inclusion" in title:
      return "Diversity and Inclusion Specialist"
    elif "hr analy" in title:
      return "HR Analyst"
    elif "hr generalist" in title or title == "hr manager" or title == "director of hr" or title == "vice president, hr":
      return "HR Generalist"
    
    ### MARKETING ###
    elif "digital marketing" in title:
      return "Digital Marketing Specialist"
    elif "email marketing" in title:
      return "Email Marketing Specialist"
    elif title == "junior marketing specialist" or title == "marketing specialist" or title == "senior marketing specialist" or title == "marketing manager" or title == "director of marketing" or title == "vice president, marketing":
      return "Marketing Specialist"
    elif "seo specialist" in title or title == "seo manager" or title == "director of seo" or title == "vice president, seo":
      return "SEO Specialist"
    elif "brand marketing" in title:
      return "Brand Marketing Specialist"
    elif "communications" in title:
      return "Communications Specialist"
    elif "product marketing" in title:
      return "Product Marketing Specialist"
    elif "event" in title:
      return "Event Coordinator"
    elif "content marketing" in title:
      return "Content Marketing Specialist"
    elif "social media" in title:
      return "Social Media Specialist"
    elif "growth marketing" in title:
      return "Growth Marketing Specialist"
    
    ### OPERATIONS & LOGISTICS ###
    elif "supply chain analy" in title:
      return "Supply Chain Analyst"
    elif "operations" in title:
      return "Operations Specialist"
    elif "logistics" in title:
      return "Logistics Specialist"
    elif "production plan" in title:
      return "Production Planner"
    elif "capacity plan" in title:
      return "Capacity Planner"
    elif "inventory control" in title:
      return "Inventory Control Specialist"

    ### LEGAL ###
    elif "legal counsel" in title or title == "legal manager" or title == "director of legal" or title == "vice president, legal":
      return "Legal Counsel"
    elif "paralegal" in title:
      return "Paralegal"
    elif "corporate counsel" in title:
      return "Corporate Counsel"
    elif "compliance" in title:
      return "Compliance Specialist"

    ### HYBRID ###
    elif "project manage" in title or "program manage" in title:
      return "Project Manager"
    elif "product owner" in title:
      return "Product Owner"
    elif "product manage" in title:
      return "Product Manager"
    else: 
      return "..."

  df["CORE POSITION"] = df["JOB TITLE"].apply(get_position)
  df = df[df['CORE POSITION'] != "..."]

  ###################################################################
  # CITY & STATE COLUMNS CREATION ###################################
  ###################################################################
  if mode == 'training':
    df_reference_locations = pd.read_csv("Cities & States.csv", encoding='ISO-8859-1')
    reference_locations = df_reference_locations['LOCATION'].dropna().unique().tolist()
    def correct_location(location):
        if pd.isna(location) or location.strip() == "":
            return None
        match, score, _ = process.extractOne(location, reference_locations)
        return match if score >= 85 else None
    df['LOCATION'] = df['LOCATION'].apply(correct_location)
    df = df[df['LOCATION'].notna()]
    df[['CITY', 'STATE']] = df['LOCATION'].str.rsplit(',', n=1, expand=True)
    df['CITY'] = df['CITY'].str.strip()
    df['STATE'] = df['STATE'].str.strip()
    df = df[df['STATE'].str.len() == 2]
  elif mode == 'inference':
    df[['CITY', 'STATE']] = df['LOCATION'].str.rsplit(',', n=1, expand=True)
    df['CITY'] = df['CITY'].str.strip()
    df['STATE'] = df['STATE'].str.strip()
  else:
    raise ValueError("Mode must be either 'training' or 'inference'.")
  ####################################################################
  # TIME FEATURES ####################################################
  ####################################################################
  df['SUBMIT DATE'] = pd.to_datetime(df['SUBMIT DATE'])
  df['START DATE'] = pd.to_datetime(df['START DATE'])
  df['SUBMIT DATE YEAR'] = df['SUBMIT DATE'].dt.year
  df['START DATE YEAR'] = df['START DATE'].dt.year
  df = df[df['START DATE YEAR']>=2000]
  df = df[df['SUBMIT DATE YEAR']>=2000]
  def days_in_month_series(years, months):
      return pd.Series([calendar.monthrange(y, m)[1] for y, m in zip(years, months)])

  def add_cyclical_day_features(df, date_col):
      dates = pd.to_datetime(df[date_col])
      day = dates.dt.day
      year = dates.dt.year
      month = dates.dt.month
      dim = days_in_month_series(year, month)
      df[f'{date_col} DAY_SIN'] = np.sin(2 * np.pi * day / dim)
      df[f'{date_col} DAY_COS'] = np.cos(2 * np.pi * day / dim)

  def add_cyclical_month_features(df, date_col):
      dates = pd.to_datetime(df[date_col])
      month = dates.dt.month
      df[f'{date_col} MONTH_SIN'] = np.sin(2 * np.pi * month / 12)
      df[f'{date_col} MONTH_COS'] = np.cos(2 * np.pi * month / 12)

  add_cyclical_day_features(df, 'SUBMIT DATE')
  add_cyclical_month_features(df, 'SUBMIT DATE')
  add_cyclical_day_features(df, 'START DATE')
  add_cyclical_month_features(df, 'START DATE')
  df['SUBMIT_DATE_DAY_INDEX'] = (df['SUBMIT DATE'] - df['SUBMIT DATE'].min()).dt.days
  df['SUBMIT_DATE_MONTH_INDEX'] = ((df['SUBMIT DATE'].dt.year - df['SUBMIT DATE'].min().year) * 12 + df['SUBMIT DATE'].dt.month)
  df['SUBMIT_DATE_YEAR_FRACTION'] = df['SUBMIT DATE'].dt.year + (df['SUBMIT DATE'].dt.dayofyear / 365)
  df['START_DATE_DAY_INDEX'] = (df['START DATE'] - df['START DATE'].min()).dt.days
  df['START_DATE_MONTH_INDEX'] = ((df['START DATE'].dt.year - df['START DATE'].min().year) * 12 + df['START DATE'].dt.month)
  df['START_DATE_YEAR_FRACTION'] = df['START DATE'].dt.year + (df['START DATE'].dt.dayofyear / 365)
  ###################################################################
  # STANDARDIZING EMPLOYER VARIABLE #################################
  ###################################################################
  suffixes = [' LLC', ' INC', ' LLP', ' LIMITED', ' LTD.', ' LTD', ' CORP',
              ' CORPORATION', ' LP', '-NA', '- NA', ' - NA',r' \(DUNS 079287817\)']
  pattern = r'(' + '|'.join([re.escape(suffix) for suffix in suffixes]) + r')$'
  df['EMPLOYER'] = df['EMPLOYER'].str.strip().str.replace(pattern, '', regex=True).str.strip()
  df['EMPLOYER'] = (
      df['EMPLOYER']
      .str.replace('AMAZONCOM SERVICE', 'AMAZON', regex=False)
      .str.replace('NETFLIX GLOB', 'NETFLIX', regex=False)
      .str.replace('META PLATFORM', 'META', regex=False)
      .str.replace('SAP LAB', 'SAP', regex=False)
      .str.replace('SAP AME', 'SAP', regex=False)
      .str.replace('SAP SE', 'SAP', regex=False)
      .str.replace('ORACLE AMERICA INC', 'ORACLE', regex=False)
      .str.replace('ORACLE ROBOTICS CORP', 'ORACLE', regex=False)
      .str.replace('ORACLE ROBOTICS CORP', 'ORACLE', regex=False)
      .str.replace('ORACLE FINANCIAL SERVICES SOFTWARE INC', 'ORACLE', regex=False)
      .str.replace('-', '', regex=False))

  if mode == 'training':
    employer_counts = df["EMPLOYER"].value_counts()
    valid_employers = employer_counts[employer_counts >= 4].index
    df = df[df["EMPLOYER"].isin(valid_employers)]
  ###################################################################
  # FAANG ###########################################################
  ###################################################################
  faang_keywords = ['Facebook', 'Meta', 'Meta Platform','Apple',
                    'Amazon', 'Netflix', 'Google', 'Alphabet']
  def faang_company(employer_name):
      employer_name = employer_name.lower()
      for keyword in faang_keywords:
          if keyword.lower() == employer_name:
              return 1
      return 0
  df['FAANG'] = df['EMPLOYER'].apply(faang_company)
  ###################################################################
  # IS LEADERSHIP POSITION ##########################################
  ###################################################################
  def is_leadership_position(seniority):
    if seniority >= 5:
      return 1
    else:
      return 0
  df["IS LEADERSHIP POSITION"] = df["SENIORITY"].apply(is_leadership_position)
  ###################################################################
  # OUTLIER CLIPPING BASED ON QUANTILE ##############################
  ###################################################################
  if mode == 'training':
    lower_bound = df['BASE SALARY'].quantile(0.02)
    upper_bound = df['BASE SALARY'].quantile(0.98)
    df = df[(df['BASE SALARY'] >= lower_bound) & (df['BASE SALARY'] <= upper_bound)]
  ###################################################################
  # SORTING DATA FOR TIME SERIES TESTING PURPOSES ###################
  ###################################################################
  if mode == 'training':
    df = df.sort_values(by='SUBMIT DATE')
  df.drop(columns = ["SUBMIT DATE", "START DATE"], inplace = True)
  ###########################################################################################
  # LOWER-CASING ############################################################################
  ###########################################################################################
  df['CORE POSITION'] = df['CORE POSITION'].str.lower()
  df['JOB TITLE'] = df['JOB TITLE'].str.lower()
  df['EMPLOYER'] = df['EMPLOYER'].str.lower()
  df['LOCATION'] = df['LOCATION'].str.lower()
  df['CITY'] = df['CITY'].str.lower()
  df['STATE'] = df['STATE'].str.lower()
  df['BRANCH'] = df['BRANCH'].str.lower()
  ###########################################################################################
  # SPLITTING DATA FRAME ####################################################################
  ###########################################################################################
  df.dropna(inplace = True)
  if mode == 'training':
    X = df.drop(columns=['BASE SALARY'])
    y = df['BASE SALARY'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=False)
 ############################################################################################
 # TENSORFLOW ML MODEL DATA PREPARATION & FINAL CALL OF PREPROCESSING PIPELINE ##############
 ############################################################################################
  categorical_features = ['EMPLOYER', 'JOB TITLE', 'LOCATION', 'CORE POSITION', 'CITY', 'STATE', 'BRANCH']
  numeric_features = ['SENIORITY','SUBMIT DATE YEAR', 'START DATE YEAR', 'SUBMIT DATE DAY_SIN',
                      'SUBMIT DATE DAY_COS', 'SUBMIT DATE MONTH_SIN', 'SUBMIT DATE MONTH_COS',
                      'START DATE DAY_SIN', 'START DATE DAY_COS', 'START DATE MONTH_SIN',
                      'START DATE MONTH_COS', 'SUBMIT_DATE_DAY_INDEX',
                      'SUBMIT_DATE_MONTH_INDEX', 'SUBMIT_DATE_YEAR_FRACTION',
                      'START_DATE_DAY_INDEX', 'START_DATE_MONTH_INDEX',
                      'START_DATE_YEAR_FRACTION', 'FAANG', "IS LEADERSHIP POSITION"]

  if mode == 'training':
    def df_to_dataset_training(features, labels, batch_size=32):
        # Convert categorical columns to strings before creating the dataset
        features = features.copy()
        for categorical_column in categorical_features:
            features[categorical_column] = features[categorical_column].astype(str)
        train_df = tf.data.Dataset.from_tensor_slices((dict(features), labels))
        train_df = train_df.batch(batch_size)
        return train_df
    train_df = df_to_dataset_training(X_train, y_train, batch_size=32)
    val_df = df_to_dataset_training(X_test, y_test, batch_size=32)
    return df, train_df, val_df, categorical_features, numeric_features, X_train, y_train, X_test, y_test, X, y
  
  elif mode == 'inference':
    def df_to_dataset_inference(df, batch_size=32):
        feature_df = df[categorical_features + numeric_features].copy()     
        for cat_feat in categorical_features:
            feature_df[cat_feat] = feature_df[cat_feat].astype(str)        
        inference_X = tf.data.Dataset.from_tensor_slices(dict(feature_df))
        inference_X = inference_X.batch(batch_size)
        return inference_X
    inference_X = df_to_dataset_inference(df, batch_size = 32)
    return df, inference_X
  else:
    raise ValueError("Mode must be either 'training' or 'inference'.")