from typing import List

from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from madr.models import table_registry
from madr.models.book import Book
from madr.models.mixins import DateMixin


@mapped_as_dataclass(table_registry)
class Novelist(DateMixin):
    __tablename__ = 'novelists'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[List[Book]] = relationship(
        init=False, cascade='all, delete-orphan',
        lazy='selectin',
        back_populates='novelist')
