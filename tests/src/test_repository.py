"""リポジトリのテスト"""

import pytest

from src.model import Room, Member
from src.repository import RoomRepository


class TestRoomRepository:

    @pytest.fixture
    def sut(self, dynamodb):
        return RoomRepository()

    @pytest.fixture
    def getter(self, table):
        return lambda x: table.get_item(Key={"room_id": x}).get("Item")

    @pytest.fixture
    def putter(self, table):
        return lambda x: table.put_item(Item=x)

    def test_query_room_dbから取得できる(self, sut, putter):
        putter({
            "room_id": "abcdef",
            "mem_1000000001": {"nickname": "ななし１", "point": 5},
            "mem_1000000002": {"nickname": "ななし２", "point": 1},
            "mem_1000000003": {"nickname": "ななし３"},
            "opened": False,
        })

        actual = sut.query_room("abcdef")

        assert actual.room_id == "abcdef"
        assert actual.opened is False
        assert set(actual.members) == {
            Member(member_id="1000000001", nickname="ななし１", point=5),
            Member(member_id="1000000002", nickname="ななし２", point=5),
            Member(member_id="1000000003", nickname="ななし３"),
        }

    def test_initialize_room_部屋を建てる(self, sut, getter):
        room = Room(room_id="abcdef")

        sut.initialize_room(room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef"
        }

    def test_initialize_room_部屋を初期化する(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "mem_1000000001": {"nickname": "ななし１", "point": 5},
            "mem_1000000002": {"nickname": "ななし２", "point": 1},
            "mem_1000000003": {"nickname": "ななし３", "point": 3},
            "opened": True,
        })
        room = Room(room_id="abcdef")

        sut.initialize_room(room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_1000000001": {"nickname": "ななし１"},
            "mem_1000000002": {"nickname": "ななし２"},
            "mem_1000000003": {"nickname": "ななし３"},
            "opened": False,
        }

    def test_act_member_部屋に参加する(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "opened": False,
        })
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1")

        sut.act_member(member, room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "opened": False,
        }

    def test_act_member_部屋に参加する_2人目(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "opened": False,
        })
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000002", nickname="test_name2")

        sut.act_member(member, room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "mem_2000000002": {"nickname": "test_name2"},
            "opened": False,
        }

    def test_act_member_ニックネーム変更(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "opened": False,
        })
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name2")

        sut.act_member(member, room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name2"},
            "opened": False,
        }

    def test_act_member_投票(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "opened": False,
        })
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1", point=5)

        sut.act_member(member, room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1", "point": 5},
            "opened": False,
        }

    def test_act_member_投票_変更(self, sut, getter, putter):
        putter({
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1", "point": 5},
            "opened": False,
        })
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1", point=8)

        sut.act_member(member, room)

        actual = getter("abcdef")
        del actual["ttl"]   # TODO 検証する
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1", "point": 8},
            "opened": False,
        }
