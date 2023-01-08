# memo

- コンテナ上で動かす
  - スクレイピング用コンテナ、配信サーバー用コンテナ、データベース用コンテナ、メール送信用コンテナ
- maimaiDXNetの仕様変更 or 予期せぬエラーがめちゃくちゃ起きそうなので、その時はかならず例外を発生させ、catchする
  - メールでエラーの内容を送信
- 30分に1回ログイン https://maimaidx.jp/maimai-mobile/record/ をcurlして取ってくる
- 保存した最新の時刻をDBに入れておいて、それより新しいものすべてのリンク先をcurl、パースしてDBに保存

備忘録(後でやること)
- prodでは.envに機密情報を書くとヤバそうなので、https://qiita.com/myabu/items/89797cddfa7225ff2b5d#_reference-b678197ab6e7b9c98072 を参考にして作る
- dbを定期的にバックアップをとっておく(うっかり本番で`make destroy`したら大変なことになるので)
- docker swarmを使って環境構築