"""テスト設定"""
import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture
def dynamodb():
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb")
        dynamodb.create_table(
            TableName="plapo",
            KeySchema=[{"AttributeName": "room_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "room_id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        )
        table = dynamodb.Table("plapo")
        table.put_item(Item={"room_id": "123456"})
        yield dynamodb


@pytest.fixture
def table(dynamodb):
    return dynamodb.Table("plapo")
