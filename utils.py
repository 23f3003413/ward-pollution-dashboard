import requests
import random
import google.generativeai as genai
from datetime import datetime

# --- 1. DATA CONFIGURATION ---
WARDS = {
    "Sitapura Ind. Area": {"lat": 26.78, "lon": 75.82, "type": "Industrial", "risk_factor": 1.5},
    "Raja Park": {"lat": 26.90, "lon": 75.83, "type": "Commercial", "risk_factor": 1.2},
    "Civil Lines": {"lat": 26.91, "lon": 75.78, "type": "Residential", "risk_factor": 0.8},
    "Nahargarh Fort": {"lat": 26.93, "lon": 75.81, "type": "Green Zone", "risk_factor": 0.6},
    "Transport Nagar": {"lat": 26.90, "lon": 75.85, "type": "Traffic Hub", "risk_factor": 1.4}
}

# --- 2. THE PROXY LOGIC ENGINE ---
# ... keep imports and WARDS list same as before ...

def fetch_ward_data(api_key):
    results = []
    
    # 1. Get Real Time
    current_hour = datetime.now().hour
    is_peak_traffic = 8 <= current_hour <= 11 or 17 <= current_hour <= 21
    
    # Fetch Base City Data
    base_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=26.90&lon=75.80&appid={api_key}"
    
    try:
        response = requests.get(base_url).json()
        if 'list' in response:
            # OpenWeatherMap returns pollutants in ug/m3
            data_point = response['list'][0]
            base_aqi = data_point['main']['aqi'] * 40
            base_pm25 = data_point['components']['pm2_5']
            base_no2 = data_point['components']['no2'] # We fetch NO2 now!
        else:
            raise Exception("API Error")
    except:
        base_aqi = 140; base_pm25 = 55; base_no2 = 20

    for ward_name, details in WARDS.items():
        # --- YOUR LOGIC IMPLEMENTATION ---
        
        # Logic 1: Time-Based Traffic Spikes
        # If it's peak time AND a traffic zone, boost NO2 and AQI
        traffic_multiplier = 1.0
        if is_peak_traffic and details['type'] == "Traffic Hub":
            traffic_multiplier = 1.5 
        
        # Logic 2: Industrial Smoke
        # Industrial zones always have higher Base PM2.5
        industrial_multiplier = 1.4 if details['type'] == "Industrial" else 1.0

        # Apply Multipliers (Simulation)
        local_aqi = int(base_aqi * details['risk_factor'] * traffic_multiplier)
        local_pm25 = int(base_pm25 * details['risk_factor'] * industrial_multiplier)
        local_no2 = int(base_no2 * details['risk_factor'] * traffic_multiplier)

        # Logic 3: Determine "Primary Cause" for the Dashboard
        primary_cause = "General Haze"
        if local_no2 > 80:
            primary_cause = "Vehicle Emissions 🚗"
        elif local_pm25 > 100:
            primary_cause = "Dust/Smoke 🏭"
        elif is_peak_traffic and details['type'] == "Commercial":
             primary_cause = "Urban Congestion 🚦"

        # Color Logic
        if local_aqi < 100: color = "green"
        elif local_aqi < 200: color = "orange"
        elif local_aqi < 300: color = "red"
        else: color = "purple"

        results.append({
            "Ward": ward_name,
            "Lat": details['lat'],
            "Lon": details['lon'],
            "Type": details['type'],
            "AQI": local_aqi,
            "PM2.5": local_pm25,
            "NO2": local_no2,        # Added this
            "Cause": primary_cause,  # Added this
            "Color": color
        })
        
    return results

# --- 3. AI GENERATOR ---
def get_ai_insights(gemini_key, ward_name, aqi, ward_type):
    if not gemini_key: return "⚠️ Key Missing"
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Act as environmental officer. Give 3 strict pollution mitigation steps for {ward_name} ({ward_type} zone, AQI {aqi})."
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "⚠️ AI Busy. Deploy Anti-Smog Guns."