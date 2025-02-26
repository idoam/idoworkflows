from datetime import datetime

from fastapi import HTTPException, status
from models import (
    DataFormBase,
    Element,
    ElementEdge,
    ElementStatus,
    Instance,
    Node,
    Workflow,
    is_legal_transition,
)
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

    def create_element_edge(
        self,
        element_edge_create: ElementEdgeCreate,
    ) -> ElementPublic:
        element_edge = ElementEdge(
            prev_id=element_edge_create.prev_id,
            next_id=element_edge_create.next_id,
        )
        self.session.add(element_edge)
        self.session.commit()
        self.session.refresh(element_edge)
        return element_edge

    def get_element(self, element_id: int) -> ElementPublicUnrolled:
        element: Element | None = self.session.get(Element, element_id)
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Element not found"
            )
        return element

    @staticmethod
    def check_dataform(
        dataform_model: type[DataFormBase] | None,
        dataform: type[DataFormBase] | None,
    ):
        if not dataform_model:
            if not dataform:
                return
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unexpected dataform field. This element does not implement a data node.",
            )
        try:
            dataform_model.model_validate(dataform)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provided dataform does not match with element's dataform_model.",
            )

    @staticmethod
    def check_status(
        base_status: str,
        update_status: str | None,
    ):
        if update_status := update_status:
            try:
                ElementStatus(update_status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{update_status} is not a valid element status",
                )
            if not ElementStatus.is_legal_transition(base_status, update_status):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Illegal transition from {update_status} to {base_status}",
                )

    def partial_update_element(
        self,
        element_id: int,
        element_update: ElementPartialUpdate,
    ) -> ElementPublic:
        element: Element | None = self.session.get(Element, element_id)
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Element #{element_id} not found",
            )
        element_node: Node = element.get_node()

        # Validate update data
        self.check_dataform(element_node.dataform_model, element_update.dataform)
        self.check_status(element.status, element_update.status)

        old_status = element.status
        element_patch_data = element_update.model_dump(exclude_unset=True)
        element.sqlmodel_update(element_patch_data)
        self.session.commit()
        self.session.refresh(element)

        # If status changed upon this patch
        if element_update.status != old_status:
            # Trigger on_ hooks
            for hook in element_node.hooks:
                hook(element=element).on_status_change()

            # If the new status is validated
            if element.status == ElementStatus.validated:
                # FIXME Archive previously instantiated next elements

                # Generate auto-next elements
                for n in element_node.get_workflow().get_next_nodes(element_node.id):
                    next_element = self.create_element(
                        ElementCreate(node_id=n.id, instance_id=element.instance.id)
                    )
                    self.create_element_edge(
                        ElementEdgeCreate(prev_id=element.id, next_id=next_element.id)
                    )
                # FIXME Generate condition-based-next elements

            # If the new status is archived
            elif element.status == ElementStatus.archived:
                # Archive auto-next elements
                for n in element.next:
                    self.partial_update_element(
                        n.id, ElementPartialUpdate(status=ElementStatus.archived)
                    )
                # FIXME Archive condition-based-next elements

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
