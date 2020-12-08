import json
from typing import Optional, Dict

from arrow import Arrow

from src import repository
from src import utils
from src.model import Room, Member

ROOM_ID_LENGTH = 6
repo = repository.RoomRepository


# アクティブな部屋のリストを取得する(MVPではないのでいったん考慮しない)
# def get_active_rooms():
#     room_list: Optional[Room] = room_repo
#     return room_list


# 新たに部屋を建てる
def create_new_room(event, context) -> Dict[str, str]:
    now = Arrow.now()
    while True:
        room_id = utils.get_random_string(ROOM_ID_LENGTH)
        if not repo.query_room(room_id):
            break
    room = repo.initialize_room(Room(room_id), now)
    # try:
    #     room = repo.initialize_room(Room(room_id), now)
    # except RuntimeError as e:
    #     print("サーバ側のエラーです。", e)
    #     res["errorCode"] = ""
    # except ConnectionError as e:
    #     print()
    body = str(room)
    return {
        'statusCode': 200,
        'headers': {
            'Location': '{}'.format()
        },
        'body': json.dumps(body),
        'isBase64Encoded': False
    }


# 部屋の状態をリセットする
def initialize_room(room_id: str):
    room = repo.initialize_room(room_id)
    return room


# 参加者が部屋に参加するか、見積りポイントを登録する
def act_member(member: Member, room: Room) -> Optional[Room]:
    room = repo.act_member(member, room)
    return room


# ブラウザを閉じたらDynamoDBからセッション情報を削除する（気分）　→　いらない...？
def delete_session_info():
    return
