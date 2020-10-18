import datetime

from plapo import utils
from plapo.repository import RoomRepository

room_repo = RoomRepository()


# 新たに部屋を建てるためのid文字列を返す
def create_new_room():
    room_id = utils.get_random_string(16)
    room_repo.create_new_room(room_id)
    return


# Lambdaのメイン関数
def lambda_handler(event, context):
    table_name = "plapo"

    # 実行時間の記録
    time_utc = datetime.datetime.today()
    time_unix = time_utc.timestamp()
    event["time"] = time_unix

    # テストデータ
    # idと氏名をデータに持たせる
    payload = {
        "id": "hogehoge1234_takahashi",
        "room_id": "hogehoge1234",
        "name": "takahashi",
    }

    # DynamoDBテーブルのオブジェクトを取得
    dynamotable = dynamodb.Table(table_name)

    try:
        # DynamoDBへのデータ登録
        res = dynamotable.put_item(
            Item=payload
        )
        return

    except Exception as e:
        print("Failed.")
        print(e)
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
