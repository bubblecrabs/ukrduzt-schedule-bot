from aiogram import Router

from . import admins, mailing, schedule, start, stats, website


def get_routers() -> Router:
    router = Router()
    router.include_router(admins.router)
    router.include_router(mailing.router)
    router.include_router(schedule.router)
    router.include_router(start.router)
    router.include_router(stats.router)
    router.include_router(website.router)
    return router
