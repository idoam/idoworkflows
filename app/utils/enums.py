from enum import Enum

"""
desc: Contains util enums. Always reference associated fields via the enum instead of via plain string.
      In database, fields are typed str because SQLAlchemy does not support db agnostic enums.
"""


class EdgeTrigger(str, Enum):
    auto = "auto"
    on_choice = "on_choice"


class ElementStatus(str, Enum):
    ongoing = "ongoing"
    completed = "completed"
    validated = "validated"
    archived = "archived"

    @staticmethod
    def is_legal_transition(from_status, to_status):
        status = ElementStatus
        allowed_transitions = {
            status.ongoing: [status.completed, status.archived],
            status.completed: [status.ongoing, status.validated, status.archived],
            status.validated: [status.archived],
            status.archived: [],
        }
        return from_status == to_status or to_status in allowed_transitions[from_status]
