import datetime

from plapo import utils
from plapo.repository import RoomRepository

room_repo = RoomRepository()
ROOM_ID_LENGTH = 6


# 新たに部屋を建てるためのid文字列を返す
def create_new_room():
    room_id = utils.get_random_string(ROOM_ID_LENGTH)
    room_repo.create_new_room(room_id)
    return


# 参加者のセッション情報をdynamoDBに書き込みに行く
def write_session_info(name: str, dynamodb=None):
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
