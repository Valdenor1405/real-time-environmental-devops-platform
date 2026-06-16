import os
import pandas as pd
import requests
import streamlit as st
import plotly.express as px

API_URL = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="Environmental Intelligence", layout="wide")
st.title("🌎 Real-Time Environmental Intelligence DevOps Platform")
st.caption("Dados climáticos e qualidade do ar coletados em tempo real via Open-Meteo, persistidos em PostgreSQL e monitorados com Prometheus/Grafana.")

@st.cache_data(ttl=30)
def load_data():
    response = requests.get(f"{API_URL}/readings/latest?limit=500", timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json())

try:
    df = load_data()
    if df.empty:
        st.warning("Aguardando a primeira coleta do worker...")
        st.stop()
    df["observed_at"] = pd.to_datetime(df["observed_at"])
    latest = df.sort_values("observed_at").groupby("city").tail(1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cidades monitoradas", latest["city"].nunique())
    c2.metric("Maior temperatura", f"{latest['temperature_c'].max():.1f} °C")
    c3.metric("Maior AQI europeu", f"{latest['european_aqi'].max():.0f}")
    c4.metric("Alertas moderados+", int((latest["risk_level"].isin(["MODERATE", "HIGH", "CRITICAL"])).sum()))

    st.subheader("Mapa de risco ambiental")
    st.map(latest.rename(columns={"latitude":"lat", "longitude":"lon"})[["lat", "lon"]])

    st.subheader("Leituras atuais")
    st.dataframe(latest[["city", "observed_at", "temperature_c", "humidity_pct", "wind_speed_kmh", "pm2_5", "pm10", "european_aqi", "risk_level"]], use_container_width=True)

    selected = st.selectbox("Cidade", sorted(df["city"].unique()))
    city_df = df[df["city"] == selected].sort_values("observed_at")
    fig = px.line(city_df, x="observed_at", y=["temperature_c", "pm2_5", "pm10", "european_aqi"], title=f"Histórico em tempo real - {selected}")
    st.plotly_chart(fig, use_container_width=True)
except Exception as exc:
    st.error(f"Não foi possível carregar os dados: {exc}")
