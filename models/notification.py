from dataclasses import dataclass

@dataclass
class Notification:
    user_id: int
    time: str       # пример: "08:30"
    mode: str       # daily | weekdays | weekends
