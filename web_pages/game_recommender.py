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

# --- Function to get a live connection ---
def get_connection():
    global conn
    try:
        if conn and not conn.closed:
            return conn
    except NameError:
        pass
    conn = psycopg2.connect(dsn=CONN_ID)
    return conn

# --- Fetch games from DB with pagination ---
def fetch_games(search_query=None, limit=50, page=1):
    offset = (page - 1) * limit
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        if search_query:
            cursor.execute(
                "SELECT * FROM board_games WHERE name ILIKE %s ORDER BY name LIMIT %s OFFSET %s;",
                (f"%{search_query}%", limit, offset)
            )
        else:
            cursor.execute(
                "SELECT * FROM board_games ORDER BY name LIMIT %s OFFSET %s;",
                (limit, offset)
            )
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

# --- Get total count for pagination ---
def get_total_count(search_query=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        if search_query:
            cursor.execute("SELECT COUNT(*) FROM board_games WHERE name ILIKE %s;", (f"%{search_query}%",))
        else:
            cursor.execute("SELECT COUNT(*) FROM board_games;")
        total = cursor.fetchone()[0]
    return total

# --- Fetch recommendations including image URL ---
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

# --- Fetch all unique categories ---
def get_all_categories():
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute("SELECT DISTINCT unnest(string_to_array(categories, ',')) FROM board_games;")
        rows = cursor.fetchall()
    return sorted(set(r[0].strip() for r in rows if r[0]))

# --- Fetch all unique mechanics ---
def get_all_mechanics():
    conn = get_connection()
    with conn.cursor() as cursor:
        conn.rollback()
        cursor.execute("SELECT DISTINCT unnest(string_to_array(mechanics, ',')) FROM board_games;")
        rows = cursor.fetchall()
    return sorted(set(r[0].strip() for r in rows if r[0]))

# --- Pagination setup ---
PAGE_SIZE = 50
total_count = get_total_count()
total_pages = max(1, (total_count // PAGE_SIZE) + (1 if total_count % PAGE_SIZE > 0 else 0))

# --- Search bar and page number ---
col1, col2 = st.columns([8, 1])
with col1:
    search_query = st.text_input("🤔 Search for a game...", placeholder="Type a board game name...")
with col2:
    page = st.number_input("📄 Page", min_value=1, max_value=total_pages, value=1, step=1, format="%d")

# --- Filters arranged 2x2 with a small gap column ---
filter_col1, gap_col, filter_col2 = st.columns([4, 0.1, 4])

with filter_col1:
    # Playing time filter
    selected_time = st.slider(
        "⏱️ Playing Time (minutes)",
        min_value=0,
        max_value=500,
        value=(0, 500)
    )

    # Categories filter
    all_categories = get_all_categories()
    selected_categories = st.multiselect(
        "📂 Categories", options=all_categories
    )

with filter_col2:
    # Players filter
    selected_players = st.slider(
        "👥 Number of Players",
        min_value=1,
        max_value=20,
        value=(1, 20)
    )

    # Mechanics filter
    all_mechanics = get_all_mechanics()
    selected_mechanics = st.multiselect(
        "⚙️ Mechanics", options=all_mechanics
    )

st.divider()
st.title("🎲 Game Results")
st.divider()

# --- Fetch data for current page ---
df = fetch_games(search_query, limit=PAGE_SIZE, page=page)

# Filter out invalid image URLs
df = df[df['image_url'].notnull() & df['image_url'].str.startswith("http")]

# --- Apply filters ---
df = df[df['playingtime'].notnull()]
df = df[(df['playingtime'] >= selected_time[0]) & (df['playingtime'] <= selected_time[1])]

df = df[df['minplayers'].notnull() & df['maxplayers'].notnull()]
df = df[(df['minplayers'] <= selected_players[1]) & (df['maxplayers'] >= selected_players[0])]

if selected_categories:
    df = df[df['categories'].notnull()]
    df = df[df['categories'].apply(lambda x: any(cat.strip() in selected_categories for cat in x.split(",")))]

if selected_mechanics:
    df = df[df['mechanics'].notnull()]
    df = df[df['mechanics'].apply(lambda x: any(mech.strip() in selected_mechanics for mech in x.split(",")))]

# --- Display cards (Improved design, fixed font and ellipsis) ---
cards_per_row = 5
for start in range(0, len(df), cards_per_row):
    row_block = df.iloc[start:start+cards_per_row]
    cols = st.columns(cards_per_row)
    for i, (_, row) in enumerate(row_block.iterrows()):
        with cols[i]:
            minplayers = int(row['minplayers']) if pd.notnull(row['minplayers']) else None
            maxplayers = int(row['maxplayers']) if pd.notnull(row['maxplayers']) else None

            if minplayers is None and maxplayers is None:
                players_text = "Unknown"
            elif minplayers is not None and maxplayers is not None:
                players_text = f"{minplayers}" if minplayers == maxplayers else f"{minplayers} - {maxplayers}"
            elif minplayers is not None:
                players_text = f"{minplayers}"
            else:
                players_text = f"{maxplayers}"

            playingtime = f"{int(row['playingtime'])} mins" if pd.notnull(row['playingtime']) else "Unknown"

            recs = fetch_recommendations(row['id'], limit=4)  # ensure 4 recommendations
            rec_images = "".join(
                f"""
                <a href="{rec_url}" target="_blank" style="
                    display:block; 
                    min-width:120px;
                    margin-bottom:10px; 
                    color:#ff7f50; 
                    text-decoration:none; 
                    font-weight:bold;
                ">
                    <img src="{rec_img}" alt="{html.escape(rec_name, quote=True)}" title="{html.escape(rec_name, quote=True)}"
                        style="width:120px; height:80px; object-fit:cover; border-radius:5px; border:1px solid #ccc;">
                    <span style="display:block; text-align:left; font-size:0.85em; color:#ff7f50; font-weight:bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{html.escape(rec_name)}</span>
                </a>
                """ for rec_id, rec_name, rec_url, rec_img in recs if rec_img
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
                " onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 8px 20px rgba(0,0,0,0.25)';" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)';">
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
                        <p><b>Recommended Games:</b></p>
                        <div style="display:flex; flex-direction:column; gap:10px; padding:5px;">{rec_images}</div>
                    </details>
                </div>
                """,
                unsafe_allow_html=True
            )