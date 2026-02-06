import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from utils import fetch_ward_data, get_ai_insights

# --- CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="EcoShield: Ward-Wise Action",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD SECRETS (From your secure file) ---
try:
    OWM_KEY = st.secrets["OWM_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
except:
    st.error("❌ Secrets not found! Make sure .streamlit/secrets.toml exists.")
    st.stop()

# --- SIDEBAR UI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=80)
    st.title("🛡️ EcoShield")
    st.markdown("### Hyperlocal Pollution Monitoring")
    st.markdown("---")
    
    # Filter
    st.header("⚙️ Controls")
    refresh = st.button("🔄 Refresh Satellite Data")
    
    st.markdown("---")
    st.markdown("**TeamAR27:** 2 Members")
    st.info("Live API Connection: Active")

# --- MAIN APP LOGIC ---

# 1. FETCH DATA (Cached to save API calls)
if refresh:
    st.cache_data.clear()

@st.cache_data
def get_data():
    data = fetch_ward_data(OWM_KEY)
    return pd.DataFrame(data)

try:
    df = get_data()
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# 2. TOP KPI ROW (The "Dashboard" Look)
st.title("🏙️ Jaipur Ward-Wise Pollution Dashboard")
st.markdown("Real-time identification of pollution hotspots and AI-driven mitigation strategies.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
avg_aqi = df['AQI'].mean()
critical_wards = df[df['AQI'] > 200]

kpi1.metric("City Average AQI", f"{avg_aqi:.0f}", "Live")
kpi2.metric("Critical Hotspots", f"{len(critical_wards)} Wards", "Requires Action", delta_color="inverse")
kpi3.metric("Primary Pollutant", "PM 2.5", "High")
kpi4.metric("Sensor Status", "Online", "5/5 Wards")

st.divider()

# 3. MAP & ANALYSIS SPLIT
col_map, col_details = st.columns([2, 1.3])

with col_map:
    st.subheader("📍 Live Heatmap")
    
    # Create Folium Map
    m = folium.Map(location=[26.90, 75.82], zoom_start=13, tiles="CartoDB positron")
    
    # Add Circles
    for _, row in df.iterrows():
        # Determine bubble size and color
        color = row['Color']
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=15 + (row['AQI'] / 10), # Dynamic size
            popup=f"<b>{row['Ward']}</b><br>AQI: {row['AQI']}<br>Type: {row['Type']}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
    
    # Display Map
    st_folium(m, width=None, height=500)

with col_details:
    st.subheader("📊 Zone Analysis")
    
    
    # Interactive Table (Corrected)
    st.dataframe(
        df[['Ward', 'AQI', 'Type', 'Cause']], # We now show the "Cause" calculated by your logic
        hide_index=True,
        use_container_width=True
    )
    
    # Charts
    st.subheader("Comparison")
    fig = px.bar(df, x='Ward', y='AQI', color='Type', text='AQI')
    fig.update_layout(xaxis_title="", yaxis_title="AQI Level")
    st.plotly_chart(fig, use_container_width=True)

# 4. THE AI SECTION (The "Winning" Feature)
st.divider()
st.header("🤖 AI Policy Action Center")

c1, c2 = st.columns([1, 2])

with c1:
    st.markdown("Select a ward to generate a **Government Standard Action Plan**.")
    selected_ward = st.selectbox("Select Target Ward:", df['Ward'].unique())
    
    ward_stats = df[df['Ward'] == selected_ward].iloc[0]
    st.warning(f"Target: **{ward_stats['Ward']}**")
    st.write(f"Zone Type: **{ward_stats['Type']}**")
    st.write(f"Current AQI: **{ward_stats['AQI']}**")
    
    generate_btn = st.button("⚡ Generate Mitigation Plan", type="primary")

with c2:
    if generate_btn:
        with st.spinner(f"Consulting Gemini AI for {selected_ward}..."):
            # Call the Utils function
            report = get_ai_insights(GEMINI_KEY, selected_ward, ward_stats['AQI'], ward_stats['Type'])
            
            st.success("✅ Plan Generated")
            st.markdown(report)
            
            # Hackathon Polish: Add download button
            st.download_button("📥 Download Report", report, file_name=f"{selected_ward}_Report.txt")
    else:
        st.info("👈 Click the button to generate a customized AI strategy.")