import streamlit as st
import pandas as pd
from transformers import pipeline
from io import BytesIO
import plotly.express as px
import os

### HEADERS ###
st.markdown(f'<div class="title-font">VERSATILE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">Text Classifier</div>', unsafe_allow_html=True)
st.markdown("""<hr style="border: none; height: 4px; background-color: white; margin: 10px 0;">""", unsafe_allow_html=True)

### SECTION SELECTION ###
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Versatile Text Classifier"

def set_section(section_name):
    st.session_state.selected_section = section_name

col1, col2 = st.columns([1, 1])
with col1:
    st.button("Versatile Text Classifier", key="btn_versatile_text_classifier", on_click=set_section, args=("Versatile Text Classifier",))
with col2:
    st.button("Description", key="btn_description_versatile_text_classifier", on_click=set_section, args=("Description Versatile Text Classifier",))

### STYLES ###
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
    [data-testid="stRadio"] label, 
    [data-testid="stRadio"] div[role="radiogroup"] > label,
    [data-testid="stRadio"] div[role="radiogroup"] label > div,
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stFileUploader"] label,
    [data-testid="stSelectbox"] label {
        color: white !important;
    }
    /* Target the file size text next to uploaded file name */
    [data-testid="stFileUploader"] small {
        color: gray !important;
        font-size: 14px !important;  /* Optional: adjust size */
        font-weight: 500 !important; /* Optional: adjust weight */
    }        
    </style>
""", unsafe_allow_html=True)

### MAIN SECTION ###
if st.session_state.get("selected_section") != "Description Versatile Text Classifier":
    st.title("Versatile Text Classifier")

    mode = st.radio("Choose input mode:", ["Typing field", "File with a text column (CSV/Excel)"])

    if mode == "Typing field" and "classified_data" in st.session_state:
        del st.session_state.classified_data

    data = None
    text = ""
    uploaded_file = None

    if mode == "File with a text column (CSV/Excel)":
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file:
            with st.spinner("Loading file..."):
                try:
                    if uploaded_file.name.endswith(".csv"):
                        data = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(".xlsx"):
                        data = pd.read_excel(uploaded_file)
                    else:
                        st.error("Unsupported file type.")
                        data = None
                    if data is not None:
                        st.write("Preview of loaded data:")
                        st.dataframe(data)
                except Exception as e:
                    st.error(f"Error loading file: {e}")
    else:
        text = st.text_area("Enter text to classify")

    ### LOAD CLASSIFIER ###
    def load_zero_shot_classifier():
        return pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
            tokenizer="typeform/distilbert-base-uncased-mnli",
            framework="pt"
        )

    classifier = load_zero_shot_classifier()


    ### LABELS ###
    if "labels" not in st.session_state:
        st.session_state.labels = []
    if "label_to_remove" not in st.session_state:
        st.session_state.label_to_remove = None

    if st.session_state.label_to_remove:
        try:
            st.session_state.labels.remove(st.session_state.label_to_remove)
        except ValueError:
            pass
        st.session_state.label_to_remove = None

    st.subheader("Classify by")

    def add_label():
        label = st.session_state.new_label_input.strip()
        if label and label not in st.session_state.labels:
            st.session_state.labels.append(label)
        st.session_state.new_label_input = ""

    st.text_input("Add a new label", key="new_label_input")
    st.button("Add Label", on_click=add_label)

    for i, label in enumerate(st.session_state.labels):
        cols = st.columns([8, 1])
        cols[0].write(label)
        if cols[1].button("✖", key=f"remove_label_{i}"):
            st.session_state.label_to_remove = label
            st.rerun()

    ### CLASSIFY TEXT FIELD ###
    if mode == "Typing field":
        if st.button("Classify"):
            if "classified_data" in st.session_state:
                del st.session_state.classified_data

            if text and st.session_state.labels:
                with st.spinner("Classifying..."):
                    result = classifier(text, candidate_labels=st.session_state.labels)

                def generate_highlighted_colors(scores, highlight_color="#ff5757", other_color="#1f1f1f"):
                    max_index = scores.index(max(scores))
                    return [highlight_color if i == max_index else other_color for i in range(len(scores))]

                colors = generate_highlighted_colors(result["scores"])

                fig = px.pie(
                    names=result["labels"],
                    values=result["scores"],
                    hole=0.55,
                    color_discrete_sequence=colors
                )

                fig.update_traces(
                    textinfo="label+percent",
                    textfont_size=16,
                    insidetextfont=dict(color="white"),
                    marker=dict(line=dict(color="#2f2f2f", width=2))
                )

                fig.update_layout(
                    paper_bgcolor="#2f2f2f",
                    plot_bgcolor="#2f2f2f",
                    showlegend=False,
                    font_color="white",
                    title={
                        "text": "Label Probabilities",
                        "x": 0.5,
                        "xanchor": "center",
                        "font": {"size": 24, "color": "white"}
                    },
                    margin=dict(t=100, b=80),
                    annotations=[
                        dict(
                            text=f"<b>Most probable</b><br>{result['labels'][0]}",
                            x=0.5,
                            y=0.5,
                            font=dict(size=14, color="white"),
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            align='center'
                        )
                    ]
                )

                st.plotly_chart(fig)

    ### CLASSIFY FILE COLUMN ###
    elif mode == "File with a text column (CSV/Excel)":
        if data is not None:
            st.subheader("Choose the Textual Column to be Classified")
            text_columns = data.select_dtypes(include=["object", "string"]).columns
            text_column = st.selectbox("Select the column to classify", text_columns)

            if st.button("Classify Column") and text_column and st.session_state.labels:
                predictions, scores = [], []
                with st.spinner("Classifying each row..."):
                    for text_entry in data[text_column].astype(str):
                        result = classifier(text_entry, candidate_labels=st.session_state.labels)
                        predictions.append(result["labels"][0])
                        scores.append(round(result["scores"][0], 3))

                data[f"Label - {text_column}"] = predictions
                data[f"Label Probability (Ratio) - {text_column}"] = scores
                data[f"Label Probability (%) - {text_column}"] = [f"{round(score * 100, 1)}%" for score in scores]
                st.session_state.classified_data = data.copy()

    ### SHOW CLASSIFIED TABLE ###
    if "classified_data" in st.session_state:
        st.subheader("Result")
        st.dataframe(st.session_state.classified_data)

        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Results')
            return output.getvalue()

        csv_data = convert_df_to_csv(st.session_state.classified_data)
        excel_data = convert_df_to_excel(st.session_state.classified_data)
        filename_without_extension = os.path.splitext(uploaded_file.name)[0] if uploaded_file else "classified_data"

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Download as CSV", data=csv_data, file_name=f"{filename_without_extension}_classified_data.csv", mime="text/csv")
        with col2:
            st.download_button("Download as Excel", data=excel_data, file_name=f"{filename_without_extension}_classified_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

### DESCRIPTION ###
else:
    st.title("Description of the Project")
    st.markdown("""<div style='color: white;'>
        This classifier is aimed to provide a versatile classification of textual data based on specified labels from you. Write down your desired labels & the classifier will show you the most probable label based on the percentage. Input can be given in an Excel or CSV file with a single textual column or can be typed within a text field. This can be specified in the "Choose input mode" section. To add a classification label, type it within the field "Add a new label" & press "Add Label" button. The label will appear underneath the "Add Label" button. You may also erase the label by clicking the "X" button on the right side of the specified label. After the labels have been selected, you can classify the textual content.
    </div>""", unsafe_allow_html=True)
