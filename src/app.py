from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import IncidentPost, IncidentDB, IncidentPut
from db import engine, get_db_session
from models import Base, Incident
from enums import IncidentStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(lifespan=lifespan)

@app.post("/incident", response_model=IncidentDB, status_code=201)
async def create_incident(incident_post: IncidentPost,
                          async_session: Annotated[AsyncSession, Depends(get_db_session)]):

    incident = Incident(**incident_post.dict())
    async_session.add(incident)
    await async_session.commit()
    return incident

@app.get("/incidents", response_model=list[IncidentDB])
async def search_incidents_by_status(status: IncidentStatus,
                          async_session: Annotated[AsyncSession, Depends(get_db_session)]):
    incidents_stmt = select(Incident).where(Incident.status == status)

    res = await async_session.execute(incidents_stmt)
    incidents = res.scalars()
    return incidents

@app.put("/incident", response_model=IncidentDB)
async def update_incident(incident: IncidentPut,
                          async_session: Annotated[AsyncSession, Depends(get_db_session)]):
    incident_db = await async_session.get(Incident, incident.id)

    if incident_db:
        incident_db.status = incident.status
        incident_db.description = incident.description
        incident_db.source = incident.source

        await async_session.commit()
        return incident_db
    else:
        raise HTTPException(status_code=404, detail="Incident not found")
