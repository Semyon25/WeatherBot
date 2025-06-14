import aiohttp
from config import WEATHER_API_KEY, CITY
from datetime import datetime

async def get_weather():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={CITY}&days=2&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

            # Текущая погода
            current = data["current"]
            temp = current["temp_c"]
            feels = current["feelslike_c"]
            condition = current["condition"]["text"]
            wind_kph = current["wind_kph"]
            wind_ms = round(wind_kph / 3.6, 1)
            humidity = current["humidity"]

            current_text = (
                f"🌤 Сейчас в {CITY}:\n"
                f"🌡 Температура: {temp}°C (ощущается как {feels}°C)\n"
                f"🌥 Состояние: {condition}\n"
                f"💨 Ветер: {wind_ms} м/с\n"
                f"💧 Влажность: {humidity}%"
            )

            # Прогноз по часам
            forecast = data["forecast"]["forecastday"]

            def format_hourly(forecast_data, label):
                raw_date = datetime.strptime(forecast_data["date"], "%Y-%m-%d")
                formatted_date = raw_date.strftime("%d.%m.%Y")
                hours = {8: "🌅 Утро", 14: "🌞 День", 20: "🌇 Вечер"}

                parts = [f"\n📅 {label} ({formatted_date}):"]
                for h, title in hours.items():
                    hour_data = forecast_data["hour"][h]
                    temp = hour_data["temp_c"]
                    wind = round(hour_data["wind_kph"] / 3.6, 1)
                    cond = hour_data["condition"]["text"]
                    parts.append(
                        f"{title}: {temp}°C, {cond}, 💨 {wind} м/с"
                    )
                return "\n".join(parts)

            today = format_hourly(forecast[0], "Сегодня")
            tomorrow = format_hourly(forecast[1], "Завтра")

            return f"{current_text}\n\n{today}\n\n{tomorrow}"
