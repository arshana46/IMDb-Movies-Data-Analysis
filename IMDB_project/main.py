import streamlit as st
import pandas as pd
from PIL import Image
import base64

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="IMDb Movies Data Analysis", layout="wide")

# ----------------------------
# Background Image
# ----------------------------
def set_bg_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }}
        .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

bg_image_path = r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\imdb.jpg"
set_bg_image(bg_image_path)

# ----------------------------
# Title
# ----------------------------
st.markdown("<h1 style='color:white'>🎬 IMDb Movies Data Analysis</h1>", unsafe_allow_html=True)

# ----------------------------
# Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\imdb_kaggle.csv")
    return df

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Movies")

# Year filter
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# IMDb rating filter
min_rating, max_rating = st.sidebar.slider("IMDb Rating Range", 0.0, 10.0, (0.0, 10.0))

# Age rating filter
age_ratings = sorted(df['age_limit'].dropna().unique())
selected_age = st.sidebar.multiselect("Select Age Rating(s)", age_ratings, default=age_ratings)

# Apply filters
filtered_df = df[
    (df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) &
    (df['rating'] >= min_rating) & (df['rating'] <= max_rating) &
    (df['age_limit'].isin(selected_age))
]

# ----------------------------
# Display Filtered Table
# ----------------------------
st.subheader("🔎 Filtered Movies")
st.write(f"Showing **{filtered_df.shape[0]}** movies after filtering.")
st.dataframe(filtered_df[['name', 'year', 'rating', 'Metascore', 'duration', 'age_limit']])

# ----------------------------
# Display Chart Images
# ----------------------------
st.subheader("📊 IMDb Analysis Charts")

charts = [
    ('Distribution of IMDb Ratings', r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\imdbdistribution.png"),
    ('Average IMDb Rating by Year', r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\AverageRating.png"),
    ('Movie Duration vs IMDb Rating', r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\movie_duration_distribution.png"),
    ('Correlation Heatmap', r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\correlation.png"),
    ('Metascore vs IMDb Rating', r"C:\Users\arsha\OneDrive\Desktop\IMDB_project\Metascore_imdb_distribution.png")
]

for title, path in charts:
    st.markdown(f"<h3 style='color:white'>{title}</h3>", unsafe_allow_html=True)
    img = Image.open(path)
    st.image(img, use_container_width=True)

# ----------------------------
# Key Insights
# ----------------------------
st.subheader("💡 Key Insights")
st.markdown("""
<div style="color:white">
- Strong correlation between IMDb Rating and Metascore ✅<br>
- Movie duration has minimal effect on ratings ⏱️<br>
- Older films and 18+ movies tend to have higher ratings 🎥
</div>
""", unsafe_allow_html=True)


