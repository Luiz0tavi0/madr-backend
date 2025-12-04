from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class Romancista:
    __tablename__ = 'romancistas'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
