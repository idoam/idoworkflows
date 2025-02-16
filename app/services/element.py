from datetime import datetime

from fastapi import HTTPException, status
from models import Element, ElementStatus
from pydantic import ValidationError
from schemas.element import *
from sqlmodel import Session


class ElementService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create_element(
        self,
        element_create: ElementCreate,
    ) -> ElementPublic:
        element = Element(
            instance_id=element_create.instance_id,
            node_id=element_create.node_id,
            updated_by="fixme_get_user",
            updated_at=datetime.now(),
        )
        self.session.add(element)
        self.session.commit()
        self.session.refresh(element)
        return element

    def get_element(self, element_id: int) -> ElementPublic:
        element: Element | None = self.session.get(Element, element_id)
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Element not found"
            )
        return element

    def partial_update_element(
        self,
        element_id: int,
        element_partial_update: ElementPartialUpdate,
    ) -> ElementPublic:
        element: Element | None = self.session.get(Element, element_id)
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Element not found"
            )
        element_node = element.get_node()

        # Validate dataform
        node_dataform: BaseModel | None = element_node.dataform_model
        if not node_dataform and element_partial_update.dataform is not None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Must not provide dataform for this element",
            )
        if element_partial_update.dataform:
            try:
                node_dataform.model_validate(element_partial_update.dataform)
            except ValidationError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dataform does not match",
                )

        # Validate status
        if update_status := element_partial_update.status:
            try:
                ElementStatus(update_status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{update_status} is not a valid element status",
                )

        old_status = element.status
        element_patch_data = element_partial_update.model_dump(exclude_unset=True)
        element.sqlmodel_update(element_patch_data)
        self.session.commit()
        self.session.refresh(element)

        # Trigger on_ hooks
        for hook in element_node.hooks:
            if element_partial_update.status != old_status:
                hook(element=element).on_status_change()

        self.session.refresh(element)
        return element

    def delete_element(
        self,
        element_id: int,
    ) -> None:
        element: Element | None = self.session.get(Element, element_id)
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Element not found"
            )
        self.session.delete(element)
        self.session.commit()
