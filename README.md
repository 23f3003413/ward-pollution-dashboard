# 🛡️ EcoSense: Enterprise Pollution Intelligence System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ward-pollution-dashboard-a6f9eu3suvv3pbh8shntdx.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11%2B-00599C)
![AI Core](https://img.shields.io/badge/GenAI-Gemini%201.5%20Flash-4285F4)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

> **"From Reactive Monitoring to Predictive Governance."**

**EcoSense** is a comprehensive decision-support system (DSS) architected for the **Jaipur Pollution Control Board**. It transforms raw IoT sensor data into actionable administrative intelligence by combining **stochastic modeling**, **financial forecasting**, and **Generative AI**.

---

## 🔗 [Launch Command Center](https://ward-pollution-dashboard-a6f9eu3suvv3pbh8shntdx.streamlit.app/)
* **Authorized Access:** Government Officials & Field Officers
* **Demo Credentials:** `admin` (For Jury Review)

---

## 1. Executive Summary
Current urban pollution management is reactive, relying on city-wide averages that mask hyperlocal crises. **EcoSense** introduces a **Digital Twin** architecture for Jaipur’s environmental grid.

Unlike traditional dashboards that merely *display* data, EcoSense *simulates* the future. It answers the critical administrative question:
> *"If we enforce an industrial shutdown in Ward 7 today, exactly how much will the AQI improve, and what will be the fiscal impact on the state budget?"*

---

## 2. Core Modules & Capabilities

### 🧠 A. The Stochastic Policy Engine (Predictive Analytics)
At the heart of EcoSense is a Monte Carlo simulation engine that models the dispersion of PM2.5 and NO2 based on ward typology (Industrial vs. Residential).
* **"What-If" Scenarios:** Administrators can toggle interventions (e.g., Odd-Even, Smog Guns) to visualize the 72-hour AQI decay curve.
* **Mathematical Framework:**
    $$AQI_{final} = AQI_{current} - \sum (AQI_{current} \times \alpha_{policy} \times \beta_{compliance})$$
    *(Where $\alpha$ is the theoretical reduction factor and $\beta$ is the granular compliance rate of the specific ward.)*

### 💸 B. Fiscal Impact & Resource Allocation (New)
Governance requires budgeting. EcoSense includes a real-time **Financial Estimation Module** that runs parallel to the environmental simulation.
* **Dynamic Costing:** Instantly calculates daily operational expenditure (OpEx) for deployed resources (Manpower + Equipment) based on **Rajasthan Minimum Wages Act 2024** and **CPCB Tender Rates**.
* **🤖 AI Budget Auditor:** An autonomous AI agent (powered by Gemini 1.5 Flash) reviews every proposed budget in real-time, providing a justification report to ensure fiscal responsibility and prevent overspending.

### 👁️ C. Citizen Sentinel (Computer Vision Verification)
To counter sensor calibration drift, the system employs a "Human-in-the-Loop" verification layer.
* **Visual Forensics:** Field officers or citizens upload images of suspected violations.
* **AI Analysis:** The Vision Model identifies specific pollutant sources (e.g., *Stubble Burning vs. Construction Dust*), estimates severity, and tags the geolocation for enforcement squads.

### 📜 D. Automated Bureaucracy (Generative Drafting)
Reduces administrative latency from hours to seconds.
* **Smart Drafting:** Generates legally binding **Show Cause Notices**, **Health Advisories**, and **Police Dispatch Orders**.
* **Vernacular Support:** Outputs documents in both **English** and **Hindi (Devanagari)** to ensure effective communication with local stakeholders.

---

## 3. System Architecture & Tech Stack
----------------------------------------------------------------------------------------------------------
|Component          | Technology              | Role                                                     | 
|-------------------|-------------------------|----------------------------------------------------------|
| **Frontend**      | Streamlit               | Enterprise-grade UI with responsive data tables.         |
| **Logic Core**    | Python 3.11             | Orchestration of simulation and API calls.               |
| **AI Brain**      | Google Gemini 1.5 Flash | Text generation, image analysis, and financial auditing. |
| **Geospatial**    | Folium & Leaflet.js     | Rendering of the Hyperlocal Heatmap.                     |
| **Data Engine**   | Pandas & NumPy          | High-performance vector calculations for the simulation. |
| **Visualization** | Plotly Express          | Interactive charts for trend analysis and forecasting.   |
----------------------------------------------------------------------------------------------------------

---

## 4. Installation & Deployment

**1. Clone the Repository**
git clone [https://github.com/23f3003413/ward-pollution-dashboard](https://github.com/23f3003413/ward-pollution-dashboard)
git clone [https://github.com/23f3003413/ward-pollution-dashboard]

cd ward-pollution-dashboard

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Environment Setup :
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install dependencies :

pip install -r requirements.txt

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Configure Secrets Create a .streamlit/secrets.toml file with your API keys:

OWM_KEY = "your_openweather_key"
GEMINI_KEY = "your_google_ai_key"
GEMINI_VISION_KEY = "your_google_ai_key"
ADMIN_PASSWORD = "admin"
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Launch Application :  streamlit run app.py

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
Future Roadmap: The "Eco-Web" (Phase 2 & 3)
We are actively seeking collaborators for the next stages of development:

 Phase 2: DePIN (Decentralized Physical Infrastructure Network)
Objective: Immutable Data Integrity.

Implementation: Integration with the Solana or Polygon blockchain to hash sensor data readings. This prevents data tampering and creates a "Trustless" environmental record.

Incentivization: Citizens hosting IoT sensors earn EcoTokens for providing verified data streams.

 Phase 3: Autonomous Enforcement Swarms
Objective: Zero-Latency Response.

Implementation: API integration with drone surveillance grids. When the Heatmap detects a "Red Zone," the system automatically dispatches a drone for visual verification, closing the loop between detection and action.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

👥 Contributors & License

Ritik Joshi (Team AR27)

Event: Jaipur Smart City Hackathon 2026

Focus: AI/ML, Geospatial Analytics, Full-Stack Python

License: This project is licensed under the MIT License - see the LICENSE file for details.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------@@
Built with precision for a cleaner, smarter Jaipur.












