import streamlit as st
import psycopg2
import pandas as pd
import html

st.title("🎲 Board Game Searcher & Recommender")

# --- Inject CSS to make labels white and hide slider min/max numbers ---
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] label, 
    div[data-testid="stNumberInput"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stSlider"] label {
        color: white !important;
    }

    /* Hide slider min/max numbers below track */
    div[data-testid="stSlider"] div[role="presentation"] > div[2] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

CONN_ID = st.secrets["conn_id"]

# --- Database connection ---
def get_connection():
    global conn
    try:
        if conn and not conn.closed:
            return conn
    except NameError:
        pass
    conn = psycopg2.connect(dsn=CONN_ID)
    return conn

# --- Fetch games dynamically ---
def fetch_games(filters, limit=50, page=1):
    offset = (page - 1) * limit
    conn = get_connection()
    conditions = []
    params = []

    if filters.get("search"):
        conditions.append("name ILIKE %s")
        params.append(f"%{filters['search']}%")

    conditions.append("playingtime BETWEEN %s AND %s")
    params.extend([filters["time_min"], filters["time_max"]])

    conditions.append("minplayers <= %s AND maxplayers >= %s")
    params.extend([filters["players_max"], filters["players_min"]])

    if filters.get("categories"):
        conditions.append(
            "EXISTS (SELECT 1 FROM unnest(string_to_array(categories, ',')) AS cat WHERE cat = ANY(%s))"
        )
        params.append(filters["categories"])

    if filters.get("mechanics"):
        conditions.append(
            "EXISTS (SELECT 1 FROM unnest(string_to_array(mechanics, ',')) AS mech WHERE mech = ANY(%s))"
        )
        params.append(filters["mechanics"])

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM board_games {where_clause} ORDER BY name LIMIT %s OFFSET %s;"
    params.extend([limit, offset])

    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

# --- Get total count dynamically ---
def get_total_count(filters):
    conn = get_connection()
    conditions = []
    params = []

    if filters.get("search"):
        conditions.append("name ILIKE %s")
        params.append(f"%{filters['search']}%")

    conditions.append("playingtime BETWEEN %s AND %s")
    params.extend([filters["time_min"], filters["time_max"]])

    conditions.append("minplayers <= %s AND maxplayers >= %s")
    params.extend([filters["players_max"], filters["players_min"]])

    if filters.get("categories"):
        conditions.append(
            "EXISTS (SELECT 1 FROM unnest(string_to_array(categories, ',')) AS cat WHERE cat = ANY(%s))"
        )
        params.append(filters["categories"])

    if filters.get("mechanics"):
        conditions.append(
            "EXISTS (SELECT 1 FROM unnest(string_to_array(mechanics, ',')) AS mech WHERE mech = ANY(%s))"
        )
        params.append(filters["mechanics"])

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT COUNT(*) FROM board_games {where_clause};"
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute(query, params)
        total = cursor.fetchone()[0]
    return total

# --- Fetch recommendations ---
def fetch_recommendations(game_id, limit=5):
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute(
            """
            SELECT b.id, b.name, b.url, b.image_url
            FROM board_games_recommendations r
            JOIN board_games b ON r.rec_id = b.id
            WHERE r.source_id = %s
            LIMIT %s;
            """,
            (game_id, limit)
        )
        recs = cursor.fetchall()
    return recs

# --- Fetch all unique categories and mechanics ---
def get_all_categories():
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute("SELECT DISTINCT unnest(string_to_array(categories, ',')) FROM board_games;")
        rows = cursor.fetchall()
    return sorted(set(r[0].strip() for r in rows if r[0]))

def get_all_mechanics():
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute("SELECT DISTINCT unnest(string_to_array(mechanics, ',')) FROM board_games;")
        rows = cursor.fetchall()
    return sorted(set(r[0].strip() for r in rows if r[0]))

# --- UI Filters ---
search_query = st.text_input("🤔 Search for a game...", placeholder="Type a board game name...")

filter_col1, gap_col, filter_col2 = st.columns([4, 0.1, 4])
with filter_col1:
    selected_time = st.slider("⏱️ Playing Time (minutes)", 0, 500, (0, 500))
    all_categories = get_all_categories()
    selected_categories = st.multiselect("📂 Categories", options=all_categories)
with filter_col2:
    selected_players = st.slider("👥 Number of Players", 1, 20, (1, 20))
    all_mechanics = get_all_mechanics()
    selected_mechanics = st.multiselect("⚙️ Mechanics", options=all_mechanics)

