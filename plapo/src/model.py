"""モデル定義"""
from dataclasses import dataclass


@dataclass
class Room:
    room_id: str
    opened: bool
    ttl: int


@dataclass()
class Member:
    member_id: str
    room_id: str
    point: int
    nickname: str
    ttl: int
