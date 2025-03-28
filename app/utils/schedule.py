from datetime import datetime, date

week_days = [
    {"name": "Понеділок", "id": "2"},
    {"name": "Вівторок", "id": "3"},
    {"name": "Середа", "id": "4"},
    {"name": "Четвер", "id": "5"},
    {"name": "П'ятниця", "id": "6"},
]


def is_weekend() -> bool:
    """Checks if today is a weekend"""
    today = datetime.today().weekday()
    return today >= 5


def get_current_week() -> str:
    """Returns current week parity (even/odd)"""
    today = date.today()
    week_number = today.isocalendar()[1]
    return "Парна" if week_number % 2 != 0 else "Непарна"


def replace_numbers(schedule: dict[int, str]) -> dict[str, str]:
    """Replaces numeric keys with emoji equivalents"""
    emoji_map = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }
    return {emoji_map.get(key, str(key)): value for key, value in schedule.items()}


def format_schedule_message(subjects: tuple[dict, dict], selected_day: str, user_group_name: str) -> str:
    """Formats schedule message based on day, subjects, and group"""
    weekend = is_weekend()
    selected_week = "наступний" if weekend else "цей"
    current_week = get_current_week()

    if weekend:
        selected_subjects = subjects[1] if current_week == "Парна" else subjects[0]
    else:
        selected_subjects = subjects[0] if current_week == "Парна" else subjects[1]

    formatted_subjects = replace_numbers(selected_subjects)
    subjects_text = "\n".join(f"{pair}: <b>{subject}</b>" for pair, subject in formatted_subjects.items())

    message_text = f"🔔 Показано розклад на <b>{selected_week}</b> тиждень!\n\n"
    if subjects_text:
        message_text += f"{subjects_text}\n\n"
    else:
        message_text += "🔍 На <b>цей</b> день ваш розклад вільний.\n\n"

    message_text += (
        f"⏰ Вибраний день — <b>{selected_day}</b>\n"
        f"📆 Поточна неділя — <b>{current_week}</b>\n"
        f"💼 Вибрана група — <b>{user_group_name}</b>"
    )
    return message_text
