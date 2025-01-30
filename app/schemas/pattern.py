from typing import Sequence

from models import PatternStep, StepForm
from pydantic import BaseModel


class PatternPublic(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool = True


class GetPatternsResponse(BaseModel):
    count: int
    patterns: Sequence[PatternPublic]


class PatternCreate(BaseModel):
    name: str
    description: str | None
    is_active: bool = True


class PatternUpdate(BaseModel):
    name: str
    description: str | None
    is_active: bool = True


class PatternPartialUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


########################################################################################################################


class PatternStepPublic(BaseModel):
    id: int
    pattern_id: int
    name: str
    description: str | None
    category: str
    is_active: bool
    prev: list[PatternStep]
    next: list[PatternStep]
    form_id: int | None
    form: StepForm | None


class PatternStepCreate(BaseModel):
    pattern_id: int
    name: str
    description: str | None
    category: str
    is_active: bool
    prev: list[PatternStep]
    next: list[PatternStep]
    form_id: int | None
    form: StepForm | None


class PatternStepPartialUpdate(BaseModel):
    pattern_id: int | None
    name: str | None
    description: str | None
    category: str | None
    is_active: bool | None
    prev: list[PatternStep] | None
    next: list[PatternStep] | None
    form_id: int | None
    form: StepForm | None


class PatternStepUpdate(BaseModel):
    pattern_id: int
    name: str
    description: str | None
    category: str
    is_active: bool
    prev: list[PatternStep]
    next: list[PatternStep]
    form_id: int | None
    form: StepForm | None
