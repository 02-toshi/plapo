"""リポジトリのテスト"""

import pytest

from src.model import Room, Member
from src.repository import RoomRepository


class TestRoomRepository:
    @pytest.fixture
    def sut(self, dynamodb):
        return RoomRepository()

    def test_query_room(self, sut):
        actual = sut.query_room("123456")
        print(actual)

    def test_initialize_room_部屋を建てる(self, sut, table):
        room = Room(room_id="abcdef")
        sut.initialize_room(room)
        actual = table.get_item(Key={"room_id": "abcdef"}).get("Item")

        assert actual is not None
        print("actual=" + str(actual))

    def test_upsert_room_部屋に参加する(self, sut, table):
        room = Room(room_id="abcdef")
        member = Member(member_id="test_member", nickname="test_name")
        sut.initialize_room(room)
        sut.upsert_room(member, room)
        actual = table.get_item(Key={"room_id": "abcdef"}).get("Item")
        print("actual" + str(actual))
        assert actual is not None

    def test_upsert_room_見積もりポイントを登録する(self, sut, table):
        room = Room(room_id="abcdef")
        member = Member(member_id="test_member", nickname="test_name", point=5)
        sut.initialize_room(room)
        sut.upsert_room(member, room)
        actual = table.get_item(Key={"room_id": "abcdef"}).get("Item")
        print("actual" + str(actual))
        assert actual is not None

    def test_upsert_room_複数人が同時に見積もりポイントを登録する(self, sut, table):
        room = Room(room_id="abcdef")
        member1 = Member(member_id="test_member2", nickname="test_name2", point=5)
        member2 = Member(member_id="test_member3", nickname="test_name3", point=3)

        sut.initialize_room(room)
        sut.upsert_room(member1, room)
        sut.upsert_room(member2, room)
        actual = table.get_item(Key={"room_id": "abcdef"}).get("Item")
        print("actual" + str(actual))
        assert actual is not None
