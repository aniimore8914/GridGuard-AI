import streamlit as st
import pandas as pd
import joblib
import datetime
import io
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="GridGuard AI", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# ── DESIGN SYSTEM ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #080C14 !important;
    color: #C8D6E8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1200px !important; }

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #0D1929 0%, #080C14 60%);
    border-bottom: 1px solid #1A2740;
    padding: 2.5rem 0 2rem;
    margin: 0 -2rem 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(0,210,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-inner { padding: 0 2rem; }
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    color: #00C2FF;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #EEF4FF;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #00C2FF; }
.hero-sub {
    font-size: 0.95rem;
    color: #6B82A0;
    font-weight: 400;
    margin-top: 0.4rem;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,194,255,0.08);
    border: 1px solid rgba(0,194,255,0.2);
    border-radius: 100px;
    padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #00C2FF;
    margin-top: 1rem;
}
.status-dot {
    width: 6px; height: 6px;
    background: #00C2FF;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Stat Cards ── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: #0D1929;
    border: 1px solid #1A2740;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00C2FF, transparent);
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4A6080;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #EEF4FF;
    line-height: 1;
}
.stat-unit {
    font-size: 0.8rem;
    color: #4A6080;
    font-weight: 400;
    margin-left: 3px;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4A6080;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1A2740;
}

/* ── Input Panel ── */
.input-panel {
    background: #0D1929;
    border: 1px solid #1A2740;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
}
.input-panel-title {
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #00C2FF;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Streamlit widget overrides ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #060A12 !important;
    border: 1px solid #1A2740 !important;
    border-radius: 8px !important;
    color: #C8D6E8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #00C2FF !important;
    box-shadow: 0 0 0 2px rgba(0,194,255,0.12) !important;
}
label, .stSelectbox label, .stNumberInput label {
    color: #6B82A0 !important;
    font-size: 0.78rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Predict Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0090CC 0%, #00C2FF 100%) !important;
    color: #000 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,194,255,0.25) !important;
}

