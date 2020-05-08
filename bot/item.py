from dataclasses import dataclass
from uuid import uuid4


@dataclass
class RestockedItem:
    title: str
    description: str
    dt: str
    image: str
