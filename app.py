import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FreshnessGuard AI",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  INJECT GLOBAL CSS — full custom theme
# ─────────────────────────────────────────────
def load_css(theme: str):
    if theme == "Dark":
        bg          = "#07090f"
        bg2         = "#0d1117"
        bg3         = "#111820"
        card_bg     = "#0f161f"
        text        = "#e8edf5"
        text_muted  = "#7a8898"
        border      = "rgba(255,255,255,0.08)"
        accent      = "#00e5a0"
        accent2     = "#0096ff"
        warn        = "#ffb800"
        danger      = "#ff4757"
        purple      = "#a78bfa"
        sidebar_bg  = "#090d14"
        metric_bg   = "#111c27"
        tag_bg      = "rgba(0,229,160,0.1)"
        shadow      = "rgba(0,0,0,0.6)"
    else:
        bg          = "#f4f6fb"
        bg2         = "#ffffff"
        bg3         = "#eef1f8"
        card_bg     = "#ffffff"
        text        = "#1a1f2e"
        text_muted  = "#6b7a8f"
        border      = "rgba(0,0,0,0.08)"
        accent      = "#00a372"
        accent2     = "#0070cc"
        warn        = "#d4900a"
        danger      = "#d63648"
        purple      = "#7c5cbf"
        sidebar_bg  = "#edf0f7"
        metric_bg   = "#f0f4ff"
        tag_bg      = "rgba(0,163,114,0.08)"
        shadow      = "rgba(0,0,0,0.08)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Bricolage+Grotesque:wght@400;500;600;700&display=swap');

    /* ── ROOT RESET ── */
    html, body, [class*="css"] {{
        font-family: 'Bricolage Grotesque', sans-serif !important;
    }}
    .stApp {{
        background: {bg} !important;
        color: {text} !important;
    }}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {text} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {{
        color: {text_muted} !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 600 !important;
    }}

    /* ── MAIN AREA ── */
    .block-container {{
        padding: 1.5rem 2rem 2rem 2rem !important;
        max-width: 1600px !important;
    }}

    /* ── HEADINGS ── */
    h1 {{ font-family: 'Syne', sans-serif !important; font-weight: 800 !important; color: {text} !important; }}
    h2 {{ font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: {text} !important; }}
    h3 {{ font-family: 'Syne', sans-serif !important; font-weight: 600 !important; color: {text} !important; }}

    /* ── METRIC CARDS ── */
    [data-testid="stMetric"] {{
        background: {metric_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 12px {shadow} !important;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 24px {shadow} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: {text_muted} !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        color: {accent} !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
    }}

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {{
        background: {bg3} !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid {border} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-radius: 8px !important;
        color: {text_muted} !important;
        padding: 8px 18px !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {accent} !important;
        color: #07090f !important;
        box-shadow: 0 2px 8px rgba(0,229,160,0.3) !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{
        padding-top: 1.5rem !important;
    }}

    /* ── SELECTBOX / INPUTS ── */
    .stSelectbox [data-baseweb="select"] > div {{
        background: {bg3} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        color: {text} !important;
    }}
    .stSelectbox label {{
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {text_muted} !important;
    }}
    .stRadio > label {{
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {text_muted} !important;
    }}

    /* ── DATAFRAME ── */
    [data-testid="stDataFrame"] {{
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}
    .stDataFrame th {{
        background: {bg3} !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: {text_muted} !important;
        font-weight: 600 !important;
    }}

    /* ── PLOTLY CHARTS ── */
    .js-plotly-plot .plotly .main-svg {{
        border-radius: 12px !important;
    }}

    /* ── CUSTOM CARD ── */
    .fg-card {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 2px 16px {shadow};
        margin-bottom: 16px;
    }}
    .fg-card-title {{
        font-family: 'Syne', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {text_muted};
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* ── BADGE PILLS ── */
    .badge-green {{ background: rgba(0,229,160,0.12); color: {accent}; border: 1px solid rgba(0,229,160,0.25); padding: 3px 10px; border-radius: 20px; font-size: 11px; font-family: 'DM Mono', monospace; font-weight: 500; }}
    .badge-blue  {{ background: rgba(0,150,255,0.12); color: {accent2}; border: 1px solid rgba(0,150,255,0.25); padding: 3px 10px; border-radius: 20px; font-size: 11px; font-family: 'DM Mono', monospace; font-weight: 500; }}
    .badge-warn  {{ background: rgba(255,184,0,0.12); color: {warn}; border: 1px solid rgba(255,184,0,0.25); padding: 3px 10px; border-radius: 20px; font-size: 11px; font-family: 'DM Mono', monospace; font-weight: 500; }}
    .badge-red   {{ background: rgba(255,71,87,0.12); color: {danger}; border: 1px solid rgba(255,71,87,0.25); padding: 3px 10px; border-radius: 20px; font-size: 11px; font-family: 'DM Mono', monospace; font-weight: 500; }}
    .badge-purple{{ background: rgba(167,139,250,0.12); color: {purple}; border: 1px solid rgba(167,139,250,0.25); padding: 3px 10px; border-radius: 20px; font-size: 11px; font-family: 'DM Mono', monospace; font-weight: 500; }}

    /* ── ACTION ITEMS ── */
    .action-item {{
        background: {bg3};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        transition: border-color 0.2s, transform 0.15s;
    }}
    .action-item:hover {{
        border-color: {accent};
        transform: translateX(3px);
    }}

    /* ── LEAKAGE TABLE ── */
    .leak-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 5px;
        border: 1px solid {border};
        font-size: 13px;
    }}
    .leak-pass {{ background: rgba(0,229,160,0.04); border-color: rgba(0,229,160,0.15); }}
    .leak-fail {{ background: rgba(255,71,87,0.04); border-color: rgba(255,71,87,0.2); }}

    /* ── PROGRESS BARS ── */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {accent}, {accent2}) !important;
        border-radius: 4px !important;
    }}
    .stProgress > div > div {{
        background: {bg3} !important;
        border-radius: 4px !important;
    }}

    /* ── DIVIDERS ── */
    hr {{ border-color: {border} !important; }}

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {border}; border-radius: 3px; }}

    /* ── INFO / WARNING BOXES ── */
    .stAlert {{
        border-radius: 10px !important;
        border: 1px solid {border} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    return {
        "bg": bg, "bg2": bg2, "bg3": bg3, "card_bg": card_bg,
        "text": text, "text_muted": text_muted, "border": border,
        "accent": accent, "accent2": accent2, "warn": warn,
        "danger": danger, "purple": purple, "shadow": shadow,
        "metric_bg": metric_bg, "tag_bg": tag_bg,
    }


# ─────────────────────────────────────────────
#  SYNTHETIC DATA (mirrors actual notebook outputs)
# ─────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42)
    random.seed(42)

    stores = [f"Store_{i}" for i in [1,2,3,4,5,6,7,8,9,10]]
    categories = ["Fresh Foods","Bakery","Dairy & Alternatives","Beverages","Frozen Foods","Pantry","Snacks"]
    products_per_cat = {
        "Fresh Foods":    ["Strawberries","Avocado","Mango","Lettuce","Spinach","Broccoli","Tomatoes","Ground Beef"],
        "Bakery":         ["Sourdough","Croissant","Multigrain Loaf","Brioche","Muffins"],
        "Dairy & Alt.":   ["Whole Milk","Greek Yogurt","Cheddar","Almond Milk","Butter"],
        "Beverages":      ["Orange Juice","Coconut Water","Cold Brew","Green Tea"],
        "Frozen Foods":   ["Mixed Veggies","Chicken Nuggets","Ice Cream","Edamame"],
        "Pantry":         ["All-Purpose Flour","Olive Oil","Canned Tomatoes","Rice","Pasta"],
        "Snacks":         ["Granola Bar","Trail Mix","Popcorn","Crackers"],
    }

    # Monthly demand (2023-01 to 2025-09)
    months = pd.date_range("2023-01", periods=33, freq="ME")
    base   = np.array([38000,42000,45000,48000,52000,58000,56000,53000,50000,
                       47000,44000,50000,55000,60000,63000,67000,71000,75000,
                       73000,69000,65000,62000,58000,64000,70000,75000,79000,
                       83000,80000,76000,72000,68000,74000])
    noise  = np.random.normal(0, 1500, len(months))
    monthly_demand = pd.DataFrame({"month": months, "units_sold": (base + noise).astype(int)})

    # Store daily forecasts (30-day)
    store_fc = {
        "Store_9":72,"Store_8":80,"Store_7":75,"Store_4":75,
        "Store_2":73,"Store_1":72,"Store_10":62,"Store_6":59,
        "Store_5":57,"Store_3":57
    }
    fc_rows = []
    base_date = datetime(2025, 9, 22)
    for store, avg in store_fc.items():
        for d in range(30):
            day  = base_date + timedelta(days=d+1)
            wknd = 1 if day.weekday() >= 5 else 0
            val  = max(0, avg + wknd*avg*0.8 + np.random.normal(0, 8))
            fc_rows.append({"store_id": store, "date": day, "forecasted_demand": round(val)})
    forecast_df = pd.DataFrame(fc_rows)

    # XGBoost per-store metrics
    xgb_metrics = pd.DataFrame({
        "store":  ["Store_1","Store_2","Store_3","Store_4","Store_5",
                   "Store_6","Store_7","Store_8","Store_9","Store_10"],
        "MAE":    [5.7, 4.7, 7.8, 3.7, 2.9, 10.8, 9.1, 7.1, 6.3, 3.7],
        "RMSE":   [24.9,15.5,14.9,11.8,11.8,14.9,13.9,18.6,12.8, 9.4],
        "MAPE":   [180.7,199.6,165.6,192.2,200.1,112.2,151.5,187.5,131.2,134.7],
    })

    # Feature importances
    features = pd.DataFrame({
        "feature":    ["stock_quantity","days_to_expiry_at_receipt","shelf_life_days",
                       "stock_to_shelf_day","Temperature_C","price_cost_ratio",
                       "stock_value","Humidity_Percent","supply_delay_days",
                       "received_month","weather_severity_n","lead_time_days","high_temp_flag"],
        "importance": [0.22, 0.18, 0.14, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04, 0.02, 0.01, 0.007, 0.003],
    })

    # Category waste
    cat_waste = pd.DataFrame({
        "category":   ["Fresh Foods","Bakery","Dairy & Alt.","Beverages","Frozen Foods","Pantry","Snacks"],
        "avg_waste":  [2586, 1655, 1420, 890, 720, 540, 380],
    })

    # Danger zone
    dz = pd.DataFrame({
        "Days to Expiry": list(range(0, 15)),
        "Transactions":   [1200,1800,2400,3100,2900,2600,2200,1900,1600,1300,1000,800,600,400,250],
    })

    # Model performance summary
    model_perf = pd.DataFrame({
        "Model":       ["Spoilage Classifier","Demand Regressor (RF)","Waste Vol. Regressor",
                        "Demand RF Part 2","XGBoost Time-Series","Prophet (Store_1)"],
        "Metric":      ["ROC-AUC","R² (log)","R²","R²","MAE","MAE"],
        "Train":       [0.9999, 0.9821, 0.9990, 0.9610, "3.1 u/d", "41.2 u/d"],
        "Test":        [0.9996, 0.9475, 0.9766, 0.8468, "6.2 u/d", "48.3 u/d"],
        "Gap":         ["0.0003","0.0346","0.0224","0.1142","~3 u/d","~7 u/d"],
        "Status":      ["✅ Clean","✅ Clean","⚠️ Check","⚠️ Gap","✅ Clean","✅ Clean"],
    })

    # Leakage registry
    leakage = pd.DataFrame({
        "Column":       ["Days_to_Expiry_at_Sale","freshness_score","sales_demand_n",
                         "discount_applied_percent","promotional_price","final_profit",
                         "sales_date","waste_quantity","units_sold",
                         "base_profit_margin","Latitude","Longitude"],
        "Type":         ["Sale-time","Derived","Target Encoding","Sale-time","Derived",
                         "Outcome","Future info","Target","Target","Collinear","Near-zero var.","Near-zero var."],
        "Status":       ["REMOVED"]*12,
        "Reason":       [
            "Requires sales_date — future info",
            "Derived from Days_to_Expiry_at_Sale",
            "Binned encoding of units_sold target",
            "Reactive decision made at sale time",
            "= unit_price × (1 - discount/100)",
            "Contains units_sold — direct leakage",
            "Date of transaction — not known at order time",
            "Spoilage target — label only",
            "Demand target — label only",
            "= unit_price - cost_price — collinear",
            "Static per store — near-zero variance",
            "Static per store — near-zero variance",
        ],
    })

    # Optimization results
    discount_opt = pd.DataFrame({
        "Store":    stores,
        "Category": ["Fresh Foods","Bakery","Dairy & Alt.","Fresh Foods","Frozen Foods",
                     "Bakery","Fresh Foods","Dairy & Alt.","Bakery","Fresh Foods"],
        "Optimal Discount %": [20.0, 15.0, 10.0, 18.0, 5.0, 22.0, 17.0, 12.0, 25.0, 14.0],
        "Revenue Before": [450000,380000,290000,510000,220000,340000,480000,310000,400000,370000],
        "Revenue After":  [396000,345000,275000,441200,214500,293600,409200,286200,320000,328780],
        "Waste Saved":    [41854,32100,38423,55200,12000,28900,44100,25600,51000,39200],
    })
    discount_opt["store_id"] = stores

    replenish_opt = pd.DataFrame({
        "Store":       stores,
        "Category":    ["Fresh Foods","Bakery","Pantry","Dairy & Alt.","Snacks",
                        "Beverages","Fresh Foods","Frozen Foods","Bakery","Pantry"],
        "Current Stock": [320, 180, 540, 260, 420, 310, 290, 380, 210, 480],
        "Optimal Order": [620, 380, 230, 490, 190, 420, 580, 200, 560, 300],
        "Order Cost INR": [124000,76000,46000,98000,38000,84000,116000,40000,112000,60000],
        "Urgency":       ["HIGH","HIGH","LOW","HIGH","MEDIUM","HIGH","HIGH","MEDIUM","HIGH","LOW"],
    })

    # Agent recommendations
    agent_recs = [
        {"store":"Store_1","type":"DISCOUNT",      "text":"Apply 15% discount on Strawberries, Ground Beef, Peach nearing expiry","icon":"🏷️"},
        {"store":"Store_1","type":"REPLENISHMENT",  "text":"Order 112 units of Fresh Foods by Sep 22 — weekend demand surge","icon":"📦"},
        {"store":"Store_2","type":"REDISTRIBUTE",   "text":"Transfer 50 units Yogurt to Store_4 — excess inventory detected","icon":"🔄"},
        {"store":"Store_3","type":"REDUCE ORDER",   "text":"Reduce Leafy Greens order by 15% — heatwave risk this week","icon":"🌡️"},
        {"store":"Store_4","type":"REPLENISHMENT",  "text":"Reorder 387 units Cashews — critically low stock by Sep 20","icon":"📦"},
        {"store":"Store_5","type":"DISCOUNT",       "text":"Apply 20% discount on Dairy section — spoilage rate above threshold","icon":"🏷️"},
        {"store":"Store_6","type":"REDUCE ORDER",   "text":"Reduce Sugar order by 10% — low demand forecast this cycle","icon":"📉"},
        {"store":"Store_7","type":"REPLENISHMENT",  "text":"Stock up 200 extra units Bread before Friday — demand spike forecast","icon":"📦"},
        {"store":"Store_8","type":"REDISTRIBUTE",   "text":"Transfer surplus Frozen Foods to Store_3 — cost savings: ₹18,400","icon":"🔄"},
        {"store":"Store_9","type":"DISCOUNT",       "text":"Flash sale on Bakery items — 3 SKUs entering danger zone","icon":"🏷️"},
        {"store":"Store_10","type":"REPLENISHMENT", "text":"Emergency reorder Fresh Produce — waste rate 82% above normal","icon":"🚨"},
    ]

    # Weather impact
    weather = pd.DataFrame({
        "Store":          stores,
        "Avg Temp (°C)":  [24.4, 22.1, 26.8, 23.5, 28.2, 21.0, 25.7, 27.3, 24.9, 22.8],
        "Max Temp (°C)":  [35.0, 32.4, 38.1, 34.2, 39.5, 30.8, 36.4, 37.9, 35.6, 33.1],
        "Heatwave Risk":  ["MEDIUM","LOW","HIGH","MEDIUM","HIGH","LOW","MEDIUM","HIGH","MEDIUM","LOW"],
        "High Temp Days": [42, 28, 67, 38, 81, 19, 53, 72, 45, 31],
        "Waste Premium":  ["+12%","+6%","+28%","+9%","+35%","+4%","+18%","+31%","+14%","+7%"],
    })

    return {
        "monthly_demand": monthly_demand,
        "forecast_df":    forecast_df,
        "xgb_metrics":    xgb_metrics,
        "features":       features,
        "cat_waste":      cat_waste,
        "dz":             dz,
        "model_perf":     model_perf,
        "leakage":        leakage,
        "discount_opt":   discount_opt,
        "replenish_opt":  replenish_opt,
        "agent_recs":     agent_recs,
        "weather":        weather,
        "stores":         stores,
    }


# ─────────────────────────────────────────────
#  PLOTLY THEME HELPER
# ─────────────────────────────────────────────
def chart_layout(c, title="", height=300, theme="Dark"):
    bg     = "#07090f" if theme == "Dark" else "#ffffff"
    paper  = "#0f161f" if theme == "Dark" else "#ffffff"
    grid   = "rgba(255,255,255,0.04)" if theme == "Dark" else "rgba(0,0,0,0.06)"
    text   = "#e8edf5" if theme == "Dark" else "#1a1f2e"
    muted  = "#7a8898" if theme == "Dark" else "#6b7a8f"
    c.update_layout(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=13, color=muted), x=0, xanchor="left"),
        paper_bgcolor=paper, plot_bgcolor=bg,
        font=dict(family="Bricolage Grotesque, sans-serif", color=text),
        height=height,
        margin=dict(l=12, r=12, t=38 if title else 12, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(gridcolor=grid, zeroline=False, color=muted, showgrid=True),
        yaxis=dict(gridcolor=grid, zeroline=False, color=muted, showgrid=True),
    )
    return c


def accent(theme="Dark"):
    return "#00e5a0" if theme == "Dark" else "#00a372"

def accent2(theme="Dark"):
    return "#0096ff" if theme == "Dark" else "#0070cc"

def warn_c(theme="Dark"):
    return "#ffb800" if theme == "Dark" else "#d4900a"

def danger_c(theme="Dark"):
    return "#ff4757" if theme == "Dark" else "#d63648"

def purple_c(theme="Dark"):
    return "#a78bfa" if theme == "Dark" else "#7c5cbf"

def paper_c(theme="Dark"):
    return "#0f161f" if theme == "Dark" else "#ffffff"

def text_c(theme="Dark"):
    return "#e8edf5" if theme == "Dark" else "#1a1f2e"

def muted_c(theme="Dark"):
    return "#7a8898" if theme == "Dark" else "#6b7a8f"

def bg3_c(theme="Dark"):
    return "#111820" if theme == "Dark" else "#eef1f8"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <span style="font-size:22px">🥬</span>
            <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;letter-spacing:-0.3px">FreshnessGuard</span>
        </div>
        <div style="font-size:10px;letter-spacing:0.12em;text-transform:uppercase;opacity:0.45;padding-left:32px;font-family:'DM Mono',monospace">AI · Operations Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    theme = st.radio("Theme", ["Dark", "Light"], horizontal=True, index=0)
    c = load_css(theme)

    st.divider()

    data     = generate_data()
    stores   = data["stores"]
    all_cats = ["Fresh Foods","Bakery","Dairy & Alt.","Beverages","Frozen Foods","Pantry","Snacks"]

    st.markdown('<div style="font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.45;font-family:\'DM Mono\',monospace;margin-bottom:6px">Store Filter</div>', unsafe_allow_html=True)
    sel_store = st.selectbox("", ["All Stores"] + stores, label_visibility="collapsed")

    st.markdown('<div style="font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.45;font-family:\'DM Mono\',monospace;margin-bottom:6px;margin-top:14px">Category</div>', unsafe_allow_html=True)
    sel_cat = st.selectbox("", ["All Categories"] + all_cats, label_visibility="collapsed", key="cat")

    st.divider()

    # Quick stats
    st.markdown(f"""
    <div style="font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.45;font-family:'DM Mono',monospace;margin-bottom:10px">Quick Stats</div>
    <div style="display:flex;flex-direction:column;gap:8px;font-size:12px;">
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Dataset</span><span style="font-family:'DM Mono',monospace;color:{c['accent']}">100,192 rows</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">After Clean</span><span style="font-family:'DM Mono',monospace;color:{c['accent']}">90,874 rows</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Stores</span><span style="font-family:'DM Mono',monospace;color:{c['accent2']}">10</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Features</span><span style="font-family:'DM Mono',monospace;color:{c['accent2']}">27 pre-sale</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Leakage Cols</span><span style="font-family:'DM Mono',monospace;color:{c['danger']}">12 removed</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Date Range</span><span style="font-family:'DM Mono',monospace;color:{c['warn']}">2022–2025</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="opacity:.55">Models</span><span style="font-family:'DM Mono',monospace;color:{c['purple']}">6 trained</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style="font-size:10px;opacity:.35;font-family:'DM Mono',monospace;text-align:center;">
        Stack: Scikit-learn · XGBoost<br>Prophet · LangChain · PuLP<br>
        <span style="color:{c['accent']}">● All models leakage-free</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────────
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(f"""
    <div style="margin-bottom:6px">
        <span style="font-family:'DM Mono',monospace;font-size:10px;color:{c['accent']};letter-spacing:.12em;text-transform:uppercase;">
            ● LIVE — {sel_store if sel_store != 'All Stores' else 'Network View'}
        </span>
    </div>
    <h1 style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;letter-spacing:-0.5px;margin-bottom:4px;color:{c['text']}">
        FreshnessGuard <span style="color:{c['accent']}">AI</span>
    </h1>
    <p style="font-size:13px;color:{c['text_muted']};margin-bottom:0;">
        AI-driven freshness optimization · Spoilage prediction · Demand forecasting · Inventory intelligence
    </p>
    """, unsafe_allow_html=True)
with header_col2:
    now = datetime.now().strftime("%d %b %Y · %H:%M")
    st.markdown(f"""
    <div style="text-align:right;padding-top:16px;">
        <div style="font-family:'DM Mono',monospace;font-size:11px;color:{c['text_muted']}">{now}</div>
        <div style="margin-top:6px;display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap;">
            <span class="badge-green">10 STORES ACTIVE</span>
            <span class="badge-blue">4 AGENTS RUNNING</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tabs = st.tabs(["📊 Overview", "📈 Demand Forecast", "🔴 Spoilage Risk", "🤖 AI Agents", "⚙️ Optimization", "🔬 Model Audit"])


# ══════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tabs[0]:

    # KPIs
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Records",    "100,192",  "+3.2K this month")
    k2.metric("Clean Records",    "90,874",   "90.7% retention")
    k3.metric("Danger Zone",      "29.5%",    "26,849 items ≤3d", delta_color="inverse")
    k4.metric("Active Stores",    "10",       "All operational")
    k5.metric("Pre-Sale Features","27",       "Zero leakage")
    k6.metric("AI Agents",        "4",        "All responding")

    st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

    # Monthly demand + category waste
    col1, col2 = st.columns([2, 1])

    with col1:
        md = data["monthly_demand"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=md["month"], y=md["units_sold"],
            mode="lines",
            fill="tozeroy",
            fillcolor=f"rgba(0,229,160,0.08)" if theme == "Dark" else "rgba(0,163,114,0.07)",
            line=dict(color=accent(theme), width=2.5),
            name="Units Sold",
            hovertemplate="<b>%{x|%b %Y}</b><br>Units: %{y:,}<extra></extra>",
        ))
        # Weekend markers
        fig.add_trace(go.Scatter(
            x=md["month"][::3], y=md["units_sold"][::3] + 1200,
            mode="markers",
            marker=dict(symbol="circle", size=6, color=accent2(theme)),
            name="Quarterly peak",
            hovertemplate="%{x|%b %Y}: %{y:,}<extra></extra>",
        ))
        chart_layout(fig, "Monthly Demand Trend — All Stores", height=280, theme=theme)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cw = data["cat_waste"].sort_values("avg_waste")
        colors_bar = [
            accent(theme) if v > 2000 else
            warn_c(theme) if v > 1000 else
            accent2(theme)
            for v in cw["avg_waste"]
        ]
        fig2 = go.Figure(go.Bar(
            x=cw["avg_waste"], y=cw["category"],
            orientation="h",
            marker=dict(color=colors_bar, opacity=0.85),
            hovertemplate="<b>%{y}</b><br>Avg waste: %{x:,} units<extra></extra>",
        ))
        chart_layout(fig2, "Avg Waste by Category", height=280, theme=theme)
        st.plotly_chart(fig2, use_container_width=True)

    # Store demand bars + expiry distribution
    col3, col4 = st.columns(2)

    with col3:
        fc_agg = data["forecast_df"].groupby("store_id")["forecasted_demand"].sum().reset_index()
        fc_agg = fc_agg.sort_values("forecasted_demand", ascending=False)
        fc_agg["color"] = [
            accent(theme) if i < 3 else
            warn_c(theme) if i < 6 else
            muted_c(theme)
            for i in range(len(fc_agg))
        ]
        fig3 = go.Figure(go.Bar(
            x=fc_agg["forecasted_demand"],
            y=fc_agg["store_id"],
            orientation="h",
            marker=dict(color=fc_agg["color"], opacity=0.9),
            hovertemplate="<b>%{y}</b><br>30-day demand: %{x:,} units<extra></extra>",
        ))
        chart_layout(fig3, "30-Day Forecasted Demand by Store", height=280, theme=theme)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        dz = data["dz"]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=dz["Days to Expiry"], y=dz["Transactions"],
            marker=dict(
                color=dz["Days to Expiry"],
                colorscale=[[0, danger_c(theme)], [0.25, warn_c(theme)], [1, accent(theme)]],
                opacity=0.85,
            ),
            hovertemplate="<b>%{x} days left</b><br>Transactions: %{y:,}<extra></extra>",
        ))
        fig4.add_vrect(x0=-0.5, x1=2.5, fillcolor=danger_c(theme), opacity=0.07, line_width=0, annotation_text="DANGER", annotation_position="top left", annotation_font_color=danger_c(theme), annotation_font_size=10)
        fig4.add_vrect(x0=2.5, x1=6.5, fillcolor=warn_c(theme), opacity=0.04, line_width=0)
        chart_layout(fig4, "Expiry Timeline Distribution — Danger Zone Highlighted", height=280, theme=theme)
        st.plotly_chart(fig4, use_container_width=True)

    # Alert strip
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:4px">
        <div style="background:{c['bg3']};border:1px solid rgba(255,71,87,0.2);border-left:3px solid {c['danger']};border-radius:10px;padding:14px 16px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{c['danger']};margin-bottom:6px">🚨 High Priority</div>
            <div style="font-size:13px;color:{c['text']}">Store_1 waste rate 78.7% — Fresh Foods critical zone</div>
        </div>
        <div style="background:{c['bg3']};border:1px solid rgba(255,184,0,0.2);border-left:3px solid {c['warn']};border-radius:10px;padding:14px 16px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{c['warn']};margin-bottom:6px">⚠️ Weekend Alert</div>
            <div style="font-size:13px;color:{c['text']}">+157% demand surge expected Sat–Sun across all stores</div>
        </div>
        <div style="background:{c['bg3']};border:1px solid rgba(0,229,160,0.2);border-left:3px solid {c['accent']};border-radius:10px;padding:14px 16px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{c['accent']};margin-bottom:6px">✅ Top Performer</div>
            <div style="font-size:13px;color:{c['text']}">Store_9 leads demand at 83 units/day — prioritize replenishment</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 2 — DEMAND FORECAST
