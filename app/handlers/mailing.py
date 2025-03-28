from datetime import datetime
from urllib.parse import urlparse

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.mailing import create_mailing_task
from app.services.users import get_users
from app.utils.keyboards import mailing_kb, back_button_kb
from app.utils.states import MailingStates

router = Router()


@router.callback_query(F.data == "manage_mailing", AdminFilter())
async def manage_mailing_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the manage_mailing callback query."""
    message_data = await state.get_data()

    text = message_data.get("text", "Не встановлено")
    image = message_data.get("image", "Не встановлено")
    button_text = message_data.get("button_text", "Не встановлено")
    button_url = message_data.get("button_url", "Не встановлено")
    scheduled = message_data.get("delay", "Не заплановано")
    is_button_set = "Встановлено" if button_text != "Не встановлено" else "Не встановлено"

    text_message = (
        f"ℹ️ <b>Інформація про розсилку:</b>\n\n"
        f"✍️ <b>Текст:</b> {text}\n"
        f"🌄 <b>Зображення:</b> {image}\n"
        f"⏹️ <b>Кнопка під текстом:</b> {is_button_set}\n"
        f"💬 <b>Текст кнопки:</b> {button_text}\n"
        f"🔗 <b>Посилання кнопки:</b> {button_url}\n"
        f"⏰ <b>Запланована розсилка:</b> {scheduled}\n"
    )
    await call.message.edit_text(
        text=text_message,
        reply_markup=mailing_kb(),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data == "add_text", AdminFilter())
async def add_text_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the add_text callback query."""
    await call.message.edit_text(
        text="💬 <b>Введіть повідомлення для розсилки.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )
    await state.set_state(MailingStates.text)


@router.message(StateFilter(MailingStates.text), AdminFilter())
async def set_text_handler(message: Message, state: FSMContext) -> None:
    """Handles the text message."""
    if len(message.text) > 2000:
        await message.answer(text="⁉️ <b>Максимальна довжина — 2000 символів. Спробуйте знову.</b>")
        return

    await state.update_data(text=message.html_text)
    await message.answer(
        text="✅ <b>Текст успішно оновлено.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )


@router.callback_query(F.data == "add_media", AdminFilter())
async def add_media_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the add_media callback query."""
    await call.message.edit_text(
        text="🌄 <b>Надішліть зображення для розсилки.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )
    await state.set_state(MailingStates.media)


@router.message(StateFilter(MailingStates.media), AdminFilter())
async def set_media_handler(message: Message, state: FSMContext) -> None:
    """Handles the media message."""
    if not message.photo:
        await message.answer(text="⁉️ <b>Надішліть будь ласка зображення.</b>")
        return

    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)
    await message.answer(
        text="✅ <b>Зображення успішно оновлено.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )


@router.callback_query(F.data == "add_button", AdminFilter())
async def add_button_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the add_button callback query."""
    await call.message.edit_text(
        text="🔘 <b>Введіть текст кнопки.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )
    await state.set_state(MailingStates.button_text)


@router.message(StateFilter(MailingStates.button_text), AdminFilter())
async def set_button_text_handler(message: Message, state: FSMContext) -> None:
    """Handles the button text message."""
    if len(message.text) > 35:
        await message.answer(text="⁉️ <b>Максимальна довжина — 35 символів. Спробуйте знову.</b>")
        return

    await state.update_data(button_text=message.html_text)
    await message.answer(text="🔗 <b>Введіть URL для кнопки.</b>")
    await state.set_state(MailingStates.button_url)


@router.message(StateFilter(MailingStates.button_url), AdminFilter())
async def set_button_url_handler(message: Message, state: FSMContext) -> None:
    """Handles the button url message."""
    parsed_url = urlparse(message.html_text)

    if not all([parsed_url.scheme, parsed_url.netloc]):
        await message.answer(text="⁉️ <b>Некоректний URL. Введіть правильне посилання.</b>")
        return

    await state.update_data(button_url=message.html_text)
    await message.answer(
        text="✅ <b>Кнопка успішно оновлена.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )


@router.callback_query(F.data == "add_delay", AdminFilter())
async def add_delay_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the add_delay callback query."""
    await call.message.edit_text(
        text=(
            f"🕒 <b>Введіть дату і час розсилки.</b>\n\n"
            f"📆 <b>Формат - <code>{datetime.now().strftime('%d.%m.%Y %H:%M')}</code> UTC+0</b>"
        ),
        reply_markup=back_button_kb("manage_mailing"),
    )
    await state.set_state(MailingStates.delay)


@router.message(StateFilter(MailingStates.delay), AdminFilter())
async def set_delay_handler(message: Message, state: FSMContext) -> None:
    """Handles the delay message."""
    try:
        datetime.strptime(message.html_text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer(text="⁉️ <b>Неправильний формат дати. Використовуйте: дд.мм.рррр гг:хх</b>")
        return

    await state.update_data(delay=message.html_text)
    await message.answer(
        text="✅ <b>Час розсилки успішно оновлено.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )


@router.callback_query(F.data == "reset_mailing", AdminFilter())
async def reset_mailing_handler(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the reset_mailing callback query."""
    await state.clear()
    await call.message.edit_text(
        text="✅ <b>Інформація про розсилку успішно видалена.</b>",
        reply_markup=back_button_kb("manage_mailing"),
    )


@router.callback_query(F.data == "start_mailing", AdminFilter())
async def start_mailing_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the start_mailing callback query."""
    message_data = await state.get_data()

    text = message_data.get("text")
    image = message_data.get("image")
    button_text = message_data.get("button_text")
    button_url = message_data.get("button_url")
    delay = message_data.get("delay")

    if not text and not image:
        await call.message.answer(text="⁉️ <b>Ви не встановили текст або зображення для розсилки.</b>")
        return

    if delay:
        await call.message.edit_text(text="✅ <b>Розсилка успішно відкладена.</b>")
    else:
        await call.message.edit_text(text="✅ <b>Розсилку запущено.</b>")

    async for user in get_users(session=session):
        mailing_data = {
            "chat_id": str(user.user_id),
            "text": text,
            "image": image,
            "button_text": button_text,
            "button_url": button_url,
            "delay": delay
        }
        await create_mailing_task(mailing_data)