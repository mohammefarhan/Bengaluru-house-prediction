# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from sklearn.ensemble import GradientBoostingRegressor

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Bengaluru House Price Predictor",
    layout="wide",
    page_icon="🏠"
)

# ==========================================
# PREMIUM UI STYLE
# ==========================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
    color:white;
}
.big-title{
    font-size:42px;
    font-weight:700;
    text-align:center;
}
.footer{
    text-align:center;
    margin-top:40px;
    color:#ddd;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# TRAIN MODEL SAFELY (NO PICKLE)
# ==========================================
@st.cache_resource
def load_model():

    df = pd.read_csv("Bengaluru_House_Data.csv")

    df = df.dropna(subset=["price"])
    df["bhk"] = df["size"].str.extract("(\d+)").astype(float)
    df["total_sqft"] = pd.to_numeric(df["total_sqft"], errors="coerce")

    df = df.dropna(subset=["bath","bhk","total_sqft","location","area_type"])

    # Reduce rare locations
    loc_counts = df["location"].value_counts()
    df["location"] = df["location"].apply(
        lambda x: x if loc_counts[x] >= 10 else "other"
    )

    X = df[["total_sqft","bath","bhk","area_type","location"]]
    y = df["price"]

    X = pd.get_dummies(X, drop_first=True)

    model = GradientBoostingRegressor()
    model.fit(X,y)

    return model, X.columns, sorted(df["location"].unique())

model, model_columns, location_list = load_model()

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="big-title">🏠 Premium Bengaluru House Price Predictor</div>',
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR INPUTS
# ==========================================
st.sidebar.header("Property Details")

total_sqft = st.sidebar.slider("Total Sqft",300,10000,1200)
bath = st.sidebar.slider("Bathrooms",1,10,2)
bhk = st.sidebar.slider("BHK",1,10,2)
balcony = st.sidebar.slider("Balcony",0,5,1)

# AREA TYPE DROPDOWN
area_type = st.sidebar.selectbox(
    "Area Type",
    ["Super built-up  Area","Built-up  Area","Plot  Area","Carpet  Area"]
)

# SEARCHABLE LOCATION DROPDOWN
location = st.sidebar.selectbox(
    "Location",
    location_list
)

# ==========================================
# PREDICT BUTTON
# ==========================================
center = st.columns([3,2,3])[1]
with center:
    predict = st.button("💰 Predict Premium Price")

# ==========================================
# RESULT DISPLAY
# ==========================================
if predict:

    # Create empty input row
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0

    input_df["total_sqft"] = total_sqft
    input_df["bath"] = bath
    input_df["bhk"] = bhk

    # set area type
    area_col = "area_type_" + area_type
    if area_col in input_df.columns:
        input_df[area_col] = 1

    # set location
    loc_col = "location_" + location
    if loc_col in input_df.columns:
        input_df[loc_col] = 1

    prediction = model.predict(input_df)[0]

    # PRICE CATEGORY
    if prediction < 80:
        label = "💚 Budget Property"
        glow = "#00ffae"
    elif prediction < 200:
        label = "🟡 Mid-Range Property"
        glow = "#ffd000"
    else:
        label = "🔥 Premium Property"
        glow = "#ff4d6d"

    components.html(f"""
    <div style="
        width:70%;
        margin:auto;
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        border-radius:22px;
        padding:45px;
        text-align:center;
        box-shadow:0 0 35px {glow};
        color:white;
        font-family:sans-serif;
    ">
        <h2>🏠 Estimated Property Value</h2>

        <h1 id="price" style="font-size:54px;font-weight:800;">₹ 0 Lakhs</h1>

        <div style="margin-top:10px;font-size:18px;">
            {label}
        </div>

        <div style="margin-top:20px;opacity:0.85;">
            📐 {total_sqft} sqft &nbsp;&nbsp;
            🛏 {bhk} BHK &nbsp;&nbsp;
            🛁 {bath} Bath &nbsp;&nbsp;
            🌇 {balcony} Balcony
        </div>
    </div>

    <script>
        let target = {round(prediction,2)};
        let count = 0;
        let speed = target / 40;

        function updateCounter(){{
            if(count < target){{
                count += speed;
                document.getElementById("price").innerHTML =
                    "₹ " + count.toFixed(2) + " Lakhs";
                setTimeout(updateCounter,20);
            }}else{{
                document.getElementById("price").innerHTML =
                    "₹ " + target.toFixed(2) + " Lakhs";
            }}
        }}
        updateCounter();
    </script>
    """, height=420)

# ==========================================
# FOOTER
# ==========================================
st.markdown('<div class="footer">Built with ❤️ by <b>Farhan</b></div>', unsafe_allow_html=True)
