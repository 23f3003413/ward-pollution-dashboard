import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from utils import PollutionEngine

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="EcoSense Enterprise",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR "INDUSTRY LOOK" ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #30333d;
        border-radius: 5px;
        padding: 15px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0e1117;
        border-radius: 4px;
        color: white;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE ENGINE ---
try:
    engine = PollutionEngine(st.secrets["OWM_KEY"], st.secrets["GEMINI_KEY"])
except (FileNotFoundError, KeyError):
    st.error("🚨 System Error: Secrets file missing or keys invalid. Please configure .streamlit/secrets.toml")
    st.stop()

# --- HEADER SECTION ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🌍 EcoSense: Hyperlocal Air Intelligence")
    st.caption(f"System Status: Online | Monitoring Nodes: Active")
with c2:
    if st.button("🔄 Force Satellite Refresh"):
        st.cache_data.clear()
        st.rerun()

# --- DATA FETCHING ---
@st.cache_data
def load_data():
    return engine.generate_live_data()

df = load_data()

# --- DASHBOARD TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Live Command Center", "📈 Trend Analytics", "🛠️ Governance Cockpit"])

# === TAB 1: LIVE MAP & METRICS ===
with tab1:
    # KPI ROW
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("City Average AQI", int(df['AQI'].mean()), delta=f"{int(df['AQI'].mean() - 140)} vs Baseline")
    k2.metric("Critical Hotspots", len(df[df['AQI'] > 200]), "Severe Zones", delta_color="inverse")
    k3.metric("Dominant Cause", df['Cause'].mode()[0])
    k4.metric("Active Sensors", f"{len(df)}/7", "100% Uptime")

    st.markdown("---")
    
    # MAP & TABLE SPLIT
    col_map, col_data = st.columns([1.8, 1.2])
    
    with col_map:
        st.subheader("📍 Geospatial Pollution Heatmap")
        m = folium.Map(location=[26.90, 75.82], zoom_start=12, tiles="CartoDB dark_matter")
        
        for _, row in df.iterrows():
            # Advanced Tooltip HTML
            html = f"""
            <div style="font-family: sans-serif; width: 150px;">
                <b>{row['Ward']}</b><br>
                AQI: {row['AQI']} ({row['Status']})<br>
                <hr style="margin: 5px 0;">
                <small>{row['Cause']}</small>
            </div>
            """
            popup = folium.Popup(html, max_width=200)
            
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=10 + (row['AQI'] / 15),
                color=row['Color'],
                fill=True,
                fill_color=row['Color'],
                fill_opacity=0.6,
                popup=popup
            ).add_to(m)
        
        st_folium(m, width=None, height=500)

    with col_data:
        st.subheader("📋 Zonal Breakdown")
        st.dataframe(
            df[['Ward', 'AQI', 'Type', 'Cause']],
            hide_index=True,
            use_container_width=True,
            height=500
        )

# === TAB 2: ANALYTICS ===
with tab2:
    st.subheader("📉 Temporal Comparisons")
    
    # 1. Comparison Bar Chart
    fig_bar = px.bar(
        df, x='Ward', y=['PM2.5', 'NO2'], 
        title="Pollutant Composition by Ward",
        barmode='group',
        color_discrete_sequence=['#00CC96', '#EF553B']
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 2. Historical Trend (Simulated)
    st.subheader("⏳ 24-Hour Trend Analysis")
    selected_ward_trend = st.selectbox("Select Ward for Historical Data:", df['Ward'].unique())
    
    history_df = engine.generate_historical_trends(selected_ward_trend)
    
    fig_line = px.area(
        history_df, x='Time', y='AQI',
        title=f"24-Hour AQI Trend: {selected_ward_trend}",
        markers=True,
        color_discrete_sequence=['#AB63FA']
    )
    st.plotly_chart(fig_line, use_container_width=True)

# === TAB 3: GOVERNANCE COCKPIT (THE BEAST MODE) ===
with tab3:
    st.header("🛠️ Authority Action & Simulation Lab")
    
    # Split: Simulation vs Reports
    c_sel, c_sim = st.columns([1, 2])
    
    with c_sel:
        st.subheader("1. Select Target")
        target_ward = st.selectbox("Select Zone for Intervention:", df['Ward'].unique())
        ward_data = df[df['Ward'] == target_ward].iloc[0]
        
        # Display Current State
        st.metric("Current AQI", ward_data['AQI'], f"{ward_data['Status']}")
        st.metric("Primary Pollutant", "NO2" if ward_data['NO2'] > 50 else "PM2.5")
        st.metric("Zone Type", ward_data['Type'])
        
    with c_sim:
        st.subheader("2. Run 'What-If' Policy Simulation")
        st.info("Select policies below to calculate predictive impact on AQI instantly.")
        
        # Policy Toggles
        c1, c2, c3 = st.columns(3)
        p1 = c1.checkbox("🚗 Odd-Even Rule")
        p2 = c2.checkbox("🏗️ Halt Construction")
        p3 = c3.checkbox("🏭 Factory Shutdown")
        p4 = c1.checkbox("💧 Smog Guns")
        p5 = c2.checkbox("⚡ EV-Only Zone")
        
        # Collect selected policies
        active_policies = []
        if p1: active_policies.append("odd_even")
        if p2: active_policies.append("construction_ban")
        if p3: active_policies.append("factory_shutdown")
        if p4: active_policies.append("smog_guns")
        if p5: active_policies.append("ev_zone_only")
        
        # RUN SIMULATION LOGIC
        if active_policies:
            pred_aqi, logs = engine.simulate_policy_impact(
                ward_data['AQI'], ward_data['NO2'], ward_data['Type'], active_policies
            )
            
            # Show Results using a Delta Metric
            improvement = ward_data['AQI'] - pred_aqi
            st.success(f"Simulation Complete: AQI reduced by {improvement} points")
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("Predicted New AQI", pred_aqi, f"-{improvement} Improvement", delta_color="normal")
            
            # Show Logic Log
            with st.expander("View Algorithm Logic"):
                for log in logs:
                    st.write(log)
        else:
            st.caption("👈 Toggle policies to see the AI prediction model work.")

    st.markdown("---")
    
    # SEGMENTED AI REPORTS
    st.subheader("3. Generate Departmental Orders (AI)")
    
    report_type = st.radio(
        "Select Department / Output Type:",
        ["🏭 Industrial Compliance Notice", "📢 Public Health Advisory", "🚓 Traffic Regulation Order", "🔮 Future Infrastructure Plan"],
        horizontal=True
    )
    
    if st.button(f"Generate {report_type}"):
        # Map radio button to dictionary key
        cat_map = {
            "🏭 Industrial Compliance Notice": "Industrial",
            "📢 Public Health Advisory": "Public",
            "🚓 Traffic Regulation Order": "Traffic",
            "🔮 Future Infrastructure Plan": "Future"
        }
        
        with st.spinner("Drafting Official Document..."):
            doc = engine.generate_segmented_report(ward_data, cat_map[report_type])
            
            st.markdown(f"### 📄 Draft: {report_type}")
            st.markdown(doc)
            
            st.download_button(
                "📥 Download Official Doc", 
                doc, 
                file_name=f"{target_ward}_{cat_map[report_type]}_Plan.md"
            )

# --- FOOTER ---
st.markdown("---")
st.markdown("Designed for **Jaipur Smart City Hackathon** | Team Beast Mode 🚀")