from datetime import datetime
from enum import Enum

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Instance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    workflow_id: int

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    elements: list["Element"] = Relationship(back_populates="instance")

    def get_workflow(self):
        from workflows import workflows

        return workflows[self.workflow_id] if self.workflow_id in workflows else None


class ElementEdge(SQLModel, table=True):
    """
    brief: Links Elements.
    """

    id: int = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
    )
    prev_id: int | None = Field(
        default=None,
        foreign_key="element.id",
        primary_key=True,
    )
    next_id: int | None = Field(
        default=None,
        foreign_key="element.id",
        primary_key=True,
    )
    trigger: str = "auto"


class ElementStatus(str, Enum):
    ongoing = "ongoing"
    completed = "completed"
    validated = "validated"
    archived = "archived"

    @staticmethod
    def is_legal_transition(from_status, to_status):
        status = ElementStatus
        allowed_transitions = {
            status.ongoing: [status.completed, status.archived],
            status.completed: [status.ongoing, status.validated, status.archived],
            status.validated: [status.archived],
            status.archived: [],
        }
        return from_status == to_status or to_status in allowed_transitions[from_status]


class Element(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    instance_id: int | None = Field(default=None, foreign_key="instance.id")
    instance: Instance | None = Relationship(back_populates="elements")
    node_id: int

    status: str = ElementStatus.ongoing
    updated_at: datetime
    updated_by: str

    dataform: dict | None = Field(sa_column=Column(JSON), default_factory=dict)

    prev: list["Element"] = Relationship(
        link_model=ElementEdge,
        back_populates="next",
        sa_relationship_kwargs=dict(
            primaryjoin="Element.id==ElementEdge.next_id",
            secondaryjoin="Element.id==ElementEdge.prev_id",
        ),
    )
    next: list["Element"] = Relationship(
        link_model=ElementEdge,
        back_populates="prev",
        sa_relationship_kwargs=dict(
            primaryjoin="Element.id==ElementEdge.prev_id",
            secondaryjoin="Element.id==ElementEdge.next_id",
        ),
    )

    def get_node(self):
        return self.instance.get_workflow().get_node(self.node_id)
