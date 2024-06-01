"""
このモジュールは、Google Cloud Vision APIを使用して画像からテキストを抽出する関数を提供します。
"""

import io
import cv2  # pylint: disable=<E0401>
from google.cloud import vision
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument


def extract_text_from_image(image_path):
    """
    画像ファイルからテキストを抽出する関数。

    Args:
        image_path (str): 画像ファイルのパス。

    Returns:
        str: 画像から抽出されたテキスト。
    """
    client = vision.ImageAnnotatorClient()

    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(  # pylint: disable=<E1101>
            image=image)

        if response.error.message:
            raise GoogleAPICallError(response.error.message)

        texts = response.text_annotations
        return texts[0].description if texts else ''

    except (GoogleAPICallError, InvalidArgument) as e:
        raise RuntimeError(f'Error during text extraction: {str(e)}') from e


def compare_images(image_path1, image_path2):
    """
    2つの画像ファイルを比較し、特徴量ベースの類似度を計算する関数。

    Args:
        image_path1 (str): 比較元の画像ファイルのパス。
        image_path2 (str): 比較先の画像ファイルのパス。

    Returns:
        float: 2つの画像間の類似度スコア。
    """
    img1 = cv2.imread(image_path1, cv2.IMREAD_COLOR)
    img2 = cv2.imread(image_path2, cv2.IMREAD_COLOR)

    mssim, _ = cv2.quality.QualitySSIM_compute(img1, img2)

    return (mssim[0] + mssim[1] + mssim[2]) / 3
