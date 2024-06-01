"""
このモジュールは、mainwindowの内容を表します。
"""

import tkinter as tk
from tkinter import ttk
import configparser
import time
import shutil
import os
import pyautogui
import pydirectinput
from PIL import Image
from app.vision.vision_api import extract_text_from_image, compare_images


class MainWindow(tk.Tk):
    """
    メインウィンドウクラス。

    Attributes:
        button (tk.Button): クリックするとon_button_click()メソッドが呼び出されるボタン。
        label (tk.Label): ボタンを押すと表示されるテキストラベル。
        dropdown (ttk.Combobox): ドロップダウンメニュー。
        entry (tk.Entry): 繰り返し回数を入力するエントリ。
    """

    CONFIG_FILE = "config.ini"
    TARGET_REGION = (1005, 270, 135, 42)
    COMPARISON_IMAGES = [
        "../app/resources/slots/slots441.png",
        "../app/resources/slots/slots431.png",
        "../app/resources/slots/slots421.png",
        "../app/resources/slots/slots411.png",
        "../app/resources/slots/slots311.png",
        "../app/resources/slots/slots310.png",
        "../app/resources/slots/slots300.png"
    ]

    def __init__(self):
        """
        ウィンドウを初期化する。

        Args:
            None
        Returns:
            None
        """
        super().__init__()
        self.title("My GUI App")
        self.geometry("400x300")

        self.config = configparser.ConfigParser()
        self.read_config(self.CONFIG_FILE)

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """
        ウィジェットを作成し、配置する。

        Args:
            None
        Returns:
            None
        """
        self.button = tk.Button(
            self, text="錬成開始", command=self.on_button_click)
        self.button.pack(pady=20)

        self.label = tk.Label(self, text="")
        self.label.pack(pady=20)

        tk.Label(self, text="消費タイプ").pack()
        self.dropdown_values = [
            "おまかせ選択(自動選択)",
            "真・尖のみ使用",
            "真・王・尖のみ使用"
        ]
        self.dropdown = ttk.Combobox(self, values=self.dropdown_values)
        self.dropdown.pack(pady=5)

        default_value = self.config.get(
            'settings', 'selection', fallback=self.dropdown_values[1])
        self.dropdown.set(default_value)

        tk.Label(self, text="回数").pack()
        vcmd = (self.register(self.validate), "%P")
        self.entry = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=5)
        self.entry.insert(0, "1")

    def read_config(self, filename):
        """
        指定されたファイルを読み込むメソッド。

        Args:
            filename (str): 読み込む設定ファイルの名前。
        Returns:
            None
        """
        with open(filename, 'r', encoding='utf-8') as file:
            self.config.read_file(file)

    def validate(self, value_if_allowed):
        """
        入力が有効かどうかを検証するメソッド。

        Args:
            value_if_allowed (str): 入力された値。
        Returns:
            bool: 入力が有効ならTrue、無効ならFalse。
        """
        if value_if_allowed.isdigit() and 1 <= int(value_if_allowed) <= 100000:
            return True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "1")
        return False

    def on_button_click(self):
        """
        ボタンがクリックされたときに実行されるメソッド。

        Args:
            None
        Returns:
            None
        """
        self.label.config(text="Macro Start!")
        repetitions = int(self.entry.get())

        temp_dir = "temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        for i in range(repetitions):
            self.consume_prime()
            time.sleep(1.65)
            file_name = self.save_screenshot(i + 1)
            self.perform_ocr(file_name)
            self.compare_target_images(i + 1)
            time.sleep(0.5)
            self.skip()

    def consume_prime(self):
        """
        座標1, 1を左クリックし、'x', 'space', 'space'の順に入力するマクロを実行するメソッド。

        Args:
            None
        Returns:
            None
        """
        self.click_at_position()
        self.set_prime()

    def click_at_position(self):
        """
        座標1, 1を左クリックするメソッド。

        Args:
            None
        Returns:
            None
        """
        pydirectinput.click(1, 1)

    def set_prime(self):
        """
        'x', 'space', 'space'の順にキーを押し、キーの間に遅延を挟むメソッド。

        Args:
            None
        Returns:
            None
        """
        pydirectinput.press('x')
        self.precise_sleep(0.017)  # 17msの遅延
        pydirectinput.press('space')
        self.precise_sleep(0.034)  # 34msの遅延
        pydirectinput.press('space')

    def save_screenshot(self, index):
        """
        スクリーンショットを取得し、temp/result_<index>.pngとして保存するメソッド。
        既にファイルが存在する場合は削除します。

        Args:
            index (int): スクリーンショットのインデックス。
        Returns:
            None
        """
        output_dir = "temp"
        output_file_name = f"result_{index}.png"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        screenshot_path = os.path.join(output_dir, output_file_name)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        return output_file_name

    def skip(self):
        """
        右クリック > 'a' > 'space' > 'space'の順にキーを押し、キーの間に遅延を挟むメソッド。

        Args:
            None
        Returns:
            None
        """
        pydirectinput.press('b')
        self.precise_sleep(0.034)  # 17msの遅延
        pydirectinput.press('a')
        self.precise_sleep(0.017)  # 17msの遅延
        pydirectinput.press('space')
        self.precise_sleep(0.017)  # 17msの遅延
        pydirectinput.press('space')

    def precise_sleep(self, duration):
        """
        指定された期間だけスリープするメソッド。

        Args:
            duration (float): スリープする時間（秒）。
        Returns:
            None
        """
        end_time = time.time() + duration
        while time.time() < end_time:
            pass

    def perform_ocr(self, file_name):
        """
        tempフォルダ内の画像に対してOCRを実行し、結果をdebug/name.txtに保存するメソッド。

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

    def compare_target_images(self, index):
        """
        画像を比較し、最も類似度が高い画像を特定するメソッド。

        Args:
            index (int): スクリーンショットのインデックス。
        Returns:
            None
        """
        output_dir = "debug"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 最初に保存したスクリーンショットのトリミング
        screenshot_path = os.path.join("temp", f"result_{index}.png")
        screenshot = Image.open(screenshot_path)
        x, y, width, height = self.TARGET_REGION
        target_image = screenshot.crop((x, y, x + width, y + height))
        target_image_path = os.path.join("temp", f"slots_{index}.png")
        target_image.save(target_image_path)

        best_match = None
        best_similarity = 0.0

        for comparison_image in self.COMPARISON_IMAGES:
            similarity = compare_images(target_image_path, comparison_image)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = comparison_image

        with open(os.path.join(output_dir, "slots.txt"), 'w', encoding='utf-8') as output_file:
            output_file.write(
                f"Best match: {best_match}\nSimilarity: {best_similarity}\n")

    def on_closing(self):
        """
        ウィンドウが閉じられるときに実行されるメソッド。選択状態を保存します。

        Args:
            None
        Returns:
            None
        """
        self.config['settings'] = {'selection': self.dropdown.get()}
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        self.destroy()
