import requests
import random
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta

# --- CONSTANTS & CONFIG ---
JAIPUR_COORDS = {"lat": 26.9124, "lon": 75.7873}

# Enhanced Ward Data with population density for impact analysis
WARDS = {
    "Sitapura Ind. Area": {"lat": 26.78, "lon": 75.82, "type": "Industrial", "risk_factor": 1.6, "pop_density": "Medium"},
    "Raja Park": {"lat": 26.90, "lon": 75.83, "type": "Commercial", "risk_factor": 1.3, "pop_density": "High"},
    "Civil Lines": {"lat": 26.91, "lon": 75.78, "type": "Residential", "risk_factor": 0.8, "pop_density": "Low"},
    "Nahargarh Fort": {"lat": 26.93, "lon": 75.81, "type": "Green Zone", "risk_factor": 0.5, "pop_density": "Very Low"},
    "Transport Nagar": {"lat": 26.90, "lon": 75.85, "type": "Traffic Hub", "risk_factor": 1.5, "pop_density": "High"},
    "Malviya Nagar": {"lat": 26.85, "lon": 75.81, "type": "Residential", "risk_factor": 0.9, "pop_density": "High"},
    "VKI Area": {"lat": 26.99, "lon": 75.77, "type": "Industrial", "risk_factor": 1.7, "pop_density": "Medium"}
}

class PollutionEngine:
    """
    Core engine for fetching, simulating, and analyzing pollution data.
    """
    def __init__(self, owm_key, gemini_key):
        self.owm_key = owm_key
        self.gemini_key = gemini_key
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)

    def _fetch_city_baseline(self):
        """Fetches the baseline AQI for the city center to anchor simulation."""
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={JAIPUR_COORDS['lat']}&lon={JAIPUR_COORDS['lon']}&appid={self.owm_key}"
        try:
            response = requests.get(url, timeout=5).json()
            if 'list' in response:
                data = response['list'][0]
                return {
                    "aqi": data['main']['aqi'] * 45,  # Scaling to Indian AQI standards
                    "pm25": data['components']['pm2_5'],
                    "no2": data['components']['no2'],
                    "o3": data['components']['o3']
                }
            raise Exception("API Error")
        except Exception as e:
            # Fallback for offline/demo mode
            return {"aqi": 160, "pm25": 85, "no2": 40, "o3": 30}

    def _calculate_cause(self, no2, pm25, ward_type, hour):
        """Logic Engine to determine pollution source."""
        is_peak = 8 <= hour <= 11 or 17 <= hour <= 21
        
        if ward_type == "Industrial" and pm25 > 100:
            return "Factory Emissions 🏭"
        elif ward_type in ["Traffic Hub", "Commercial"] and is_peak and no2 > 50:
            return "Vehicular Congestion 🚗"
        elif ward_type == "Residential" and pm25 > 150:
            return "Waste Burning/Dust 🔥"
        elif no2 > 80:
            return "Heavy Diesel Transport 🚛"
        else:
            return "Background Haze 🌫️"

    def generate_live_data(self):
        """Generates real-time ward data based on baseline."""
        baseline = self._fetch_city_baseline()
        current_hour = datetime.now().hour
        results = []

        for name, meta in WARDS.items():
            # Stochastic Simulation
            noise = random.uniform(0.9, 1.1)
            
            # Apply multipliers
            local_aqi = int(baseline['aqi'] * meta['risk_factor'] * noise)
            local_pm25 = int(baseline['pm25'] * meta['risk_factor'] * noise)
            local_no2 = int(baseline['no2'] * (1.5 if meta['type'] == "Traffic Hub" else 1.0) * noise)
            
            # Derived metrics
            cause = self._calculate_cause(local_no2, local_pm25, meta['type'], current_hour)
            
            status = "Good" if local_aqi < 50 else "Satisfactory" if local_aqi < 100 else "Moderate" if local_aqi < 200 else "Poor" if local_aqi < 300 else "Severe"
            color = "#00e400" if local_aqi < 50 else "#ffff00" if local_aqi < 100 else "#ff7e00" if local_aqi < 200 else "#ff0000" if local_aqi < 300 else "#7e0023"

            results.append({
                "Ward": name,
                "Lat": meta['lat'],
                "Lon": meta['lon'],
                "Type": meta['type'],
                "AQI": local_aqi,
                "PM2.5": local_pm25,
                "NO2": local_no2,
                "Status": status,
                "Cause": cause,
                "Color": color,
                "Impact": meta['pop_density']
            })
        return pd.DataFrame(results)

    def generate_historical_trends(self, ward_name):
        """Simulates 24-hour historical data for trend charts."""
        ward_meta = WARDS.get(ward_name, WARDS["Raja Park"])
        base_factor = ward_meta['risk_factor'] * 150
        
        hours = []
        aqi_levels = []
        
        current_time = datetime.now()
        for i in range(24):
            time_point = current_time - timedelta(hours=i)
            hour_val = time_point.hour
            
            # Time-of-day logic
            time_factor = 1.3 if (8 <= hour_val <= 11 or 18 <= hour_val <= 22) else 0.8
            simulated_aqi = int(base_factor * time_factor + random.randint(-10, 10))
            
            hours.append(time_point.strftime("%H:00"))
            aqi_levels.append(simulated_aqi)
            
        return pd.DataFrame({"Time": hours[::-1], "AQI": aqi_levels[::-1]})

    def simulate_policy_impact(self, current_aqi, current_no2, ward_type, active_policies):
        """
        Mathematically estimates AQI improvement based on selected policies.
        """
        predicted_aqi = current_aqi
        impact_log = []

        # Define Policy Impact Weights
        policy_weights = {
            "odd_even": {"reduction": 0.15, "target": ["Traffic Hub", "Commercial"]}, 
            "construction_ban": {"reduction": 0.20, "target": ["Residential", "Commercial"]},
            "factory_shutdown": {"reduction": 0.35, "target": ["Industrial"]},
            "smog_guns": {"reduction": 0.08, "target": ["All"]},
            "ev_zone_only": {"reduction": 0.25, "target": ["Traffic Hub", "Green Zone"]}
        }

        for policy in active_policies:
            if policy in policy_weights:
                rule = policy_weights[policy]
                # Check if policy applies to this ward type
                if ward_type in rule["target"] or "All" in rule["target"]:
                    drop = int(current_aqi * rule["reduction"])
                    predicted_aqi -= drop
                    impact_log.append(f"✅ {policy.replace('_', ' ').title()}: -{drop} AQI")
                else:
                    impact_log.append(f"⚠️ {policy.replace('_', ' ').title()}: Low impact in {ward_type} zone")
        
        return max(predicted_aqi, 30), impact_log

    def generate_segmented_report(self, ward_data, category):
        """Generates specific reports for specific departments."""
        if not self.gemini_key: return "AI Offline"
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompts = {
            "Industrial": f"Draft a strict legal notice for factories in {ward_data['Ward']} (Type: {ward_data['Type']}, AQI: {ward_data['AQI']}). Cite relevant Indian Environmental Acts.",
            "Public": f"Write a WhatsApp-style advisory for citizens in {ward_data['Ward']} regarding PM2.5 exposure. Include mask type and outdoor timing.",
            "Future": f"Propose 3 infrastructure projects for {ward_data['Ward']} to permanently lower AQI by 2030. Focus on urban planning.",
            "Traffic": f"Create a deployment plan for Traffic Police in {ward_data['Ward']}. Focus on choke points and vehicle checks."
        }
        
        try:
            response = model.generate_content(prompts[category])
            return response.text
        except:
            return "Analysis Pending..."