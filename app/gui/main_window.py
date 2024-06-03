"""
このモジュールは、mainwindowの内容を表します
"""

import tkinter as tk
from tkinter import ttk, simpledialog
import configparser
import time
import shutil
import os
import pyautogui
import pydirectinput
from app.lib.crafting_result.crafting_result import get_crafting_result
from app.lib.macro.macro import consume_prime, consume_royal, consume_pure, skip
from app.lib.service.discord.discord import send_to_discord, send_discord_message


class MainWindow(tk.Tk):
    """
    メインウィンドウクラス

    Attributes:
        button (tk.Button): クリックするとon_button_click()メソッドが呼び出されるボタン
        label (tk.Label): ボタンを押すと表示されるテキストラベル
        dropdown (ttk.Combobox): ドロップダウンメニュー
        entry (tk.Entry): 繰り返し回数を入力するエントリ
        discord_webhook_url (str): Discord Webhook URL
    """

    CONFIG_FILE = "config.ini"

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
        self.discord_webhook_url = ""
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
        default_repetitions = self.config.get(
            'settings', 'repetitions', fallback="1")
        self.entry.insert(0, default_repetitions)

        # Discord Webhook URL 設定ボタン
        self.webhook_button = tk.Button(
            self, text="Discord Web hook の設定", command=self.set_discord_webhook)
        self.webhook_button.pack(pady=10)

    def read_config(self, filename):
        """
        指定されたファイルを読み込むメソッド

        Args:
            filename (str): 読み込む設定ファイルの名前。
        Returns:
            None
        """
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                self.config.read_file(file)
        self.discord_webhook_url = self.config.get(
            'settings', 'DISCORD_WEBHOOK_URL', fallback="")

    def validate(self, value_if_allowed):
        """
        入力が有効かどうかを検証するメソッド

        Args:
            value_if_allowed (str): 入力された値。
        Returns:
            bool: 入力が有効ならTrue、無効ならFalse。
        """
        if value_if_allowed.isdigit() and 0 <= int(value_if_allowed) <= 100000:
            return True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "0")
        return False

    def on_button_click(self):
        """
        ボタンがクリックされたときに実行されるメソッド

        Args:
            None
        Returns:
            None
        """
        repetitions = int(self.entry.get())
        send_discord_message(self.discord_webhook_url, f"{repetitions}連開始します")

        temp_dir = "temp"
        result_dir = "result"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        if os.path.exists(result_dir):
            shutil.rmtree(result_dir)
        os.makedirs(result_dir)

        # ウィンドウを切り替え
        pydirectinput.click(1, 1)

        dropdown_selection = self.dropdown.get()

        for i in range(repetitions):
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
            file_name = self.save_screenshot(temp_dir, i + 1)

            success = get_crafting_result(
                os.path.join(temp_dir, file_name), i + 1)
            if success:
                print("Crafting result obtained successfully")
                shutil.copy(
                    os.path.join(temp_dir, file_name),
                    os.path.join(result_dir, file_name)
                )
                send_to_discord(
                    self.discord_webhook_url,
                    os.path.join(result_dir, file_name)
                )

            skip()
            os.remove(os.path.join(temp_dir, file_name))

            # 100回ごとに残りの回数を通知
            if (repetitions - i - 1) % 100 == 0 and repetitions - i - 1 != 0:
                send_discord_message(
                    self.discord_webhook_url, f"残り{repetitions - i - 1}連")

        send_discord_message(self.discord_webhook_url, "錬成終了！")

    def save_screenshot(self, output_dir, index):
        """
        スクリーンショットを取得し、指定されたディレクトリにresult_<index>.pngとして保存するメソッド
        既にファイルが存在する場合は削除します

        Args:
            output_dir (str): スクリーンショットを保存するディレクトリ。
            index (int): スクリーンショットのインデックス。
        Returns:
            str: 保存したファイル名
        """
        output_file_name = f"result_{index}.png"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        screenshot_path = os.path.join(output_dir, output_file_name)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        return output_file_name

    def set_discord_webhook(self):
        """
        Discord Webhook URLを設定するためのダイアログを表示するメソッド

        Args:
            None
        Returns:
            None
        """
        new_url = simpledialog.askstring(
            "Discord Webhook の設定",
            "Discord Webhook URLを入力してください:",
            initialvalue=self.discord_webhook_url
        )
        if new_url:
            self.discord_webhook_url = new_url
            self.config.set('settings', 'DISCORD_WEBHOOK_URL', new_url)
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)

    def on_closing(self):
        """
        ウィンドウが閉じられるときに実行されるメソッド。選択状態を保存する

        Args:
            None
        Returns:
            None
        """
        self.config['settings'] = {
            'selection': self.dropdown.get(),
            'repetitions': self.entry.get(),
            'DISCORD_WEBHOOK_URL': self.discord_webhook_url
        }
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        self.destroy()
