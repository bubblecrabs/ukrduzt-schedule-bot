from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

redis_dsn = str(settings.redis_dsn)

storage = RedisStorage.from_url(url=redis_dsn)

dp = Dispatcher(storage=MemoryStorage())
