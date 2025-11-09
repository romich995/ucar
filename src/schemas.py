import datetime

from pydantic import BaseModel, ConfigDict

from enums import IncidentSource, IncidentStatus


class IncidentPost(BaseModel):
    description: str
    source: IncidentSource


class IncidentPut(IncidentPost):
    id: int
    status: IncidentStatus


class IncidentDB(IncidentPut):
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)