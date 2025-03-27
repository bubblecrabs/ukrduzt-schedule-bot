from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.users import update_user
from app.utils.keyboards import manage_admins_kb, back_button_kb
from app.utils.states import AdminStates

router = Router()


@router.callback_query(F.data == "manage_admins", AdminFilter())
async def manage_admins_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the manage_admins callback query."""
    await call.message.edit_text(
        text="<b>Виберіть, що хочете зробити ⬇️</b>",
        reply_markup=manage_admins_kb(),
    )
    await state.set_state(AdminStates.func)


@router.callback_query(F.data.in_({"add_admin", "delete_admin"}), AdminFilter())
async def get_admin_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the add_admin and delete_admin callback query."""
    await state.update_data(func=call.data)
    await call.message.edit_text(
        text=(
            "✍️ <b>Введіть ID користувача або адміністратора.</b>\n\n"
            "🔍 Отримати ID - <a href='tg://resolve?domain=getmyid_bot'>@getmyid_bot</a>"
        ),
        reply_markup=back_button_kb("options"),
    )
    await state.set_state(AdminStates.id)


@router.message(StateFilter(AdminStates.id), AdminFilter())
async def set_admin_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Handles for the admin id message."""
    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Неправильний ID користувача.</b>")
        return

    data = await state.get_data()
    user_id = int(message.text)
    admin = True if data["func"] == "add_admin" else False

    result = await update_user(
        session=session,
        user_id=user_id,
        is_admin=admin,
    )
    if not result:
        await message.answer(text="⁉️ <b>Користувача не знайдено.</b>")
        return

    await message.answer(text="✅ <b>Статус користувача успішно змінено.</b>")
    await state.clear()
