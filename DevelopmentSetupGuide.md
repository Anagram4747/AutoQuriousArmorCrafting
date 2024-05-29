# 仮想環境開発手順

## 環境構築(初回のみ)

仮想環境の作成コマンド

```shell
py -m venv myenv
```

パッケージのインストール

```shell
pip install pydirectinput
pip install pyautogui # ないと座標がおかしくなるらしい 参考：https://namake2.hatenablog.com/entry/2023/12/28/055412
pip install numpy
pip install google-cloud-vision # google Cloud VisionAPI用
```

## 開発環境の起動(デバッグ時)

仮想環境の起動

```shell
$ myenv\Scripts\activate
(myenv) PS C:***\AutoQuriousArmorCrafting
```

仮想環境の終了

```shell
$ deactivate
PS C:***\AutoQuriousArmorCrafting
```
