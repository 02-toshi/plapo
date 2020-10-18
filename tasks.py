import boto3


# データベースの指定
db =

# 参加者のセッション情報をdynamoDBに書き込みに行く
def write_session_info(, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')
    response = table.put_item(
       Item={
            'year': year,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response


# 各バックログの見積もりを確定してDynamoDBに書き込みに行く
def write_estimate_result():
    return


# ブラウザを閉じたらDynamoDBからセッション情報を削除する
def delete_session_info():
    return

# 過去の見積結果のポイントをDynamoDBから削除して履歴をリセットする
def reset_estimate_history():
    return


if __name__ == '__main__':
