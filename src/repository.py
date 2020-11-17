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
        if not res:
            return None
        members = []
        for key, value in res.items():
            if key.startswith('mem_'):
                member = Member(
                    member_id=key[4:],
                    nickname=value["nickname"],
                    point=value.get("point")
                )
                members.append(member)
        # TODO 内包表記になおす！
        return Room(room_id=res["room_id"], opened=res["opened"], members=members)

    def initialize_room(self, room: Room) -> Room:
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param room: 部屋
        :return:
        """
        # item = {"room_id": room.room_id}
        # if room.members is not None:
        #     item["members"] = room.members
        # if room.opened:
        #     item["members"] = room.members
        #
        self.table.put_item(
            Item={
                "room_id": room.room_id,
                "opened": room.opened,
                "members": room.members,
                "ttl": 0,
            },
        )
        return room

    def act_member(self, member: Member, room: Room) -> Room:
        """
        部屋に参加する / 見積もりポイントを登録する
        :return: セッションインスタンス
        """
        room.members.append(member)

        self.table.put_item(
            Item={
                "room_id": room.room_id,
                "members": room.members
                # "ttl": 0,
            },
        )
        return room
