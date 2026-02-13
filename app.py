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
    page_title="Ultra Premium Bengaluru Price Predictor",
    layout="wide",
    page_icon="🏠"
)

# ==========================================
# GLOBAL STYLE
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
    margin-bottom:15px;
}
.glass{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius:16px;
    padding:25px;
    box-shadow:0px 4px 25px rgba(0,0,0,0.25);
}
.metric-box{
    background: rgba(255,255,255,0.06);
    padding:15px;
    border-radius:12px;
    text-align:center;
}
.footer{
    text-align:center;
    margin-top:40px;
    padding:20px;
    font-size:16px;
    color:#dddddd;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD + TRAIN MODEL SAFELY (NO PICKLE)
# ==========================================
@st.cache_resource
def load_model():

    df = pd.read_csv("Bengaluru_House_Data.csv")

    # ---- Minimal preprocessing ----
    df = df.dropna(subset=["price"])
    df["bhk"] = df["size"].str.extract("(\d+)").astype(float)

    # simple sqft conversion
    df["total_sqft"] = pd.to_numeric(df["total_sqft"], errors="coerce")

    df = df.dropna(subset=["bath","bhk","total_sqft"])

    X = df[["total_sqft","bath","bhk"]]
    y = df["price"]

    model = GradientBoostingRegressor()
    model.fit(X,y)

    return model

model = load_model()

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="big-title">🏠 Ultra Premium Bengaluru House Price Predictor</div>',
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

# ==========================================
# SUMMARY CARD
# ==========================================
st.markdown('<div class="glass">', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)

c1.markdown(f'<div class="metric-box">📐 Sqft<br><b>{total_sqft}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-box">🛏 BHK<br><b>{bhk}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-box">🛁 Bath<br><b>{bath}</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-box">🌇 Balcony<br><b>{balcony}</b></div>', unsafe_allow_html=True)

st.write("")

# ==========================================
# PREDICT BUTTON
# ==========================================
center = st.columns([3,2,3])[1]
with center:
    predict = st.button("💰 Predict Premium Price")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# RESULT DISPLAY (ULTRA PREMIUM)
# ==========================================
if predict:

    input_df = pd.DataFrame([[total_sqft,bath,bhk]],
                            columns=["total_sqft","bath","bhk"])

    prediction = model.predict(input_df)[0]

    # CATEGORY LOGIC
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
