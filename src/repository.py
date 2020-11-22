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
        new_dict_room = {}
        new_members = []

        latest_room = self.query_room(room.room_id)
        if latest_room:
            if len(latest_room.members) > 0:
                new_members = [
                    Member(
                        member_id=member.member_id, nickname=member.nickname
                    )
                    for member in latest_room.members
                ]
                new_dict_room = {
                    "mem_"
                    + new_member.member_id: {"nickname": new_member.nickname}
                    for new_member in new_members
                }

        # opened: Falseが本当に正しいっけ？部屋を立てたらその部屋は開いていて欲しい気がする
        new_dict_room["room_id"] = room.room_id
        new_dict_room["opened"] = False
        new_dict_room["ttl"] = 0

        put_result = self.table.put_item(
            Item=new_dict_room,
        )

        new_room = Room(
            room_id=new_dict_room["room_id"], opened=False, members=new_members
        )

        return new_room

    def act_member(self, member: Member, room: Room) -> Room:
        """
        部屋に参加する / 見積もりポイントを登録する
        :return: セッションインスタンス
        """
        latest_room = self.query_room(room.room_id)
        new_dict_room = {}

        if latest_room:
            if len(latest_room.members) > 0:
                present_members = [
                    Member(
                        member_id=member.member_id, nickname=member.nickname
                    )
                    for member in latest_room.members
                ]
                for present_member in present_members:
                    new_dict_room["mem_" + present_member.member_id] = {
                        "nickname": present_member.nickname
                    }
                    if present_member.point:
                        new_dict_room["mem_" + present_member.member_id] = {
                            "point": present_member.point
                        }

        new_dict_room["room_id"] = room.room_id
        new_dict_room["mem_" + member.member_id] = {
            "nickname": member.nickname
        }
        new_dict_room["opened"] = False
        new_dict_room["ttl"] = 0

        # if member.point:
        #     new_dict_room["mem_" + member.member_id["point": member.point]]

        print("new_dict_room")
        print(new_dict_room)

        self.table.put_item(
            Item=new_dict_room,
        )
        return room
