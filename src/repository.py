from typing import Optional, List

import boto3

from src.model import Member, Room

table_name = "plapo"


def filter_member_key(dict_keys: List) -> List:
    """
    リストの中からmemで始まるキーのリストを返す
    :param dict_keys: 抽出対象のリスト
    :return: memで始まるキーのリスト
    """
    memlist = [key for key in dict_keys if 'mem_' in key]
    return memlist


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
        member_keys = filter_member_key(res.keys())
        members = []
        for member_key in member_keys:
            member = Member(
                member_id=member_key[4:],
                nickname=res.get(member_key).get("nickname"),
            )
            if res.get(member_key).get("point") is not None:
                member.point = res.get(member_key).get("point")
            members.append(member)
        room = Room(room_id=res.get("room_id"), opened=res.get("opened"), members=members)

        return room

    def initialize_room(self, room: Room) -> Room:
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param room: 部屋
        :return:
        """
        self.table.put_item(
            Item={
                "room_id": room.room_id,
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
