import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
import base64
from PIL import Image
import requests
from io import BytesIO

### HEADERS ###
st.markdown(f'<div class="title-font">BANGKOK AIRBNB</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-font">Recommender & Report</div>', unsafe_allow_html=True)
st.markdown("""<hr style="border: none; height: 4px; background-color: white; margin: 10px 0;">""", unsafe_allow_html=True)

### SECTION SELECTION ###
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Bangkok AirBnB Recommender"

def set_section(section_name):
    st.session_state.selected_section = section_name

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("Recommender", key="btn_bangkok_airbnb_recommender", on_click=set_section, args=("Bangkok AirBnB Recommender",))
with col2:
    st.button("Report", key="btn_bangkok_airbnb_report", on_click=set_section, args=("Bangkok AirBnB Report",))
with col3:
    st.button("Description", key="btn_bangkok_airbnb_recommender_and_report", on_click=set_section, args=("Description Bangkok AirBnB Recommender & Report",))

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

df_original = pd.read_csv("./data/bangkok_airbnb_listings.csv")

def resize_then_crop_center_rectangle(img, target_width, target_height):
    width, height = img.size
    aspect_ratio_original = width / height
    aspect_ratio_target = target_width / target_height
    if aspect_ratio_original > aspect_ratio_target:
        new_height = target_height
        new_width = int(aspect_ratio_original * target_height)
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio_original)
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img_cropped = img_resized.crop((left, top, right, bottom))
    return img_cropped

