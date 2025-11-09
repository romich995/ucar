import enum

class IncidentStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in progress"
    CLOSED = "closed"

class IncidentSource(enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
