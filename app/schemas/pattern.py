from typing import Sequence

from pydantic import BaseModel


class WorkflowPatternPublic(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool = True


class WorkflowPatternCreate(BaseModel):
    name: str
    description: str | None
    is_active: bool = True


class WorkflowPatternUpdate(BaseModel):
    name: str
    description: str | None
    is_active: bool = True


class WorkflowPatternPartialUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class GetWorkflowPatternsResponse(BaseModel):
    count: int
    patterns: Sequence[WorkflowPatternPublic]
