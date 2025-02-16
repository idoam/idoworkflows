from datetime import datetime
from enum import Enum

from pydantic import BaseModel
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


class ElementStatus(str, Enum):
    ongoing = "ongoing"
    completed = "completed"
    validated = "validated"
    archived = "archived"


class Element(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    instance_id: int | None = Field(default=None, foreign_key="instance.id")
    instance: Instance | None = Relationship(back_populates="elements")
    node_id: int

    status: str = ElementStatus.ongoing
    updated_at: datetime
    updated_by: str

    dataform: dict | None = Field(sa_column=Column(JSON), default_factory=dict)

    def get_node(self):
        return self.instance.get_workflow().get_node(self.node_id)


class HookBase(BaseModel):
    element: Element

    def on_status_change(self):
        if self.element.status == ElementStatus.ongoing:
            return self.on_ongoing()
        elif self.element.status == ElementStatus.completed:
            return self.on_completed()
        elif self.element.status == ElementStatus.validated:
            return self.on_validated()
        elif self.element.status == ElementStatus.archived:
            return self.on_archived()

    def on_ongoing(self):
        pass

    def on_completed(self):
        pass

    def on_validated(self):
        pass

    def on_archived(self):
        pass
