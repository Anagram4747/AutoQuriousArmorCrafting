# AutoQuriousArmorCrafting

MHR:Sの傀異錬成を自動化する

## 事前準備

- python3をインストールしている
- pytessaractをインストールし、環境変数にパスを通している

## 実行方法

1. コマンドプロンプトを開き、以下のコマンドを順番に実行
2. distフォルダ配下に`main.exe`ができるので、ダブルクリックで起動
3. 「Discord Web hookの設定」を押下し、以下手順で取得したURLを貼りつける
   1. 管理者権限を持ってるサーバーで、サーバー設定を開く
   2. 連携サービス > ウェブフック
   3. 新しいウェブフックを押下
   4. 名前と投稿先チャンネルを選択
   5. ウェブフックURLをコピーを押下
4. 錬成の回数を設定し、「錬成開始」を押下して実行  
  ※途中で止まらないので注意

### コマンド

```shell
py -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
pyinstaller main.spec
```

## 開発開発環境

`docs/DevelopmentSetupGuide.md`参照
