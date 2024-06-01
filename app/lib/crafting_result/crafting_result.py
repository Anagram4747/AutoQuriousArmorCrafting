"""
このモジュールは、傀異錬成の結果を判定する処理を提供します。
"""

import os
import sys
from PIL import Image
from app.lib.vision.vision_api import extract_text_from_image
from app.lib.opencv.cv2 import compare_images

# スロットに対する領域
SLOT_TARGET_REGION = (1005, 270, 135, 42)

# スキル名のトリミング範囲
SKILL_NAME_REGIONS = [
    (806, 549, 300, 35),  # スキル1
    (806, 625, 300, 35),  # スキル2
    (806, 701, 300, 35)   # スキル3
]

# スキル上昇値のトリミング範囲
SKILL_VALUE_REGIONS = [
    (1006, 586, 160, 36),   # スキル1の上昇値
    (1006, 662, 160, 36),   # スキル2の上昇値
    (1006, 738, 160, 36)    # スキル3の上昇値
]


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
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"File not found: {screenshot_path}")

    screenshot = Image.open(screenshot_path)
    x, y, width, height = SLOT_TARGET_REGION
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


def get_skills(screenshot_path):
    """
    スクリーンショットからスキル名と上昇値を取得するメソッド

    Args:
        screenshot_path (str): スクリーンショットのファイルパス
    Returns:
        list: スキル名と上昇値のリスト
    """
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"File not found: {screenshot_path}")

    screenshot = Image.open(screenshot_path)
    skills = []

    for idx, (name_region, value_region) in enumerate(zip(SKILL_NAME_REGIONS, SKILL_VALUE_REGIONS)):
        name_x, name_y, name_width, name_height = name_region
        value_x, value_y, value_width, value_height = value_region

        name_image = screenshot.crop(
            (name_x, name_y, name_x + name_width, name_y + name_height))
        value_image = screenshot.crop(
            (value_x, value_y, value_x + value_width, value_y + value_height))

        name_image_path = os.path.join("temp", f"skill_name_{idx}.png")
        value_image_path = os.path.join("temp", f"skill_value_{idx}.png")

        name_image.save(name_image_path)
        value_image.save(value_image_path)

        name_text = extract_text_from_image(name_image_path)
        value_text = extract_text_from_image(value_image_path)

        if name_text.strip() and value_text.strip():  # 両方が空白でないことを確認
            skills.append((name_text, value_text))

    return skills


def get_crafting_result(file_name, index):
    """
    傀異錬成の結果を取得するメソッド

    Args:
        file_name (str): OCRを行うファイル名
        index (int): 画像比較を行うインデックス
    Returns:
        bool: 成功時にはTrueを返す
    """
    slot_count = get_slots_count(index)
    skills = get_skills(os.path.join("temp", file_name))
    output_dir = "debug"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"result{index}.txt"), 'w', encoding='utf-8') as output_file:
        output_file.write(f"slot:{slot_count}\n")
        for skill_name, skill_value in skills:
            output_file.write(f"{skill_name} : {skill_value}\n")

    # デバッグ情報の追加
    print(f"Slot count: {slot_count}")
    for skill_name, skill_value in skills:
        print(f"Skill: {skill_name}, Value: {skill_value}")

    return True
