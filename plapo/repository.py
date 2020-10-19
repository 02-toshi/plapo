import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table_name = "plapo"


class RoomRepository:
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

    def create_new_room(self, room_id: str):
        """
        新しい部屋を作成する
        :param room_id: 部屋番号
        :return: none
        """
        self.table.put_item(Item={
            "room_id": room_id,
            "opened": False,
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

    def vote(self, room_id: str, name: str, point: int):
        """
        自分の見積もり結果を保存する
        :param room_id: 部屋番号
        :param name: 見積もりをした人の名前
        :param point: 見積もりポイント
        :return:
        """
        # TODO:あとでかく！
        pass

    def cancel_vote(self, room_id: str, name: str):
        """
        一度保存した見積もり結果を取り消す
        :param room_id: 部屋番号
        :param name: 見積もりを取り消す人の名前
        :return: none
        """
        # TODO:あとでかく！
        pass
