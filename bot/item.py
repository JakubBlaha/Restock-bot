from dataclasses import dataclass
from uuid import uuid4


@dataclass
class RestockedItem:
    title: str
    id: str = None
    
    def __post_init__(self):
        if not self.id:
            self.id = uuid4().hex