@st.cache_data(show_spinner=False)
def recommend_bangkok_airbnb(df, user_chosen_listing_id, top_n=5):
    ### FEATURE ENGINEERING ###
        df_original = df.copy()
        df["host_since"] = pd.to_datetime(df["host_since"], errors='coerce')
        df["host_since_year"] = df["host_since"].dt.year
        df["host_since_month"] = df["host_since"].dt.month
        df["host_since_day"] = df["host_since"].dt.day
        true_false_map = {"t":1,"f":0}
        df["host_is_superhost"] = df["host_is_superhost"].map(true_false_map)
        df["instant_bookable"] = df["instant_bookable"].map(true_false_map)
        df["host_identity_verified"] = df["host_identity_verified"].map(true_false_map)
        response_time_map = {"within an hour":0, "within a few hours":1, "within a day":2, "a few days or more":3}
        df["host_response_time"] = df["host_response_time"].map(response_time_map)
        df["host_verification_phone"] = df["host_verifications"].astype(str).apply(lambda x: 1 if "phone" in x.lower() else 0)
        df["host_verification_email"] = df["host_verifications"].astype(str).apply(lambda x: 1 if "email" in x.lower() else 0)
        df["amenities_internet_connection"] = df["amenities"].astype(str).apply(lambda x: 1 if "wifi" in x.lower() or "ethernet connection" in x.lower() else 0)
        df["amenities_gym"] = df["amenities"].astype(str).apply(lambda x: 1 if "gym" in x.lower() else 0)
        df["amenities_tv"] = df["amenities"].astype(str).apply(lambda x: 1 if "TV" in x else 0)
        df["amenities_hot_tub"] = df["amenities"].astype(str).apply(lambda x: 1 if "hot tub" in x.lower() else 0)
        df["amenities_pool"] = df["amenities"].astype(str).apply(lambda x: 1 if "pool" in x.lower() else 0)
        df["amenities_elevator"] = df["amenities"].astype(str).apply(lambda x: 1 if "elevator" in x.lower() else 0)
        df["amenities_air_conditioning"] = df["amenities"].astype(str).apply(lambda x: 1 if "air conditioning" in x.lower() else 0)
        df["amenities_housekeeping"] = df["amenities"].astype(str).apply(lambda x: 1 if "housekeeping" in x.lower() else 0)
        df["amenities_parking"] = df["amenities"].astype(str).apply(lambda x: 1 if "parking" in x.lower() else 0)
        df["amenities_long_term_stay_allowed"] = df["amenities"].astype(str).apply(lambda x: 1 if "long term stays allowed" in x.lower() else 0)
        df["amenities_microwave"] = df["amenities"].astype(str).apply(lambda x: 1 if "microwave" in x.lower() else 0)
        df["amenities_kitchen"] = df["amenities"].astype(str).apply(lambda x: 1 if "kitchen" in x.lower() else 0)
        df["amenities_stove"] = df["amenities"].astype(str).apply(lambda x: 1 if "stove" in x.lower() else 0)
        df["amenities_self_checkin"] = df["amenities"].astype(str).apply(lambda x: 1 if "self check-in" in x.lower() else 0)
        df["amenities_hair_dryer"] = df["amenities"].astype(str).apply(lambda x: 1 if "hair dryer" in x.lower() else 0)
        df["amenities_smoke_alarm"] = df["amenities"].astype(str).apply(lambda x: 1 if "smoke alarm" in x.lower() else 0)
        df["amenities_dedicated_workspace"] = df["amenities"].astype(str).apply(lambda x: 1 if "dedicated workspace" in x.lower() else 0)
        df["amenities_shower_gel"] = df["amenities"].astype(str).apply(lambda x: 1 if "shower gel" in x.lower() or "body soap" in x.lower() else 0)
        df["amenities_shampoo"] = df["amenities"].astype(str).apply(lambda x: 1 if "shampoo" in x.lower() else 0)
        df["amenities_sauna"] = df["amenities"].astype(str).apply(lambda x: 1 if "sauna" in x.lower() else 0)
        df["amenities_first_aid_kit"] = df["amenities"].astype(str).apply(lambda x: 1 if "first aid kit" in x.lower() else 0)
        df["amenities_refrigerator"] = df["amenities"].astype(str).apply(lambda x: 1 if "refrigerator" in x.lower() or "freezer" in x.lower() else 0)
        df["amenities_board_games"] = df["amenities"].astype(str).apply(lambda x: 1 if "board games" in x.lower() else 0)
        df["amenities_AC"] = df["amenities"].astype(str).apply(lambda x: 1 if "air conditioning" in x.lower() else 0)
        df["amenities_hangers"] = df["amenities"].astype(str).apply(lambda x: 1 if "hangers" in x.lower() else 0)
        df["amenities_heating"] = df["amenities"].astype(str).apply(lambda x: 1 if "heating" in x.lower() else 0)
        df["amenities_keypad"] = df["amenities"].astype(str).apply(lambda x: 1 if "keypad" in x.lower() else 0)
        df["amenities_fire_extinguisher"] = df["amenities"].astype(str).apply(lambda x: 1 if "fire extinguisher" in x.lower() else 0)
        df["amenities_patio_balcony"] = df["amenities"].astype(str).apply(lambda x: 1 if "balcony" in x.lower() or "patio" in x.lower() else 0)
        review_score_cols = [col for col in df.columns if col.startswith("review_scores_")]
        df[review_score_cols] = df[review_score_cols] / 5.0
    ### OMITTING UNWANTED COLUMNS ###
        df.drop(columns=[
            "listing_url","scrape_id","last_scraped","source","name",
            "description","neighborhood_overview","picture_url","host_url",
            "host_name","host_location","host_about","host_picture_url",
            "host_thumbnail_url","host_since","license", "host_has_profile_pic",
            "host_verifications","bathrooms_text", "has_availability","first_review",
            "last_review", "minimum_minimum_nights","maximum_minimum_nights","minimum_maximum_nights",
            "maximum_maximum_nights","calendar_last_scraped","minimum_nights_avg_ntm",
            "maximum_nights_avg_ntm","calendar_updated","estimated_occupancy_l365d",
            "estimated_revenue_l365d","neighbourhood_group_cleansed","host_neighbourhood",
            "neighbourhood", "amenities", "number_of_reviews_ltm", "number_of_reviews_l30d", "availability_eoy", "number_of_reviews_ly"], inplace=True)
    ### STANDARDIZING NUMERICAL FEATURES & ENCODING STRING VARIABLES ###
        item_id = ["id"]
        numerical_cols = ["host_id", "host_response_time", "host_response_rate", "host_acceptance_rate", "host_listings_count", "host_total_listings_count", "latitude", "longitude", "accommodates", "bathrooms", "bedrooms", "beds", "price", "minimum_nights", "maximum_nights", "availability_30", "availability_60", "availability_90", "availability_365", "number_of_reviews", "calculated_host_listings_count", "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms", "reviews_per_month", "host_since_year", "host_since_month", "host_since_day"]
        categorical_cols = ["neighbourhood_cleansed", "property_type", "room_type"]
        binary__or_standardized_cols = ["host_is_superhost", "host_identity_verified", "instant_bookable"] + [col for col in df.columns if col.startswith("amenities_")] + [col for col in df.columns if col.startswith("host_verification_")] + [col for col in df.columns if col.startswith("review_scores_")]
        df[numerical_cols] = df[numerical_cols].fillna(-1)
        df[categorical_cols] = df[categorical_cols].fillna(-1)
        df[binary__or_standardized_cols] = df[binary__or_standardized_cols].fillna(-1)
        def get_feature_names(preprocessor):
                num_features = numerical_cols
                cat_features = []
                cat_ohe = preprocessor.named_transformers_["cat"]
                if hasattr(cat_ohe, "get_feature_names_out"):
                    cat_features = cat_ohe.get_feature_names_out(categorical_cols).tolist()
                else:
                    cat_features = categorical_cols
                bin_features = binary__or_standardized_cols
                return item_id + num_features + cat_features + bin_features
        preprocessor = ColumnTransformer(transformers=[
        ("item_id", "passthrough", item_id),
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("bin", "passthrough", binary__or_standardized_cols)])
        df_values = preprocessor.fit_transform(df)
        all_variables = get_feature_names(preprocessor)
        df = pd.DataFrame(df_values.toarray() if hasattr(df_values, "toarray") else df_values, columns=all_variables)
        item_ids = df["id"].values
        features = df.drop(columns=["id"])
        cosine_sim = cosine_similarity(features)
        idx = list(item_ids).index(user_chosen_listing_id)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        recommended_listing_ids = [int(item_ids[i]) for i, _ in sim_scores]
        df_recommended_listing_ids = pd.DataFrame(data=recommended_listing_ids, columns=['id'])
        df_recommendation = pd.merge(df_original, df_recommended_listing_ids, how = 'inner', on = 'id')
        df_recommendation = df_recommendation[["listing_url", "picture_url", "name", "description","room_type","neighbourhood_cleansed","accommodates", "bedrooms","beds","price", "number_of_reviews", "review_scores_rating"]]
        return df_recommendation

