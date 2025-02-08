from datetime import datetime
from enum import Enum

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from .pattern import PatternNode, WorkflowPattern


class WorkflowInstance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    workflow_pattern_id: int | None = Field(
        default=None,
        foreign_key="workflowpattern.id",
    )
    workflow_pattern: WorkflowPattern | None = Relationship(back_populates="nodes")

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    elements: list["InstanceElement"] = Relationship(back_populates="workflow_instance")


class InstanceElementStatus(str, Enum):
    blocked = "blocked"
    ongoing = "ongoing"
    completed = "completed"
    validated = "validated"
    archived = "archived"


class InstanceElement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    workflow_instance_id: int | None = Field(
        default=None,
        foreign_key="workflowinstance.id",
    )
    workflow_instance: WorkflowInstance | None = Relationship(back_populates="elements")
    pattern_node_id: int | None = Field(
        default=None,
        foreign_key="patternnode.id",
    )
    pattern_node: PatternNode | None = Relationship(back_populates="elements")

    updated_at: datetime
    updated_by: str

    dataform: dict = Field(sa_column=Column(JSON), default_factory=dict)
    # `dataform` implements the pattern_node's `dataform_pydantic` model.
