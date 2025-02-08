from fastapi import HTTPException, status
from models import PatternNode
from schemas.pattern_node import *
from sqlmodel import Session, func, select


class PatternNodeService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create_pattern_node(
        self,
        pattern_node_create: PatternNodeCreate,
    ) -> PatternNodePublic:
        pattern_node = PatternNode(
            name=pattern_node_create.name,
            description=pattern_node_create.description,
            is_active=pattern_node_create.is_active,
            workflow_pattern_id=pattern_node_create.workflow_pattern_id,
            category=pattern_node_create.category,
            dataform_pydantic_str=pattern_node_create.dataform_pydantic_str,
        )
        self.session.add(pattern_node)
        self.session.commit()
        self.session.refresh(pattern_node)
        return pattern_node

    def get_pattern_nodes(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> GetPatternNodesResponse:
        pattern_nodes = self.session.exec(
            select(PatternNode).offset(offset).limit(limit)
        ).all()
        count = self.session.exec(select(func.count(PatternNode.id))).one()
        return {"count": count, "pattern_nodes": pattern_nodes}
        # return GetPatternsResponse(count=count, patterns=patterns)

    def get_pattern_node(self, pattern_node_id: int) -> PatternNodePublic:
        pattern_node: PatternNode | None = self.session.get(
            PatternNode, pattern_node_id
        )
        if not pattern_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Node not found"
            )
        return pattern_node

    def partial_update_pattern_node(
        self,
        pattern_node_id: int,
        pattern_node_partial_update: PatternNodePartialUpdate,
    ) -> PatternNodePublic:
        pattern_node: PatternNode | None = self.session.get(
            PatternNode, pattern_node_id
        )
        if not pattern_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Node not found"
            )
        pattern_patch_data = pattern_node_partial_update.model_dump(exclude_unset=True)
        pattern_node.sqlmodel_update(pattern_patch_data)
        self.session.commit()
        self.session.refresh(pattern_node)
        return pattern_node

    def update_pattern_node(
        self,
        pattern_node_id: int,
        pattern_node_update: PatternNodeUpdate,
    ) -> PatternNodePublic:
        pattern_node: PatternNode | None = self.session.get(
            PatternNode, pattern_node_id
        )
        if not pattern_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Node not found"
            )
        pattern_update__data = pattern_node_update.model_dump()
        pattern_node.sqlmodel_update(pattern_update__data)
        self.session.commit()
        self.session.refresh(pattern_node)
        return pattern_node

    def delete_pattern_node(
        self,
        pattern_node_id: int,
    ) -> None:
        pattern_node: PatternNode | None = self.session.get(
            PatternNode, pattern_node_id
        )
        if not pattern_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pattern Node not found"
            )
        self.session.delete(pattern_node)
        self.session.commit()
