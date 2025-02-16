from datetime import datetime
from typing import Sequence

from pydantic import BaseModel
from schemas.element import ElementNestedInInstance


class InstancePublic(BaseModel):
    id: int
    workflow_id: int

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class InstancePublicUnrolled(BaseModel):
    id: int
    workflow_id: int

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    elements: list[ElementNestedInInstance]


class InstanceCreate(BaseModel):
    workflow_id: int


class InstancePartialUpdate(BaseModel):
    # FIXME elements: list["Element"] = []
    pass


class GetInstancesResponse(BaseModel):
    count: int
    instances: Sequence[InstancePublic]
