# 仮想環境開発手順

## 環境構築(初回のみ)

仮想環境の作成コマンド

```shell
py -m venv myenv
```

仮想環境の起動

```shell
myenv\Scripts\activate
```

パッケージのインストール  
pyautoguiは、ないとpydirectinputの座標がおかしくなるらしい  
参考：[pythonで、ゲームを自動化する「pydirectinput」](https://namake2.hatenablog.com/entry/2023/12/28/055412)  

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
