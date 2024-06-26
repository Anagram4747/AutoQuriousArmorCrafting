"""
このモジュールは、傀異錬成の結果を判定する処理を提供します
"""

# なぜかlint警告が出ていたので、ファイル全体で無視してる
# pylint: disable=no-member

import os
import sys
import json
import cv2
import pyautogui  # pylint: disable=unused-import
from PIL import Image
from app.lib.ocr.pytesseract import extract_text_from_image
from app.lib.ssim.skimage import compare_images

# スロットに対する領域
SLOT_TARGET_REGION = (1005, 270, 135, 42)

# y座標のずらし幅, 微妙にずれもあるけど、妥協できるライン
Y_OFFSET = 38

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

# スキル変動のチェック領域
SKILL_FLUCTUATION_REGION = (802, 274, 125, 32)


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


def load_skills_json():
    """ スキル情報を JSON ファイルから読み込む関数 """
    json_path = get_resource_path("app/resources/skills.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    skill_dict = {
        skill.get('skillNameEn').replace(" ", ""): {
            'cost': int(skill.get('cost')),
            'isUniqueSkill': bool(skill.get('isUniqueSkill'))
        }
        for skill in data['skills']
    }
    # 狂竜症【蝕】、龍気活性は固有スキル扱い
    skill_dict["Bloodlust"]["isUniqueSkill"] = True
    skill_dict["Dragonheart"]["isUniqueSkill"] = True
    return skill_dict


# スキル情報を読み込んで定数として保持
SKILL_DICT = load_skills_json()


def remove_noise(image):
    """ 画像のノイズを除去する関数 """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(
        gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
    return denoised


def is_skill_fluctuation_orver_limit(screenshot_path):
    """
    傀異錬成の結果が4スキル以上あるかどうかを判定

    Args:
        screenshot_path (str): スクリーンショットのファイルパス

    Returns
        bool: 文字認識の結果が "Slots" の場合はTrue、それ以外はFalse。
    """
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"File not found: {screenshot_path}")

    screenshot = Image.open(screenshot_path)
    x, y, width, height = SKILL_FLUCTUATION_REGION
    target_image = screenshot.crop((x, y, x + width, y + height))
    skill_fluctuation_check_image_path = os.path.join(
        "temp", "skill_fluctuation_check.png")
    target_image.save(skill_fluctuation_check_image_path)

    # ノイズ除去
    image = cv2.imread(skill_fluctuation_check_image_path)
    denoised_image = remove_noise(image)
    cv2.imwrite(skill_fluctuation_check_image_path, denoised_image)

    recognized_text = extract_text_from_image(
        skill_fluctuation_check_image_path)

    os.remove(skill_fluctuation_check_image_path)

    return recognized_text == "Defense"


def get_slots_count(index, is_offset):
    """
    画像を比較し、最も類似度が高い画像のスロット数を返すメソッド

    Args:
        index (int): スクリーンショットのインデックス
        is_offset (bool): 座標ずれがあるかどうか
    Returns:
        int: 最も類似度が高いスロットの番号
    """
    screenshot_path = os.path.join("temp", f"result_{index}.png")
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"File not found: {screenshot_path}")

    screenshot = Image.open(screenshot_path)
    x, y, width, height = SLOT_TARGET_REGION
    if is_offset:
        y += Y_OFFSET
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

    os.remove(target_image_path)

    return best_slot


def get_skills(screenshot_path, index, is_offset):
    """
    スクリーンショットからスキル名と上昇値を取得するメソッド

    Args:
        screenshot_path (str): スクリーンショットのファイルパス
        index (int): 呼び出し元の繰り返し回数
        is_offset (bool): 座標ずれがあるかどうか
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
        if is_offset:
            name_y += Y_OFFSET
            value_y += Y_OFFSET

        name_image = screenshot.crop(
            (name_x, name_y, name_x + name_width, name_y + name_height))
        value_image = screenshot.crop(
            (value_x, value_y, value_x + value_width, value_y + value_height))

        name_image_path = os.path.join("temp", f"skill_name_{idx}_{index}.png")
        value_image_path = os.path.join(
            "temp", f"skill_value_{idx}_{index}.png")

        name_image.save(name_image_path)
        value_image.save(value_image_path)

        # ノイズ除去
        name_image_cv = cv2.imread(name_image_path)
        denoised_name_image = remove_noise(name_image_cv)
        cv2.imwrite(name_image_path, denoised_name_image)

        value_image_cv = cv2.imread(value_image_path)
        denoised_value_image = remove_noise(value_image_cv)
        cv2.imwrite(value_image_path, denoised_value_image)

        name_text = extract_text_from_image(name_image_path)
        value_text = extract_text_from_image(value_image_path)

        os.remove(name_image_path)
        os.remove(value_image_path)

        if name_text.strip() and value_text.strip():  # 両方が空白でないことを確認
            # value_textの内容を変換
            name_text = name_text.replace(" ", "")
            value_text = value_text.replace(" ", "")
            if value_text == "None":
                value = -2
            elif value_text == "Lv-1":
                value = -1
            elif value_text.startswith("Lv+"):
                try:
                    value = int(value_text[3:])
                except ValueError:
                    value = 100  # 変換できない場合のデフォルト値
            else:
                value = 100  # 変換できない場合のデフォルト値

            skills.append((name_text, value))

    # 4スキル以上出た場合、災禍転福が-1されているとして処理する
    if is_offset:
        skills.append(("Coalescence", -1))

    return skills


def get_crafting_result(screenshot_path, index):
    """
    傀異錬成の結果を取得するメソッド

    Args:
        screenshot_path (str): 傀異錬成の結果の画像ファイルのパス
        index (int): 画像比較を行うインデックス
    Returns:
        bool: 成功時にはTrueを返す
    """
    is_offset = is_skill_fluctuation_orver_limit(screenshot_path)

    slot_count = get_slots_count(index, is_offset)
    skills = get_skills(screenshot_path, index, is_offset)

    # コスト計算
    cost = slot_count * 6
    total_negative_skill_value = 0
    unique_skill_count = 0

    for skill_name, skill_value in skills:
        if skill_value > 0:
            cost += SKILL_DICT.get(skill_name, {}
                                   ).get('cost', 100) * skill_value
        elif skill_value < 0:
            total_negative_skill_value += skill_value

        if SKILL_DICT.get(skill_name, {}).get('isUniqueSkill', False):
            unique_skill_count += 1

    # 戻り値の条件分岐
    result = False
    if total_negative_skill_value == 0:
        if cost >= 21:
            result = True
        elif cost >= 18 and unique_skill_count >= 1:
            result = True
    elif total_negative_skill_value == -1:
        if unique_skill_count >= 2:
            result = True
        elif unique_skill_count >= 1 and cost >= 21:
            result = True
        elif unique_skill_count == 0 and cost >= 24:
            result = True
    elif total_negative_skill_value <= -2:
        if unique_skill_count >= 2:
            result = True
        elif unique_skill_count >= 1 and cost >= 24:
            result = True
        elif unique_skill_count == 0 and cost >= 27:
            result = True

    return result
