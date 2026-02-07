<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/ef5e0484-b963-436f-a7bb-7715b64fc0a4" /><img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/6b91c66f-8408-4d87-9b38-53732b6908e4" /># EcoSense: Hyperlocal Environmental Intelligence Platform

**EcoSense** is a decision-support system designed for the Jaipur Pollution Control Board. It bridges the gap between raw sensor data and administrative action by utilizing stochastic modeling for policy simulation and computer vision for ground-truth verification.

project interface:-

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/112d0723-2d45-41ec-8b9c-42d688ccd1b7" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/01af9bc7-e32d-4462-8fb1-12794e3c3319" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/8074aa3b-bea1-4ff1-880b-d1eca2e3d345" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/a7f800cb-bd10-40fd-a7fb-9b7a879972fb" />

---

## 🔗 [Launch Live Dashboard](https://ward-pollution-dashboard-a6f9eu3suvv3pbh8shntdx.streamlit.app/)
* **Access Level:** Admin / Field Officer
* **ADMIN_PASSWORD = "admin"

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
| **Reasoning Model**     | Gemini Api   |
| **Vision Model**        | Google Gemini 1.5 Flash (Image Analysis) |
| **Data Processing**     | Pandas, NumPy (Vectorized Operations)    |
| **Visualization**       | Plotly Express (Interactive Analytics)   |
| **External API**        | OpenWeatherMap (Satellite Feeds)         |
----------------------------------------------------------------------
---

## 4. Installation & Local Deployment

To deploy EcoSense in a local environment for development or testing:

**1. Clone the Repository**

git clone [https://github.com/23f3003413/ward-pollution-dashboard]
cd ward-pollution-dashboard

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Environment Setup :
# Recommended: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

Execution = streamlit run app.py



 Future Roadmap
IoT Integration: Direct API hooks for ESP32-based low-cost sensor networks.

Historical Regression: Integration of ARIMA models for long-term seasonal forecasting.

Public API: Exposing ward-level safety ratings for third-party real estate and health applications.



@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
Developed by Team AR27 for Jaipur Smart City Hackathon 2026.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@















