import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
from PIL import Image
from utils import PollutionEngine

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EcoSense Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ENTERPRISE CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .metric-card { background-color: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 15px; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1f2937; border-radius: 4px; color: #e5e7eb; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #3b82f6; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURITY GATE (LOGIN) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login_screen():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.title("🔐 EcoSense Command")
        st.markdown("### Restricted Access: Government Officials Only")
        st.info("Authorized Personnel: Please enter your Secure Access Token.")
        password = st.text_input("Access Token", type="password")
        if st.button("Authenticate"):
            if password == st.secrets.get("ADMIN_PASSWORD", "admin"):
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied: Invalid Token")

if not st.session_state['authenticated']:
    login_screen()
    st.stop()

# --- 4. INITIALIZE ENGINE ---
try:
    engine = PollutionEngine(
        st.secrets["OWM_KEY"], 
        st.secrets["GEMINI_KEY"],
        st.secrets.get("GEMINI_VISION_KEY", st.secrets["GEMINI_KEY"])
    )
except Exception as e:
    st.error(f"🚨 System Error: Credentials Missing. {e}")
    st.stop()

# --- 5. MAIN DASHBOARD ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🌍 EcoSense: City Command Center")
    st.caption("🟢 Live Grid Status: ONLINE | 📡 Source Apportionment: ACTIVE")
with c2:
    if st.button("🔄 Force Satellite Refresh"):
        st.cache_data.clear()
        st.rerun()

@st.cache_data
def load_data(): return engine.generate_live_data()
df = load_data()

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Grid (Heatmap)", "📈 Analytics & Safety", "🚨 Action Console", "👁️ Citizen Eye"])

# === TAB 1: SENSOR GRID (HEATMAP) ===
with tab1:
    k1, k2, k3, k4 = st.columns(4)
    active = df[df['Status'].str.contains("Online")]
    avg_aqi = int(df[df['AQI']>0]['AQI'].mean()) if not df.empty else 0
    
    k1.metric("City Average AQI", avg_aqi, delta=f"{avg_aqi - 140} vs Baseline", delta_color="inverse")
    k2.metric("Active Sensors", f"{len(active)}/{len(df)}", "Real-time Monitoring")
    k3.metric("Primary Pollutant", "PM 2.5", "High Severity")
    k4.metric("Severe Hotspots", len(df[df['AQI'] > 300]), "Immediate Action", delta_color="inverse")

    col_map, col_data = st.columns([2, 1])
    with col_map:
        st.subheader("📍 Satellite-Grade Pollution Heatmap")
        m = folium.Map(location=[26.90, 75.82], zoom_start=12, tiles="CartoDB dark_matter")
        
        heat_data = [[row['Lat'], row['Lon'], row['AQI']] for index, row in df.iterrows() if row['AQI'] > 0]
        HeatMap(heat_data, radius=25, blur=15, gradient={0.4: 'green', 0.65: 'yellow', 0.9: 'red', 1.0: 'purple'}).add_to(m)
        
        for _, row in df.iterrows():
            tooltip_html = f"""
            <div style='font-family:sans-serif; width:150px;'>
                <b>{row['Ward']}</b><br>
                <span style='color:{row['Color']}; font-weight:bold;'>AQI: {row['AQI']}</span><br>
                <small>{row['Cause']}</small>
            </div>
            """
            color = "#808080" if "Offline" in row['Status'] else row['Color']
            folium.CircleMarker(
                [row['Lat'], row['Lon']], radius=8, color="white", weight=1, fill=True, fill_color=color, fill_opacity=0.9,
                popup=folium.Popup(tooltip_html, max_width=200)
            ).add_to(m)
        st_folium(m, width=None, height=500)
        
    with col_data:
        st.subheader("📋 Zonal Status Report")
        st.dataframe(df[['Ward', 'AQI', 'Cause', 'Status']], hide_index=True, use_container_width=True, height=500)

# === TAB 2: ANALYTICS (SAFETY LINES) ===
with tab2:
    st.subheader("📉 Pollutant Analysis vs Safety Standards")
    
    clean_df = df[df['AQI'] > 0] 
    fig = px.bar(clean_df, x='Ward', y=['PM2.5', 'NO2'], barmode='group', 
                 title="Pollutant Levels vs WHO/CPCB Limits", color_discrete_sequence=['#00CC96', '#EF553B'])
    
    fig.add_hline(y=60, line_dash="dash", line_color="#FF4B4B", annotation_text="PM2.5 Limit (60)")
    fig.add_hline(y=80, line_dash="dash", line_color="#FFA500", annotation_text="NO2 Limit (80)")
    fig.update_layout(legend_title_text='Pollutant')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⏳ 24-Hour Forecast Trend")
    sel_ward = st.selectbox("Select Ward for Trend:", clean_df['Ward'].unique())
    history_df = engine.generate_historical_trends(sel_ward)
    fig_line = px.area(history_df, x='Time', y='AQI', title=f"Predicted Trend: {sel_ward}", markers=True, color_discrete_sequence=['#AB63FA'])
    st.plotly_chart(fig_line, use_container_width=True)

# === TAB 3: ACTION CONSOLE (BEAST MODE MATH RESTORED) ===
with tab3:
    st.header("🚨 Authority Response Console")
    
    c_sel, c_profile, c_act = st.columns([1, 1, 1.5])
    
    with c_sel:
        st.subheader("1. Select Zone")
        target = st.selectbox("Target Ward", df[df['AQI']>0]['Ward'].unique())
        w_dat = df[df['Ward'] == target].iloc[0]
        st.metric("Current AQI", w_dat['AQI'], w_dat['Status'])
        st.metric("Identified Cause", w_dat['Cause'])
        st.metric("Population Risk", w_dat['Impact'])
        
    with c_profile:
        st.subheader("2. Field Officer")
        officer = engine.get_ward_officer(target)
        
        with st.container():
            st.markdown(f"**👮 {officer.get('Name', 'Unknown')}**")
            st.caption(f"🆔 Badge: {officer.get('ID', 'N/A')}")
            st.caption(f"📍 Unit: {officer.get('Unit', 'General')}")
            st.caption(f"📞 Contact: {officer.get('Phone', '100')}")
            
            if w_dat['AQI'] > 200:
                st.error("⚠️ Status: HIGH ALERT")
            else:
                st.success("🟢 Status: PATROLLING")

    with c_act:
        st.subheader("3. Dispatch & Strategy")
        
        btn_label = f"📲 Alert {officer.get('Name', 'Officer')}"
        if st.button(btn_label, type="primary"):
            st.toast(f"🚨 ALERT SENT to {officer.get('Unit')} via Secure Line.", icon="📡")
            st.success("Dispatch Sent Successfully.")
            
        st.divider()
        st.markdown("#### 🛠️ Strategic 'What-If' Simulation")
        st.info("Select policies to see predictive AI modeling on AQI reduction.")
        
        # --- RESTORED ALL 5 POLICY OPTIONS (Beast Mode) ---
        c_sim1, c_sim2, c_sim3 = st.columns(3)
        active_policies = []
        
        # Row 1
        if c_sim1.checkbox("🚗 Odd-Even Rule"): active_policies.append("odd_even")
        if c_sim2.checkbox("🏗️ Halt Construction"): active_policies.append("construction_ban")
        if c_sim3.checkbox("🏭 Factory Shutdown"): active_policies.append("factory_shutdown")
        
        # Row 2
        c_sim4, c_sim5 = st.columns(2)
        if c_sim4.checkbox("💧 Deploy Smog Guns"): active_policies.append("smog_guns")
        if c_sim5.checkbox("⚡ EV-Only Zone"): active_policies.append("ev_zone_only")
        
        if active_policies:
            # Calls the AI Math Engine from utils.py
            # This requires utils.py to return 3 values (pred, math_df, forecast_df)
            pred, math_df, forecast_df = engine.simulate_policy_impact(w_dat['AQI'], w_dat['NO2'], w_dat['Type'], active_policies)
            
            improvement = w_dat['AQI'] - pred
            st.success(f"📉 Prediction: AQI will drop by {improvement} points.")
            
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("Predicted New AQI", pred, f"-{improvement}", delta_color="normal")
            
            # --- THE MATH & GRAPHS SECTION ---
            with st.expander("📊 View Mathematical Model & Projections", expanded=True):
                st.markdown("##### 1. Calculation Formula")
                # Showing the "Hard" Math
                st.latex(r'''AQI_{final} = AQI_{current} - \sum (AQI_{current} \times \alpha_{policy})''')
                
                st.markdown("##### 2. Statistical Impact Breakdown")
                st.dataframe(math_df, hide_index=True, use_container_width=True)
                
                st.markdown("##### 3. 3-Day Projected Sustainment")
                # Visualization of the 3-day forecast
                fig_forecast = px.line(forecast_df, x="Day", y="Predicted AQI", markers=True, title="Projected Impact Decay Curve")
                fig_forecast.update_layout(height=250)
                st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.caption("👈 Select strategies to run the predictive model.")

        st.divider()
        st.caption("Official Orders")
        col_type, col_lang, col_go = st.columns([2, 1, 1])
        rtype = col_type.selectbox("Doc Type", ["Public Health Advisory", "Industrial Notice", "Traffic Order"])
        lang = col_lang.radio("Language", ["English", "Hindi"], horizontal=True)
        
        if col_go.button("Draft"):
            cat_map = {"Public Health Advisory": "Public", "Industrial Notice": "Industrial", "Traffic Order": "Traffic"}
            with st.spinner(f"AI Drafting in {lang}..."):
                doc = engine.generate_segmented_report(w_dat, cat_map[rtype], lang)
                st.success(f"📄 Generated: {rtype}")
                st.code(doc, language='markdown')

# === TAB 4: CITIZEN EYE (VISION AI) ===
with tab4:
    st.header("👁️ Citizen Sentinel (AI Vision)")
    st.write("Capture evidence of pollution (Traffic jams, Garbage burning).")
    
    col_input, col_analysis = st.columns([1, 1])
    
    with col_input:
        tab_cam, tab_upl = st.tabs(["📸 Camera", "📂 Upload"])
        final_image = None
        with tab_cam:
            cam_img = st.camera_input("Capture Site Evidence")
            if cam_img: final_image = Image.open(cam_img)
        with tab_upl:
            upl_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
            if upl_img: final_image = Image.open(upl_img)
            
    with col_analysis:
        if final_image:
            st.image(final_image, caption="Evidence for Analysis", width=400)
            if st.button("🚀 Run Gemini Vision Analysis"):
                with st.spinner("Scanning image for pollution sources..."):
                    result = engine.analyze_uploaded_image(final_image)
                    st.success("Analysis Complete")
                    st.write(result)
        else:
            st.info("Waiting for image input...")

# --- FOOTER ---
st.markdown("---")
st.caption("Jaipur Smart City Hackathon 2026 | Powered by **TeamAR27** | Secured Connection")