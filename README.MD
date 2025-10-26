# 🧩 GateGroup AI-Driven Productivity Dashboard

![GateGroup Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Gategroup_logo.png/320px-Gategroup_logo.png)

## 🚀 Overview

Every day, thousands of airline trolleys are stocked manually — yet no one truly knows who’s performing best or where time is being lost.  
Our solution integrates an **AI-driven analytics dashboard** and a **digital twin powered by IoT** to transform manual operations into measurable, comparable data.

Through one unified platform, GateGroup teams can monitor productivity in real time, benchmark performance across sites, and continuously improve through machine learning insights.

---

## 💡 Problem Statement

GateGroup’s challenge lies in the lack of standardization and visibility during trolley assembly:

- Productivity is manually measured, often inconsistently.  
- Consumption prediction is based on historical averages.  
- Expiration tracking is fragmented, risking waste and compliance issues.

These disconnected processes prevent accurate forecasting and benchmarking across global operations.

---

## 🧭 Our Solution

### 🧠 AI-Driven Analytics
A central dashboard that visualizes **EBT (Estimated Build Time)** vs **ABT (Actual Build Time)** for every trolley, employee, and site — transforming operational data into clear KPIs.

### 📡 Digital Twin Integration (IoT)
Each trolley is represented by a **digital twin**, simulating refill times and tracking missing items in real time.  
This allows the model to learn from each session and optimize its future estimations.

### 🌍 Global Benchmark
Compare performance consistency between sites worldwide with an **Efficiency Index** map and ranking tables.
---

## 🧩 Key Features

- 📊 **AI Model Performance Tracking:** Accuracy, bias, and learning trends.
- 👷 **Employee Efficiency Dashboard:** Compare EBT vs ABT and detect outliers.
- 🌐 **Benchmark & Global Comparison:** Site-level analysis via interactive maps.
- 🧾 **Model Explainability:** Visual feature importance and retraining logs.
- 🔁 **Continuous Learning:** Model retrains automatically with new sessions.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Deck.GL |
| Backend / AI | Python (ML models) |
| IoT Simulation | Digital Twin (CSV or API Integration) |
| Deployment | Streamlit Cloud / Docker |

---

## 🧪 MVP Highlights

✅ Dashboard with live AI metrics  
✅ Global Benchmark map  
✅ Feature Importance visualization  
✅ Accuracy Mapping Test (90.2% precision)  
✅ EBT vs ABT comparative KPIs  

---

## 📈 Assumptions

- Each trolley’s digital twin feeds inventory deltas (ΔItems, ΔSKUs).  
- EBT is estimated via AI model; ABT measured via time logs.  
- Sites differ in workflow complexity, layout, and ergonomics — adjusted by the model.  
- IoT/Barcode integration ensures expiration traceability.  

## 👨‍💻 Contributors

- **[Enrique Vidó Villalvazo]**  
  Hackathon 2025 — Productivity Estimation Challenge  

---

## 🧾 License

MIT License © 2025 — Created for the GateGroup Hackathon.

---

