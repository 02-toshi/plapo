"""リポジトリのテスト"""
import unittest

import boto3

from src.repository import PlapoRepository

table_name = "plapo"
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


class TestPlapoRepository(unittest.TestCase):
    def test_query_room(self):
        # クエリするためのroomをまずdynamoに登録する
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

        # 登録したroomをクエリする
        # ↓こいつ書かないと詰む!!!!!!!!!!
        plapo = PlapoRepository()
        room_id: str = "123456"
        room = PlapoRepository.query_room(plapo, room_id)
        # assert room.

    # def test_(self):
