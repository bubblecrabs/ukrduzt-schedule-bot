from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.users import create_user, get_user_is_admin
from app.utils.keyboards import start_kb

router = Router()
start_message = "✋ Привіт, я допоможу дізнатися <b>актуальний розклад</b> на тиждень!"


@router.message(CommandStart())
async def start_command_handler(message: Message, session: AsyncSession) -> None:
    """Handles for the start command."""
    user = await create_user(
        session=session,
        user_id=message.from_user.id,
        username=message.from_user.username,
    )
    await message.answer(
        text=start_message,
        reply_markup=start_kb(is_admin=user.is_admin),
    )


@router.callback_query(F.data == "start")
async def start_callback_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the start callback query."""
    is_admin = await get_user_is_admin(
        session=session,
        user_id=call.from_user.id,
    )
    await call.message.edit_text(
        text=start_message,
        reply_markup=start_kb(is_admin=is_admin),
    )
