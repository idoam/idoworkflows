from datetime import datetime

from pydantic import BaseModel


class ElementNestedInInstance(BaseModel):
    id: int
    node_id: int
    status: str
    updated_at: datetime
    updated_by: str
    dataform: dict | None


class ElementPublic(BaseModel):
    id: int
    instance_id: int
    node_id: int
    status: str
    updated_at: datetime
    updated_by: str
    dataform: dict | None


class ElementPublicUnrolled(BaseModel):
    id: int
    instance_id: int
    node_id: int
    status: str
    updated_at: datetime
    updated_by: str
    dataform: dict | None
    prev: list[ElementPublic]
    next: list[ElementPublic]


class ElementCreate(BaseModel):
    instance_id: int
    node_id: int


class ElementEdgeCreate(BaseModel):
    prev_id: int
    next_id: int


class ElementPartialUpdate(BaseModel):
    status: str | None = None
    dataform: dict | None = None
    next_node_ids: list[int] | None = None
