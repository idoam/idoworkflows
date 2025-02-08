from typing import Sequence

from pydantic import BaseModel


class PatternEdgePublic(BaseModel):
    id: int
    prev_id: int
    next_id: int
    trigger: str


class PatternEdgeCreate(BaseModel):
    prev_id: int
    next_id: int
    trigger: str


class PatternEdgeUpdate(BaseModel):
    prev_id: int
    next_id: int
    trigger: str


class PatternEdgePartialUpdate(BaseModel):
    prev_id: int | None = None
    next_id: int | None = None
    trigger: str | None = None


class GetPatternEdgesResponse(BaseModel):
    count: int
    pattern_edges: Sequence[PatternEdgePublic]
