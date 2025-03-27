from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.users import get_latest_user, get_users_count
from app.utils.keyboards import back_button_kb

router = Router()


@router.callback_query(F.data == "stats", AdminFilter())
async def stats_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the stats callback query."""
    count_users = await get_users_count(session=session)
    latest_user = await get_latest_user(session=session)

    username_or_id = latest_user.username if latest_user.username else latest_user.user_id
    registration_time = latest_user.created_at.strftime("%d.%m.%Y %H:%M")

    await call.message.edit_text(
        text=(
            f"📊 <b>Статистика:</b>\n\n"
            f"👥 <b>Кількість користувачів:</b> {count_users}\n"
            f"👤 <b>Останній зареєстрований:</b> {username_or_id}\n"
            f"🕒 <b>Час реєстрації:</b> {registration_time}"
        ),
        reply_markup=back_button_kb("options"),
    )
