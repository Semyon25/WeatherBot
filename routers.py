from aiogram import Router
from handlers import start, weather, settings, location, back

def setup_routers() -> Router:
  router = Router()
  router.include_router(start.router)
  router.include_router(weather.router)
  router.include_router(back.router)
  router.include_router(settings.router)
  router.include_router(location.router)
  return router
  