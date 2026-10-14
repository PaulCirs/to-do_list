from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Todo(Base):
    """Table 'todos' : une ligne = une tâche."""

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(default=False)
