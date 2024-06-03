"""
このモジュールは、scikit-imageを使用して画像比較を行う関数を提供します。
"""

from skimage.metrics import structural_similarity as ssim  # pylint: disable=no-name-in-module
from skimage.io import imread
import numpy as np


def compare_images(image_path1, image_path2):
    """
    2つの画像ファイルを比較し、構造的類似度（SSIM）を計算する関数。

    Args:
        image_path1 (str): 比較元の画像ファイルのパス。
        image_path2 (str): 比較先の画像ファイルのパス。

    Returns:
        float: 2つの画像間の類似度スコア。
    """
    img1 = imread(image_path1, as_gray=True)
    img2 = imread(image_path2, as_gray=True)

    # 画像が浮動小数点の場合のデータ範囲を指定
    if img1.dtype == np.float32 or img1.dtype == np.float64:
        data_range = img1.max() - img1.min()
    else:
        data_range = 255

    similarity, _ = ssim(img1, img2, full=True, data_range=data_range)
    return similarity
