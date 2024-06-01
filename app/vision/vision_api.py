"""
このモジュールは、Google Cloud Vision APIを使用して画像からテキストを抽出する関数を提供します。
"""

import io
from google.cloud import vision
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
import numpy as np


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
        response = client.text_detection(image=image)

        if response.error.message:
            raise GoogleAPICallError(response.error.message)

        texts = response.text_annotations
        return texts[0].description if texts else ''

    except (GoogleAPICallError, InvalidArgument) as e:
        raise RuntimeError(f'Error during text extraction: {str(e)}') from e


def extract_image_features(image_path):
    """
    画像ファイルから特徴量を抽出する関数。

    Args:
        image_path (str): 画像ファイルのパス。

    Returns:
        list: 画像の特徴量ベクトル。
    """
    client = vision.ImageAnnotatorClient()

    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.feature_extraction(image=image)

        if response.error.message:
            raise GoogleAPICallError(response.error.message)

        features = response.feature_extraction
        return features

    except (GoogleAPICallError, InvalidArgument) as e:
        raise RuntimeError(f'Error during feature extraction: {str(e)}') from e


def compare_images(image_path1, image_path2):
    """
    2つの画像ファイルを比較し、特徴量ベースの類似度を計算する関数。

    Args:
        image_path1 (str): 比較元の画像ファイルのパス。
        image_path2 (str): 比較先の画像ファイルのパス。

    Returns:
        float: 2つの画像間の類似度スコア。
    """
    features1 = extract_image_features(image_path1)
    features2 = extract_image_features(image_path2)

    # 特徴量ベクトルのユークリッド距離を計算
    distance = np.linalg.norm(np.array(features1) - np.array(features2))
    # 類似度スコアは距離の逆数とする（距離が小さいほど類似度が高い）
    similarity = 1 / (1 + distance)
    return similarity