# ══════════════════════════════════════════════
with tabs[1]:

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Prophet MAE",      "48.3 u/d",  "Store_1 only")
    k2.metric("XGBoost Avg MAE",  "6.2 u/d",   "All 10 stores ↓")
    k3.metric("Demand R²",        "0.9475",    "log-space RF")
    k4.metric("Weekend Surge",    "+157%",     "vs weekday", delta_color="off")
    k5.metric("Top Store",        "83 u/day",  "Store_9")

    col1, col2 = st.columns([3, 2])

    with col1:
        # Multi-store 30-day forecast lines
        fc = data["forecast_df"]
        fig = go.Figure()
        palette = [accent(theme), accent2(theme), warn_c(theme), danger_c(theme), purple_c(theme),
                   "#f97316","#06b6d4","#84cc16","#ec4899","#fb923c"]
        all_s = sorted(fc["store_id"].unique())
        if sel_store != "All Stores":
            plot_stores = [sel_store]
        else:
            plot_stores = all_s[:5]  # top 5 for clarity

        for i, s in enumerate(plot_stores):
            df_s = fc[fc["store_id"] == s].sort_values("date")
            fig.add_trace(go.Scatter(
                x=df_s["date"], y=df_s["forecasted_demand"],
                mode="lines", name=s,
                line=dict(color=palette[i % len(palette)], width=2),
                hovertemplate=f"<b>{s}</b> — %{{x|%d %b}}: %{{y}} units<extra></extra>",
            ))
        chart_layout(fig, "30-Day Walk-Forward Demand Forecast", height=300, theme=theme)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        xm = data["xgb_metrics"].sort_values("MAE")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=xm["MAE"], y=xm["store"],
            orientation="h",
            marker=dict(
                color=[accent(theme) if v < 5 else warn_c(theme) if v < 8 else danger_c(theme) for v in xm["MAE"]],
                opacity=0.88,
            ),
            name="MAE",
            hovertemplate="<b>%{y}</b><br>MAE: %{x:.1f} units/day<extra></extra>",
        ))
        chart_layout(fig2, "XGBoost MAE per Store (lower = better)", height=300, theme=theme)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns([2, 3])

    with col3:
        st.markdown(f"""
        <div class="fg-card">
            <div class="fg-card-title">📐 Model Comparison</div>
        """, unsafe_allow_html=True)
        model_compare = pd.DataFrame({
            "Model":    ["Prophet","XGBoost TS","RF Regressor","RF Part 2"],
            "MAE":      ["48.3","6.2","88.8","—"],
            "RMSE":     ["53.7","14.9","184.9","—"],
            "R²":       ["—","—","0.9475","0.8468"],
            "Split":    ["Time","Time","Time","Time"],
        })
        st.dataframe(model_compare, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Weekend vs weekday
        wknd = data["forecast_df"].copy()
        wknd["is_weekend"] = pd.to_datetime(wknd["date"]).dt.dayofweek >= 5
        wknd_avg = wknd[wknd["is_weekend"]]["forecasted_demand"].mean()
        wkdy_avg = wknd[~wknd["is_weekend"]]["forecasted_demand"].mean()
        fig_bar = go.Figure(go.Bar(
            x=["Weekday","Weekend"],
            y=[round(wkdy_avg, 1), round(wknd_avg, 1)],
            marker_color=[accent2(theme), accent(theme)],
            text=[f"{round(wkdy_avg,1)}", f"{round(wknd_avg,1)}"],
            textposition="outside",
            hovertemplate="%{x}: %{y:.1f} units/day<extra></extra>",
        ))
        chart_layout(fig_bar, "Weekend vs Weekday Demand", height=220, theme=theme)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col4:
        # Scatter MAE vs RMSE
        xm2 = data["xgb_metrics"]
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=xm2["MAE"], y=xm2["RMSE"],
            mode="markers+text",
            marker=dict(
                size=14, color=xm2["MAPE"],
                colorscale=[[0, accent(theme)],[0.5, warn_c(theme)],[1, danger_c(theme)]],
                showscale=True,
                colorbar=dict(title=dict(text="MAPE%", font=dict(size=10)), tickfont=dict(size=9)),
                opacity=0.9,
            ),
            text=xm2["store"],
            textposition="top center",
            textfont=dict(size=9, color=text_c(theme)),
            hovertemplate="<b>%{text}</b><br>MAE: %{x:.1f}<br>RMSE: %{y:.1f}<extra></extra>",
        ))
        chart_layout(fig3, "MAE vs RMSE — XGBoost per Store (color = MAPE)", height=320, theme=theme)
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 3 — SPOILAGE RISK
# ══════════════════════════════════════════════
with tabs[2]:

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("ROC-AUC",          "0.9996",  "Volume target")
    k2.metric("Precision / Recall","0.99",   "Both classes")
    k3.metric("Waste Vol R²",     "0.9766",  "Test set")
    k4.metric("Waste MAE",        "132.7 u", "Per transaction")
    k5.metric("Danger Zone",      "29.5%",   "26,849 items ≤3d", delta_color="inverse")

    col1, col2, col3 = st.columns([1.5, 1, 1.5])

    with col1:
        feats = data["features"]
        colors_f = [
            danger_c(theme) if i < 2 else
            warn_c(theme)   if i < 5 else
            accent2(theme)  if i < 9 else
            muted_c(theme)
            for i in range(len(feats))
        ]
        fig = go.Figure(go.Bar(
            x=feats["importance"],
            y=feats["feature"],
            orientation="h",
            marker=dict(color=colors_f[::-1], opacity=0.88),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.3f}<extra></extra>",
        ))
        chart_layout(fig, "Top Feature Importances — Spoilage Model", height=350, theme=theme)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Confusion matrix heatmap
        cm_data = [[8997, 98], [72, 9008]]
        fig2 = go.Figure(go.Heatmap(
            z=cm_data,
            x=["Pred: Low","Pred: High"],
            y=["True: Low","True: High"],
            colorscale=[[0, bg3_c(theme)],[0.5, accent2(theme)],[1, accent(theme)]],
            text=[[f"{v:,}" for v in row] for row in cm_data],
            texttemplate="%{text}",
            textfont=dict(size=16, family="Syne, sans-serif"),
            showscale=False,
            hovertemplate="True: %{y}<br>Pred: %{x}<br>Count: %{z:,}<extra></extra>",
        ))
        chart_layout(fig2, "Confusion Matrix (18,175 test samples)", height=350, theme=theme)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        # Waste by category donut
        cw = data["cat_waste"]
        fig3 = go.Figure(go.Pie(
            labels=cw["category"],
            values=cw["avg_waste"],
            hole=0.58,
            marker=dict(colors=[danger_c(theme), warn_c(theme), accent2(theme),
                                 purple_c(theme), accent(theme), muted_c(theme),
                                 "#f97316"]),
            hovertemplate="<b>%{label}</b><br>Avg waste: %{value:,} units (%{percent})<extra></extra>",
        ))
        chart_layout(fig3, "Waste Distribution by Category", height=350, theme=theme)
        fig3.update_layout(showlegend=True, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig3, use_container_width=True)

    # Weather impact
    col4, col5 = st.columns([2, 3])

    with col4:
        st.markdown(f"""
        <div class="fg-card">
            <div class="fg-card-title">🌡️ Weather Risk by Store</div>
        </div>""", unsafe_allow_html=True)
        weather = data["weather"].copy()
        def risk_badge(r):
            if r == "HIGH":   return f'<span class="badge-red">{r}</span>'
            if r == "MEDIUM": return f'<span class="badge-warn">{r}</span>'
            return f'<span class="badge-green">{r}</span>'
        weather["Risk"] = weather["Heatwave Risk"].apply(risk_badge)
        st.markdown(weather[["Store","Avg Temp (°C)","Max Temp (°C)","Waste Premium","Risk"]].to_html(escape=False, index=False, classes="dz-table"), unsafe_allow_html=True)

    with col5:
        weather2 = data["weather"]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name="Avg Temp (°C)",
            x=weather2["Store"], y=weather2["Avg Temp (°C)"],
            marker_color=accent2(theme), opacity=0.8,
        ))
        fig4.add_trace(go.Bar(
            name="Max Temp (°C)",
            x=weather2["Store"], y=weather2["Max Temp (°C)"],
            marker_color=danger_c(theme), opacity=0.6,
        ))
        fig4.add_trace(go.Scatter(
            name="High Temp Days",
            x=weather2["Store"], y=weather2["High Temp Days"],
            mode="lines+markers",
            yaxis="y2",
            line=dict(color=warn_c(theme), width=2, dash="dot"),
            marker=dict(size=8),
        ))
        chart_layout(fig4, "Temperature Profile & High-Temp Days by Store", height=300, theme=theme)
        fig4.update_layout(
            barmode="group",
            yaxis2=dict(overlaying="y", side="right", title="High Temp Days", showgrid=False,
                        color=muted_c(theme)),
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 4 — AI AGENTS
# ══════════════════════════════════════════════
with tabs[3]:

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Agents Active",    "4",        "Inventory·Demand·Weather·Decision")
    k2.metric("Stores Processed", "10/10",    "100% coverage")
    k3.metric("LLM",              "LLaMA 3",  "Local via Ollama")
    k4.metric("Avg Waste Rate",   "78.7%",    "Store_1 highest")
    k5.metric("Heatwave Risk",    "MEDIUM",   "Avg 24.4°C / Max 35°C")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Agent pipeline visual
        st.markdown(f"""
        <div class="fg-card" style="height:100%">
            <div class="fg-card-title">🔗 Agent Pipeline</div>
            <div style="display:flex;flex-direction:column;gap:0;">
                <div style="background:{c['bg3']};border:1px solid {c['border']};border-radius:10px;padding:14px 16px;position:relative">
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{c['accent']}">📦 Inventory Agent</div>
                    <div style="font-size:11px;color:{c['text_muted']};margin-top:4px">Stock · Expiry · Waste rate · Low-stock alerts</div>
                </div>
                <div style="text-align:center;font-size:18px;color:{c['text_muted']};padding:4px 0">↓</div>
                <div style="background:{c['bg3']};border:1px solid {c['border']};border-radius:10px;padding:14px 16px;">
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{c['accent2']}">📈 Demand Agent</div>
                    <div style="font-size:11px;color:{c['text_muted']};margin-top:4px">30-day forecast · Replenishment · Weekend peaks</div>
                </div>
                <div style="text-align:center;font-size:18px;color:{c['text_muted']};padding:4px 0">↓</div>
                <div style="background:{c['bg3']};border:1px solid {c['border']};border-radius:10px;padding:14px 16px;">
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{c['warn']}">🌡️ Weather Agent</div>
                    <div style="font-size:11px;color:{c['text_muted']};margin-top:4px">Temp risk · Humidity · Shelf-life reduction</div>
                </div>
                <div style="text-align:center;font-size:18px;color:{c['text_muted']};padding:4px 0">↓</div>
                <div style="background:linear-gradient(135deg,rgba(0,229,160,0.08),rgba(0,150,255,0.06));border:1px solid {c['accent']};border-radius:10px;padding:14px 16px;">
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{c['text']}">🧠 Decision Agent</div>
                    <div style="font-size:11px;color:{c['text_muted']};margin-top:4px">Synthesizes all 3 reports → Final action plan</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Action recommendations
        st.markdown(f"""
        <div class="fg-card-title" style="margin-bottom:14px">🎯 AI Recommendations — All Stores</div>
        """, unsafe_allow_html=True)

        recs = data["agent_recs"]
        if sel_store != "All Stores":
            recs = [r for r in recs if r["store"] == sel_store]

        type_colors = {
            "DISCOUNT":     (c["accent"],  "badge-green"),
            "REPLENISHMENT":(c["accent2"], "badge-blue"),
            "REDISTRIBUTE": (c["purple"],  "badge-purple"),
            "REDUCE ORDER": (c["warn"],    "badge-warn"),
        }

        for rec in recs:
            col, badge_cls = type_colors.get(rec["type"], (c["text_muted"], "badge-blue"))
            st.markdown(f"""
            <div class="action-item">
                <span style="font-size:18px;flex-shrink:0">{rec['icon']}</span>
                <div style="flex:1">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
                        <span class="{badge_cls}">{rec['type']}</span>
                        <span style="font-family:'DM Mono',monospace;font-size:10px;color:{c['text_muted']}">{rec['store']}</span>
                    </div>
                    <div style="font-size:13px;color:{c['text']};line-height:1.5">{rec['text']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 5 — OPTIMIZATION
# ══════════════════════════════════════════════
with tabs[4]:

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Optimizer",        "PuLP LP",   "Linear Programming")
    k2.metric("Discount Models",  "10 stores", "Per-category LP")
    k3.metric("Total Waste Saved","411K units","Via discounting")
    k4.metric("Replenish Cost",   "₹7.94L",   "Optimal orders")

    col1, col2 = st.columns(2)

    with col1:
        disc = data["discount_opt"]
        if sel_store != "All Stores":
            disc = disc[disc["store_id"] == sel_store]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Revenue Before Discount",
            x=disc["Store"], y=disc["Revenue Before"],
            marker_color=danger_c(theme), opacity=0.75,
        ))
        fig.add_trace(go.Bar(
            name="Revenue After Discount",
            x=disc["Store"], y=disc["Revenue After"],
            marker_color=accent(theme), opacity=0.85,
        ))
        chart_layout(fig, "Revenue: Before vs After Optimal Discounting (INR)", height=300, theme=theme)
        fig.update_layout(barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        disc2 = data["discount_opt"]
        fig2 = go.Figure(go.Bar(
            x=disc2["Store"],
            y=disc2["Optimal Discount %"],
            marker=dict(
                color=disc2["Optimal Discount %"],
                colorscale=[[0, accent(theme)],[0.5, warn_c(theme)],[1, danger_c(theme)]],
                opacity=0.88,
            ),
            text=[f"{v}%" for v in disc2["Optimal Discount %"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Optimal discount: %{y}%<extra></extra>",
        ))
        fig2.add_hline(y=20, line_color=danger_c(theme), line_dash="dot",
                       annotation_text="20% threshold", annotation_font_color=danger_c(theme), annotation_font_size=10)
        chart_layout(fig2, "Optimal Discount % per Store (LP Solution)", height=300, theme=theme)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns([3, 2])

    with col3:
        rep = data["replenish_opt"]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Current Stock",
            x=rep["Store"], y=rep["Current Stock"],
            marker_color=accent2(theme), opacity=0.75,
        ))
        fig3.add_trace(go.Bar(
            name="Optimal Order",
            x=rep["Store"], y=rep["Optimal Order"],
            marker_color=accent(theme), opacity=0.85,
        ))
        chart_layout(fig3, "Replenishment Optimizer — Current Stock vs Optimal Order", height=280, theme=theme)
        fig3.update_layout(barmode="group")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown(f"""
        <div class="fg-card">
            <div class="fg-card-title">⚡ Replenishment Urgency</div>
        </div>""", unsafe_allow_html=True)
        rep2 = data["replenish_opt"][["Store","Category","Urgency","Order Cost INR"]].copy()
        def urgency_badge(u):
            if u == "HIGH":   return f'<span class="badge-red">{u}</span>'
            if u == "MEDIUM": return f'<span class="badge-warn">{u}</span>'
            return f'<span class="badge-green">{u}</span>'
        rep2["Urgency"] = rep2["Urgency"].apply(urgency_badge)
        rep2["Order Cost INR"] = rep2["Order Cost INR"].apply(lambda x: f"₹{x:,}")
        st.markdown(rep2.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Waste saved bar
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    disc3 = data["discount_opt"]
    fig4 = go.Figure(go.Bar(
        x=disc3["Store"], y=disc3["Waste Saved"],
        marker=dict(color=disc3["Waste Saved"],
                    colorscale=[[0, accent(theme)],[1, accent2(theme)]],
                    opacity=0.88),
        text=[f"{v:,}" for v in disc3["Waste Saved"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Units saved from waste: %{y:,}<extra></extra>",
    ))
    chart_layout(fig4, "Total Units Saved from Waste — Optimal Discounting Strategy", height=250, theme=theme)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 6 — MODEL AUDIT
# ══════════════════════════════════════════════
with tabs[5]:

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Models Trained",   "6",        "All leakage-free")
    k2.metric("Leakage Cols",     "12",       "All removed ✓")
    k3.metric("Spoilage AUC",     "0.9996",   "Train gap: 0.0003")
    k4.metric("Demand R²",        "0.9475",   "log-space test")
    k5.metric("XGBoost MAE",      "6.2 u/d",  "Avg all stores")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div class="fg-card-title" style="margin-bottom:12px">🔒 Data Leakage Registry — 12 Columns Removed</div>
        """, unsafe_allow_html=True)

        leakage = data["leakage"]
        type_colors_leak = {
            "Sale-time":       c["danger"],
            "Derived":         c["warn"],
            "Target Encoding": c["purple"],
            "Outcome":         c["danger"],
            "Future info":     c["danger"],
            "Target":          c["accent2"],
            "Collinear":       c["warn"],
            "Near-zero var.":  c["text_muted"],
        }
        for _, row in leakage.iterrows():
            col_c = type_colors_leak.get(row["Type"], c["text_muted"])
            st.markdown(f"""
            <div class="leak-row leak-pass">
                <span style="font-size:14px">✅</span>
                <span style="font-family:'DM Mono',monospace;font-size:12px;font-weight:500;color:{c['accent']};width:200px;flex-shrink:0">{row['Column']}</span>
                <span style="font-size:11px;padding:2px 8px;border-radius:4px;background:rgba(255,255,255,0.05);color:{col_c};flex-shrink:0;margin-right:8px">{row['Type']}</span>
                <span style="font-size:12px;color:{c['text_muted']}">{row['Reason']}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="fg-card-title" style="margin-bottom:12px">📊 Model Performance — Train vs Test</div>
        """, unsafe_allow_html=True)
        mp = data["model_perf"]
        def status_badge(s):
            if "✅" in s: return f'<span class="badge-green">{s}</span>'
            if "⚠️" in s: return f'<span class="badge-warn">{s}</span>'
            return f'<span class="badge-red">{s}</span>'
        mp_display = mp.copy()
        mp_display["Status"] = mp_display["Status"].apply(status_badge)
        st.markdown(mp_display.to_html(escape=False, index=False), unsafe_allow_html=True)

        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

        # 4 fixes applied
        st.markdown(f"""
        <div style="background:{c['bg3']};border:1px solid rgba(0,229,160,0.2);border-radius:12px;padding:16px 18px;margin-top:8px">
            <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{c['accent']};margin-bottom:12px">✅ 4 Critical Fixes Applied</div>
            <div style="display:flex;flex-direction:column;gap:7px;font-size:12px;color:{c['text']}">
                <div>🔧 <b>Fix #1</b> — Spoilage threshold computed on train set only</div>
                <div>🔧 <b>Fix #2</b> — LabelEncoder fitted on train set only</div>
                <div>🔧 <b>Fix #3</b> — Train + test scores for every model</div>
                <div>🔧 <b>Fix #4</b> — Waste rate target (waste/stock) added</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Feature importance radar
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        feats = data["features"]
        fig5 = go.Figure(go.Bar(
            x=feats["importance"],
            y=feats["feature"],
            orientation="h",
            marker=dict(
                color=feats["importance"],
                colorscale=[[0, muted_c(theme)],[0.5, accent2(theme)],[1, accent(theme)]],
                opacity=0.88,
            ),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
        ))
        chart_layout(fig5, "Feature Importances — Spoilage Classifier (RF)", height=320, theme=theme)
        st.plotly_chart(fig5, use_container_width=True)

    with col4:
        # Model AUC / R2 bar
        models_bar = pd.DataFrame({
            "model":  ["Spoilage AUC","Demand R²","Waste R²","RF Part2 R²"],
            "train":  [0.9999, 0.9821, 0.9990, 0.9610],
            "test":   [0.9996, 0.9475, 0.9766, 0.8468],
        })
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(name="Train", x=models_bar["model"], y=models_bar["train"],
                              marker_color=accent2(theme), opacity=0.7))
        fig6.add_trace(go.Bar(name="Test", x=models_bar["model"], y=models_bar["test"],
                              marker_color=accent(theme), opacity=0.9))
        chart_layout(fig6, "Train vs Test Score — All Models (no overfitting if gap < 0.03)", height=320, theme=theme)
        fig6.update_layout(barmode="group", yaxis=dict(range=[0.7, 1.02]))
        st.plotly_chart(fig6, use_container_width=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid {c['border']};padding-top:16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
    <div style="font-size:11px;color:{c['text_muted']}">
        <span style="font-family:'DM Mono',monospace">FreshnessGuard AI</span> — Built with Streamlit · Python · Plotly · LangChain · PuLP · XGBoost · Prophet
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <span class="badge-green">✅ Leakage-Free</span>
        <span class="badge-blue">6 ML Models</span>
        <span class="badge-purple">4 AI Agents</span>
        <span class="badge-warn">10 Stores</span>
    </div>
</div>
""", unsafe_allow_html=True)
