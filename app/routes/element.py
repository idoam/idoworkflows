from fastapi import APIRouter, Depends
from schemas.element import *
from services.element import ElementService
from sqlmodel import Session
from vd_fastapi_core.auth import get_auth
from vd_fastapi_core.db import get_session

router = APIRouter(
    prefix="/element", tags=["Element"], dependencies=[Depends(get_auth)]
)


@router.post("/")
def create_element(
    element_create: ElementCreate,
    session: Session = Depends(get_session),
) -> ElementPublic:
    return ElementService(session).create_element(element_create)


@router.get("/{element_id}")
def get_element(
    element_id: int,
    session: Session = Depends(get_session),
) -> ElementPublicUnrolled:
    return ElementService(session).get_element(element_id)


@router.patch("/{element_id}")
def partial_update_element(
    element_id: int,
    element_update: ElementPartialUpdate,
    session: Session = Depends(get_session),
) -> ElementPublic:
    return ElementService(session).partial_update_element(element_id, element_update)


@router.delete("/{element_id}")
def delete_element(element_id: int, session: Session = Depends(get_session)) -> None:
    return ElementService(session).delete_element(element_id)
