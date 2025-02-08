from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class WorkflowPattern(SQLModel, table=True):
    """
    brief: A pattern of a workflow. Users should be able to create instances of this pattern.
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    is_active: bool = True
    nodes: list["PatternNode"] = Relationship(back_populates="workflow_pattern")
    instances: list["WorkflowInstance"] = Relationship(
        back_populates="workflow_pattern"
    )


class PatternEdgeTrigger(str, Enum):
    auto = "auto"  # Unlocks `next` on prev validation status.
    on_choice = (
        "on_choice"  # Like `auto`, if user chose this path from all possible edges.
    )


class PatternEdge(SQLModel, table=True):
    """
    brief: Links PatternNodes to create a dependency graph.
    """

    id: int = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
    )
    prev_id: int | None = Field(
        default=None,
        foreign_key="patternnode.id",
        primary_key=True,
    )
    next_id: int | None = Field(
        default=None,
        foreign_key="patternnode.id",
        primary_key=True,
    )
    trigger: str = PatternEdgeTrigger.auto


class PatternNode(SQLModel, table=True):
    """
    brief: Step of a workflow pattern.
    """

    id: int = Field(default=None, primary_key=True)
    workflow_pattern_id: int | None = Field(
        default=None,
        foreign_key="workflowpattern.id",
    )
    workflow_pattern: WorkflowPattern | None = Relationship(back_populates="nodes")

    name: str
    description: str | None = None
    category: str
    is_active: bool = True

    prev: list["PatternNode"] = Relationship(
        link_model=PatternEdge,
        back_populates="next",
        sa_relationship_kwargs=dict(
            primaryjoin="PatternNode.id==PatternEdge.next_id",
            secondaryjoin="PatternNode.id==PatternEdge.prev_id",
        ),
    )
    next: list["PatternNode"] = Relationship(
        link_model=PatternEdge,
        back_populates="prev",
        sa_relationship_kwargs=dict(
            primaryjoin="PatternNode.id==PatternEdge.prev_id",
            secondaryjoin="PatternNode.id==PatternEdge.next_id",
        ),
    )
    # /!\ In joins, use pascal case for tables, because it's at the ORM/python level

    dataform_pydantic_str: str
    # `dataform_pydantic_str` corresponds to an existing pydantic BaseModel which
    # should be used for data serialization on this node.
    # /!\ This is extremely unsafe as we are manipulating objects as strings
    #
    # Example:
    # > class UserDataForm(BaseModel):
    # >     first_name: str
    # >     last_name: str

    elements: list["InstanceElement"] = Relationship(back_populates="pattern_node")
