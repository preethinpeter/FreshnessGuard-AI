# 🥬 FreshnessGuard AI — Streamlit Dashboard

Professional dark-themed data science dashboard for AI-driven freshness & spoilage optimization.

## Features
- **Overview & EDA** — waste by category, demand distributions, correlation heatmap, monthly trends
- **Spoilage Model** — confusion matrix, ROC curve, feature importances, store-level risk
- **Demand Forecast** — 30-day XGBoost/Prophet forecast with confidence bands, all-store summary
- **AI Agent System** — LangChain 4-agent workflow (Inventory → Demand → Weather → Decision)
- **Waste Reduction** — before/after comparisons, active action table, replenishment signals
- **Presentation Deck** — 8-slide project summary with key insights

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py
```

## Optional: Connect Real Models
Drop these files into the same folder to activate real ML inference:
- `demand_forecast_model.pkl`
- `spoilage_risk_model.pkl`
- `label_encoders.pkl`
- `timeseries_xgb_model.pkl`
- `demand_forecast_30days.csv`
- `LangChain_Perfected_Freshness_Dataset.csv`

The dashboard runs with **synthetic demo data** out of the box — no dataset required.

## Tech Stack
| Component | Library |
|-----------|---------|
| Dashboard | Streamlit |
| Visualizations | Plotly |
| ML Models | scikit-learn, XGBoost, Prophet |
| Agent Framework | LangChain + Ollama (LLaMA3) |
| Styling | Custom CSS dark theme (Syne + JetBrains Mono) |