def pil_image_to_base64(img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode()

### REPORT ###
if st.session_state.get("selected_section") == "Bangkok AirBnB Report":
    st.title("Report")

### DESCRIPTION ###
if st.session_state.get("selected_section") == "Description Bangkok AirBnB Recommender & Report":
    st.title("Description")
    st.markdown("""<div style='color: white;'>
        ...
    </div>""", unsafe_allow_html=True)

### RECOMMENDER ###
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


if "preview_indices" not in st.session_state or "preview_index_pos" not in st.session_state:
    df_original_for_init = pd.read_csv("./data/bangkok_airbnb_listings.csv").dropna(subset=["picture_url"])
    st.session_state.preview_indices = df_original_for_init.sample(frac=1, random_state=42).index.tolist()
    st.session_state.preview_index_pos = 0

if st.session_state.selected_section == "Bangkok AirBnB Recommender":
    st.title("Recommender")

    df_original = pd.read_csv("./data/bangkok_airbnb_listings.csv").dropna(subset=["picture_url"])
    current_index = st.session_state.preview_indices[st.session_state.preview_index_pos]
    listing = df_original.loc[current_index]

    response_main_img = requests.get(listing["picture_url"])
    main_img = Image.open(BytesIO(response_main_img.content)).convert("RGB")
    main_img_cropped = resize_then_crop_center_rectangle(main_img, 2000, 600)
    st.image(main_img_cropped, use_container_width=True)

    nav_col1, nav_col2 = st.columns([1, 1])
    with nav_col1:
        btn_left = st.button("◀", key="left_swipe", help="Previous", use_container_width=True)
    with nav_col2:
        btn_right = st.button("▶", key="right_swipe", help="Next", use_container_width=True)
    if btn_left:
        st.session_state.preview_index_pos = (st.session_state.preview_index_pos - 1) % len(st.session_state.preview_indices)
    if btn_right:
        st.session_state.preview_index_pos = (st.session_state.preview_index_pos + 1) % len(st.session_state.preview_indices)

    if pd.isna(listing['price']):
        listing_price_text_formatted = "Unknown"
    else:
        try:
            listing_price_text_formatted = f"{int(listing['price'])} USD/month"
        except:
            listing_price_text_formatted = "Unknown"

    if pd.isna(listing['review_scores_rating']):
        listing_review_score_text_formatted = "Unknown"
    else:
        try:
            listing_review_score_text_formatted = round(float(listing['review_scores_rating']),1)
        except:
            listing_review_score_text_formatted = "Unknown"

    st.markdown(f"""
        <div style="text-align: center;">
            <h4><b>{listing['name']}</b></h4>
            <p><b>Room Type:</b> {listing['room_type']} | <b>Neighborhood:</b> {listing['neighbourhood_cleansed']} | <b>Price:</b> {listing_price_text_formatted} | <b>Rating:</b> {listing_review_score_text_formatted}</p>
            <p><a href="{listing["listing_url"]}" target="_blank" style="color: coral; text-decoration: none; font-size: 22px;"><b>Check me out<b></a></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    with st.spinner("Loading recommendations..."):
        df_recommendation = recommend_bangkok_airbnb(df=df_original, user_chosen_listing_id=listing["id"], top_n=5)
    st.markdown("## What about these?")

    number_of_recommendations = len(df_recommendation)
    if number_of_recommendations is not None and number_of_recommendations >= 1:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(df_recommendation):
                r = df_recommendation.iloc[i]
                with col:
                    try:
                        response = requests.get(r["picture_url"], timeout=5)
                        img = Image.open(BytesIO(response.content)).convert("RGB")
                        img_cropped = resize_then_crop_center_rectangle(img, 1000, 1000)
                        img_base64 = pil_image_to_base64(img_cropped)
                        img_html = f'<img src="data:image/png;base64,{img_base64}" width="300" style="border-radius: 24px;" />'
                    except Exception as e:
                        img_html = '<div style="width:300px; height:300px; background:#eee; display:flex; align-items:center; justify-content:center;">Image Unavailable</div>'

                    try:
                        price = f"{int(r['price'])} USD/month" if not pd.isna(r['price']) else "Unknown"
                    except:
                        price = "Unknown"

                    try:
                        score = round(float(r['review_scores_rating']), 1) if not pd.isna(r['review_scores_rating']) else "Unknown"
                    except:
                        score = "Unknown"

                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            {img_html}
                            <h5>{r.get('name', 'No name')}</h5>
                            <p>{r.get('neighbourhood_cleansed', 'Unknown')}</p>
                            <p>{price}</p>
                            <p>{score}</p>
                            <a href="{r.get("listing_url", "#")}" style="color: coral; text-decoration: none;">View</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    else:
        st.text("Couldn't find any similar AirBnB in Bangkok.")

