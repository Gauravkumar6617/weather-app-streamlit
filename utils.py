import requests

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    res = requests.get(url, timeout=5)

    if res.status_code == 200 and res.json().get("results"):
        data = res.json()["results"][0]
        return data["latitude"], data["longitude"], data["name"]

    return None, None, None


def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=temperature_2m"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=auto"
    )

    res = requests.get(url, timeout=5)
    return res.json() if res.status_code == 200 else None