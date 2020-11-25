from typing import Optional

import boto3
from arrow import Arrow

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
        if not res:
            return None

        # 内包表記ver.
        members = [
            Member(
                member_id=key[4:],
                nickname=value["nickname"],
                point=value.get("point"),
            )
            for key, value in res.items()
            if key.startswith("mem_")
        ]

        return Room(
            room_id=res["room_id"], opened=res["opened"], members=members
        )

    def initialize_room(self, room: Room, now: Arrow) -> Room:
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param now:
        :param room: 部屋
        :return:
        """
        item = {
            "room_id": room.room_id,
            "opened": False,
            "ttl": now.shift(days=1).int_timestamp,
        }
        for member in room.members:
            item[f"mem_{member.member_id}"] = {"nickname": member.nickname}

        self.table.put_item(Item=item)

        new_room = self.query_room(room.room_id)
        if new_room:
            return new_room
        raise Exception

    def act_member(self, member: Member, room: Room) -> Room:
        """
        部屋に参加する / 見積もりポイントを登録する
        :return: セッションインスタンス
        """

        item = {
            ':m': {"nickname": member.nickname},
        }
        update_expression_str = f"set mem_{member.member_id}=:m"

        if member.point:
            item = {
                ':m': {"nickname": member.nickname, "point": member.point},
            }

        print("item")
        print(item)
        print("update_expression_str")
        print(update_expression_str)

        self.table.update_item(
            Key={'room_id': room.room_id},
            UpdateExpression=update_expression_str,
            ExpressionAttributeValues=item,
            ReturnValues="UPDATED_NEW"
        )

        new_room = self.query_room(room.room_id)

        if new_room:
            return new_room
        raise Exception
