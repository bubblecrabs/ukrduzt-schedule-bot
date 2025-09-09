from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.scraper import scraper
from app.services.users import get_user_by_id, update_user
from app.services.website import get_website
from app.utils.keyboards import (
    update_user_kb,
    get_days_kb,
    get_faculties_kb,
    get_courses_kb,
    get_groups_kb,
    back_button_kb,
)
from app.utils.scraper import week_days

router = Router()


@router.callback_query(F.data == "schedule")
async def schedule_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the schedule callback query."""
    user = await get_user_by_id(
        session=session,
        user_id=call.from_user.id,
    )
    if not user.user_group:
        await call.message.edit_text(
            text="Будь ласка, <b>заповніть дані</b>. Це займе лише <b>одну хвилину</b>! 😊",
            reply_markup=update_user_kb(),
        )
    else:
        await call.message.edit_text(
            text="<b>Виберіть день ⬇️</b>",
            reply_markup=get_days_kb(user_exists=True),
        )


@router.callback_query(F.data == "change_group")
async def get_faculties_handler(call: CallbackQuery) -> None:
    """Handles for the change_group callback query."""
    faculties = await scraper.get_faculties()
    await call.message.edit_text(
        text="<b>Виберіть факультатив ⬇️</b>",
        reply_markup=get_faculties_kb(faculties=faculties),
    )


@router.callback_query(F.data.startswith("faculty_"))
async def get_courses_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the faculty_ callback queries."""
    faculty = call.data.replace("faculty_", "")
    await update_user(
        session=session,
        user_id=call.from_user.id,
        user_faculty=int(faculty),
    )
    await call.message.edit_text(
        text="<b>Виберіть курс ⬇️</b>",
        reply_markup=get_courses_kb(),
    )


@router.callback_query(F.data.startswith("course_"))
async def get_groups_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the course_ callback queries."""
    course = call.data.replace("course_", "")
    user = await update_user(
        session=session,
        user_id=call.from_user.id,
        user_course=int(course),
    )
    website = await get_website(session=session)
    groups = await scraper.get_groups(
        year_id=website.year,
        faculty=user.user_faculty,
        course=user.user_course,
    )
    await call.message.edit_text(
        text="<b>Виберіть групу ⬇️</b>",
        reply_markup=get_groups_kb(groups=groups),
    )


@router.callback_query(F.data.startswith("group_"))
async def get_days_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the group_ callback queries."""
    group = call.data.split(";")[0].replace("group_", "")
    group_name = call.data.split(";")[1]
    await update_user(
        session=session,
        user_id=call.from_user.id,
        user_group=int(group),
        user_group_name=group_name,
    )
    await call.message.edit_text(
        text="<b>Виберіть день ⬇️</b>",
        reply_markup=get_days_kb(user_exists=False),
    )


@router.callback_query(F.data.in_([f"{day['id']};{day['name']}" for day in week_days]))
async def get_schedule_handler(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for the week days callback queries."""
    day = call.data.split(";")[0]
    day_name = call.data.split(";")[1]
    website = await get_website(session=session)
    user = await get_user_by_id(
        session=session,
        user_id=call.from_user.id,
    )

    # Get schedule returns tuple of (paired_subjects, unpaired_subjects)
    paired_subjects, unpaired_subjects = await scraper.get_schedule(
        year=website.year,
        semester=website.semester,
        faculty=user.user_faculty,
        course=user.user_course,
        group=user.user_group,
        day=int(day),
    )

    # Format message using class method
    formatted_message = scraper.format_schedule_message(
        paired_subjects=paired_subjects,
        unpaired_subjects=unpaired_subjects,
        selected_day=day_name,
        user_group_name=user.user_group_name,
    )

    await call.message.edit_text(
        text=formatted_message,
        reply_markup=back_button_kb("schedule"),
    )
