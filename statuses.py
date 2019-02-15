# Available task statuses enumeration

from enum import Enum


class Status(Enum):
    IN_QUEUE = 1
    RUN = 2
    COMPLETED = 3
