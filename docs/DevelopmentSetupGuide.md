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
pip install opencv-python
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

# main.specの内容でビルド
pyinstaller main.spec
```

## Google Cloud Vision API

基本Webサイトなど参考に行うのがよいと思うが、とりあえずgramがやったこと記載

- Google Cloud Consleにログインし、プロジェクト作成
  - Google Cloud Consoleにアクセス
  - プロジェクト作成Vision APIを有効化
- サービスアカウントキーの作成
  - 「APIとサービス」>「認証情報」に移動し、「認証情報を作成」>「サービスアカウントキー」を選択
  - 新しいサービスアカウントを作成し、JSON形式のキーをダウンロード
  - jsonのファイル名まで含めたパスを環境変数`GOOGLE_APPLICATION_CREDENTIALS`に設定
- Google Cloud SDKのインストール
  - 64bit版のインストーラー取得
  - インストーラーの指示に従ってインストール
  - インストール後にプロジェクト選択が必要なので、新しく作ったプロジェクトを選択
