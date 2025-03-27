from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.website import update_website
from app.utils.keyboards import back_button_kb
from app.utils.states import SiteStates

router = Router()


@router.callback_query(F.data.in_({"update_semester", "update_year"}), AdminFilter())
async def get_website_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the update_semester and update_year callback queries."""
    if call.data == "update_semester":
        await call.message.edit_text(
            text="✍️ <b>Введіть <code>semester_id</code>, який вказаний на сайті.</b>",
            reply_markup=back_button_kb("options"),
        )
        await state.set_state(SiteStates.semester)
    elif call.data == "update_year":
        await call.message.edit_text(
            text="✍️ <b>Введіть <code>year_id</code>, який вказаний на сайті.</b>",
            reply_markup=back_button_kb("options"),
        )
        await state.set_state(SiteStates.year)


@router.message(StateFilter(SiteStates.semester, SiteStates.year), AdminFilter())
async def set_website_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Handles for the website message."""
    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Неправильний формат. Введіть коректне число.</b>")
        return

    current_state = await state.get_state()
    if current_state == SiteStates.semester:
        await update_website(session=session, semester=int(message.text))
        await message.answer(text="✅ <b>Семестр успішно змінено.</b>")
    elif current_state == SiteStates.year:
        await update_website(session=session, year=int(message.text))
        await message.answer(text="✅ <b>Рік навчання успішно змінено.</b>")

    await state.clear()