/* ── Result Cards ── */
.result-danger {
    background: linear-gradient(135deg, #1A0A0A, #200D0D);
    border: 1px solid #4A1515;
    border-left: 3px solid #FF3B3B;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-top: 1rem;
}
.result-safe {
    background: linear-gradient(135deg, #0A1A12, #0D201A);
    border: 1px solid #15402A;
    border-left: 3px solid #00E88F;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-top: 1rem;
}
.result-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.result-label {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4A6080;
    margin-bottom: 0.25rem;
}
.result-title-danger { font-size: 1.4rem; font-weight: 700; color: #FF3B3B; }
.result-title-safe   { font-size: 1.4rem; font-weight: 700; color: #00E88F; }
.result-prob {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.5rem;
    font-weight: 600;
    margin-top: 0.75rem;
    line-height: 1;
}
.result-prob-label { font-size: 0.7rem; color: #4A6080; margin-top: 0.2rem; }

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00C2FF, #FF3B3B) !important;
    border-radius: 4px !important;
}
.stProgress > div > div {
    background: #1A2740 !important;
    border-radius: 4px !important;
    height: 6px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px !important;
    border-bottom: 1px solid #1A2740 !important;
    margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #4A6080 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px 8px 0 0 !important;
    letter-spacing: 0.02em !important;
}
.stTabs [aria-selected="true"] {
    color: #00C2FF !important;
    background: rgba(0,194,255,0.06) !important;
    border-bottom: 2px solid #00C2FF !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    background: #0D1929 !important;
    border: 1px dashed #1A2740 !important;
    border-radius: 12px !important;
}
.stFileUploader label { color: #6B82A0 !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px !important; overflow: hidden !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #1A2740 !important;
    color: #C8D6E8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
}
.stDownloadButton > button:hover {
    border-color: #00C2FF !important;
    color: #00C2FF !important;
}

/* ── Info box ── */
.stAlert {
    background: rgba(0,194,255,0.05) !important;
    border: 1px solid rgba(0,194,255,0.15) !important;
    border-radius: 10px !important;
    color: #6B82A0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── MODEL ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load(BASE_DIR / "models" / "power_outage_model.pkl")

try:
    model = load_model()
    model_ok = True
except Exception as e:
    model_ok = False
    st.error(f"Model load failed: {e}")
    st.stop()

MODEL_COLUMNS = [
    'country','lat','lon','grid_zone','hour_of_day','day_of_week',
    'month','season','is_holiday','temperature_celsius','rainfall_mm',
    'wind_speed_kmh','storm_happened','storm_type','lightning_strikes',
    'total_power_capacity_mw','renewable_power_mw','fossil_power_mw',
    'electricity_demand_mw','grid_load_percent','outages_last_7_days',
    'outages_last_30_days','high_grid_load','demand_capacity_ratio','renewable_share'
]

COUNTRY_MAP   = {0:'Australia',1:'Brazil',2:'Canada',3:'China',4:'France',5:'Germany',6:'India',7:'Japan',8:'Russia',9:'USA'}
GRID_ZONE_MAP = {0:'Central',1:'East',2:'North',3:'South',4:'West'}
DAY_MAP       = {0:'Fri',1:'Mon',2:'Sat',3:'Sun',4:'Thu',5:'Tue',6:'Wed'}
SEASON_MAP    = {0:'Autumn',1:'Monsoon',2:'Summer',3:'Winter'}
STORM_MAP     = {0:'None',1:'Duststorm',2:'Heatwave',3:'Thunderstorm'}

def smart_read(uploaded_file):
    raw_bytes = uploaded_file.read()
    try:
        content = raw_bytes.decode("utf-8")
        first_line = content.split('\n')[0]
        if first_line.startswith('"') and ',' in first_line:
            lines = [line.strip().strip('"') for line in content.strip().split('\n')]
            content = '\n'.join(lines)
        return pd.read_csv(io.StringIO(content))
    except Exception:
        return pd.read_excel(io.BytesIO(raw_bytes))

def restore_text_columns(df):
    work = df.copy()
    if pd.api.types.is_integer_dtype(work.get('country', pd.Series(dtype=str))):
        work['country']     = work['country'].map(COUNTRY_MAP).fillna('India')
    if pd.api.types.is_integer_dtype(work.get('grid_zone', pd.Series(dtype=str))):
        work['grid_zone']   = work['grid_zone'].map(GRID_ZONE_MAP).fillna('North')
    if pd.api.types.is_integer_dtype(work.get('day_of_week', pd.Series(dtype=str))):
        work['day_of_week'] = work['day_of_week'].map(DAY_MAP).fillna('Mon')
    if pd.api.types.is_integer_dtype(work.get('season', pd.Series(dtype=str))):
        work['season']      = work['season'].map(SEASON_MAP).fillna('Summer')
    if pd.api.types.is_integer_dtype(work.get('storm_type', pd.Series(dtype=str))):
        work['storm_type']  = work['storm_type'].map(STORM_MAP).fillna('None')
    return work

def prepare_features(df):
    work = df.copy()
    work = work.drop(columns=[c for c in ["outage_in_next_24_hours","state","district","id"] if c in work.columns])
    work = restore_text_columns(work)
    work['demand_capacity_ratio'] = work['electricity_demand_mw'] / work['total_power_capacity_mw']
    work['renewable_share']       = work['renewable_power_mw']    / work['total_power_capacity_mw']
    work['high_grid_load']        = (work['grid_load_percent'] > 80).astype(int)
    missing = [c for c in MODEL_COLUMNS if c not in work.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return work[MODEL_COLUMNS]

# ── HERO ──────────────────────────────────────────────────────────────────────
now = datetime.datetime.now()
st.markdown(f"""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">Power Grid Intelligence System</div>
    <div class="hero-title">Grid<span>Guard</span> AI</div>
    <div class="hero-sub">XGBoost · 85% Accuracy · Real-time outage risk scoring</div>
    <div class="status-pill">
      <div class="status-dot"></div>
      MODEL ONLINE &nbsp;·&nbsp; {now.strftime("%d %b %Y, %H:%M")}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["⚡  Manual Prediction", "📂  Batch Prediction"])

# ════════════════════════════════════════════════════════
# TAB 1 — MANUAL
# ════════════════════════════════════════════════════════
with tab1:

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # Grid parameters
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-title">⚡ Grid Parameters</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            demand   = st.number_input("Demand (MW)",   value=5000.0, step=100.0)
            capacity = st.number_input("Capacity (MW)", value=8000.0, step=100.0)
        with c2:
            renewable   = st.number_input("Renewable (MW)", value=2500.0, step=100.0)
            temperature = st.number_input("Temperature (°C)", value=30.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

        # Location & time
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-title">🌍 Location & Conditions</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            country   = st.selectbox("Country",   ["Australia","Brazil","Canada","China","France","Germany","India","Japan","Russia","USA"])
            grid_zone = st.selectbox("Grid Zone", ["Central","East","North","South","West"])
            season    = st.selectbox("Season",    ["Autumn","Monsoon","Summer","Winter"])
        with c4:
            storm_type     = st.selectbox("Storm Type",     ["None","Duststorm","Heatwave","Thunderstorm"])
            storm_happened = st.selectbox("Storm Active?",  [0, 1], format_func=lambda x: "Yes" if x else "No")
            is_holiday     = st.selectbox("Public Holiday?", [0, 1], format_func=lambda x: "Yes" if x else "No")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Live stats
        load_pct = (demand / capacity * 100) if capacity else 0
        fossil   = capacity - renewable
        st.markdown(f"""
        <div class="stat-row" style="grid-template-columns:1fr 1fr; margin-bottom:1rem;">
          <div class="stat-card">
            <div class="stat-label">Grid Load</div>
            <div class="stat-value">{load_pct:.0f}<span class="stat-unit">%</span></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Fossil MW</div>
            <div class="stat-value">{fossil:,.0f}<span class="stat-unit">MW</span></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Demand</div>
            <div class="stat-value">{demand:,.0f}<span class="stat-unit">MW</span></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Renewable</div>
            <div class="stat-value">{renewable:,.0f}<span class="stat-unit">MW</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if load_pct > 100:
            st.warning("⚠️ Demand exceeds capacity — critical overload!")

        predict_btn = st.button("Run Prediction →", key="manual_predict", use_container_width=True)

        if predict_btn:
            raw = pd.DataFrame([{
                "country": country, "lat": 0, "lon": 0, "grid_zone": grid_zone,
                "hour_of_day": now.hour, "day_of_week": now.strftime("%a"),
                "month": now.month, "season": season, "is_holiday": is_holiday,
                "temperature_celsius": temperature, "rainfall_mm": 0,
                "wind_speed_kmh": 10, "storm_happened": storm_happened,
                "storm_type": storm_type, "lightning_strikes": 0,
                "total_power_capacity_mw": capacity, "renewable_power_mw": renewable,
                "fossil_power_mw": fossil, "electricity_demand_mw": demand,
                "grid_load_percent": load_pct,
                "outages_last_7_days": 0, "outages_last_30_days": 0,
            }])
            try:
                input_df = prepare_features(raw)
                pred = model.predict(input_df)[0]
                prob = model.predict_proba(input_df)[0][1] if hasattr(model, "predict_proba") else None

                if pred == 1:
                    st.markdown(f"""
                    <div class="result-danger">
                      <div class="result-icon">🔴</div>
                      <div class="result-label">Risk Assessment</div>
                      <div class="result-title-danger">High Outage Risk</div>
                      <div class="result-prob" style="color:#FF3B3B">{prob:.0%}</div>
                      <div class="result-prob-label">outage probability</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-safe">
                      <div class="result-icon">🟢</div>
                      <div class="result-label">Risk Assessment</div>
                      <div class="result-title-safe">Grid Stable</div>
                      <div class="result-prob" style="color:#00E88F">{prob:.0%}</div>
                      <div class="result-prob-label">outage probability</div>
                    </div>
                    """, unsafe_allow_html=True)
                if prob is not None:
                    st.progress(float(prob))
            except Exception as e:
                st.exception(e)

# ════════════════════════════════════════════════════════
# TAB 2 — BATCH
# ════════════════════════════════════════════════════════
with tab2:
    st.info("Upload your raw or cleaned data file — CSV or XLS, both work. Predictions are added as new columns.")
    uploaded = st.file_uploader("Drop file here", type=["csv","xls","xlsx"], label_visibility="collapsed")

    if uploaded:
        try:
            df = smart_read(uploaded)
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows loaded",    f"{len(df):,}")
            c2.metric("Columns",        f"{len(df.columns)}")
            c3.metric("File",           uploaded.name)
            st.dataframe(df.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            df = None

        if df is not None and st.button("Run Batch Prediction →", key="batch_predict", use_container_width=True):
            try:
                with st.spinner("Scoring all rows…"):
                    input_df = prepare_features(df)
                    preds = model.predict(input_df)
                    probs = model.predict_proba(input_df)[:,1] if hasattr(model,"predict_proba") else None

                # Build the downloadable result from input_df (which has readable
                # text labels restored) rather than the raw uploaded df (which may
                # still have encoded numbers like country=0,1,2...)
                result = input_df.copy()
                result["Prediction"]        = ["⚠️ Outage" if p==1 else "✅ Stable" for p in preds]
                if probs is not None:
                    result["Outage Probability %"] = [f"{p:.1%}" for p in probs]

                outage_count = sum(preds)
                st.markdown(f"""
                <div class="stat-row">
                  <div class="stat-card">
                    <div class="stat-label">Total Rows</div>
                    <div class="stat-value">{len(result):,}</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-label">Outage Risk</div>
                    <div class="stat-value" style="color:#FF3B3B">{outage_count:,}</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-label">Grid Stable</div>
                    <div class="stat-value" style="color:#00E88F">{len(result)-outage_count:,}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(result, use_container_width=True)
                st.download_button(
                    "⬇️  Download Results CSV",
                    result.to_csv(index=False).encode(),
                    "gridguard_predictions.csv", "text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.exception(e)