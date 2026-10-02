"""
SQLAlchemy Declarative Base and common model mixins with timezone-aware timestamps.
"""

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass


class TimestampMixin:
    """
    Mixin adding created_at and updated_at timestamp columns with timezone support.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# Import model modules to ensure they are registered with Base.metadata
import app.models.user  # noqa: E402, F401
import app.models.task  # noqa: E402, F401
