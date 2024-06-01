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


# スロット画像とそのスロット番号の辞書
SLOT_IMAGES = {
    0: get_resource_path("app/resources/slots/slots300.png"),
    1: get_resource_path("app/resources/slots/slots310.png"),
    2: get_resource_path("app/resources/slots/slots311.png"),
    3: get_resource_path("app/resources/slots/slots411.png"),
    4: get_resource_path("app/resources/slots/slots421.png"),
    5: get_resource_path("app/resources/slots/slots431.png"),
    6: get_resource_path("app/resources/slots/slots441.png")
}


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


def get_slots_count(index):
    """
    画像を比較し、最も類似度が高い画像のスロット数を返すメソッド

    Args:
        index (int): スクリーンショットのインデックス
    Returns:
        int: 最も類似度が高いスロットの番号
    """
    # 最初に保存したスクリーンショットのトリミング
    screenshot_path = os.path.join("temp", f"result_{index}.png")
    screenshot = Image.open(screenshot_path)
    x, y, width, height = TARGET_REGION
    target_image = screenshot.crop((x, y, x + width, y + height))
    target_image_path = os.path.join("temp", f"slots_{index}.png")
    target_image.save(target_image_path)

    best_similarity = 0.0
    best_slot = -1

    for slot_plus, comparison_image in SLOT_IMAGES.items():
        similarity = compare_images(target_image_path, comparison_image)
        if similarity > best_similarity:
            best_similarity = similarity
            best_slot = slot_plus

    return best_slot


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
    slot_count = get_slots_count(index)
    output_dir = "debug"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "result.txt"), 'w', encoding='utf-8') as output_file:
        output_file.write(f"slot:{slot_count}\n")

    return True
