import streamlit as st
from utils import get_coordinates, get_weather
import plotly.graph_objects as go

st.set_page_config(page_title="Weather Pro", layout="wide")

# 🌙 Dark Mode Toggle
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("<style>body {background-color: #0E1117; color: white;}</style>", unsafe_allow_html=True)

st.title("🌦️ Weather Pro App")

city = st.text_input("Enter City Name")

# 📍 Current Location (mock for now)
if st.button("📍 Use My Location"):
    city = "Lucknow"

if city:
    lat, lon, location = get_coordinates(city)

    if lat:
        data = get_weather(lat, lon)

        if data:
            current = data["current_weather"]

            # 🌤️ Weather Icons (simple logic)
            weather_code = current["weathercode"]
            if weather_code == 0:
                icon = "☀️ Clear"
            elif weather_code < 3:
                icon = "⛅ Partly Cloudy"
            else:
                icon = "🌧️ Rainy"

            st.subheader(f"{icon} {location}")
            st.write(f"🌡️ Temp: {current['temperature']}°C")
            st.write(f"💨 Wind: {current['windspeed']} km/h")

            # 📊 Hourly Chart
            st.markdown("### ⏱️ Hourly Temperature")

            hourly_temp = data["hourly"]["temperature_2m"]
            hourly_time = data["hourly"]["time"]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hourly_time[:24], y=hourly_temp[:24], mode='lines+markers'))

            st.plotly_chart(fig, use_container_width=True)

            # 📅 7-Day Forecast
            st.markdown("### 📅 7-Day Forecast")

            daily = data["daily"]
            for i in range(len(daily["time"])):
                st.write(
                    f"{daily['time'][i]} → "
                    f"🌡️ {daily['temperature_2m_max'][i]}°C / {daily['temperature_2m_min'][i]}°C"
                )
        else:
            st.error("Weather data not available")
    else:
        st.error("City not found")