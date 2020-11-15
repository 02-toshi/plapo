from typing import Optional

import boto3

from src.model import Member, Room

table_name = "plapo"


class RoomRepository:
    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(table_name)

    def query_room(self, room_id: str) -> Optional[Room]:
        """
        指定したidの部屋が存在すれば返す
        :param room_id:
        :return: 指定したidの部屋が存在すれば返す
        """
        res = self.table.get_item(Key={"room_id": room_id}).get("Item")

        return res

    def initialize_room(self, room: Room) -> Room:
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param room: 部屋
        :return:
        """
        self.table.put_item(
            Item={
                "room_id": room.room_id,
                # TODO: ttlの値をいい感じにする
                "ttl": 0,
            },
        )
        return room

    def vote(self, member: Member, room: Room) -> Room:
        """
        参加者を新規作成する
        :return: セッションインスタンス
        """
        if len(nickname) == 0:
            nickname = "匿名"

        self.table.put_item(
            Item={
                "member_id": member_id,
                "room_id": room_id,
                "nickname": nickname,
                "point": 0,
                # TODO: ttlの値をいい感じにする
                "ttl": 0,
            }
        )

        pass
