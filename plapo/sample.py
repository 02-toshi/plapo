"""boto3の参考にするためだけのただのサンプル。あとで消そう"""
import boto3

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table('sample')


# メイン処理
def main(event, context):
    search(event)
    insert(event)
    update(event)
    delete(event)

    return


# 取得処理
def search(event):
    query_data = table.get_item(
        Key={
            'id': event['id']
        }
    )
    print("GetItem succeeded:")

    # 取り出す時は
    sample_value = query_data['Item']['sample_value']

    return


# 登録処理
def insert(event, context):
    table.put_item(
        Item={
            'id': event['id'],
            'sample_value': event['sample_value']
        }
    )
    print("PutItem succeeded:")

    return


# 更新処理
def update(event):
    table.update_item(
        Key={'id': event['id']},
        UpdateExpression='set sample_value = :s',
        ExpressionAttributeValues={
            ':s': event['sample_value']
        }
    )
    print("UpdateItem succeeded:")

    return


# 削除処理
def delete(event):
    table.delete_item(
        Key={
            'id': event['id']
        }
    )

    print("DeleteItem succeeded:")

    return
