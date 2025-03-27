import asyncio
import logging

from app.core.bot import bot, dp
from app.handlers import get_routers
from app.middlewares.database import DatabaseMiddleware


async def on_startup() -> None:
    """Function to execute on bot startup."""
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.include_routers(get_routers())


async def on_shutdown() -> None:
    """Function to execute on bot shutdown."""
    await dp.storage.close()
    await dp.fsm.storage.close()
    await bot.session.close()


async def main() -> None:
    """Main function to start the bot."""
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    asyncio.run(main())
