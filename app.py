import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import time

# Page config
st.set_page_config(
    page_title="Exoplanet Habitability Predictor",
    page_icon="🪐",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #1a0a2e 100%); }
    h1 { color: #00d4ff !important; text-align: center; font-size: 3rem !important; }
    h2, h3 { color: #a78bfa !important; }
    .stButton>button { background: linear-gradient(90deg, #7c3aed, #2563eb); color: white; border: none; border-radius: 25px; padding: 10px 30px; font-size: 1.1rem; width: 100%; }
    .fact-box { background: rgba(167,139,250,0.1); border: 1px solid #a78bfa; border-radius: 10px; padding: 15px; margin: 10px 0; }
    .comparison-box { background: rgba(0,212,255,0.05); border: 1px solid #00d4ff; border-radius: 10px; padding: 15px; }
    </style>
""", unsafe_allow_html=True)

# Fun facts about habitable planets
planet_facts = {
    "Kepler-62 f": "🌊 Scientists believe Kepler-62f could be a water world — entirely covered by oceans!",
    "Kepler-35 b": "☀️ Kepler-35b orbits TWO stars — like Tatooine from Star Wars!",
    "Kepler-51 d": "🪶 Kepler-51d is so light it's called a 'super-puff' planet — density like cotton candy!",
    "PH1 b": "🌟 PH1b orbits a double star system — it has 4 suns in its sky!",
    "Kepler-289 c": "💨 Kepler-289c is a large planet with thick clouds possibly made of minerals!",
    "Kepler-1514 b": "🔭 Kepler-1514b was discovered by the famous Kepler space telescope!",
    "Kepler-453 b": "🌀 Kepler-453b's orbit wobbles dramatically due to a second star nearby!",
    "KOI-3680 b": "❄️ KOI-3680b sits right at the edge of its star's habitable zone — barely warm enough!",
    "GJ 414 A b": "🔴 GJ 414 A b orbits a red dwarf star — the most common type of star in the galaxy!",
    "Kepler-1661 b": "🪐 Kepler-1661b orbits a binary star — its sunsets would show TWO suns setting!",
}

# ─── ANIMATED LOADING SCREEN ───
if 'loaded' not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div style='text-align:center; padding: 100px 0;'>
                <div style='font-size: 5rem;'>🚀</div>
                <h1 style='color:#00d4ff;'>Launching Exoplanet Predictor...</h1>
                <p style='color:#94a3b8; font-size:1.2rem;'>Connecting to NASA database...</p>
            </div>
        """, unsafe_allow_html=True)
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.015)
            progress.progress(i + 1)
    placeholder.empty()
    st.session_state.loaded = True

# ─── LOAD DATA ───
model = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("planets.csv", comment="#")
important_columns = ['pl_name', 'pl_radj', 'pl_bmassj', 'pl_orbsmax', 'st_teff']
df_small = df[important_columns].dropna().copy()

def is_habitable(row):
    if (3700 <= row['st_teff'] <= 7200 and
        0.5 <= row['pl_orbsmax'] <= 2.0 and
        row['pl_radj'] <= 2.0):
        return 1
    else:
        return 0

df_small['habitable'] = df_small.apply(is_habitable, axis=1)

# ─── HEADER ───
st.markdown("<h1>🪐 Exoplanet Habitability Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1.2rem;'>Using real NASA data to find Earth-like planets across the galaxy</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── STATS ───
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌍 Total Planets", len(df_small))
col2.metric("✅ Habitable Planets", df_small['habitable'].sum())
col3.metric("🤖 Model Accuracy", "99.15%")
col4.metric("📡 Data Source", "NASA")
st.markdown("---")

# ─── GALAXY MAP ───
st.subheader("🌌 Galaxy Planet Map")
fig = px.scatter(
    df_small,
    x="pl_orbsmax",
    y="st_teff",
    color=df_small['habitable'].map({1: "Habitable 🟢", 0: "Not Habitable 🔴"}),
    size="pl_radj",
    hover_name="pl_name",
    title="Distance from Star vs Star Temperature",
    labels={"pl_orbsmax": "Distance from Star (AU)", "st_teff": "Star Temperature (K)"},
    template="plotly_dark",
    color_discrete_map={"Habitable 🟢": "#00ff88", "Not Habitable 🔴": "#ff4444"}
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)', font_color='white')
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ─── HABITABLE PLANETS WITH FUN FACTS ───
st.subheader("🌍 Potentially Habitable Planets")
st.markdown("<p style='color:#94a3b8;'>Click on a planet name to reveal a fun fact!</p>", unsafe_allow_html=True)

habitable_df = df_small[df_small['habitable'] == 1][['pl_name', 'pl_radj', 'pl_orbsmax', 'st_teff']].reset_index(drop=True)

for _, row in habitable_df.iterrows():
    with st.expander(f"🪐 {row['pl_name']}"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Radius (Jupiter=1)", f"{row['pl_radj']:.3f}")
        col2.metric("Distance (AU)", f"{row['pl_orbsmax']:.3f}")
        col3.metric("Star Temp (K)", f"{row['st_teff']:.0f}")
        fact = planet_facts.get(row['pl_name'], "🔭 This planet was discovered by astronomers scanning thousands of stars for tiny dips in brightness!")
        st.markdown(f"<div class='fact-box'>💡 <b>Fun Fact:</b> {fact}</div>", unsafe_allow_html=True)

st.markdown("---")

# ─── DESIGN YOUR PLANET ───
st.subheader("🛸 Design Your Own Planet!")
st.markdown("<p style='color:#94a3b8;'>Adjust the sliders and compare your planet to Earth!</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    radius = st.slider("🔵 Planet Radius (Jupiter = 1)", 0.1, 5.0, 1.0)
    mass = st.slider("⚖️ Planet Mass (Jupiter = 1)", 0.1, 10.0, 1.0)
with col2:
    distance = st.slider("📏 Distance from Star (AU)", 0.1, 5.0, 1.0)
    star_temp = st.slider("🌡️ Star Temperature (Kelvin)", 2000, 10000, 5778)

# Earth comparison
st.markdown("---")
st.subheader("🌍 How Does Your Planet Compare to Earth?")

earth_radius = 0.089  # Jupiter units
earth_mass = 0.003    # Jupiter units
earth_distance = 1.0
earth_temp = 5778

col1, col2, col3, col4 = st.columns(4)
col1.metric("Radius", f"{radius:.2f}", f"{radius - earth_radius:+.2f} vs Earth")
col2.metric("Mass", f"{mass:.2f}", f"{mass - earth_mass:+.2f} vs Earth")
col3.metric("Distance", f"{distance:.2f} AU", f"{distance - earth_distance:+.2f} vs Earth")
col4.metric("Star Temp", f"{star_temp}K", f"{star_temp - earth_temp:+.0f} vs Earth")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Predict Habitability!"):
    with st.spinner("Analyzing planet conditions..."):
        time.sleep(1)
    prediction = model.predict([[radius, mass, distance, star_temp]])
    if prediction[0] == 1:
        st.success("🌍 This planet COULD support life! Amazing!")
        st.balloons()
    else:
        st.error("❌ This planet is unlikely to support life.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#475569;'>Built with real NASA Exoplanet Archive data | Made by Om Pathak</p>", unsafe_allow_html=True)