from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.website import Website


async def get_website(session: AsyncSession) -> Website | None:
    """Get the first record from the Website table."""
    query = select(Website).limit(1)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_website(
    session: AsyncSession,
    year: int | None = None,
    semester: int | None = None,
) -> Website | None:
    """Updating the data in the Website table."""
    website = await get_website(session=session)
    if not website:
        return

    update_data = {}
    if year is not None:
        update_data["year"] = year
    if semester is not None:
        update_data["semester"] = semester

    if update_data:
        query = (
            update(Website)
            .where(Website.id == website.id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()
        await session.refresh(website)

    return website
