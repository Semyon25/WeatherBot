import aiohttp
from config import WEATHER_API_KEY
from datetime import datetime
from typing import Any

WEATHER_URL = "http://api.weatherapi.com/v1/forecast.json"

HOURS_TO_DISPLAY = {
    8: "🌅 Утро",
    14: "🌞 День",
    20: "🌇 Вечер"
}


async def fetch_weather_data(city: str, days: int = 2, lang: str = "ru") -> dict[str, Any] | None:
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "days": days,
        "lang": lang
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


def parse_current_weather(data: dict[str, Any], city: str) -> str:
    current = data["current"]
    temp = int(current["temp_c"])
    feels = int(current["feelslike_c"])
    condition = current["condition"]["text"]
    wind_ms = round(current["wind_kph"] / 3.6, 1)
    humidity = current["humidity"]

    return (
        f"🌤 Сейчас в {city}:\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels}°C)\n"
        f"🌥 Состояние: {condition}\n"
        f"💨 Ветер: {wind_ms} м/с\n"
        f"💧 Влажность: {humidity}%"
    )


def format_forecast_day(forecast_data: dict[str, Any], label: str) -> str:
    raw_date = datetime.strptime(forecast_data["date"], "%Y-%m-%d")
    date_str = raw_date.strftime("%d.%m.%Y")

    parts = [f"\n📅 {label} ({date_str}):"]
    for hour, time_label in HOURS_TO_DISPLAY.items():
        hour_data = forecast_data["hour"][hour]
        temp = int(hour_data["temp_c"])
        condition = hour_data["condition"]["text"]
        wind = round(hour_data["wind_kph"] / 3.6, 1)

        parts.append(f"{time_label}: {temp}°C, {condition}, 💨 {wind} м/с")

    return "\n".join(parts)


async def get_weather(city: str) -> str:
    data = await fetch_weather_data(city)
    if not data:
        return "⚠ Не удалось получить данные о погоде."

    current_weather = parse_current_weather(data, city)
    forecast_days = data["forecast"]["forecastday"]
    today = format_forecast_day(forecast_days[0], "Сегодня")
    tomorrow = format_forecast_day(forecast_days[1], "Завтра")

    return f"{current_weather}\n\n{today}\n\n{tomorrow}"

async def is_weather_available(city: str) -> bool:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return False
            data = await resp.json()
            # WeatherAPI вернёт "error" в JSON при несуществующем городе
            return "error" not in data
