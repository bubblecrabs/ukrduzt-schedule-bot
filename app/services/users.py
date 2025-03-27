from sqlalchemy import select, update, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Get a single user by their unique user_id."""
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession, limit: int = 100, offset: int = 0) -> list[User]:
    """Getting the list of all users in the database with pagination."""
    query = select(User).limit(limit).offset(offset).order_by(User.created_at.desc())
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_user_is_admin(session: AsyncSession, user_id: int) -> bool:
    """Check if the user is an admin."""
    query = select(User.is_admin).filter_by(user_id=user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_users_count(session: AsyncSession) -> int:
    """Get the total count of users in the database."""
    stmt = select(func.count()).select_from(User)
    result = await session.execute(stmt)
    return result.scalar() or 0


async def get_latest_user(session: AsyncSession) -> User | None:
    """Get the most recently created user based on ID."""
    query = select(User).order_by(desc(User.id)).limit(1)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_id: int,
    username: str | None = None,
    user_faculty: int | None = None,
    user_course: int | None = None,
    user_group: int | None = None,
    user_group_name: str | None = None,
    is_admin: bool = False,
) -> User:
    """Add a new user to the database."""
    user = await get_user_by_id(session=session, user_id=user_id)
    if user:
        return user

    new_user = User(
        user_id=user_id,
        username=username,
        user_faculty=user_faculty,
        user_course=user_course,
        user_group=user_group,
        user_group_name=user_group_name,
        is_admin=is_admin,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def update_user(
    session: AsyncSession,
    user_id: int,
    username: str | None = None,
    user_faculty: int | None = None,
    user_course: int | None = None,
    user_group: int | None = None,
    user_group_name: str | None = None,
    is_admin: bool | None = None,
) -> User | None:
    """Updating user data in the database."""
    user = await get_user_by_id(session=session, user_id=user_id)
    if not user:
        return

    update_data = {}
    if username is not None:
        update_data["username"] = username
    if user_faculty is not None:
        update_data["user_faculty"] = user_faculty
    if user_course is not None:
        update_data["user_course"] = user_course
    if user_group is not None:
        update_data["user_group"] = user_group
    if user_group_name is not None:
        update_data["user_group_name"] = user_group_name
    if is_admin is not None:
        update_data["is_admin"] = is_admin

    if update_data:
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()
        await session.refresh(user)

    return user
