from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.schedule import week_days


def start_kb(is_admin: bool) -> InlineKeyboardMarkup:
    """Generates the start menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📆 Розклад занять", callback_data="schedule"))
    if is_admin:
        kb.add(InlineKeyboardButton(text="⚡️ Панель розробника", callback_data="options"))
    kb.adjust(1)
    return kb.as_markup()


def back_button_kb(callback_data: str) -> InlineKeyboardMarkup:
    """Generates the back button keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=callback_data))
    kb.adjust(1)
    return kb.as_markup()


def options_kb() -> InlineKeyboardMarkup:
    """Generates the admin menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="👤 Статистика", callback_data="stats"))
    kb.add(InlineKeyboardButton(text="📨 Повідомлення", callback_data="manage_mailing"))
    kb.add(InlineKeyboardButton(text="🔑 Контроль доступу", callback_data="manage_admins"))
    kb.add(InlineKeyboardButton(text="📅 Оновити рік навчання", callback_data="update_year"))
    kb.add(InlineKeyboardButton(text="🎓 Оновити семестр", callback_data="update_semester"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(2, 1, 2, 1)
    return kb.as_markup()


def manage_admins_kb() -> InlineKeyboardMarkup:
    """Generates the manage admins menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="➕ Додати", callback_data="add_admin"))
    kb.add(InlineKeyboardButton(text="➖ Видалити", callback_data="delete_admin"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="options"))
    kb.adjust(2, 1)
    return kb.as_markup()


def mailing_kb() -> InlineKeyboardMarkup:
    """Generates the mailing menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📥 Почати розсилку", callback_data="start_mailing"))
    kb.add(InlineKeyboardButton(text="✍️ Текст", callback_data="add_text"))
    kb.add(InlineKeyboardButton(text="🌄 Медіа", callback_data="add_media"))
    kb.add(InlineKeyboardButton(text="⏹️ Кнопка", callback_data="add_button"))
    kb.add(InlineKeyboardButton(text="⏰ Запланувати", callback_data="add_delay"))
    kb.add(InlineKeyboardButton(text="🔄 Видалити інформацію", callback_data="reset_mailing"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="options"))
    kb.adjust(1, 2, 2, 1)
    return kb.as_markup()


def update_user_kb() -> InlineKeyboardMarkup:
    """Generates the add user menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📝 Заповнити дані", callback_data="change_group"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


def get_days_kb(user_exists: bool) -> InlineKeyboardMarkup:
    """Generates the days menu keyboard."""
    kb = InlineKeyboardBuilder()
    if user_exists:
        kb.add(InlineKeyboardButton(text="📝 Змінити групу", callback_data="change_group"))
    for day in week_days:
        kb.add(InlineKeyboardButton(text=day["name"], callback_data=f"{day['id']};{day['name']}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


def get_faculties_kb(faculties: dict) -> InlineKeyboardMarkup:
    """Generates the faculties menu keyboard."""
    kb = InlineKeyboardBuilder()
    for key, value in faculties.items():
        kb.add(InlineKeyboardButton(text=value, callback_data=f"faculty_{key}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="schedule"))
    kb.adjust(1)
    return kb.as_markup()


def get_courses_kb() -> InlineKeyboardMarkup:
    """Generates the courses menu keyboard."""
    kb = InlineKeyboardBuilder()
    for i in range(1, 7):
        kb.add(InlineKeyboardButton(text=f"{i}-й курс", callback_data=f"course_{i}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="schedule"))
    kb.adjust(1)
    return kb.as_markup()


def get_groups_kb(groups: dict) -> InlineKeyboardMarkup:
    """Generates the groups menu keyboard."""
    kb = InlineKeyboardBuilder()
    for key, value in groups.items():
        kb.add(InlineKeyboardButton(text=value, callback_data=f"group_{key};{value}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="schedule"))
    kb.adjust(1)
    return kb.as_markup()
