from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class WorkflowPattern(SQLModel, table=True):
    """
    brief: A pattern of a workflow. Users should be able to create instances of this pattern.
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    is_active: bool = Field(default=True)
    nodes: list["patternnode"] = Relationship(back_populates="workflow_pattern")


class PatternEdgeTrigger(str, Enum):
    auto = "auto"  # Unlocks `next` on prev validation status.
    on_choice = (
        "on_choice"  # Like `auto`, if user chose this path from all possible edges.
    )


class PatternEdge(SQLModel, table=True):
    """
    brief: Links PatternNodes to create a dependency graph.
    """

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
    is_active: bool = Field(default=True)

    prev: list["patternnode"] = Relationship(
        link_model=PatternEdge,
        back_populates="next",
        sa_relationship_kwargs=dict(
            primaryjoin="patternnode.id==patternedge.next_id",
            secondaryjoin="patternnode.id==patternedge.prev_id",
        ),
    )
    next: list["patternnode"] = Relationship(
        link_model=PatternEdge,
        back_populates="prev",
        sa_relationship_kwargs=dict(
            primaryjoin="patternnode.id==patternedge.prev_id",
            secondaryjoin="patternnode.id==patternedge.next_id",
        ),
    )

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
