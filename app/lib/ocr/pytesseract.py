"""
指定された画像ファイルからテキストを抽出する関数を提供します。この関数はpytesseractライブラリを使用します。

必要なライブラリ:
- pytesseract
- Pillow

インストール方法:
pip install pytesseract pillow

また、Tesseract OCRエンジンがインストールされている必要があります。
詳細は以下のリンクを参照してください。
https://github.com/tesseract-ocr/tesseract
"""

import pytesseract
from PIL import Image


def extract_text_from_image(image_path):
    """
    指定された画像ファイルからpytesseractを使用してテキストを抽出します。言語は英語に設定されています。

    Args:
        image_path (str): 画像ファイルへのパス。

    Returns:
        str: 抽出されたテキスト。
    """
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
    # 両端の空白文字(改行文字を含む)を除去して返却
    return text.strip()
