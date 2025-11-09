import enum
import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum, Text

from enums import IncidentStatus, IncidentSource

class Base(DeclarativeBase):
    pass


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    source: Mapped[IncidentSource] = mapped_column(Enum(IncidentSource))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
