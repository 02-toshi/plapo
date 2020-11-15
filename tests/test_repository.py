"""リポジトリのテスト"""

import pytest

from src.model import Room
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
        print(actual)
