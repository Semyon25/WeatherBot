import aiohttp

async def get_city_from_coords(lat: float, lon: float) -> str | None:
  url = "https://nominatim.openstreetmap.org/reverse"
  params = {
      "lat": lat,
      "lon": lon,
      "format": "json",
      "zoom": 10,
      "addressdetails": 1,
  }
  headers = {
      "User-Agent": "TelegramBot (youremail@example.com)"
  }

  async with aiohttp.ClientSession() as session:
      async with session.get(url, params=params, headers=headers) as resp:
          if resp.status == 200:
              data = await resp.json()
              address = data.get("address", {})
              city = address.get("city") or address.get("town") or address.get("village")
              return city
  return None

async def get_city_from_name(city_name: str) -> str | None:
  url = "https://nominatim.openstreetmap.org/search"
  params = {
      "q": city_name,
      "format": "json",
      "limit": 1,
  }
  headers = {
      "User-Agent": "TelegramBot (youremail@example.com)"
  }

  async with aiohttp.ClientSession() as session:
      async with session.get(url, params=params, headers=headers) as resp:
          if resp.status == 200:
              results = await resp.json()
              if results:
                  return results[0].get("display_name")
  return None

# Проверка существования города
async def check_city_exists(city_name) -> bool:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "WeatherTelegramBot (youremail@example.com)"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return bool(data)
            return False
