from fastapi import APIRouter, Depends
from schemas.instance import *
from services.instance import InstanceService
from sqlmodel import Session
from vd_fastapi_core.auth import get_auth
from vd_fastapi_core.db import get_session

router = APIRouter(
    prefix="/instance", tags=["Instance"], dependencies=[Depends(get_auth)]
)


@router.get("/")
def get_instances(
    limit: int | None = 100,
    offset: int | None = 0,
    session: Session = Depends(get_session),
) -> GetInstancesResponse:
    return InstanceService(session).get_instances(limit, offset)


@router.post("/")
def create_instance(
    instance_create: InstanceCreate,
    session: Session = Depends(get_session),
) -> InstancePublicUnrolled:
    return InstanceService(session).create_instance(instance_create)


@router.get("/{instance_id}")
def get_instance(
    instance_id: int,
    session: Session = Depends(get_session),
) -> InstancePublicUnrolled:
    return InstanceService(session).get_instance(instance_id)


@router.patch("/{instance_id}")
def partial_update_instance(
    instance_id: int,
    instance_update: InstancePartialUpdate,
    session: Session = Depends(get_session),
) -> InstancePublic:
    return InstanceService(session).partial_update_instance(
        instance_id, instance_update
    )


@router.delete("/{instance_id}")
def delete_instance(instance_id: int, session: Session = Depends(get_session)) -> None:
    return InstanceService(session).delete_instance(instance_id)
