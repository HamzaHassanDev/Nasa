import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

HERE = Path(__file__).parent

FEATURE_COLS = [
    "Area_km2",
    "d_glacier_km",
    "S_dam_deg",
    "Elevation_m",
    "S_up_deg",
    "Temp_C",
    "Rain_mm",
    "Snow_Depth_m",
]

RAIN_PTS_PER_100PCT = 28.0
TEMP_PTS_PER_DEG = 3.4


@st.cache_resource
def load_ml_model():
    p = HERE / "trained_glof_model.pkl"
    if not p.exists():
        p = Path("trained_glof_model.pkl")
    if p.exists():
        with open(p, "rb") as f:
            return pickle.load(f)
    return None


def clip(v):
    return np.clip(v, 0.0, 1.0)


def compute_geotechnical_physics_score(A, g, S_dam, elev, S_up, T, Rx1, snow):
    A = max(float(A), 0.001)
    g = max(float(g), 0.0)
    S_dam, S_up, elev, T, Rx1, snow = map(float, (S_dam, S_up, elev, T, Rx1, snow))

    f_A_log = clip((np.log10(A) - np.log10(0.10)) / (np.log10(4.5) - np.log10(0.10)))
    f_A = 0.65 * f_A_log + 0.35 * clip((A / 3.5) ** 1.2)
    f_G = (1.0 - clip(g / 0.70)) ** 1.35
    f_D = (clip((S_dam - 14.0) / 19.0)) ** 1.6
    f_U = clip((S_up - 17.0) / 18.0)
    f_E = clip((elev - 3400.0) / 2500.0)
    f_M = clip((T + 6.0) / 16.0)
    f_R = 0.70 * clip(Rx1 / 160.0) + 0.30 * clip(snow / 25.0)

    path_steep_dam = (clip((S_dam - 18.5) / 14.0) ** 1.3) * (0.50 + 0.25 * f_U + 0.25 * f_E)
    path_volume_overload = (clip((A - 1.75) / 2.2) ** 1.1) * (1.0 - clip(g / 0.30))
    f_avalanche = (clip((snow - 16.0) / 10.0) ** 1.3) * clip((elev - 4800.0) / 600.0)
    f_calving = clip((0.08 - g) / 0.04) * clip((A - 0.6) / 1.0)

    breach = np.maximum.reduce([path_steep_dam, path_volume_overload, np.maximum(f_avalanche, f_calving)])
    base = 100.0 * (0.18 * f_A + 0.20 * f_G + 0.20 * f_D + 0.10 * f_U + 0.08 * f_E + 0.12 * f_M + 0.12 * f_R)
    amp = 45.0 * (f_G ** 0.7) * breach * (0.55 + 0.25 * f_M + 0.20 * f_R)
    return float(np.clip(base + amp, 5.0, 96.0))


def row_to_df(r, **over):
    vals = {c: float(r[c]) for c in FEATURE_COLS}
    vals.update(over)
    return pd.DataFrame([[vals[c] for c in FEATURE_COLS]], columns=FEATURE_COLS)


def predict_single_lake_risk(row_df):
    ml_model = load_ml_model()
    r = row_df.iloc[0]
    phys = compute_geotechnical_physics_score(
        r["Area_km2"],
        r["d_glacier_km"],
        r["S_dam_deg"],
        r["Elevation_m"],
        r["S_up_deg"],
        r["Temp_C"],
        r["Rain_mm"],
        r["Snow_Depth_m"],
    )
    if ml_model is not None:
        val = 0.45 * float(ml_model.predict(row_df[FEATURE_COLS])[0]) + 0.55 * phys
    else:
        val = phys
    return float(np.clip(val, 0.0, 100.0))


def key_factors(r):
    A = max(float(r["Area_km2"]), 0.001)
    g = max(float(r["d_glacier_km"]), 0.0)
    s_dam = float(r["S_dam_deg"])
    rain = float(r["Rain_mm"])
    snow = float(r["Snow_Depth_m"])

    f_A_log = clip((np.log10(A) - np.log10(0.08)) / (np.log10(5.2) - np.log10(0.08)))
    f_exp = float(np.clip(0.65 * f_A_log + 0.35 * clip((A / 4.2) ** 1.15), 0.06, 0.92))
    f_slp = float(np.clip((s_dam - 8.0) / 28.0, 0.08, 0.89))
    f_rn = float(np.clip(0.72 * clip(rain / 220.0) + 0.28 * clip(snow / 28.0), 0.05, 0.90))
    f_prx = float(np.clip((1.0 - clip(g / 0.80)) ** 1.25, 0.06, 0.92))

    return {
        "expansion": f_exp,
        "slope": f_slp,
        "rain": f_rn,
        "proximity": f_prx,
    }


def risk_level(s):
    if s >= 85:
        return "Very High Risk", "#e03131"
    if s >= 66:
        return "High Risk", "#e03131"
    if s >= 33:
        return "Moderate Risk", "#f08c00"
    return "Low Risk", "#2f9e44"


def scenario_score(base, rain_pct, temp_chg):
    sens = 0.5 + base / 100.0
    raw_rain = RAIN_PTS_PER_100PCT * (rain_pct / 100.0) * sens
    raw_temp = TEMP_PTS_PER_DEG * temp_chg * sens
    total_raw = raw_rain + raw_temp

    if total_raw >= 0:
        head = max(99.0 - base, 1.0)
        new = 99.0 - head * np.exp(-total_raw / (head + 25.0))
    else:
        new = base + total_raw

    new = round(float(np.clip(new, 3.0, 99.0)), 1)
    base_rounded = round(float(base), 1)
    actual_delta = round(new - base_rounded, 1)

    if abs(total_raw) > 1e-6:
        scale = actual_delta / total_raw
        d_rain = round(raw_rain * scale, 1)
        d_temp = round(actual_delta - d_rain, 1)
    else:
        d_rain, d_temp = 0.0, 0.0

    return new, d_rain, d_temp


def dynamic_y_domain(values, pad=10.0, min_span=26.0):
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) == 0:
        return [0.0, 100.0]
    lo = float(np.min(arr)) - pad
    hi = float(np.max(arr)) + pad
    if (hi - lo) < min_span:
        mid = 0.5 * (hi + lo)
        lo = mid - min_span / 2.0
        hi = mid + min_span / 2.0
    lo = max(0.0, np.floor(lo / 5.0) * 5.0)
    hi = min(100.0, np.ceil(hi / 5.0) * 5.0)
    if hi <= lo:
        return [0.0, 100.0]
    return [float(lo), float(hi)]
