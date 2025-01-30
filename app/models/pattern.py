from enum import Enum

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Pattern(SQLModel, table=True):
    """
    brief: A pattern of a workflow. Users should be able to create instances of this pattern - workflows.
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    is_active: bool = Field(default=True)

    steps: list["PatternStep"] = Relationship(back_populates="pattern")
    instances: list["Instance"] = Relationship(back_populates="pattern")


class StepEdge(SQLModel, table=True):
    """
    brief: Links PatternSteps to create a dependency graph.
    """

    prev_id: int | None = Field(
        default=None,
        foreign_key="patternstep.id",
        primary_key=True,
    )
    next_id: int | None = Field(
        default=None,
        foreign_key="patternstep.id",
        primary_key=True,
    )


class StepForm(SQLModel, table=True):
    """
    brief: Form associated with a step.
    """

    id: int = Field(default=None, primary_key=True)
    steps: list["PatternStep"] = Relationship(back_populates="form")
    fields: list["FormField"] = Relationship(back_populates="step_form")


class BaseFieldEntryType(str, Enum):
    boolean = "boolean"
    text = "text"
    number = "number"
    date = "date"
    unique_choice = "unique_choice"
    multiple_choice = "multiple_choice"


class FormField(SQLModel, table=True):
    """
    brief: Fields of a step's form.
    """

    id: int = Field(default=None, primary_key=True)
    step_form_id: int | None = Field(default=None, foreign_key="stepform.id")
    step_form: StepForm | None = Relationship(back_populates="fields")
    label: str
    description: str | None = None
    is_required: bool = False
    entry_type: str = BaseFieldEntryType.boolean
    entry_props: dict = Field(sa_column=Column(JSON), default_factory=dict)


class PatternStep(SQLModel, table=True):
    """
    brief: Step of a workflow pattern.
    """

    id: int = Field(default=None, primary_key=True)
    pattern_id: int | None = Field(default=None, foreign_key="pattern.id")
    pattern: Pattern | None = Relationship(back_populates="steps")

    name: str
    description: str | None = None
    category: str
    is_active: bool = Field(default=True)

    prev: list["PatternStep"] = Relationship(
        link_model=StepEdge,
        back_populates="next",
        sa_relationship_kwargs=dict(
            primaryjoin="patternstep.id==stepedge.next_id",
            secondaryjoin="patternstep.id==stepedge.prev_id",
        ),
    )
    next: list["PatternStep"] = Relationship(
        link_model=StepEdge,
        back_populates="prev",
        sa_relationship_kwargs=dict(
            primaryjoin="patternstep.id==stepedge.prev_id",
            secondaryjoin="patternstep.id==stepedge.next_id",
        ),
    )

    form_id: int | None = Field(default=None, foreign_key="stepform.id")
    form: StepForm | None = Relationship(back_populates="steps")
