"""
このモジュールは、mainwindowの内容を表します
"""

import tkinter as tk
from tkinter import ttk
import configparser
import time
import shutil
import os
import requests
import pyautogui
import pydirectinput
from app.lib.crafting_result.crafting_result import get_crafting_result
from app.lib.macro.macro import consume_prime, consume_royal, consume_pure, skip


class MainWindow(tk.Tk):
    """
    メインウィンドウクラス

    Attributes:
        button (tk.Button): クリックするとon_button_click()メソッドが呼び出されるボタン
        label (tk.Label): ボタンを押すと表示されるテキストラベル
        dropdown (ttk.Combobox): ドロップダウンメニュー
        entry (tk.Entry): 繰り返し回数を入力するエントリ
    """

    CONFIG_FILE = "config.ini"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1246517307086475324/Rg4nTN3mjkrhed36Op9r_GoDPXpzlWVN5_fRA75CXrFOZHywjo5IeT0JDKVuH5Iv5jEO"

    def __init__(self):
        """
        ウィンドウを初期化する

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
        ウィジェットを作成し、配置する

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
        指定されたファイルを読み込むメソッド

        Args:
            filename (str): 読み込む設定ファイルの名前。
        Returns:
            None
        """
        with open(filename, 'r', encoding='utf-8') as file:
            self.config.read_file(file)

    def validate(self, value_if_allowed):
        """
        入力が有効かどうかを検証するメソッド

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
        ボタンがクリックされたときに実行されるメソッド

        Args:
            None
        Returns:
            None
        """
        self.label.config(text="錬成開始！")
        repetitions = int(self.entry.get())

        temp_dir = "temp"
        result_dir = "result"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # ウィンドウを切り替え
        pydirectinput.click(1, 1)

        dropdown_selection = self.dropdown.get()

        for i in range(repetitions):
            # 繰り返し回数の表示
            self.label.config(text=f"錬成中: {i + 1} / {repetitions}")
            self.update_idletasks()  # ラベルの更新を即座に反映

            if dropdown_selection == "おまかせ選択(自動選択)":
                consume_prime()
            elif dropdown_selection == "真・尖のみ使用":
                if i % 2 == 0:
                    consume_pure()
                else:
                    consume_prime()
            elif dropdown_selection == "真・王・尖のみ使用":
                cycle = i % 4
                if cycle == 0:
                    consume_royal()
                elif cycle == 1:
                    consume_pure()
                else:
                    consume_prime()

            time.sleep(1.65)
            file_name = self.save_screenshot(i + 1)
            success = get_crafting_result(file_name, i + 1)
            if success:
                print("Crafting result obtained successfully")
                result_path = os.path.join(result_dir, file_name)
                shutil.copy(os.path.join(temp_dir, file_name), result_path)
                self.send_to_discord(result_path)
            else:
                os.remove(os.path.join(temp_dir, file_name))
            time.sleep(0.5)
            skip()

        self.label.config(text="錬成終了！")

    def save_screenshot(self, index):
        """
        スクリーンショットを取得し、temp/result_<index>.pngとして保存するメソッド
        既にファイルが存在する場合は削除します

        Args:
            index (int): スクリーンショットのインデックス。
        Returns:
            str: 保存したファイル名
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

    def send_to_discord(self, file_path):
        """
        画像をDiscordに送信するメソッド

        Args:
            file_path (str): 送信する画像ファイルのパス。
        Returns:
            None
        """
        with open(file_path, 'rb') as f:
            response = requests.post(
                self.DISCORD_WEBHOOK_URL,
                files={'file': f},
                timeout=30  # タイムアウトを30秒に設定
            )
            if response.status_code == 204:
                print("Image sent to Discord successfully")
            else:
                print(
                    f"Failed to send image to Discord: {response.status_code}")

    def on_closing(self):
        """
        ウィンドウが閉じられるときに実行されるメソッド。選択状態を保存する

        Args:
            None
        Returns:
            None
        """
        self.config['settings'] = {'selection': self.dropdown.get()}
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        self.destroy()
