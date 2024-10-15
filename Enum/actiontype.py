from enum import Enum
class ActionType(Enum):
    LOGIN=1
    START_RECORD = 2
    STOP_RECORD = 3
    OPEN_RECORD=4,
    START_MEETING=5,
    STOP_MEETING=6,
    DISCUSS_REQUEST=7