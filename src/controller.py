from datetime import datetime
from typing import Optional

from src import repository
from src import utils
from src.model import Room

ROOM_ID_LENGTH = 6
repo = repository.RoomRepository


# アクティブな部屋のリストを取得する(MVPではないのでいったん考慮しない)
# def get_active_rooms():
#     room_list: Optional[Room] = room_repo
#     return room_list


# 新たに部屋を建てる
def create_new_room() -> Optional[Room]:
    now = datetime.now()
    room_id = utils.get_random_string(ROOM_ID_LENGTH)
    room = repo.query_room(room_id)
    room = repo.initialize_room(room, now)
    # TODO: 新しい部屋を建てるのに失敗した場合のエラーハンドリングを追記する
    return room


# 参加者が部屋に入室する
def enter_room(room_id: str) -> Optional[Room]:
    return


# 各バックログの見積もりを確定してDynamoDBに書き込みに行く
def write_estimate_result():
    return


# ブラウザを閉じたらDynamoDBからセッション情報を削除する（気分）
def delete_session_info():
    return


# 過去の見積結果のポイントをDynamoDBから削除して履歴をリセットする
def reset_estimate_history():
    return
