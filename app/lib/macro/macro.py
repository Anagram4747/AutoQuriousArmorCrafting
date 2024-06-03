"""
このモジュールは、マクロ操作を定義する関数を提供します
"""

import time
# 座標ずれ対策で、pyautoguiを追加している
import pyautogui  # pylint: disable=<W0611>
import pydirectinput


def consume_prime():
    """
        精気琥珀・尖を選択し、錬成を行う

        Args:
            None
        Returns:
            None
        """
    pydirectinput.press('x')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('space')


def consume_royal():
    """
        精気琥珀・王を選択し、錬成を行う

        Args:
            None
        Returns:
            None
        """
    pydirectinput.press('w')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('w')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('w')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('w')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('tab')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('space')


def consume_pure():
    """
        精気琥珀・真を選択し、錬成を行う

        Args:
            None
        Returns:
            None
        """
    pydirectinput.press('w')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('w')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('w')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('tab')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.034)  # 34msの遅延
    pydirectinput.press('space')


def skip():
    """
    傀異錬成の結果を受け取らずにスキップする

    Args:
        None
    Returns:
        None
    """
    pydirectinput.press('b')
    precise_sleep(0.034)  # 17msの遅延
    pydirectinput.press('a')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')
    precise_sleep(0.017)  # 17msの遅延
    pydirectinput.press('space')


def precise_sleep(duration):
    """
    指定された期間だけスリープする

    Args:
        duration (float): スリープする時間（秒）
    Returns:
        None
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        pass
