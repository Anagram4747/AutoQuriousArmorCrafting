# 仮想環境開発手順

## 環境構築(初回のみ)

仮想環境の作成コマンド

```shell
py -m venv myenv
```

パッケージのインストール  
pyautoguiは、ないとpydirectinputの座標がおかしくなるらしい  
参考：[pythonで、ゲームを自動化する「pydirectinput」](https://namake2.hatenablog.com/entry/2023/12/28/055412)

```shell
pip install pydirectinput
pip install pyautogui
pip install numpy
pip install google-cloud-vision
pip3 install pytk
pip install pyinstaller==5.13.2
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

## exeファイルの作成

```shell
pyinstaller --onefile --windowed app/main.py
```
