from models import Element
from pydantic import BaseModel
from utils.enums import ElementStatus

"""
desc: Contains base models to enforce strong typing and ensure model method definitions.
"""


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


class DataFormBase(BaseModel):
    pass
