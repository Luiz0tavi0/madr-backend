from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from madr.models import table_registry
from madr.models.mixins import DateMixin
from madr.models.novelists import Novelist


@mapped_as_dataclass(table_registry)
class Book(DateMixin):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    id_novelist: Mapped[str] = mapped_column(ForeignKey('novelists.id'))
    novelist: Mapped[Novelist] = relationship(back_populates='books')
