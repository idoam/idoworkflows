from typing import Sequence

from pydantic import BaseModel


class PatternNodeFromPattern(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    dataform_pydantic_str: str


class PatternNodePublic(BaseModel):
    id: int
    workflow_pattern_id: int
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    dataform_pydantic_str: str


class PatternNodePublicExtended(BaseModel):
    id: int
    workflow_pattern_id: int
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    dataform_pydantic_str: str
    prev: list[PatternNodePublic]
    next: list[PatternNodePublic]


class PatternNodeCreate(BaseModel):
    workflow_pattern_id: int
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    dataform_pydantic_str: str


class PatternNodeUpdate(BaseModel):
    name: str
    description: str | None = None
    category: str
    is_active: bool = True
    dataform_pydantic_str: str


class PatternNodePartialUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    is_active: bool | None = None
    dataform_pydantic_str: str | None = None


class GetPatternNodesResponse(BaseModel):

    count: int
    pattern_nodes: Sequence[PatternNodePublic]
