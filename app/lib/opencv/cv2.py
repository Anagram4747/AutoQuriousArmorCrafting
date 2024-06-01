"""
このモジュールは、OpenCVを使用して画像比較を行う関数を提供します。
"""

import cv2  # pylint: disable=<E0401>


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
