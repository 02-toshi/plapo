"""リポジトリのテスト"""
from datetime import datetime

import pytest

from src.model import Member, Room
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
        putter(
            {
                "room_id": "abcdef",
                "mem_1000000001": {"nickname": "ななし１", "point": 5},
                "mem_1000000002": {"nickname": "ななし２", "point": 1},
                "mem_1000000003": {"nickname": "ななし３"},
                "opened": False,
            }
        )
        actual = sut.query_room("abcdef")
        assert actual.room_id == "abcdef"
        assert actual.opened is False
        assert len(actual.members) == 3
        assert (
                Member(member_id="1000000001", nickname="ななし１", point=5)
                in actual.members
        )
        assert (
                Member(member_id="1000000002", nickname="ななし２", point=1)
                in actual.members
        )
        assert (
                Member(member_id="1000000003", nickname="ななし３") in actual.members
        )

    def test_query_room_dbが空の場合はNoneが返る(self, sut):
        actual = sut.query_room("abcdef")
        assert actual is None

    def test_initialize_room_部屋を建てる(self, sut, getter):
        room = Room(room_id="abcdef")

        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)
        sut.initialize_room(room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }

    def test_initialize_room_部屋を初期化する(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "mem_1000000001": {"nickname": "ななし１", "point": 5},
                "mem_1000000002": {"nickname": "ななし２", "point": 1},
                "mem_1000000003": {"nickname": "ななし３", "point": 3},
                "opened": True,
            }
        )
        room = Room(room_id="abcdef")
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.initialize_room(room, now)

        actual = getter("abcdef")

        assert actual["opened"] is False
        assert actual["mem_1000000001"] == {"nickname": "ななし１"}
        assert actual["mem_1000000002"] == {"nickname": "ななし２"}
        assert actual["mem_1000000003"] == {"nickname": "ななし３"}
        assert actual["ttl"] == int(tomorrow.strftime("%s"))

    def test_act_member_部屋に参加する(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "opened": False,
            }
        )
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1")
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.act_member(member, room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }

    def test_act_member_部屋に参加する_2人目(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "mem_2000000001": {"nickname": "test_name1"},
                "opened": False,
            }
        )
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000002", nickname="test_name2")
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.act_member(member, room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1"},
            "mem_2000000002": {"nickname": "test_name2"},
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }

    def test_act_member_ニックネーム変更(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "mem_2000000001": {"nickname": "test_name1"},
                "opened": False,
            }
        )
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name2")
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.act_member(member, room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name2"},
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }

    def test_act_member_投票(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "mem_2000000001": {"nickname": "test_name1"},
                "opened": False,
            }
        )
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1", point=5)
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.act_member(member, room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1", "point": 5},
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }

    def test_act_member_投票_変更(self, sut, getter, putter):
        putter(
            {
                "room_id": "abcdef",
                "mem_2000000001": {"nickname": "test_name1", "point": 5},
                "opened": False,
            }
        )
        room = Room(room_id="abcdef")
        member = Member(member_id="2000000001", nickname="test_name1", point=8)
        now = datetime(2020, 11, 22, 0, 0, 0)
        tomorrow = datetime(2020, 11, 23, 0, 0, 0)

        sut.act_member(member, room, now)

        actual = getter("abcdef")
        assert actual == {
            "room_id": "abcdef",
            "mem_2000000001": {"nickname": "test_name1", "point": 8},
            "opened": False,
            "ttl": int(tomorrow.strftime("%s")),
        }
