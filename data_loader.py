from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

HERE = Path(__file__).parent


def sanitize_geotechnical_df(d):
    d = d.copy()
    if "S_dam_deg" in d.columns:
        s = d["S_dam_deg"].astype(float)
        s = np.where(s > 31.0, 21.0 + 7.5 * np.tanh((s - 31.0) / 25.0), s)
        d["S_dam_deg"] = np.clip(s, 8.0, 31.5)
    if "S_up_deg" in d.columns:
        u = d["S_up_deg"].astype(float)
        u = np.where(u > 35.0, 24.0 + 8.0 * np.tanh((u - 35.0) / 25.0), u)
        d["S_up_deg"] = np.clip(u, 10.0, 34.0)
    if "Lake_Name" in d.columns:
        mask_cb = d["Lake_Name"] == "Cordillera_Blanca_Lake"
        d.loc[mask_cb, "Latitude"] = -8.995
        d.loc[mask_cb, "Longitude"] = -77.675
    return d


@st.cache_data
def load_base_data():
    p = HERE / "lake_data.csv"
    if not p.exists():
        p = Path("lake_data.csv")
    if not p.exists():
        return None
    d = pd.read_csv(p)
    num_cols = [
        "Area_km2",
        "d_glacier_km",
        "S_dam_deg",
        "Elevation_m",
        "S_up_deg",
        "Temp_C",
        "Rain_mm",
        "Snow_Depth_m",
    ]
    for c in num_cols:
        if c in d.columns:
            d[c] = d[c].fillna(d[c].median())
    return sanitize_geotechnical_df(d)


def get_combined_dataframe():
    base_df = load_base_data()
    if "uploaded_lakes_df" not in st.session_state:
        st.session_state.uploaded_lakes_df = pd.DataFrame()

    if base_df is not None and not st.session_state.uploaded_lakes_df.empty:
        return pd.concat([st.session_state.uploaded_lakes_df, base_df], ignore_index=True)
    return base_df


def process_uploaded_lake_csv(up_file):
    if up_file is None:
        return
    file_sig = f"{up_file.name}_{up_file.size}"
    if st.session_state.get("last_uploaded_sig") == file_sig:
        return
    try:
        u = pd.read_csv(up_file)
    except Exception as e:
        st.toast(f"❌ Error reading CSV: {e}")
        return

    base_df = load_base_data()
    required_numeric = [
        "Area_km2",
        "d_glacier_km",
        "S_dam_deg",
        "Elevation_m",
        "S_up_deg",
        "Temp_C",
        "Rain_mm",
        "Snow_Depth_m",
        "Latitude",
        "Longitude",
    ]
    for col in required_numeric:
        baseline_median = float(base_df[col].median()) if (base_df is not None and col in base_df.columns) else 0.0
        if col not in u.columns:
            u[col] = baseline_median
        else:
            col_median = u[col].median() if not u[col].isna().all() else baseline_median
            u[col] = u[col].fillna(col_median)

    if "Region" not in u.columns:
        u["Region"] = "External_Basin"
    else:
        u["Region"] = u["Region"].fillna("External_Basin")

    u = sanitize_geotechnical_df(u)

    if "Year" not in u.columns or "Month" not in u.columns:
        if "Date" in u.columns:
            dt = pd.to_datetime(u["Date"], errors="coerce").fillna(pd.Timestamp("2023-01-01"))
            u["Year"] = dt.dt.year
            u["Month"] = dt.dt.month
        else:
            dt = pd.date_range(start="2020-01-01", periods=len(u), freq="MS")
            u["Year"] = dt.year
            u["Month"] = dt.month

    if "Lake_Name" not in u.columns or u["Lake_Name"].isna().all():
        u["Lake_Name"] = Path(up_file.name).stem

    new_lake_name = str(u["Lake_Name"].iloc[0])
    prev = st.session_state.uploaded_lakes_df
    if not prev.empty and "Lake_Name" in prev.columns:
        prev = prev[prev["Lake_Name"] != new_lake_name]

    st.session_state.uploaded_lakes_df = pd.concat([u, prev], ignore_index=True)
    st.session_state.last_uploaded_sig = file_sig
    st.session_state.lake = new_lake_name
    st.toast(f"✅ Loaded lake: {new_lake_name}")
    st.rerun()