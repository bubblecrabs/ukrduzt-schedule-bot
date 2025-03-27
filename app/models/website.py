from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Website(Base):
    __tablename__ = "website"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
