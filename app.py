from contextlib import contextmanager

import altair as alt
import folium
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from data_loader import get_combined_dataframe, process_uploaded_lake_csv
from risk_engine import (
    dynamic_y_domain,
    key_factors,
    predict_single_lake_risk,
    risk_level,
    row_to_df,
    scenario_score,
)
from style import NAVY, get_css, icon_img, landscape_svg, photo_or_svg, svg, to_uri

st.set_page_config(
    page_title="GlacierWatch",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page_names = ["Home", "Dashboard", "What-If Simulator", "About"]
if "page" not in st.session_state:
    qp = st.query_params.get("page")
    st.session_state.page = qp if qp in page_names else "Home"
page = st.session_state.page

try:
    st.query_params["page"] = page
except Exception:
    pass

st.markdown(get_css(page), unsafe_allow_html=True)
df = get_combined_dataframe()


@contextmanager
def card():
    with st.container():
        st.markdown('<span class="cardmark"></span>', unsafe_allow_html=True)
        yield


def show_chart(ch):
    try:
        st.altair_chart(ch, width="stretch")
    except TypeError:
        st.altair_chart(ch, use_container_width=True)


def go(p):
    st.session_state.page = p


NAV = [
    ("Home", ":material/home:"),
    ("Dashboard", ":material/grid_view:"),
    ("What-If Simulator", ":material/science:"),
    ("About", ":material/info:"),
]

with st.sidebar:
    st.markdown(f'<div class="sb-logo">{icon_img("logo_white", 78)}</div>', unsafe_allow_html=True)
    for name, ic in NAV:
        st.button(
            name,
            icon=ic,
            key=f"nav_{name}",
            on_click=go,
            args=(name,),
            type="primary" if page == name else "secondary",
        )


with st.container(key="topnav"):
    _cols = st.columns(len(NAV), gap="small")
    for _c, (name, ic) in zip(_cols, NAV):
        with _c:
            st.button(name, icon=ic, key=f"top_{name}", on_click=go, args=(name,),
                      type="primary" if page == name else "secondary", use_container_width=True)


def lake_picker(key):
    lakes = list(df["Lake_Name"].dropna().unique())
    if "lake" not in st.session_state or st.session_state.lake not in lakes:
        st.session_state.lake = lakes[0]

    st.session_state[key] = st.session_state.lake

    def _sync():
        st.session_state.lake = st.session_state[key]

    st.selectbox("Lake", lakes, key=key, on_change=_sync, label_visibility="collapsed")
    return st.session_state.lake


def latest_row(lake):
    sub = df[df["Lake_Name"] == lake].sort_values(["Year", "Month"])
    return sub, sub.iloc[-1]


def need_data():
    if df is None or df.empty:
        st.error("❌ 'lake_data.csv' not found next to app.py")
        st.stop()


if page == "Home":
    uri, is_photo = photo_or_svg(["hero.jpg", "hero.jpeg", "hero.png"], dark=True)
    overlay = (
        "linear-gradient(90deg,rgba(9,25,60,.9) 0%,rgba(9,25,60,.45) 48%,rgba(9,25,60,0) 100%),"
        if is_photo
        else "linear-gradient(90deg,rgba(9,25,60,.55) 0%,rgba(9,25,60,0) 55%),"
    )
    st.markdown(
        f"""<div class="hero" style="background: {overlay} url({uri}) center / cover no-repeat;">
<h1>GlacierWatch</h1>
<p class="tag">Monitor. Analyze. Be Prepared.</p>
<p class="desc">An intelligent platform to assess the risk of Glacial Lake Outburst Floods (GLOF) using satellite data and scientific analysis.</p>
<a class="cta" href="?page=Dashboard" target="_self">Explore the Dashboard &nbsp;›</a>
</div>""",
        unsafe_allow_html=True,
    )

elif page == "Dashboard":
    need_data()
    h1, h2, h3 = st.columns([2.5, 1.15, 0.85], gap="small")
    with h1:
        st.markdown(f'<div class="page-title">{svg("mountain", 44)} Risk Dashboard</div>', unsafe_allow_html=True)
    with h2:
        lake = lake_picker("lake_dash")
    with h3:
        with st.popover("📂 Upload Lake", use_container_width=True):
            st.markdown("**Upload External Lake CSV**")
            up_csv = st.file_uploader("Select CSV file (e.g. GEE export)", type=["csv"], key="top_right_csv_uploader")
            if up_csv is not None:
                process_uploaded_lake_csv(up_csv)

    lake_hist, r = latest_row(lake)
    score = predict_single_lake_risk(row_to_df(r))
    label, color = risk_level(score)
    fac = key_factors(r)

    left, right = st.columns([1.05, 2.35], gap="medium")
    with left:
        st.markdown(
            f"""<div class="gwcard" style="margin-bottom:18px"><div class="card-title" style="text-align:center">Current Risk Score</div>
<div class="donut" style="background: conic-gradient(#2f6fe4 {score*3.6:.1f}deg, #a9c6f5 0deg);"><div class="donut-in"><b>{score:.0f}</b><small>%</small></div></div>
<div class="risk-label" style="color:{color}">{label}</div></div>""",
            unsafe_allow_html=True,
        )
        rows = [
            ("lake", "Lake Area", fac["expansion"], f"{float(r['Area_km2']):.2f} km²"),
            ("glacier", "Glacier Dist.", fac["proximity"], f"{float(r['d_glacier_km']):.2f} km"),
            ("slope", "Dam Slope", fac["slope"], f"{float(r['S_dam_deg']):.1f}°"),
            ("rain", "Rainfall", fac["rain"], f"{float(r['Rain_mm']):.0f} mm"),
        ]
        bars = "".join(
            f'<div class="fbar"><span class="nm" style="width:130px">{svg(i, 20)}{n}</span>'
            f'<div class="track"><div class="fill" style="width:{v*100:.0f}%"></div></div>'
            f'<span class="pc" style="width:68px">{unit_txt}</span></div>'
            for i, n, v, unit_txt in rows
        )
        st.markdown(f'<div class="gwcard"><div class="card-title">Key Factors</div>{bars}</div>', unsafe_allow_html=True)

    with right:
        lat, lon = float(r["Latitude"]), float(r["Longitude"])
        m = folium.Map(
            location=[lat, lon],
            zoom_start=14,max_zoom=18,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery",
            zoom_control=False,
        )
        lake_r = float(np.clip(np.sqrt(max(float(r["Area_km2"]), 0.04) * 1e6 / np.pi), 220.0, 1300.0))
        folium.Circle(
            [lat, lon],
            radius=lake_r * 2.2,
            color="#ff9f43",
            weight=3,
            fill=True,
            fill_color="#ff9f43",
            fill_opacity=0.14,
            dash_array="8,6",
        ).add_to(m)
        folium.Circle(
            [lat, lon],
            radius=lake_r,
            color="#8be0ff",
            weight=3,
            fill=True,
            fill_color="#4cc9f0",
            fill_opacity=0.45,
            popup=f"<b>{lake}</b><br>Risk: {score:.1f}%",
        ).add_to(m)
        folium.Marker([lat, lon], tooltip=f"{lake} (approx. coordinates)",
                      icon=folium.Icon(color="red", icon="tint", prefix="fa")).add_to(m)
        m.get_root().html.add_child(
            folium.Element(
                "<div style='position:fixed;top:14px;right:14px;z-index:9999;background:rgba(15,42,92,.82);color:#fff;"
                "padding:10px 16px;border-radius:14px;font:13px sans-serif;line-height:1.9'>"
                "<span style='color:#4cc9f0;font-size:16px'>●</span> Lake Boundary<br>"
                "<span style='color:#ff9f43;font-size:16px'>●</span> Risk Zone</div>"
            )
        )
        components.html(m.get_root().render(), height=430)

        if score < 33:
            safe_reasons = []
            if float(r["d_glacier_km"]) >= 0.4:
                safe_reasons.append(f"safe distance from the glacier tongue ({float(r['d_glacier_km']):.2f} km)")
            if float(r["Area_km2"]) < 0.8:
                safe_reasons.append(f"moderate water volume ({float(r['Area_km2']):.2f} km²)")
            if float(r["Rain_mm"]) < 50:
                safe_reasons.append(f"low seasonal precipitation ({float(r['Rain_mm']):.0f} mm)")
            if len(safe_reasons) < 2:
                safe_reasons.extend(["stable moraine dam geometry", "low hydrostatic stress"])
            banner_msg = f"The lake is classified as <b>{label.lower()}</b> due to {safe_reasons[0]} and {safe_reasons[1]}."
        else:
            drivers = sorted(
                [
                    ("lake volume expansion", fac["expansion"]),
                    ("steep moraine dam slope", fac["slope"]),
                    ("heavy seasonal precipitation", fac["rain"]),
                    ("close proximity to the glacier tongue", fac["proximity"]),
                ],
                key=lambda x: -x[1],
            )[:2]
            banner_msg = f"The lake is classified as <b>{label.lower()}</b> primarily driven by {drivers[0][0]} and {drivers[1][0]}."

        st.markdown(
            f'<div class="banner">{icon_img("icon_info", 30)}<div>{banner_msg}</div></div>',
            unsafe_allow_html=True,
        )

    with st.expander("📈 Risk timeline: history + 3-year forecast (2020 – 2029)", expanded=True):
        d = lake_hist.copy()
        d["Datetime"] = pd.to_datetime(d["Year"].astype(str) + "-" + d["Month"].astype(str).str.zfill(2) + "-01")
        d["Risk"] = [predict_single_lake_risk(row_to_df(d.iloc[i])) for i in range(len(d))]
        
        num = ["Risk", "Area_km2", "d_glacier_km", "Rain_mm", "Temp_C", "Snow_Depth_m"]
        d = d.groupby("Datetime", as_index=False)[num].mean().sort_values("Datetime").reset_index(drop=True)

        first_yr, last_yr = int(d["Datetime"].dt.year.min()), int(d["Datetime"].dt.year.max())
        span = max(1, last_yr - first_yr)
        early = d[d["Datetime"].dt.year <= first_yr + 1]["Area_km2"].mean()
        late = d[d["Datetime"].dt.year >= last_yr - 1]["Area_km2"].mean()
        growth = float(np.clip((late - early) / (max(early, 0.05) * span), -0.02, 0.07))
        clim = d.groupby(d["Datetime"].dt.month)[["Area_km2", "d_glacier_km", "Rain_mm", "Temp_C", "Snow_Depth_m"]].mean()
        last_dt = d["Datetime"].iloc[-1]
        
        fut = []
        for step in range(1, 37, 3):
            dt = last_dt + pd.DateOffset(months=step)
            c = clim.loc[dt.month] if dt.month in clim.index else clim.mean()
            ya = step / 12.0
            fr = row_to_df(
                r,
                Area_km2=max(0.01, c["Area_km2"] * (1 + growth) ** ya),
                d_glacier_km=max(0.015, c["d_glacier_km"] * (1 - 0.35 * max(0, growth)) ** ya),
                Rain_mm=max(0, c["Rain_mm"] * (1 + 0.015 * ya)),
                Temp_C=c["Temp_C"] + 0.08 * ya,
                Snow_Depth_m=max(0.02, c["Snow_Depth_m"]),
            )
            fut.append({"Datetime": dt, "Risk": predict_single_lake_risk(fr), "Phase": "Forecast"})
            
        tl = pd.concat([d[["Datetime", "Risk"]].assign(Phase="History"), pd.DataFrame(fut)], ignore_index=True)
        y_dom = dynamic_y_domain(tl["Risk"], pad=8.0, min_span=24.0)

        base = alt.Chart(tl).encode(
            x=alt.X("Datetime:T", title=None),
            y=alt.Y("Risk:Q", scale=alt.Scale(domain=y_dom, clamp=True), title="Risk Score (%)"),
            tooltip=[
                alt.Tooltip("Datetime:T", title="Date", format="%Y-%m"),
                alt.Tooltip("Phase:N", title="Phase"),
                alt.Tooltip("Risk:Q", title="Risk Score", format=".1f"),
            ],
        )
        chart = (
            base.mark_line(strokeWidth=3.2, interpolate="monotone").encode(
                color=alt.Color("Phase:N", scale=alt.Scale(domain=["History", "Forecast"], range=["#2563eb", "#ef4444"]))
            )
            + base.mark_circle(size=45).encode(
                color=alt.Color("Phase:N", scale=alt.Scale(domain=["History", "Forecast"], range=["#2563eb", "#ef4444"]))
            )
            + alt.Chart(pd.DataFrame({"c": [last_dt]})).mark_rule(strokeDash=[4, 4], color=NAVY).encode(x="c:T")
        ).properties(height=360).configure(background="transparent").configure_view(strokeWidth=0).configure_axis(
            labelColor=NAVY, titleColor=NAVY, gridColor="#c4d5f0"
        ).configure_legend(labelColor=NAVY, titleColor=NAVY)
        show_chart(chart)

elif page == "What-If Simulator":
    need_data()
    h1, h2 = st.columns([3.4, 1.1])
    with h1:
        st.markdown(
            f'<div class="page-title">{svg("flask", 40)} What-If Simulator</div>'
            '<div class="subtitle">Explore how changes in environmental conditions affect the risk level.</div>',
            unsafe_allow_html=True,
        )
    with h2:
        lake = lake_picker("lake_sim")
    lake_hist, r = latest_row(lake)

    if "rain_pct" not in st.session_state:
        st.session_state.rain_pct = 40.0
    else:
        st.session_state.rain_pct = float(np.clip(st.session_state.rain_pct, -50.0, 100.0))

    if "temp_chg" not in st.session_state:
        st.session_state.temp_chg = 1.5
    else:
        st.session_state.temp_chg = float(np.clip(st.session_state.temp_chg, -10.0, 10.0))

    st.session_state["rain_slider"] = float(st.session_state.rain_pct)
    st.session_state["rain_num"] = float(st.session_state.rain_pct)
    st.session_state["temp_slider"] = float(st.session_state.temp_chg)
    st.session_state["temp_num"] = float(st.session_state.temp_chg)

    def _sync_rain_from_slider():
        v = round(float(st.session_state["rain_slider"]), 1)
        st.session_state.rain_pct = v
        st.session_state["rain_num"] = v

    def _sync_rain_from_num():
        v = round(float(np.clip(st.session_state["rain_num"], -50.0, 100.0)), 1)
        st.session_state.rain_pct = v
        st.session_state["rain_slider"] = v

    def _sync_temp_from_slider():
        v = round(float(st.session_state["temp_slider"]), 1)
        st.session_state.temp_chg = v
        st.session_state["temp_num"] = v

    def _sync_temp_from_num():
        v = round(float(np.clip(st.session_state["temp_num"], -10.0, 10.0)), 1)
        st.session_state.temp_chg = v
        st.session_state["temp_slider"] = v

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        with card():
            rh1, rh2 = st.columns([1.8, 1.0], gap="small")
            with rh1:
                st.markdown(
                    f'<div class="sim-head"><span class="l">{svg("rain", 30)} Rainfall Change (%)</span></div>',
                    unsafe_allow_html=True,
                )
            with rh2:
                st.number_input(
                    "Rainfall (%)",
                    min_value=-50.0,
                    max_value=100.0,
                    step=0.1,
                    format="%.1f",
                    key="rain_num",
                    on_change=_sync_rain_from_num,
                    label_visibility="collapsed",
                )
            st.slider(
                "Rainfall Change",
                -50.0,
                100.0,
                step=0.1,
                format="%.1f%%",
                key="rain_slider",
                on_change=_sync_rain_from_slider,
                label_visibility="collapsed",
            )
            st.markdown(
                '<div class="ticks"><span style="left:0">-50%</span>'
                '<span style="left:33.33%;transform:translateX(-50%)">0%</span><span style="right:0">+100%</span></div>',
                unsafe_allow_html=True,
            )
    with c2:
        with card():
            th1, th2 = st.columns([1.8, 1.0], gap="small")
            with th1:
                st.markdown(
                    f'<div class="sim-head"><span class="l">{svg("thermo", 30)} Temperature Change (°C)</span></div>',
                    unsafe_allow_html=True,
                )
            with th2:
                st.number_input(
                    "Temperature (°C)",
                    min_value=-10.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f",
                    key="temp_num",
                    on_change=_sync_temp_from_num,
                    label_visibility="collapsed",
                )
            st.slider(
                "Temperature Change",
                -10.0,
                10.0,
                step=0.1,
                format="%.1f°C",
                key="temp_slider",
                on_change=_sync_temp_from_slider,
                label_visibility="collapsed",
            )
            st.markdown(
                '<div class="ticks"><span style="left:0">-10°C</span>'
                '<span style="left:50%;transform:translateX(-50%)">0°C</span><span style="right:0">+10°C</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("Analyze Scenario", icon=":material/bar_chart:", key="analyze", type="primary"):
        st.session_state.scenario = {
            "lake": lake,
            "rain": float(st.session_state.rain_pct),
            "temp": float(st.session_state.temp_chg),
        }

    sc = st.session_state.get("scenario")
    if sc and sc["lake"] == lake:
        base_score = predict_single_lake_risk(row_to_df(r))
        new_score, d_rain, d_temp = scenario_score(base_score, sc["rain"], sc["temp"])
        lvl, lcol = risk_level(new_score)
        delta = new_score - base_score

        st.markdown(
            f'<div class="page-title" style="font-size:26px;margin:22px 0 12px 0">{icon_img("icon_chart", 36)} Scenario Results</div>',
            unsafe_allow_html=True,
        )
        rl, rr = st.columns([1, 2.3], gap="medium")
        with rl:
            st.markdown(
                f"""<div class="gwcard" style="min-height:360px"><div class="card-title">New Risk Score</div>
<div class="big-score" style="color:{lcol}">{new_score:.1f}%</div>
<span class="pill" style="background:{lcol}22;color:{lcol}">{lvl}</span>
<div class="pts"><b>{delta:+.1f} pts</b> vs. current ({base_score:.1f}%)<br>Rainfall ({sc['rain']:+.1f}%): {d_rain:+.1f} pts &nbsp;·&nbsp; Temp ({sc['temp']:+.1f}°C): {d_temp:+.1f} pts</div></div>""",
                unsafe_allow_html=True,
            )
        with rr:
            with card():
                st.markdown('<div class="card-title">Risk Trend</div>', unsafe_allow_html=True)
                pts = [
                    ("Current", base_score),
                    (f"Temp ({sc['temp']:+.1f}°C)", scenario_score(base_score, 0.0, sc["temp"])[0]),
                    ("Selected Scenario", new_score),
                    ("Extreme (+75% Rain)", scenario_score(base_score, 75.0, sc["temp"])[0]),
                ]
                tdf = pd.DataFrame(pts, columns=["Scenario", "Risk"])
                order = [p[0] for p in pts]
                sim_y_dom = dynamic_y_domain(tdf["Risk"], pad=8.0, min_span=22.0)

                ln = alt.Chart(tdf).encode(
                    x=alt.X(
                        "Scenario:N",
                        sort=order,
                        title=None,
                        axis=alt.Axis(labelAngle=0, labelColor=NAVY, labelFontSize=13, domain=False, ticks=False, grid=False),
                    ),
                    y=alt.Y(
                        "Risk:Q",
                        scale=alt.Scale(domain=sim_y_dom, clamp=True),
                        title=None,
                        axis=alt.Axis(
                            labelExpr="datum.value + '%'",
                            labelColor=NAVY,
                            labelFontSize=12,
                            gridColor="#c4d5f0",
                            domain=False,
                            ticks=False,
                        ),
                    ),
                    tooltip=[alt.Tooltip("Scenario:N"), alt.Tooltip("Risk:Q", format=".1f")],
                )
                area = ln.mark_area(
                    color=alt.Gradient(
                        gradient="linear",
                        stops=[
                            alt.GradientStop(color="rgba(224,49,49,0.35)", offset=0),
                            alt.GradientStop(color="rgba(224,49,49,0.04)", offset=1),
                        ],
                        x1=1,
                        x2=1,
                        y1=0,
                        y2=1,
                    ),
                    interpolate="monotone",
                )
                chart = (
                    area
                    + ln.mark_line(color="#d62828", strokeWidth=3.2, interpolate="monotone")
                    + ln.mark_circle(color="#d62828", size=110)
                ).properties(height=310).configure(background="transparent").configure_view(strokeWidth=0)
                show_chart(chart)

        if sc["rain"] > 0 and d_rain >= d_temp:
            msg = "Increased rainfall significantly raises the risk of a GLOF event, especially in already high-risk lakes."
        elif sc["temp"] > 0:
            msg = "Warming accelerates glacier melt and lake growth, which increases the pressure on the moraine dam."
        elif sc["rain"] < 0 or sc["temp"] < 0:
            msg = "Lower rainfall and cooler conditions reduce the water load and ease the pressure on the moraine dam."
        else:
            msg = "No change in conditions: the risk stays at its current level."

        pic, _ = photo_or_svg(["insight.jpg", "insight.jpeg", "insight.png"], dark=True)
        st.markdown(
            f"""<div class="gwcard" style="margin-top:18px"><div class="insight-row"><div class="txt"><div class="card-title" style="display:flex;align-items:center;gap:10px">{svg("bulb", 26)} Key Insights</div>
A <b>{sc['rain']:+.1f}%</b> change in rainfall with a <b>{sc['temp']:+.1f}°C</b> change in temperature moves this lake from <b>{base_score:.1f}%</b> to <b>{new_score:.1f}%</b>. {msg}</div>
<div class="pic" style="background-image:url({pic})"></div></div></div>""",
            unsafe_allow_html=True,
        )

else:
    left, right = st.columns([2.7, 1], gap="medium")
    with left:
        st.markdown(
            f"""<div class="about-top" style="background: url({to_uri(landscape_svg(False))}) right bottom / 52% auto no-repeat;">
<div class="page-title">{icon_img("icon_info", 38)} About GlacierWatch</div>
<p>GlacierWatch uses key environmental factors — such as lake area, glacier proximity, terrain slope, and rainfall — to calculate the risk of glacial lake outburst floods (GLOF).</p></div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div class="gwcard" style="margin-bottom:18px"><div class="card-title">Our Methodology</div><div class="steps">
<div class="step"><div class="ico">{icon_img("icon_satellite", 62)}</div>Data Collection<br><small>(Satellite Data)</small></div><div class="arrow">→</div>
<div class="step"><div class="ico">{icon_img("icon_chart", 62)}</div>Risk Analysis<br><small>(6 Key Factors)</small></div><div class="arrow">→</div>
<div class="step"><div class="ico">{icon_img("icon_gauge", 62)}</div>Risk Score<br><small>(0 – 100)</small></div><div class="arrow">→</div>
<div class="step"><div class="ico">{icon_img("icon_sliders", 62)}</div>What-If Scenarios</div></div></div>""",
            unsafe_allow_html=True,
        )
        cells = [
            ("lake", "Lake Area<br>Expansion"),
            ("glacier", "Glacier<br>Proximity"),
            ("slope", "Terrain<br>Slope"),
            ("rain", "Rainfall<br>Trends"),
            ("shield", "Moraine Dam<br>Stability"),
            ("houses", "Downstream<br>Exposure"),
        ]
        grid = "".join(f'<div class="fcell">{svg(i, 52)}<span>{t}</span></div>' for i, t in cells)
        st.markdown(
            f'<div class="gwcard"><div class="card-title">Key Factors Used</div><div class="fgrid">{grid}</div></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""<div class="safer"><div style="display:flex;justify-content:center">{svg("globe", 78)}</div>
<h3>A Safer Tomorrow<br>with GlacierWatch</h3><p>Early detection.</p><p>Greater preparedness.</p><p>A safer world.</p></div>""",
            unsafe_allow_html=True,
        )