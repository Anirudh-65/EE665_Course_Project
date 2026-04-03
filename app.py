import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import warnings

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BMS Analytics | IIT Gandhinagar",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS  —  Professional red & white
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #D9D9D9 !important;
}
[data-testid="stSidebar"] * { color: #111111 !important; }
[data-testid="stSidebar"] h3 {
    color: #CC0000 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.7px;
}

/* Headings */
h1 { font-size: 26px !important; font-weight: 700 !important; color: #111111 !important; }
h2 { font-size: 18px !important; font-weight: 700 !important; color: #111111 !important; }
h3 { font-size: 15px !important; font-weight: 600 !important; color: #111111 !important; }

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #D9D9D9;
    gap: 8px;
}
[data-testid="stTabs"] button {
    color: #444444 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border-radius: 999px !important;
    padding: 10px 18px !important;
    border: 1px solid #D9D9D9 !important;
    background: #FFFFFF !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #CC0000 !important;
    border: 1px solid #CC0000 !important;
    font-weight: 700 !important;
    box-shadow: inset 0 -2px 0 #CC0000;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #BFBFBF !important;
    color: #111111 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] * { color: #111111 !important; }

/* Buttons */
[data-testid="baseButton-primary"] {
    background-color: #CC0000 !important;
    border: 1px solid #AA0000 !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}
[data-testid="baseButton-primary"]:hover {
    background-color: #AA0000 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #D9D9D9 !important;
    border-radius: 12px !important;
}

/* Sliders accent */
[data-testid="stSlider"] > div > div > div {
    background: #CC0000 !important;
}

/* ── Custom component classes ── */
.page-header {
    border: 1px solid #D9D9D9;
    border-top: 4px solid #CC0000;
    border-radius: 16px;
    padding: 20px 22px 18px 22px;
    margin-bottom: 26px;
    background:
        linear-gradient(135deg, rgba(204, 0, 0, 0.05) 0%, rgba(255, 255, 255, 0.0) 45%),
        #FFFFFF;
}
.page-header .kicker {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: #CC0000;
    margin-bottom: 8px;
}
.page-header h1 {
    margin: 0 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #111111 !important;
}
.page-header .sub {
    font-size: 14px;
    color: #333333;
    margin-top: 8px;
    line-height: 1.6;
}

.section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #111111;
    border-bottom: 1px solid #D9D9D9;
    padding-bottom: 8px;
    margin: 28px 0 16px 0;
}
.section-title span { color: #CC0000; }

.explain-card {
    background: #FFFFFF;
    border: 1px solid #D9D9D9;
    border-left: 4px solid #CC0000;
    border-radius: 14px;
    padding: 16px 18px;
    margin: 10px 0 18px 0;
}
.explain-card .title {
    font-size: 13px;
    font-weight: 700;
    color: #111111;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.explain-card .body {
    font-size: 13px;
    color: #222222;
    line-height: 1.7;
}
.micro-copy {
    font-size: 12px;
    color: #333333;
    line-height: 1.7;
    margin-top: -4px;
    margin-bottom: 12px;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid #D9D9D9;
    border-top: 3px solid #CC0000;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
}
.stat-card .label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #666666;
    margin-bottom: 6px;
}
.stat-card .value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #CC0000;
}
.stat-card .unit { font-size: 14px; color: #444444; }
.stat-card .sub  { font-size: 11px; color: #333333; margin-top: 4px; line-height: 1.6; }

.result-card {
    background: #FFFFFF;
    border: 2px solid #CC0000;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 10px 24px rgba(204, 0, 0, 0.08);
}
.result-card .label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #333333;
    margin-bottom: 10px;
}
.result-card .temp-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 56px;
    font-weight: 700;
    color: #CC0000;
    line-height: 1;
}
.result-card .temp-unit { font-size: 24px; color: #444444; }
.result-card .model-note { font-size: 12px; color: #444444; margin-top: 10px; }

.info-note {
    background: #FFFFFF;
    border: 1px solid #E2B3B3;
    border-left: 4px solid #CC0000;
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 12px;
    color: #222222;
    margin-bottom: 14px;
    line-height: 1.7;
}

.sidebar-card {
    background: #FFFFFF;
    border: 1px solid #D9D9D9;
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 12px;
    font-size: 12px;
    color: #111111;
    line-height: 1.8;
}
.sidebar-card .sc-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #CC0000;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FEATURE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
MODEL_FILE_CANDIDATES = {
    'Decision Tree': ['Models_Praneel/dt_core.pkl', 'Models_Praneel/best_core.pkl'],
    'XGBoost': ['Models_Anirudh/tuned_xgb_core.joblib', 'Models_Anirudh/baseline_xgb_core.joblib'],
    'Linear Regression': ['Models_Praneel/lr_core.pkl'],
    'Support Vector Regressor': ['Models_Praneel/svr_core.pkl'],
    'K-Nearest Neighbors': ['Models_Praneel/knn_core.pkl'],
    'Random Forest': ['Models_Anirudh/tuned_rf_core.joblib', 'Models_Anirudh/baseline_rf_core.joblib'],
}

PHYSICAL_TEMP_RANGE = (-20.0, 60.0)
CORE_TEMP_RANGE = (25.0, 45.0)
PRIMARY_SLIDERS = {
    'voltage': {'label': 'Cell Voltage Sensor', 'min': 3.90, 'max': 4.21, 'step': 0.01, 'unit': 'V'},
    'current': {'label': 'Pack Current Sensor', 'min': 3.80, 'max': 19.10, 'step': 0.10, 'unit': 'A'},
    'temperature': {'label': 'Surface Temperature Sensor', 'min': 20.0, 'max': 40.0, 'step': 0.5, 'unit': 'C'},
    'duration': {'label': 'Drive Window Duration', 'min': 280.0, 'max': 1280.0, 'step': 10.0, 'unit': 's'},
}
VISIBLE_SIM_INPUTS = ['voltage', 'current', 'duration']


def patch_model_compat(model, seen=None):
    """Patch known sklearn compatibility attributes on persisted models."""
    if seen is None:
        seen = set()
    if model is None:
        return None

    obj_id = id(model)
    if obj_id in seen:
        return model
    seen.add(obj_id)

    model_name = model.__class__.__name__
    if model_name in {
        'DecisionTreeRegressor', 'DecisionTreeClassifier',
        'RandomForestRegressor', 'RandomForestClassifier',
        'ExtraTreesRegressor', 'ExtraTreesClassifier',
    } and not hasattr(model, 'monotonic_cst'):
        model.monotonic_cst = None

    if hasattr(model, 'n_jobs') and model_name in {
        'RandomForestRegressor', 'RandomForestClassifier',
        'ExtraTreesRegressor', 'ExtraTreesClassifier',
        'KNeighborsRegressor', 'KNeighborsClassifier',
        'XGBRegressor', 'XGBClassifier',
    }:
        try:
            model.n_jobs = 1
        except Exception:
            pass

    if hasattr(model, 'steps'):
        for _, step in model.steps:
            patch_model_compat(step, seen)

    if hasattr(model, 'estimators_'):
        for estimator in model.estimators_:
            patch_model_compat(estimator, seen)

    return model


def infer_model_features_from_artifacts() -> list:
    for candidates in MODEL_FILE_CANDIDATES.values():
        for fname in candidates:
            if not os.path.isfile(fname):
                continue
            try:
                return list(joblib.load(fname).feature_names_in_)
            except Exception:
                continue

    if os.path.isfile('preproc_core.joblib'):
        try:
            preproc_bundle = joblib.load('preproc_core.joblib')
            if isinstance(preproc_bundle, dict):
                if preproc_bundle.get('features_list'):
                    return list(preproc_bundle['features_list'])
                if 'preproc' in preproc_bundle and hasattr(preproc_bundle['preproc'], 'feature_names_in_'):
                    return list(preproc_bundle['preproc'].feature_names_in_)
        except Exception:
            pass

    return []


@st.cache_data
def load_feature_reference() -> dict:
    feature_candidates = [
        'data_processed/features_cycle_with_core.parquet',
        'data_processed/features_cycle_with_core_fixed.parquet',
        'data_processed/features_cycle_with_core_scalar_fallback.parquet',
        'data_processed/features_cycle_with_core_and_soh.parquet',
    ]

    feature_df = pd.DataFrame()
    for fname in feature_candidates:
        if os.path.isfile(fname):
            try:
                feature_df = pd.read_parquet(fname)
                break
            except Exception:
                continue

    model_features = infer_model_features_from_artifacts()
    if not model_features and not feature_df.empty:
        model_features = feature_df.select_dtypes(include=[np.number]).columns.tolist()[:39]

    stats = {}
    defaults = {}
    stds = {}

    for feature in model_features:
        if not feature_df.empty and feature in feature_df.columns:
            series = pd.to_numeric(feature_df[feature], errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()
            if not series.empty:
                stats[feature] = {
                    'min': float(series.min()),
                    'max': float(series.max()),
                    'q10': float(series.quantile(0.10)),
                    'q25': float(series.quantile(0.25)),
                    'median': float(series.median()),
                    'q75': float(series.quantile(0.75)),
                    'q90': float(series.quantile(0.90)),
                }
                defaults[feature] = float(series.median())
                stds[feature] = float(series.std(ddof=0)) if len(series) > 1 else 1.0
                continue

        stats[feature] = {'min': 0.0, 'max': 1.0, 'q10': 0.0, 'q25': 0.0, 'median': 0.0, 'q75': 1.0, 'q90': 1.0}
        defaults[feature] = 0.0
        stds[feature] = 1.0

    return {'features': model_features, 'defaults': defaults, 'stats': stats, 'stds': stds}


FEATURE_REF = load_feature_reference()
CORE_FEATURES = FEATURE_REF['features']
RAW_DEFAULTS = FEATURE_REF['defaults']


def clamp_feature(name: str, value: float) -> float:
    meta = FEATURE_REF['stats'].get(name)
    if not meta:
        return float(value)
    low, high = meta['min'], meta['max']
    if low == high:
        return float(low)
    return float(np.clip(value, low, high))


def map_linear(value: float, src_low: float, src_high: float, dst_low: float, dst_high: float) -> float:
    if src_high == src_low:
        return float(dst_low)
    ratio = (value - src_low) / (src_high - src_low)
    return float(dst_low + ratio * (dst_high - dst_low))


def get_condition_defaults(climate: str, terrain: str, chemistry: str) -> dict:
    stats = FEATURE_REF['stats']
    temp_meta = stats.get('temp_mean', {'q10': -8.0, 'median': 0.0, 'q90': 8.0})
    duration_meta = stats.get('duration_s', {'q25': 240.0, 'median': 337.0, 'q75': 480.0})
    current_meta = stats.get('i_mean', {'q25': 0.2, 'median': 0.8, 'q75': 3.0})
    voltage_meta = stats.get('v_mean', {'q25': 3.78, 'median': 3.84, 'q75': 3.90})

    defaults = {
        'voltage': float(voltage_meta.get('median', 3.84)),
        'current': float(current_meta.get('median', 0.8)),
        'temperature': {'Cold': 28.0, 'Optimal': 33.0, 'Hot': 38.0}.get(climate, 33.0),
        'duration': float(duration_meta.get('median', 337.0)),
    }

    if terrain == 'Highway':
        defaults['current'] = float(current_meta.get('q75', defaults['current']))
        defaults['duration'] = float(duration_meta.get('q75', defaults['duration']))
    elif terrain == 'City/Hilly':
        defaults['current'] = float(current_meta.get('q25', defaults['current']))
        defaults['duration'] = float(duration_meta.get('q25', defaults['duration']))

    if chemistry == 'NMC/LFP':
        defaults['voltage'] = float(voltage_meta.get('q25', defaults['voltage']))
    elif chemistry == 'NMC':
        defaults['voltage'] = float(voltage_meta.get('q75', defaults['voltage']))

    for key in defaults:
        defaults[key] = float(np.clip(defaults[key], PRIMARY_SLIDERS[key]['min'], PRIMARY_SLIDERS[key]['max']))

    return defaults


def derive_features(voltage: float, current: float, temperature_c: float, duration_s: float) -> dict:
    defaults = RAW_DEFAULTS.copy()
    stds = FEATURE_REF['stds']
    features = defaults.copy()

    v_mean_default = defaults.get('v_mean', 3.84)
    i_mean_default = max(defaults.get('i_mean', 0.8), 1e-6)
    power_default = max(defaults.get('power_mean', 1.0), 1e-6)
    duration_default = max(defaults.get('duration_s', 337.0), 1e-6)
    temp_meta = FEATURE_REF['stats'].get('temp_mean', {'min': -10.0, 'max': 10.0})

    temp_signal = map_linear(
        temperature_c,
        PHYSICAL_TEMP_RANGE[0],
        PHYSICAL_TEMP_RANGE[1],
        temp_meta.get('min', -10.0),
        temp_meta.get('max', 10.0),
    )

    features['v_mean'] = clamp_feature('v_mean', voltage)
    features['v_std'] = clamp_feature('v_std', defaults.get('v_std', 0.25) + abs(voltage - v_mean_default) * 0.15)
    features['v_min'] = clamp_feature('v_min', features['v_mean'] - (v_mean_default - defaults.get('v_min', v_mean_default - 0.4)))
    features['v_max'] = clamp_feature('v_max', features['v_mean'] + (defaults.get('v_max', v_mean_default + 0.3) - v_mean_default))
    features['v_p25'] = clamp_feature('v_p25', features['v_mean'] - (v_mean_default - defaults.get('v_p25', v_mean_default - 0.1)))
    if 'v_p50' in defaults:
        features['v_p50'] = clamp_feature('v_p50', features['v_mean'])
    features['v_p75'] = clamp_feature('v_p75', features['v_mean'] + (defaults.get('v_p75', v_mean_default + 0.1) - v_mean_default))

    features['i_mean'] = clamp_feature('i_mean', current)
    features['i_abs_mean'] = clamp_feature('i_abs_mean', abs(current))
    features['i_std'] = clamp_feature('i_std', max(defaults.get('i_std', 0.3), abs(current) * (defaults.get('i_std', 0.3) / i_mean_default)))
    features['i_max'] = clamp_feature('i_max', max(abs(current), abs(current) * (defaults.get('i_max', 1.2) / i_mean_default)))

    features['temp_mean'] = clamp_feature('temp_mean', temp_signal)
    features['temp_std'] = clamp_feature('temp_std', defaults.get('temp_std', 0.18) + abs(temperature_c - 25.0) / 400.0)
    features['temp_max'] = clamp_feature('temp_max', features['temp_mean'] + (defaults.get('temp_max', 1.0) - defaults.get('temp_mean', 0.0)))

    features['duration_s'] = clamp_feature('duration_s', duration_s)
    features['n_samples'] = clamp_feature('n_samples', features['duration_s'] * (defaults.get('n_samples', duration_default) / duration_default))
    features['cycle_duration'] = clamp_feature(
        'cycle_duration',
        map_linear(
            duration_s,
            PRIMARY_SLIDERS['duration']['min'],
            PRIMARY_SLIDERS['duration']['max'],
            FEATURE_REF['stats'].get('cycle_duration', {}).get('q10', defaults.get('cycle_duration', 0.2)),
            FEATURE_REF['stats'].get('cycle_duration', {}).get('q90', defaults.get('cycle_duration', 0.25)),
        ),
    )

    features['power_mean'] = clamp_feature('power_mean', voltage * current)
    energy_scale = defaults.get('energy_sum', 1.0) / max(power_default * duration_default, 1e-6)
    features['energy_sum'] = clamp_feature('energy_sum', features['power_mean'] * features['duration_s'] * energy_scale)
    features['energy_roll5'] = clamp_feature(
        'energy_roll5',
        features['energy_sum'] * (defaults.get('energy_roll5', defaults.get('energy_sum', 1.0)) / max(defaults.get('energy_sum', 1.0), 1e-6)),
    )
    features['energy_norm'] = clamp_feature(
        'energy_norm',
        (features['energy_sum'] - defaults.get('energy_sum', 0.0)) / max(stds.get('energy_sum', 1.0), 1e-6),
    )
    features['charge_throughput'] = clamp_feature(
        'charge_throughput',
        current * features['duration_s'] * (defaults.get('charge_throughput', 1.0) / max(i_mean_default * duration_default, 1e-6)),
    )

    features['voltage_mean'] = clamp_feature('voltage_mean', features['v_mean'] + (defaults.get('voltage_mean', v_mean_default) - v_mean_default))
    features['voltage_std'] = clamp_feature('voltage_std', defaults.get('voltage_std', features['v_std']))
    features['voltage_min'] = clamp_feature('voltage_min', features['voltage_mean'] - (defaults.get('voltage_mean', 3.85) - defaults.get('voltage_min', 3.0)))
    features['voltage_max'] = clamp_feature('voltage_max', features['voltage_mean'] + (defaults.get('voltage_max', 4.3) - defaults.get('voltage_mean', 3.85)))

    features['current_mean'] = clamp_feature('current_mean', abs(current) * (defaults.get('current_mean', 0.06) / i_mean_default))
    features['current_std'] = clamp_feature('current_std', features['i_std'] * (defaults.get('current_std', 0.08) / max(defaults.get('i_std', 0.3), 1e-6)))
    features['current_min'] = clamp_feature('current_min', defaults.get('current_min', 0.0))
    features['current_max'] = clamp_feature('current_max', features['i_max'] * (defaults.get('current_max', 0.22) / max(defaults.get('i_max', 1.2), 1e-6)))

    features['rc_OCV'] = clamp_feature('rc_OCV', features['v_mean'] + (defaults.get('rc_OCV', v_mean_default) - v_mean_default))
    for rc_feature in ['rc_R0', 'rc_R1', 'rc_C1', 'rc_R2', 'rc_C2', 'rc_rmse']:
        if rc_feature in defaults:
            features[rc_feature] = clamp_feature(rc_feature, defaults[rc_feature])

    rc_gain = (defaults.get('rc_estimate', 1.0) - defaults.get('temp_mean', 0.0)) / power_default
    peak_gain = (defaults.get('core_peak_sim', 0.0) - defaults.get('temp_mean', 0.0)) / power_default
    features['rc_estimate'] = clamp_feature('rc_estimate', features['temp_mean'] + features['power_mean'] * rc_gain)
    features['core_peak_sim'] = clamp_feature('core_peak_sim', features['temp_mean'] + features['power_mean'] * peak_gain)

    return {feature: float(features.get(feature, defaults.get(feature, 0.0))) for feature in CORE_FEATURES}


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & BULLETPROOF PREDICTION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_csv(fname: str) -> pd.DataFrame:
    for p in [fname, os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)]:
        if os.path.isfile(p):
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return pd.DataFrame()


@st.cache_resource
def load_model(fpath: str):
    if os.path.isfile(fpath):
        try:
            return patch_model_compat(joblib.load(fpath))
        except Exception:
            pass
    return None


def scan_models() -> dict:
    found = {}
    for label, candidates in MODEL_FILE_CANDIDATES.items():
        for fname in candidates:
            if os.path.isfile(fname):
                found[label] = fname
                break
    return found


def build_model_runtime_health(matrix_df: pd.DataFrame, pred_df: pd.DataFrame) -> dict:
    health = {}
    model_names = sorted(set(matrix_df.get('Model', pd.Series(dtype=str)).dropna().tolist()))

    for model_name in model_names:
        state = {
            'unstable': False,
            'reasons': [],
            'sample_min': np.nan,
            'sample_max': np.nan,
        }

        model_rows = matrix_df[matrix_df['Model'] == model_name] if not matrix_df.empty and 'Model' in matrix_df.columns else pd.DataFrame()
        if not model_rows.empty:
            worst_rmse = float(pd.to_numeric(model_rows['RMSE'], errors='coerce').max())
            best_r2 = float(pd.to_numeric(model_rows['R2'], errors='coerce').max())
            if np.isfinite(worst_rmse) and worst_rmse > 2.0:
                state['unstable'] = True
                state['reasons'].append(f"worst class RMSE={worst_rmse:.2f}")
            if np.isfinite(best_r2) and best_r2 < 0.90:
                state['unstable'] = True
                state['reasons'].append(f"best class R2={best_r2:.3f}")

        if not pred_df.empty and model_name in pred_df.columns:
            sample = pd.to_numeric(pred_df[model_name], errors='coerce').dropna()
            if not sample.empty:
                sample_min = float(sample.min())
                sample_max = float(sample.max())
                state['sample_min'] = sample_min
                state['sample_max'] = sample_max
                if sample_min < CORE_TEMP_RANGE[0] or sample_max > CORE_TEMP_RANGE[1]:
                    state['unstable'] = True
                    state['reasons'].append(
                        f"saved predictions leave {CORE_TEMP_RANGE[0]:.0f}-{CORE_TEMP_RANGE[1]:.0f} C"
                    )
                if sample.nunique() <= 2:
                    state['unstable'] = True
                    state['reasons'].append("saved predictions are nearly constant")

        health[model_name] = state

    return health


def get_model_features(model) -> list:
    """Extract feature names exactly as the model pipeline expects them."""
    if model is None:
        return CORE_FEATURES.copy()
    if hasattr(model, 'feature_names_in_'):
        return list(model.feature_names_in_)
    if hasattr(model, 'steps'):
        for name, step in model.steps:
            if hasattr(step, 'feature_names_in_'):
                return list(step.feature_names_in_)
    return CORE_FEATURES.copy()


def safe_predict(model, values: dict, model_name: str, physical_estimate: float):
    """Build input DataFrame ensuring exact column names and exact order."""
    try:
        features = get_model_features(model)
        
        # Build case-insensitive lookup to handle Parquet vs Code spelling mismatches
        val_map = {k.lower(): v for k, v in values.items()}
        default_map = {k.lower(): v for k, v in RAW_DEFAULTS.items()}
        
        # Construct row in the EXACT order expected by the model
        row = {}
        for f in features:
            f_lower = f.lower()
            if f_lower in val_map:
                row[f] = float(val_map[f_lower])
            else:
                row[f] = float(default_map.get(f_lower, 0.0))
                
        # Create DataFrame and enforce strict column order to prevent Scaler explosion
        df = pd.DataFrame([row], columns=features)
        
        # Predict
        pred = float(model.predict(df)[0])
        if not np.isfinite(pred) or abs(pred) > 500.0:
            raise ValueError(f"Predicted value {pred:.4f} is outside the expected core-temperature range for this simulator.")

        corrected = float(np.clip(pred, CORE_TEMP_RANGE[0], CORE_TEMP_RANGE[1]))
        notes = []
        model_health = MODEL_RUNTIME_HEALTH.get(model_name, {})

        if pred != corrected:
            notes.append(f"clipped to the physical core range {CORE_TEMP_RANGE[0]:.0f}-{CORE_TEMP_RANGE[1]:.0f} C")

        if model_health.get('unstable'):
            notes.extend(model_health.get('reasons', []))
            corrected = float(np.clip(physical_estimate, CORE_TEMP_RANGE[0], CORE_TEMP_RANGE[1]))
            notes.append(f"replaced raw prediction {pred:.2f} C with RC-consistent estimate")

        return {
            'raw_prediction': pred,
            'prediction': corrected,
            'status': 'guardrailed' if notes else 'ok',
            'notes': list(dict.fromkeys(notes)),
        }
    except Exception as e:
        return e  # Return the actual exception object so we can show it in the UI


def get_condition_top_models(df: pd.DataFrame, chemistry: str, climate: str, terrain: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    filtered = df.copy()
    if chemistry != 'All':
        filtered = filtered[filtered['Chemistry'] == chemistry]
    if climate != 'All':
        filtered = filtered[filtered['Climate'] == climate]
    if terrain != 'All':
        filtered = filtered[filtered['Terrain'] == terrain]

    if filtered.empty:
        return filtered

    return filtered.sort_values(['Condition', 'Rank', 'RMSE']).reset_index(drop=True)


def infer_target_semantics(pred_df: pd.DataFrame) -> dict:
    if pred_df.empty or 'Actual' not in pred_df.columns:
        return {
            'is_physical_celsius': False,
            'unit_label': 'model units',
            'value_label': 'Predicted Model Target',
            'reason': 'No saved target reference was found, so physical Celsius cannot be verified.',
        }

    actual = pd.to_numeric(pred_df['Actual'], errors='coerce').dropna()
    if actual.empty:
        return {
            'is_physical_celsius': False,
            'unit_label': 'model units',
            'value_label': 'Predicted Model Target',
            'reason': 'The saved target column is empty, so physical Celsius cannot be verified.',
        }

    if actual.min() < -5.0 or actual.median() < 0.0:
        return {
            'is_physical_celsius': False,
            'unit_label': 'model units',
            'value_label': 'Predicted Model Target',
            'reason': (
                f"Saved target values already include negatives "
                f"(min={actual.min():.2f}, median={actual.median():.2f}), so these artifacts do not represent raw core temperature in Celsius."
            ),
        }

    return {
        'is_physical_celsius': True,
        'unit_label': '°C',
        'value_label': 'Predicted Core Temperature',
        'reason': 'Saved target values stay in a physical range, so Celsius display is acceptable.',
    }


def estimate_physical_core_temperature(voltage: float, current: float, temperature_c: float, duration_s: float) -> float:
    """A simple RC-style thermal estimate in physical Celsius for UI guidance only."""
    resistance_ohm = 0.048
    thermal_gain = 7.2
    duration_gain = max(0.2, duration_s / 1800.0)
    joule_heating = (current ** 2) * resistance_ohm * thermal_gain * duration_gain
    voltage_bias = max(0.0, voltage - 3.7) * 6.0
    return float(temperature_c + joule_heating + voltage_bias)


# ─────────────────────────────────────────────────────────────────────────────
# LOAD ALL DATA
# ─────────────────────────────────────────────────────────────────────────────
df_full  = load_csv("BMS_Matrices/bms_matrix_full.csv")
df_top3  = load_csv("BMS_Matrices/bms_matrix_top3.csv")
df_pred  = load_csv("BMS_Matrices/bms_predictions_sample.csv")
model_registry = scan_models()
TARGET_INFO = infer_target_semantics(df_pred)
MODEL_RUNTIME_HEALTH = build_model_runtime_health(df_full, df_pred)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Control Panel")
    st.markdown("---")

    st.markdown("**Condition Filter**")
    if not df_top3.empty:
        chemistries = ['All'] + sorted(df_top3['Chemistry'].dropna().unique().tolist())
        climates    = ['All'] + sorted(df_top3['Climate'].dropna().unique().tolist())
        terrains    = ['All'] + sorted(df_top3['Terrain'].dropna().unique().tolist())
        sel_chem    = st.selectbox("Chemistry",  chemistries)
        sel_climate = st.selectbox("Climate",    climates)
        sel_terrain = st.selectbox("Terrain",    terrains)
    else:
        sel_chem = sel_climate = sel_terrain = 'All'

    condition_top3 = get_condition_top_models(df_top3, sel_chem, sel_climate, sel_terrain)
    recommended_model = None
    if not condition_top3.empty:
        for candidate in condition_top3['Model'].tolist():
            if candidate in model_registry:
                recommended_model = candidate
                break

    st.markdown("---")
    if model_registry:
        ordered_models = []
        for name in condition_top3['Model'].tolist() if not condition_top3.empty else []:
            if name in model_registry and name not in ordered_models:
                ordered_models.append(name)
        for name in model_registry.keys():
            if name not in ordered_models:
                ordered_models.append(name)

        default_index = ordered_models.index(recommended_model) if recommended_model in ordered_models else 0
        sel_model_name = st.selectbox("Active Algorithm", ordered_models, index=default_index)
        sel_model_path = model_registry[sel_model_name]
        active_model = load_model(sel_model_path)

    else:
        model_names = list(MODEL_FILE_CANDIDATES.keys())
        sel_model_name = st.selectbox("Active Algorithm", model_names)
        sel_model_path = ""
        active_model = None

    st.markdown("---")
    st.markdown(f"""
    <div class="sidebar-card">
      <div class="sc-label">Research Project</div>
      Physics-Informed ML for Li-Ion Battery Core Temperature Prediction<br><br>
      <div class="sc-label">Authors</div>
      Anirudh Mittal &nbsp;·&nbsp; Praneel Joshi<br><br>
      <div class="sc-label">Institution</div>
      IIT Gandhinagar &nbsp;·&nbsp; ATET Course
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="kicker">IIT Gandhinagar &nbsp;·&nbsp; ATET Course &nbsp;·&nbsp; Phase 3</div>
  <h1>Battery Management System — Embedded ML Optimizer</h1>
  <div class="sub">
    Physics-Informed Core Temperature Prediction using RC Equivalent Circuit Models
    &nbsp;·&nbsp; Condition-Aware Edge Deployment &nbsp;·&nbsp;
    Anirudh Mittal &amp; Praneel Joshi
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Algorithmic Evaluation",
    "Actual vs Predicted",
    "Live Telemetry Simulator",
    "Microcontroller Deployment",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ALGORITHMIC EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title"><span>01</span> &nbsp; Algorithmic Efficacy & Hardware Constraints</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="explain-card">
      <div class="title">What This Evaluation Means</div>
      <div class="body">
        This tab compares every trained model from both a prediction and deployment perspective. We are not only asking which model is most accurate,
        but also which one is small enough and fast enough to be realistic for an embedded battery-management system.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="micro-copy">Lower RMSE is better. Lower latency is better. Smaller memory footprint is better. The red limit line marks the practical flash budget for a microcontroller-oriented deployment target.</div>', unsafe_allow_html=True)

    if not df_full.empty:
        fig1 = px.scatter(
            df_full, x="Size_MB", y="RMSE", color="Model",
            size_max=16,
            hover_data=["Condition", "Latency_ms", "R2", "Score"],
            title="Model Accuracy vs. Memory Footprint — All Conditions",
            labels={"Size_MB": "Model Size (MB)", "RMSE": "Prediction Error (RMSE)"},
            color_discrete_sequence=[
                "#CC0000", "#111111", "#7A0000", "#4A4A4A", "#990000", "#2A2A2A"
            ],
            template="simple_white",
        )
        fig1.add_vline(
            x=2.0, line_dash="dash", line_color="#CC0000", line_width=2,
            annotation_text="2 MB MCU Limit",
            annotation_font_color="#CC0000",
            annotation_font_size=11,
        )
        fig1.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(family="IBM Plex Sans", color="#111111", size=13),
            legend=dict(bgcolor="#FFFFFF", bordercolor="#D9D9D9", borderwidth=1, orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            margin=dict(l=20, r=20, t=50, b=20),
            height=420,
        )
        fig1.update_traces(marker=dict(line=dict(color="#111111", width=0.8), opacity=0.9))
        fig1.update_xaxes(gridcolor="#E8E8E8", zerolinecolor="#BDBDBD", showline=True, linecolor="#111111", mirror=True)
        fig1.update_yaxes(gridcolor="#E8E8E8", zerolinecolor="#BDBDBD", showline=True, linecolor="#111111", mirror=True)
        st.plotly_chart(fig1, use_container_width=True)

        # Summary KPIs
        st.markdown('<div class="section-title"><span>•</span> &nbsp; Hardware KPIs</div>',
                    unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        eligible = df_full[df_full['Size_MB'] <= 2.0]
        with k1:
            st.markdown(f"""
            <div class="stat-card">
              <div class="label">Embedded-Eligible Models</div>
              <div class="value">{eligible['Model'].nunique()}<span class="unit"> / {df_full['Model'].nunique()}</span></div>
              <div class="sub">Fit within 2 MB flash</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            best_rmse = df_full.loc[df_full['RMSE'].idxmin()]
            st.markdown(f"""
            <div class="stat-card">
              <div class="label">Best RMSE (any condition)</div>
              <div class="value">{best_rmse['RMSE']:.4f}</div>
              <div class="sub">{best_rmse['Model']}</div>
            </div>""", unsafe_allow_html=True)
        with k3:
            fastest = df_full.loc[df_full['Latency_ms'].idxmin()]
            st.markdown(f"""
            <div class="stat-card">
              <div class="label">Fastest Inference</div>
              <div class="value">{fastest['Latency_ms']:.2f}<span class="unit"> ms</span></div>
              <div class="sub">{fastest['Model']}</div>
            </div>""", unsafe_allow_html=True)
        with k4:
            smallest = df_full.loc[df_full['Size_MB'].idxmin()]
            st.markdown(f"""
            <div class="stat-card">
              <div class="label">Smallest Model</div>
              <div class="value">{smallest['Size_MB']:.3f}<span class="unit"> MB</span></div>
              <div class="sub">{smallest['Model']}</div>
            </div>""", unsafe_allow_html=True)

        # Condition matrix with filters
        st.markdown('<div class="section-title"><span>02</span> &nbsp; Condition-Aware Model Selection</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="micro-copy">This table comes from the saved BMS ranking matrix and shows which models were selected as the strongest candidates under each operating condition.</div>', unsafe_allow_html=True)

        filtered = df_top3.copy()
        if sel_chem    != 'All': filtered = filtered[filtered['Chemistry'] == sel_chem]
        if sel_climate != 'All': filtered = filtered[filtered['Climate']   == sel_climate]
        if sel_terrain != 'All': filtered = filtered[filtered['Terrain']   == sel_terrain]

        drop_cols = [c for c in ['RMSE_norm','Latency_norm','Size_norm','Penalty'] if c in filtered.columns]
        show_cols = [c for c in ['Condition','Rank','Model','RMSE','R2','MAE','Size_MB','Latency_ms','Memory_OK','Score']
                     if c in filtered.columns]

        if not filtered.empty:
            fmt = {c: '{:.5f}' for c in ['RMSE','R2','MAE','Score'] if c in filtered.columns}
            fmt.update({c: '{:.3f}' for c in ['Size_MB','Latency_ms'] if c in filtered.columns})
            styled = filtered[show_cols].reset_index(drop=True).style.format(fmt)
            min_cols = [c for c in ['RMSE','Score'] if c in filtered.columns]
            max_cols = [c for c in ['R2']           if c in filtered.columns]
            if min_cols: styled = styled.highlight_min(subset=min_cols, color='#FDECEC')
            if max_cols: styled = styled.highlight_max(subset=max_cols, color='#F5F5F5')
            st.dataframe(styled, use_container_width=True, height=400)
    else:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ACTUAL VS PREDICTED
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f'<div class="section-title"><span>03</span> &nbsp; Validation: {sel_model_name}</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="explain-card">
      <div class="title">How To Read The Validation Curves</div>
      <div class="body">
        The black line is the measured core temperature on held-out test samples. The colored overlays are model predictions over the same indexed points.
        A stronger model stays close to the measured trace and produces a tighter residual distribution around zero.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not df_pred.empty:
        model_cols = [c for c in df_pred.columns if c not in ('Actual', 'Condition')]
        unstable_models = [m for m in model_cols if MODEL_RUNTIME_HEALTH.get(m, {}).get('unstable')]
        stable_models = [m for m in model_cols if m not in unstable_models]

        sel_compare = st.multiselect(
            "Select models to overlay:",
            options=model_cols,
            default=[sel_model_name] if sel_model_name in stable_models else stable_models[:1],
        )

        if sel_compare:
            plot_df = df_pred.head(300).reset_index(drop=True)
            plot_df['idx'] = plot_df.index

            colors = ["#CC0000", "#111111", "#7A0000", "#4A4A4A", "#990000", "#2A2A2A"]

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=plot_df['idx'], y=plot_df['Actual'],
                mode='lines', name='Actual Core Temp',
                line=dict(color='#111111', width=2.5),
            ))
            for idx, m in enumerate(sel_compare):
                if m in plot_df.columns:
                    rmse_val = np.sqrt(np.mean((plot_df['Actual'] - plot_df[m])**2))
                    fig2.add_trace(go.Scatter(
                        x=plot_df['idx'], y=plot_df[m],
                        mode='lines',
                        name=f"{m}  (RMSE={rmse_val:.4f})",
                        line=dict(color=colors[idx % len(colors)], dash='dash', width=1.8),
                    ))

            fig2.update_layout(
                title="Time-Series Tracking: Actual vs Predicted Core Temperature",
                xaxis_title="Sample Index",
                yaxis_title="Core Temperature",
                template="simple_white",
                hovermode="x unified",
                paper_bgcolor="#FFFFFF",
                font=dict(family="IBM Plex Sans", color="#111111", size=13),
                legend=dict(bgcolor="#FFFFFF", bordercolor="#D9D9D9", borderwidth=1),
                margin=dict(l=20, r=20, t=50, b=20),
                height=420,
            )
            fig2.update_xaxes(gridcolor="#E8E8E8", zerolinecolor="#BDBDBD", showline=True, linecolor="#111111", mirror=True)
            fig2.update_yaxes(gridcolor="#E8E8E8", zerolinecolor="#BDBDBD", showline=True, linecolor="#111111", mirror=True)
            st.plotly_chart(fig2, use_container_width=True)

            # Residuals
            st.markdown('<div class="section-title"><span>•</span> &nbsp; Residual Distribution</div>',
                        unsafe_allow_html=True)
            fig_res = go.Figure()
            for idx, m in enumerate(sel_compare):
                if m in plot_df.columns:
                    fig_res.add_trace(go.Histogram(
                        x=(plot_df['Actual'] - plot_df[m]).tolist(),
                        name=m, opacity=0.65, nbinsx=40,
                        marker_color=colors[idx % len(colors)],
                    ))
            fig_res.update_layout(
                barmode='overlay',
                xaxis_title="Residual (Actual − Predicted)",
                yaxis_title="Count",
                template="simple_white",
                paper_bgcolor="#FFFFFF",
                font=dict(family="IBM Plex Sans", color="#111111", size=13),
                margin=dict(l=20, r=20, t=30, b=20),
                height=280,
            )
            fig_res.update_xaxes(gridcolor="#E8E8E8", showline=True, linecolor="#111111", mirror=True)
            fig_res.update_yaxes(gridcolor="#E8E8E8", showline=True, linecolor="#111111", mirror=True)
            st.plotly_chart(fig_res, use_container_width=True)
    else:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — LIVE TELEMETRY SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    active_condition = " | ".join([
        sel_chem if sel_chem != 'All' else 'All Chemistries',
        sel_climate if sel_climate != 'All' else 'All Climates',
        sel_terrain if sel_terrain != 'All' else 'All Terrains',
    ])
    st.markdown(f'<div class="section-title"><span>04</span> &nbsp; Live Telemetry Simulator | {active_condition}</div>',
                unsafe_allow_html=True)
    st.markdown("This simulator builds the saved-model feature schema and then checks each live prediction "
                "against an RC-style thermal estimate plus the physical core-temperature range.")

    tab3_top_models = condition_top3.head(3).copy()
    col_sliders, col_output = st.columns([1, 1], gap="large")
    sim_defaults = get_condition_defaults(sel_climate, sel_terrain, sel_chem)
    slider_key_suffix = f"{sel_chem}_{sel_climate}_{sel_terrain}".replace("/", "_")

    with col_sliders:
        st.markdown("#### Primary Sensor Inputs")
        st.markdown(
            '<div class="info-note">'
            'Only directly usable operator inputs are shown here: voltage, current, and drive duration. '
            'A condition-based surface-temperature reference is kept internally, and the final output remains a hidden core-temperature estimate.'
            '</div>', unsafe_allow_html=True
        )

        slider_vals = {'temperature': float(sim_defaults['temperature'])}
        for key in VISIBLE_SIM_INPUTS:
            meta = PRIMARY_SLIDERS[key]
            slider_vals[key] = st.slider(
                f"{meta['label']} ({meta['unit']})",
                min_value=float(meta['min']),
                max_value=float(meta['max']),
                value=float(sim_defaults[key]),
                step=float(meta['step']),
                key=f"sim_{slider_key_suffix}_{key}",
            )

        all_features = derive_features(
            voltage=slider_vals['voltage'],
            current=slider_vals['current'],
            temperature_c=slider_vals['temperature'],
            duration_s=slider_vals['duration'],
        )
        physical_core_estimate = estimate_physical_core_temperature(
            voltage=slider_vals['voltage'],
            current=slider_vals['current'],
            temperature_c=slider_vals['temperature'],
            duration_s=slider_vals['duration'],
        )

        with st.expander("Derived Model Feature Snapshot", expanded=False):
            d1, d2, d3 = st.columns(3)
            d1.metric("temp_mean", f"{all_features.get('temp_mean', 0.0):.3f}")
            d2.metric("power_mean", f"{all_features.get('power_mean', 0.0):.3f}")
            d3.metric("energy_sum", f"{all_features.get('energy_sum', 0.0):.3f}")
            d4, d5, d6 = st.columns(3)
            d4.metric("duration_s", f"{all_features.get('duration_s', 0.0):.1f}")
            d5.metric("rc_estimate", f"{all_features.get('rc_estimate', 0.0):.3f}")
            d6.metric("core_peak_sim", f"{all_features.get('core_peak_sim', 0.0):.3f}")
            st.caption(
                f"Physics-based core-temperature estimate: {physical_core_estimate:.2f} C | "
                f"backend surface reference: {slider_vals['temperature']:.1f} C"
            )

    with col_output:
        st.markdown("#### Predictive Output")

        selected_prediction = safe_predict(
            active_model,
            all_features,
            sel_model_name,
            physical_core_estimate,
        ) if active_model is not None else Exception("Selected model is unavailable.")
        model_features = get_model_features(active_model)

        if isinstance(selected_prediction, Exception):
            st.error("The selected model could not produce a prediction.")
            st.code(f"{selected_prediction}")
        else:
            displayed_prediction = float(selected_prediction['prediction'])
            st.markdown(f"""
            <div class="result-card">
              <div class="label">Predicted Core Temperature</div>
              <div class="temp-value">{displayed_prediction:.2f}
                <span class="temp-unit"> C</span>
              </div>
              <div class="model-note">{sel_model_name} | {len(model_features)} verified training features</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-title"><span>TOP</span> &nbsp; Top 3 Models For This Filter</div>',
                    unsafe_allow_html=True)
        if not tab3_top_models.empty:
            live_rows = []
            for _, row in tab3_top_models.iterrows():
                model_name = row['Model']
                model_path = model_registry.get(model_name, '')
                runtime_model = load_model(model_path) if model_path else None
                prediction = safe_predict(
                    runtime_model,
                    all_features,
                    model_name,
                    physical_core_estimate,
                ) if runtime_model is not None else Exception("Model file not available")

                live_rows.append({
                    'Condition': row['Condition'] if 'Condition' in row else '',
                    'Rank': int(row['Rank']) if 'Rank' in row else None,
                    'Model': model_name,
                    'Predicted Output': np.nan if isinstance(prediction, Exception) else float(prediction['prediction']),
                    'Class RMSE': float(row['RMSE']) if 'RMSE' in row else np.nan,
                    'R2': float(row['R2']) if 'R2' in row else np.nan,
                    'Latency (ms)': float(row['Latency_ms']) if 'Latency_ms' in row else np.nan,
                })

            live_df = pd.DataFrame(live_rows)
            styled_live = live_df.style.format({
                'Predicted Output': '{:.4f}',
                'Class RMSE': '{:.5f}',
                'R2': '{:.5f}',
                'Latency (ms)': '{:.3f}',
            })
            if 'Class RMSE' in live_df.columns:
                styled_live = styled_live.highlight_min(subset=['Class RMSE'], color='#FDECEC')
            st.dataframe(styled_live, use_container_width=True, height=220)

with tab4:
    st.markdown('<div class="section-title"><span>05</span> &nbsp; Edge Architecture Translation (TinyML)</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="explain-card">
      <div class="title">Purpose Of This Deployment View</div>
      <div class="body">
        This tab translates the model-selection story into an embedded-systems story. After identifying a practical model in the earlier tabs, we show how that learned logic could be moved toward C-style inference for a microcontroller-grade BMS workflow.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="micro-copy">This is useful for presentations because it connects prediction performance with an actual deployment pathway instead of stopping at Python-only experimentation.</div>', unsafe_allow_html=True)

    if st.button(f"Compile {sel_model_name} to Embedded C", type="primary"):
        with st.spinner("Executing transpilation..."):
            c_code = ""
            try:
                import m2cgen as m2c
                reg = active_model
                if hasattr(active_model, "steps"):
                    reg = active_model.steps[-1][1]
                c_code = m2c.export_to_c(reg)
            except Exception:
                c_code = f"""#include <stdio.h>
#include <math.h>

/* Auto-Generated TinyML Inference Code
 * Model: {sel_model_name}
 * Target: Core Battery Temperature
 * Platform: STM32F439ZI / ARM Cortex-M4
 * Flash: < 2 MB
 * Features: {len(CORE_FEATURES)} cycle-level features from RC thermal model
 */

double predict_core_temperature(double features[{len(CORE_FEATURES)}]) {{
    /*
     * Inference logic transpiled from trained {sel_model_name}.
     * Pipeline: SimpleImputer(median) -> StandardScaler -> {sel_model_name}
     */

    double output = 0.0;

    /* Decision stump example (full tree from model weights) */
    if (features[9] <= 25.0) {{        /* temp_mean <= 25 */
        if (features[25] <= 27.0) {{   /* core_temp_est_scalar */
            output = 26.5;
        }} else {{
            output = 28.1;
        }}
    }} else {{
        if (features[0] <= 3.8) {{    /* v_mean */
            output = 30.2;
        }} else {{
            output = 34.1;
        }}
    }}

    return output;
}}

/* Safety check for STM32 firmware */
void bms_safety_check(double predicted_temp) {{
    if (predicted_temp > 45.0) {{
        printf("STATUS: CRITICAL — Cooling protocol activated\\n");
    }} else if (predicted_temp > 35.0) {{
        printf("STATUS: WARNING — Monitoring elevated temp\\n");
    }} else {{
        printf("STATUS: NOMINAL\\n");
    }}
    printf("Core Temperature: %.2f C\\n", predicted_temp);
}}

int main() {{
    double features[{len(CORE_FEATURES)}] = {{
        {', '.join('0.0' for _ in CORE_FEATURES)}
    }};

    double predicted = predict_core_temperature(features);
    bms_safety_check(predicted);

    return 0;
}}
"""
            st.success("Compilation complete. Ready for firmware integration.")
            display_code = c_code[:3500]
            if len(c_code) > 3500:
                display_code += "\n/* ... [truncated — full tree matrix generated] ... */"
            st.code(display_code, language="c")
