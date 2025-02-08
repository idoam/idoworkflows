from fastapi import APIRouter, Depends
from schemas.pattern_edge import *
from services.pattern_edge import PatternEdgeService
from sqlmodel import Session
from vd_fastapi_core.auth import get_auth
from vd_fastapi_core.db import get_session

router = APIRouter(
    prefix="/pattern/edge", tags=["Pattern", "Edge"], dependencies=[Depends(get_auth)]
)


@router.get("/")
def get_pattern_edges(
    limit: int | None = 100,
    offset: int | None = 0,
    session: Session = Depends(get_session),
) -> GetPatternEdgesResponse:
    return PatternEdgeService(session).get_pattern_edges(limit, offset)


@router.post("/")
def create_pattern_edge(
    pattern_edge_create: PatternEdgeCreate,
    session: Session = Depends(get_session),
) -> PatternEdgePublic:
    return PatternEdgeService(session).create_pattern_edge(pattern_edge_create)


@router.get("/{pattern_edge_id}")
def get_pattern_edge(
    pattern_edge_id: int,
    session: Session = Depends(get_session),
) -> PatternEdgePublic:
    return PatternEdgeService(session).get_pattern_edge(pattern_edge_id)


@router.patch("/{pattern_edge_id}")
def partial_update_pattern_edge(
    pattern_edge_id: int,
    pattern_edge_update: PatternEdgePartialUpdate,
    session: Session = Depends(get_session),
) -> PatternEdgePublic:
    return PatternEdgeService(session).partial_update_pattern_edge(
        pattern_edge_id, pattern_edge_update
    )


@router.put("/{pattern_edge_id}")
def update_pattern_edge(
    pattern_id: int,
    pattern_update: PatternEdgeUpdate,
    session: Session = Depends(get_session),
) -> PatternEdgePublic:
    return PatternEdgeService(session).update_pattern_edge(pattern_id, pattern_update)


@router.delete("/{pattern_edge_id}")
def delete_pattern_edge(
    pattern_edge_id: int, session: Session = Depends(get_session)
) -> None:
    return PatternEdgeService(session).delete_pattern_edge(pattern_edge_id)
