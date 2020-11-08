"""リポジトリのテスト"""
import unittest

import boto3
import pytest

from src.repository import PlapoRepository

table_name = "plapo"
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


class TestPlapoRepository(unittest.TestCase):
    @pytest.fixture
    def create_new_room(self):
        dynamodb.table = dynamodb.Table(table_name)
        record_id = "12345678901234567890123456789012"
        room_id = "123456"

        dynamodb.table.put_item(Item={
            "record_id": record_id,
            "room_id": room_id,
            "opened": True,
            # TODO: ttlの値をいい感じにする
            "ttl": 0
        })
        return

    def test_query_room(self):
        # ↓こいつ書かないと詰む!!!!!!!!!!
        plapo = PlapoRepository()
        room_id: str = "123456"
        PlapoRepository.query_room(plapo, room_id)
