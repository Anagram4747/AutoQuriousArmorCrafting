# 仮想環境開発手順

## 環境構築(初回のみ)

仮想環境の作成コマンド

```shell
python3 -m venv myenv
```

パッケージのインストール  
pyautoguiは、ないとpydirectinputの座標がおかしくなるらしい  
参考：[pythonで、ゲームを自動化する「pydirectinput」](https://namake2.hatenablog.com/entry/2023/12/28/055412)  
opencvも使っていないが、座標ずれが発生するようになったため追加している(直接原因かは不明)

```shell
pip install -r requirements.txt
```

## 開発環境の起動(デバッグ時)

仮想環境の起動

```shell
$ myenv\Scripts\activate
(myenv) PS *\AutoQuriousArmorCrafting
```

仮想環境の終了

```shell
$ deactivate
PS *\AutoQuriousArmorCrafting
```

## exeファイルの作成

```shell
pyinstaller main.spec
```

## Discord bot

サーバー設定 > Webフックを作成 > bot名と送信先チャネルを選択 > URLをメモ
URLを設定する
