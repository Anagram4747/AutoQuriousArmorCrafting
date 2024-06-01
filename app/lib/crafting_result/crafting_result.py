"""
このモジュールは、傀異錬成の結果を判定する処理を提供します。
"""

import os
import sys
from PIL import Image
from app.lib.vision.vision_api import extract_text_from_image
from app.lib.opencv.cv2 import compare_images

TARGET_REGION = (1005, 270, 135, 42)


def get_resource_path(relative_path):
    """ ビルドされたEXEファイルに対するリソースの相対パスを取得する """
    # pylint: disable=protected-access
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


COMPARISON_IMAGES = [
    get_resource_path("app/resources/slots/slots441.png"),
    get_resource_path("app/resources/slots/slots431.png"),
    get_resource_path("app/resources/slots/slots421.png"),
    get_resource_path("app/resources/slots/slots411.png"),
    get_resource_path("app/resources/slots/slots311.png"),
    get_resource_path("app/resources/slots/slots310.png"),
    get_resource_path("app/resources/slots/slots300.png")
]


def perform_ocr(file_name):
    """
    tempフォルダ内の画像に対してOCRを実行し、結果をdebug/name.txtに保存するメソッド

    Args:
        file_name (str): 読み込みファイル名
    Returns:
        None
    """
    output_dir = "debug"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "name.txt"), 'w', encoding='utf-8') as output_file:
        image_path = os.path.join("temp", file_name)
        text = extract_text_from_image(image_path)
        output_file.write(f"{file_name}:\n{text}\n\n")


def compare_target_images(index):
    """
    画像を比較し、最も類似度が高い画像を特定するメソッド

    Args:
        index (int): スクリーンショットのインデックス
    Returns:
        None
    """
    output_dir = "debug"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 最初に保存したスクリーンショットのトリミング
    screenshot_path = os.path.join("temp", f"result_{index}.png")
    screenshot = Image.open(screenshot_path)
    x, y, width, height = TARGET_REGION
    target_image = screenshot.crop((x, y, x + width, y + height))
    target_image_path = os.path.join("temp", f"slots_{index}.png")
    target_image.save(target_image_path)

    best_match = None
    best_similarity = 0.0

    for comparison_image in COMPARISON_IMAGES:
        similarity = compare_images(target_image_path, comparison_image)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = comparison_image

    with open(os.path.join(output_dir, "slots.txt"), 'w', encoding='utf-8') as output_file:
        output_file.write(
            f"Best match: {best_match}\nSimilarity: {best_similarity}\n")


def get_crafting_result(file_name, index):
    """
    傀異錬成の結果を取得するメソッド

    Args:
        file_name (str): OCRを行うファイル名
        index (int): 画像比較を行うインデックス
    Returns:
        bool: 成功時にはTrueを返す
    """
    perform_ocr(file_name)
    compare_target_images(index)
    return True
