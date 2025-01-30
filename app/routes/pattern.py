from fastapi import APIRouter, Depends
from schemas.pattern import *
from services.pattern import PatternService
from sqlmodel import Session
from vd_fastapi_core.auth import get_auth
from vd_fastapi_core.db import get_session

router = APIRouter(
    prefix="/pattern", tags=["Pattern"], dependencies=[Depends(get_auth)]
)


@router.get("/")
def get_patterns(
    limit: int | None = 100,
    offset: int | None = 0,
    session: Session = Depends(get_session),
) -> GetPatternsResponse:
    return PatternService(session).get_patterns(limit, offset)


@router.post("/")
def create_pattern(
    pattern_create: PatternCreate,
    session: Session = Depends(get_session),
) -> PatternPublic:
    return PatternService(session).create_pattern(pattern_create)


@router.get("/{pattern_id}")
def get_pattern(
    pattern_id: int,
    session: Session = Depends(get_session),
) -> PatternPublic:
    return PatternService(session).get_pattern(pattern_id)


@router.patch("/{pattern_id}")
def partial_update_pattern(
    pattern_id: int,
    pattern_update: PatternPartialUpdate,
    session: Session = Depends(get_session),
) -> PatternPublic:
    return PatternService(session).partial_update_pattern(pattern_id, pattern_update)


@router.put("/{pattern_id}")
def update_pattern(
    pattern_id: int,
    pattern_update: PatternUpdate,
    session: Session = Depends(get_session),
) -> PatternPublic:
    return PatternService(session).update_pattern(pattern_id, pattern_update)


@router.delete("/{pattern_id}")
def delete_pattern(pattern_id: int, session: Session = Depends(get_session)) -> None:
    return PatternService(session).delete_pattern(pattern_id)


@router.get("/")
def get_patterns(
    limit: int | None = 100,
    offset: int | None = 0,
    session: Session = Depends(get_session),
) -> GetPatternsResponse:
    return PatternService(session).get_patterns(limit, offset)


########################################################################################################################


@router.post("/")
def create_pattern_step(
    pattern_step_create: PatternStepCreate,
    session: Session = Depends(get_session),
) -> PatternStepPublic:
    return PatternStepService(session).create_pattern_step(pattern_step_create)


@router.get("/{pattern_step_id}")
def get_pattern_step(
    pattern_step_id: int,
    session: Session = Depends(get_session),
) -> PatternStepPublic:
    return PatternStepService(session).get_pattern_step(pattern_step_id)


@router.patch("/{pattern_step_id}")
def partial_update_pattern_step(
    pattern_step_id: int,
    pattern_step_update: PatternStepPartialUpdate,
    session: Session = Depends(get_session),
) -> PatternStepPublic:
    return PatternStepService(session).partial_update_pattern_step(
        pattern_step_id, pattern_step_update
    )


@router.put("/{pattern_step_id}")
def update_pattern_step(
    pattern_step_id: int,
    pattern_step_update: PatternStepUpdate,
    session: Session = Depends(get_session),
) -> PatternStepPublic:
    return PatternStepService(session).update_pattern_step(
        pattern_step_id, pattern_step_update
    )


@router.delete("/{pattern_step_id}")
def delete_pattern_step(
    pattern_step_id: int, session: Session = Depends(get_session)
) -> None:
    return PatternStepService(session).delete_pattern_step(pattern_step_id)
