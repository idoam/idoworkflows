from enum import Enum

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from .pattern import Pattern, PatternStep


class Instance(SQLModel, table=True):
    """
    brief: An instance of a workflow pattern.
    """

    id: int = Field(default=None, primary_key=True)
    pattern_id: int | None = Field(default=None, foreign_key="pattern.id")
    pattern: Pattern | None = Relationship(back_populates="instances")

    steps: list["StepInstance"] = Relationship(back_populates="instance_id")


class StepStatus(str, Enum):
    blocked = "blocked"
    ongoing = "ongoing"
    completed = "completed"
    validated = "validated"


class StepInstance(SQLModel, table=True):
    """
    brief: An instance of a step. Contains end-data.
    """

    id: int = Field(default=None, primary_key=True)
    instance_id: int | None = Field(default=None, foreign_key="instance.id")
    instance: Instance | None = Relationship(back_populates="steps")

    pattern_step_id: int | None = Field(default=None, foreign_key="patternstep.id")
    pattern_step: PatternStep | None = Relationship(back_populates="instances")

    status: str = StepStatus.blocked
    data: dict = Field(sa_column=Column(JSON), default_factory=dict)
