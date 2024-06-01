"""
このモジュールは、Google Cloud Vision APIを使用して画像からテキストを抽出する関数を提供します。
"""

import io
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
