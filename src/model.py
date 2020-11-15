"""モデル定義"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Member:
    member_id: str
    nickname: str
    point: Optional[int] = 0


@dataclass
class Room:
    room_id: str
    opened: bool = False
    members: List[Member] = field(default_factory=list)
