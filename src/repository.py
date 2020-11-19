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

        # 通常表記ver.
        # members = []
        # for key, value in res.items():
        #     if key.startswith('mem_'):
        #         member = Member(
        #             member_id=key[4:],
        #             nickname=value["nickname"],
        #             point=value.get("point")
        #         )
        #         members.append(member)

        return Room(
            room_id=res["room_id"], opened=res["opened"], members=members
        )

    def initialize_room(self, room: Room) -> Optional[Room]:
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param room: 部屋
        :return:
        """
        initialized_members = [
            Member(
                member_id=key[4:],
                nickname=value["nickname"],
                point=None,
            )
            for key, value in room.members
            if key.startswith("mem_")
        ]
        # TODO : UTが通らない原因の調査から！
        # opened: Falseが本当に正しいっけ？部屋を立てたらその部屋は開いていて欲しい気がする
        res = self.table.put_item(
            Item={
                "room_id": room.room_id,
                "members": initialized_members,
                "opened": False,
                "ttl": 0,
            },
        )
        if not res:
            return None

        initialized_room = Room(room_id=room.room_id, opened=False)

        if len(initialized_members) > 0:
            initialized_room.members = initialized_members

        return initialized_room

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
