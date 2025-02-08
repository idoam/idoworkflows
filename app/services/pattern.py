from fastapi import HTTPException, status
from models import WorkflowPattern
from schemas.pattern import *
from sqlmodel import Session, func, select


class PatternService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create_pattern(
        self,
        pattern_create: WorkflowPatternCreate,
    ) -> WorkflowPattern:
        pattern = WorkflowPattern(
            name=pattern_create.name,
            description=pattern_create.description,
            is_active=pattern_create.is_active,
        )
        self.session.add(pattern)
        self.session.commit()
        self.session.refresh(pattern)
        return pattern

    def get_patterns(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> GetWorkflowPatternsResponse:
        patterns = self.session.exec(
            select(WorkflowPattern).offset(offset).limit(limit)
        ).all()
        count = self.session.exec(select(func.count(WorkflowPattern.id))).one()
        return {"count": count, "patterns": patterns}
        # return GetPatternsResponse(count=count, patterns=patterns)

    def get_pattern(self, pattern_id: int) -> WorkflowPatternPublic:
        pattern: WorkflowPattern | None = self.session.get(WorkflowPattern, pattern_id)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
            )
        return pattern

    def partial_update_pattern(
        self,
        pattern_id: int,
        pattern_partial_update: WorkflowPatternPartialUpdate,
    ) -> WorkflowPatternPublic:
        pattern: WorkflowPattern | None = self.session.get(WorkflowPattern, pattern_id)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
            )
        pattern_patch_data = pattern_partial_update.model_dump(exclude_unset=True)
        pattern.sqlmodel_update(pattern_patch_data)
        self.session.commit()
        self.session.refresh(pattern)
        return pattern

    def update_pattern(
        self,
        pattern_id: int,
        pattern_update: WorkflowPatternUpdate,
    ) -> WorkflowPatternPublic:
        pattern: WorkflowPattern | None = self.session.get(WorkflowPattern, pattern_id)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
            )
        pattern_update__data = pattern_update.model_dump()
        pattern.sqlmodel_update(pattern_update__data)
        self.session.commit()
        self.session.refresh(pattern)
        return pattern

    def delete_pattern(
        self,
        pattern_id: int,
    ) -> None:
        pattern: WorkflowPattern | None = self.session.get(WorkflowPattern, pattern_id)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
            )
        self.session.delete(pattern)
        self.session.commit()
