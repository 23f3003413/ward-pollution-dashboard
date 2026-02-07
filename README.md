# EcoSense: Hyperlocal Environmental Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ward-pollution-dashboard.streamlit.app/)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-00599C)
![AI Model](https://img.shields.io/badge/AI-Gemini%201.5%20Pro%20%26%20Flash-4285F4)
![License](https://img.shields.io/badge/License-MIT-green)

**EcoSense** is a decision-support system designed for the Jaipur Pollution Control Board. It bridges the gap between raw sensor data and administrative action by utilizing stochastic modeling for policy simulation and computer vision for ground-truth verification.

---

## 🔗 [Launch Live Dashboard](https://ward-pollution-dashboard.streamlit.app/)
* **Access Level:** Admin / Field Officer
* **Demo Credentials:** `admin`

---

## 1. Executive Summary
Traditional pollution monitoring systems rely on city-wide averages, which mask critical ward-level variance. EcoSense introduces a **Digital Twin** architecture for Jaipur’s environmental health, enabling authorities to move from reactive monitoring to proactive governance.

The platform integrates satellite data streams with ground-level reporting to provide a holistic view of air quality, specifically targeting PM2.5 and NO2 concentrations in high-density zones.

## 2. Core Architecture & Features

### A. Stochastic Policy Simulation Engine
Unlike static dashboards, EcoSense includes a predictive modeling layer. It allows administrators to simulate the impact of specific interventions before implementation.
* **Methodology:** The engine uses a weighted reduction algorithm based on ward typology (Industrial vs. Residential) and pollutant source apportionment.
* **Mathematical Model:**
    $$AQI_{final} = AQI_{current} - \sum (AQI_{current} \times \alpha_{policy} \times \beta_{compliance})$$
    *(Where $\alpha$ represents the theoretical reduction factor of a policy and $\beta$ represents the estimated compliance rate of the specific ward.)*
* **Outcome:** Provides a 3-day decay forecast, helping officials visualize the sustainability of an intervention.

### B. Multimodal Verification (Citizen Eye)
To counter sensor calibration errors and data gaps, EcoSense employs a "Human-in-the-Loop" verification system powered by **Google Gemini 1.5 Flash**.
* **Workflow:** Field officers upload raw imagery of suspected pollution sources.
* **AI Analysis:** The computer vision model identifies specific combustion signatures (e.g., biomass burning smoke vs. vehicular smog) and estimates severity levels to validate sensor readings.

### C. Automated Governance & Dispatch
The system reduces administrative latency by automating the "Last Mile" of pollution control.
* **Dynamic Dispatch:** Automatically routes alerts to specific Zone Officers based on geospatial coordinates.
* **Multilingual Drafting:** Instantly generates legally compliant Show Cause Notices and Health Advisories in both **Hindi (Devanagari)** and **English**, ready for official signature.

---

## 3. Technical Specifications
----------------------------------------------------------------------
| Component               | Technology Stack                         |
| :-----------------------| :----------------------------------------|
| **Frontend Framework**  | Streamlit (Custom CSS for Enterprise UI) |
| **Geospatial Engine**   | Folium / Leaflet.js (Heatmap Rendering)  |
| **Reasoning Model**     | Google Gemini Pro (Policy Logic & NLP)   |
| **Vision Model**        | Google Gemini 1.5 Flash (Image Analysis) |
| **Data Processing**     | Pandas, NumPy (Vectorized Operations)    |
| **Visualization**       | Plotly Express (Interactive Analytics)   |
| **External API**        | OpenWeatherMap (Satellite Feeds)         |
----------------------------------------------------------------------
---

## 4. Installation & Local Deployment

To deploy EcoSense in a local environment for development or testing:

**1. Clone the Repository**

git clone [https://github.com/your-username/ward-pollution-dashboard.git](https://github.com/your-username/ward-pollution-dashboard.git)
cd ward-pollution-dashboard

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Environment Setup :
# Recommended: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Configuration Create a .streamlit/secrets.toml file in the root directory with the following keys:

OWM_KEY = "your_openweather_api_key"
GEMINI_KEY = "your_google_gemini_key"
GEMINI_VISION_KEY = "your_google_gemini_key"
ADMIN_PASSWORD = "admin"

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Execution - streamlit run app.py



 Future Roadmap
IoT Integration: Direct API hooks for ESP32-based low-cost sensor networks.

Historical Regression: Integration of ARIMA models for long-term seasonal forecasting.

Public API: Exposing ward-level safety ratings for third-party real estate and health applications.



@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
Developed by Team AR27 for Jaipur Smart City Hackathon 2026.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@















