from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.filters.admin import AdminFilter
from app.utils.keyboards import options_kb

router = Router()


@router.callback_query(F.data == "options", AdminFilter())
async def options_handler(call: CallbackQuery) -> None:
    """Handles for the options callback query."""
    await call.message.edit_text(
        text="<b>Виберіть, що хочете зробити ⬇️</b>",
        reply_markup=options_kb(),
    )
