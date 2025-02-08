from fastapi import APIRouter, Depends
from schemas.pattern_node import *
from services.pattern_node import PatternNodeService
from sqlmodel import Session
from vd_fastapi_core.auth import get_auth
from vd_fastapi_core.db import get_session

router = APIRouter(
    prefix="/pattern/nodes", tags=["Pattern", "Node"], dependencies=[Depends(get_auth)]
)


@router.get("/")
def get_pattern_nodes(
    limit: int | None = 100,
    offset: int | None = 0,
    session: Session = Depends(get_session),
) -> GetPatternNodesResponse:
    return PatternNodeService(session).get_pattern_nodes(limit, offset)


@router.post("/")
def create_pattern_node(
    pattern_node_create: PatternNodeCreate,
    session: Session = Depends(get_session),
) -> PatternNodePublic:
    return PatternNodeService(session).create_pattern_node(pattern_node_create)


@router.get("/{pattern_node_id}")
def get_pattern_node(
    pattern_node_id: int,
    session: Session = Depends(get_session),
) -> PatternNodePublic:
    return PatternNodeService(session).get_pattern_node(pattern_node_id)


@router.patch("/{pattern_node_id}")
def partial_update_pattern_node(
    pattern_node_id: int,
    pattern_node_update: PatternNodePartialUpdate,
    session: Session = Depends(get_session),
) -> PatternNodePublic:
    return PatternNodeService(session).partial_update_pattern_node(
        pattern_node_id, pattern_node_update
    )


@router.put("/{pattern_node_id}")
def update_pattern_node(
    pattern_id: int,
    pattern_update: PatternNodeUpdate,
    session: Session = Depends(get_session),
) -> PatternNodePublic:
    return PatternNodeService(session).update_pattern_node(pattern_id, pattern_update)


@router.delete("/{pattern_node_id}")
def delete_pattern_node(
    pattern_node_id: int, session: Session = Depends(get_session)
) -> None:
    return PatternNodeService(session).delete_pattern_node(pattern_node_id)
