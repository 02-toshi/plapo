import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table_name = "plapo"


class PlapoRepository:
    def __init__(self):
        self.table = dynamodb.Table(table_name)

    def query_room(self, room_id: str):
        """
        部屋の情報を取得する
        :param room_id:
        :return: 指定したidの部屋が存在すれば返す
        """
        return self.table.get_item(Key={
            "room_id": room_id
        })

    def create_new_room(self, record_id: str, room_id: str):
        """
        新しい部屋を作成する
        :param record_id: id
        :param room_id: 部屋id
        :return: none
        """
        self.table.put_item(Item={
            "id": record_id,
            "room_id": room_id,
            "opened": True,
            # TODO: ttlの値をいい感じにする
            "ttl": 0
        })

    def initialize_room(self, room_id: str):
        """
        部屋の情報を初期化する。次のバックログの見積もりを始める際に実施する。
        :param room_id: 部屋番号
        :return:
        """
        self.create_new_room(room_id)
        pass

    def create_new_member(self, member_id: str, room_id: str, nickname: str):
        """
        参加者を新規作成する
        :return: セッションインスタンス
        """
        if len(nickname) == 0:
            nickname = "匿名"

        self.table.put_item(Item={
            "member_id": member_id,
            "room_id": room_id,
            "nickname": nickname,
            "point": 0,
            # TODO: ttlの値をいい感じにする
            "ttl": 0
        })
        pass

    def vote(self, record_id: str, point: int):
        """
        自分の見積もり結果を保存する
        :param record_id: id
        :param point: 見積もりポイント
        :return:
        """
        self.table.update_item(
            Key={
                'id': record_id
            },
            UpdateExpression="""
                SET point = :point
            """,
            ExpressionAttributeValues={
                ':point': point
            }
        )
        pass

    def cancel_vote(self, member_id: str):
        """
        一度保存した見積もり結果を取り消す
        :param member_id: 参加者のID
        :return: none
        """
        # TODO:あとでかく！
        pass
