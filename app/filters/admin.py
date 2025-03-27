from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.users import get_user_is_admin


class AdminFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        if not event.from_user:
            return False

        return await get_user_is_admin(session=session, user_id=event.from_user.id)
