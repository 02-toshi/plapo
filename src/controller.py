from src import utils
from src.repository import PlapoRepository

room_repo = PlapoRepository()
ROOM_ID_LENGTH = 6
SESSION_ID_LENGTH = 10
RECORD_ID_LENGTH = 32


# アクティブな部屋のリストを取得する(MVPではないのでいったん考慮しない)
# def get_active_rooms():
#     room_list: Optional[Room] = room_repo
#     return room_list


# 新たに部屋を建てる
def create_new_room():
    record_id = utils.get_random_string(RECORD_ID_LENGTH)
    room_id = utils.get_random_string(ROOM_ID_LENGTH)
    room_repo.create_new_room(record_id, room_id)
    # TODO: 新しい部屋を建てるのに失敗した場合のエラーハンドリングを追記する
    return room_id


# 参加者が部屋に入室する
def enter_room():
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
