"""モデル定義"""
from dataclasses import dataclass

import arrow as arrow
from numpy.core import number


@dataclass
class Room:
    room_id: str
    opened: bool
    point: int
    ttl: number


@dataclass()
class Session:
    session_id: str
    room_id: str
    nickname: str
    ttl: number


@dataclass()
class Planning:
    # PK
    session_id: str
    story_pt: int
    register_datetime: arrow
    # 何回目の見積もりかを表すインクリメントを想定（物理削除するならいらない）
    # index: int
    # del_flg: bool
    ttl: number
