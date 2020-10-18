# plapo

### 概要
 - プランニングポーカーを自分たちで作ってみる試み

### できること
 - あとで書こう

### 構成
 - サーバレスアーキテクチャ(APIGW + Lambda + DynamoDBの鉄板構成に)
 - RESTfulにする
  - https://qiita.com/NagaokaKenichi/items/0647c30ef596cedf4bf2
 - なるべくシンプルにする

### 環境構築手順
#### ローカル環境にserverlessフレームワークとlocal dynamodbをインストールする
 - 参考ページ
  - https://qiita.com/noralife/items/e36621ddd0e5b8ff4447
 - 基本的に上記のページ通りで行けるけど詰まった点
  - sls dynamodb startしてもdev環境は利用不可だよ！みたいなエラーが吐かれた
   - stages - dev を追加したら通るようになった(serverless.yml L:17,18)
  - なんか以下のエラーで怒られた
   - ValidationException: The number of attributes in key schema must match the number of attributesdefined in attribute definitions
   - 原因はserverless.ymlのAttributeDefinitionsとKeySchemasの数が一致していなかったこと。
     カラムを全て書く必要はないらしく、一つだけに絞ったらエラー解消された

#### poetryの導入
 - pycharmの実行環境とpoetryの実行環境を合わせておく
  - poetry new plapo // 新たに環境を構築
   - ルートの下にplapoディレクトリが作成されるので、名前をplapo_とかに変更する(後で消す)
   - plapo_ディレクトリの配下にplapoとtestsができるので、配下の2ディレクトリをルート直下に移動
   - 同じくpyproject.tomlもルート直下に移動
   - plapo_ディレクトリは削除
  - poetry install // どこかにplapoの実行環境が作成される
  - poetry env list // 作成されたことを確認する
  - poetry config --list // 作成されたパスをコピーしておく
  - pycharmのpreferenceからprojectのinterpreterを選び、歯車をクリックしてadd
  - existing environmentから先ほどコピーしたパスを貼り付ける
  - 配下の階層にpythonがあるので、それを選択してOK -> OK