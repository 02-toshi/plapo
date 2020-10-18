import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table_name = "plapo"


class RoomRepository:
    def __init__(self):
        self.table = dynamodb.Table(table_name)

    def query_room(self, room_id: str):
        """

        :param room_id:
        :return:
        """
        return self.table.get_item(Key={
            "room_id": room_id
        })

    def create_new_room(self, room_id: str):
        """

        :param room_id:
        :return:
        """
        self.table.put_item(Item={
            "room_id": room_id,
            "opened": False,
            # TODO: ttlの値をいい感じにする
            "ttl": 0
        })

    def initialize_room(self, room_id: str):
        """

        :param room_id:
        :return:
        """
        self.create_new_room(room_id)

    def vote(self, room_id: str, name: str, point: int):
        # TODO:あとでかく！
        pass

    def cancel_vote(self, room_id: str):
        # TODO:あとでかく！
        pass
