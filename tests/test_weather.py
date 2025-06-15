import pytest
from services.weather import is_weather_available

@pytest.mark.asyncio
async def test_is_weather_available():
  result = await is_weather_available("Москва")
  assert result == True

@pytest.mark.asyncio
async def test_is_weather_unavailable():
  result = await is_weather_available("во")
  assert result == False