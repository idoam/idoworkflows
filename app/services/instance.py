from datetime import datetime

from fastapi import HTTPException, status
from models import Instance
from schemas.element import ElementCreate
from schemas.instance import *
from services.element import ElementService
from sqlmodel import Session, func, select


class InstanceService:
    session: Session
    elementService: ElementService

    def __init__(self, session: Session):
        self.session = session
        self.elementService = ElementService(session)

    def create_instance(
        self,
        instance_create: InstanceCreate,
    ) -> InstancePublicUnrolled:
        date_now: datetime = datetime.now()
        instance = Instance(
            workflow_id=instance_create.workflow_id,
            created_by="fixme_get_user",
            created_at=date_now,
            updated_by="fixme_get_user",
            updated_at=date_now,
        )
        workflow = instance.get_workflow()
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"Workflow {instance.workflow_id} not found",
            )
        self.session.add(instance)
        self.session.commit()
        for node in workflow.get_initial_nodes():
            self.elementService.create_element(
                ElementCreate(instance_id=instance.id, node_id=node.id)
            )
        self.session.refresh(instance)
        return instance

    def get_instances(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> GetInstancesResponse:
        instances = self.session.exec(
            select(Instance).offset(offset).limit(limit)
        ).all()
        count = self.session.exec(select(func.count(Instance.id))).one()
        return {"count": count, "instances": instances}

    def get_instance(self, instance_id: int) -> InstancePublicUnrolled:
        instance: Instance | None = self.session.get(Instance, instance_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found"
            )
        return instance

    def partial_update_instance(
        self,
        instance_id: int,
        instance_partial_update: InstancePartialUpdate,
    ) -> InstancePublic:
        instance: Instance | None = self.session.get(Instance, instance_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found"
            )
        instance_patch_data = instance_partial_update.model_dump(exclude_unset=True)
        instance.sqlmodel_update(instance_patch_data)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete_instance(
        self,
        instance_id: int,
    ) -> None:
        instance: Instance | None = self.session.get(Instance, instance_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found"
            )
        self.session.delete(instance)
        self.session.commit()
