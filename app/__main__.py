import asyncio
import logging

from app.core.bot import bot, dp
from app.handlers import get_routers
from app.middlewares.database import DatabaseMiddleware
from app.services.mailing import process_mailing_tasks


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

    async with asyncio.TaskGroup() as tg:
        tg.create_task(dp.start_polling(bot))
        tg.create_task(process_mailing_tasks())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    asyncio.run(main())
