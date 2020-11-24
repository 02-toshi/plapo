from datetime import datetime
from typing import Optional

import boto3
from arrow import Arrow

from src import utils
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
        item = {}

        new_dict_room["room_id"] = room.room_id
        new_dict_room["mem_" + member.member_id] = {
            "nickname": member.nickname
        }
        new_dict_room["opened"] = False
        new_dict_room["ttl"] = utils.get_ttl_value(now, 1)

        if member.point:
            new_dict_room["mem_" + member.member_id]["point"] = member.point

        # ここは条件付き書き込みにする
        # self.table.update_item(
        #     Key="mem_"+member.member_id,
        #     AttributeUpdates={"nickname": member.nickname, "point": member.point},
        # )
        self.table.put_item(
            Item=new_dict_room,
        )
        return room
