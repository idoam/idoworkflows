from fastapi import HTTPException, status
from models import PatternEdge
from schemas.pattern_edge import *
from sqlmodel import Session, func, select


class PatternEdgeService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create_pattern_edge(
        self,
        pattern_edge_create: PatternEdgeCreate,
    ) -> PatternEdgePublic:
        pattern_edge = PatternEdge(
            prev_id=pattern_edge_create.prev_id,
            next_id=pattern_edge_create.next_id,
            trigger=pattern_edge_create.trigger,
        )
        self.session.add(pattern_edge)
        self.session.commit()
        self.session.refresh(pattern_edge)
        return pattern_edge

    def get_pattern_edges(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> GetPatternEdgesResponse:
        pattern_edges = self.session.exec(
            select(PatternEdge).offset(offset).limit(limit)
        ).all()
        count = self.session.exec(select(func.count(PatternEdge.id))).one()
        return {"count": count, "pattern_edges": pattern_edges}

    def get_pattern_edge(self, pattern_edge_id: int) -> PatternEdgePublic:
        pattern_edge: PatternEdge | None = self.session.get(
            PatternEdge, pattern_edge_id
        )
        if not pattern_edge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Edge not found"
            )
        return pattern_edge

    def partial_update_pattern_edge(
        self,
        pattern_edge_id: int,
        pattern_edge_partial_update: PatternEdgePartialUpdate,
    ) -> PatternEdgePublic:
        pattern_edge: PatternEdge | None = self.session.get(
            PatternEdge, pattern_edge_id
        )
        if not pattern_edge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Edge not found"
            )
        pattern_patch_data = pattern_edge_partial_update.model_dump(exclude_unset=True)
        pattern_edge.sqlmodel_update(pattern_patch_data)
        self.session.commit()
        self.session.refresh(pattern_edge)
        return pattern_edge

    def update_pattern_edge(
        self,
        pattern_edge_id: int,
        pattern_edge_update: PatternEdgePublic,
    ) -> PatternEdgePublic:
        pattern_edge: PatternEdge | None = self.session.get(
            PatternEdge, pattern_edge_id
        )
        if not pattern_edge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Edge not found"
            )
        pattern_update__data = pattern_edge_update.model_dump()
        pattern_edge.sqlmodel_update(pattern_update__data)
        self.session.commit()
        self.session.refresh(pattern_edge)
        return pattern_edge

    def delete_pattern_edge(
        self,
        pattern_edge_id: int,
    ) -> None:
        pattern_edge: PatternEdge | None = self.session.get(
            PatternEdge, pattern_edge_id
        )
        if not pattern_edge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Edge not found"
            )
        self.session.delete(pattern_edge)
        self.session.commit()