# --- Prepare filters ---
filters = {
    "search": search_query,
    "time_min": selected_time[0],
    "time_max": selected_time[1],
    "players_min": selected_players[0],
    "players_max": selected_players[1],
    "categories": selected_categories if selected_categories else None,
    "mechanics": selected_mechanics if selected_mechanics else None,
}

# --- Session state: reset page if filters changed ---
if "last_filters" not in st.session_state:
    st.session_state.last_filters = filters
    st.session_state.page = 1

if filters != st.session_state.last_filters:
    st.session_state.page = 1
    st.session_state.last_filters = filters

# --- Pagination setup ---
PAGE_SIZE = 50
total_count = get_total_count(filters)
total_pages = max(1, (total_count // PAGE_SIZE) + (1 if total_count % PAGE_SIZE > 0 else 0))
current_page = min(st.session_state.page, total_pages)

# --- Page input ---
page = st.number_input("📄 Page", min_value=1, max_value=total_pages, value=current_page, step=1, format="%d", key="page")

st.divider()
st.title("🎲 Game Results")
st.divider()

# --- Fetch current page games ---
df = fetch_games(filters, limit=PAGE_SIZE, page=page)
df = df[df['image_url'].notnull() & df['image_url'].str.startswith("http")]

# --- Display cards ---
cards_per_row = 5
for start in range(0, len(df), cards_per_row):
    row_block = df.iloc[start:start+cards_per_row]
    cols = st.columns(cards_per_row)
    for i, (_, row) in enumerate(row_block.iterrows()):
        with cols[i]:
            minplayers = int(row['minplayers']) if pd.notnull(row['minplayers']) else None
            maxplayers = int(row['maxplayers']) if pd.notnull(row['maxplayers']) else None
            players_text = (
                "Unknown" if minplayers is None and maxplayers is None else
                f"{minplayers}" if minplayers == maxplayers else
                f"{minplayers} - {maxplayers}"
            )
            playingtime = f"{int(row['playingtime'])} mins" if pd.notnull(row['playingtime']) else "Unknown"

            # --- Recommended games block ---
            recs = fetch_recommendations(row['id'], limit=4)
            rec_images = "".join(
                f'<div style="text-align:center; margin-bottom:10px;">'
                f'<a href="{rec_url}" target="_blank" style="display:block; text-decoration:none;">'
                f'<img src="{rec_img}" alt="{html.escape(rec_name, quote=True)}" title="{html.escape(rec_name, quote=True)}" '
                f'style="width:100%; height:150px; object-fit:cover; border-radius:5px; border:1px solid #ccc;">'
                f'<span style="display:block; text-align:center; font-size:0.85em; color:#ff7f50; font-weight:bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">'
                f'{html.escape(rec_name)}</span>'
                f'</a></div>'
                for rec_id, rec_name, rec_url, rec_img in recs if rec_img
            ) if recs else "<p>No recommendations available.</p>"

            st.markdown(
                f"""
                <div style="
                    border-radius:15px;
                    padding:15px;
                    margin-bottom:15px;
                    background: linear-gradient(to bottom, #fefefe, #f2f2f2);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    text-align:center;
                    transition: transform 0.2s, box-shadow 0.2s;
                    color:#333;
                ">
                    <a href="{row['url']}" target="_blank" style="text-decoration:none;">
                        <img src="{row['image_url']}" alt="{row['name']}" 
                            style="width:100%; height:250px; object-fit:cover; border-radius:15px;">
                    </a>
                    <details style="padding:10px; text-align:left;">
                        <summary style="
                            font-size:1.1em; 
                            font-weight:bold; 
                            color:#ff7f50; 
                            cursor:pointer;
                            margin-bottom:5px;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">
                            {row['name']}
                        </summary>
                        <p><b>Players:</b> {players_text}</p>
                        <p><b>Playing time:</b> {playingtime}</p>
                        <p><b>Categories:</b> {row['categories']}</p>
                        <p><b>Mechanics:</b> {row['mechanics']}</p>
                        <p><a href="{row['url']}" target="_blank" style="
                            display:block; 
                            width:100%;
                            padding:10px 0; 
                            background-color:#ff7f50; 
                            color:white; 
                            border-radius:5px; 
                            text-decoration:none;
                            font-weight:bold;
                            text-align:center;
                        ">
                            🔗 Check out this game!
                        </a></p>
                        <hr>
                        <p style="font-size: clamp(0.8em, 2.5vw, 1.5em); font-weight:bold; margin:5px 0;text-align: center;">Recommended Games</p>
                        <p></p>
                        <div style="display:flex; flex-direction:column; gap:10px; width:100%;">{rec_images}</div>
                    </details>
                </div>
                """,
                unsafe_allow_html=True
            )
