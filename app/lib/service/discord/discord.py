"""
このモジュールは、Discord Web hookへのリクエスト送信処理を提供します
"""

import requests


def send_to_discord(discord_webhook_url, file_path):
    """
    画像をDiscordに送信するメソッド

    Args:
            discord_webhook_url (str): Discord Web hook のURL
        file_path (str): 送信する画像ファイルのパス。
    Returns:
        None
    """
    with open(file_path, 'rb') as f:
        requests.post(
            discord_webhook_url,
            files={'file': f},
            timeout=30  # タイムアウトを30秒に設定
        )


def send_discord_message(discord_webhook_url, message):
    """
        Discordにメッセージを送信するメソッド

        Args:
            discord_webhook_url (str): Discord Web hook のURL
            message (str): 送信するメッセージ
        Returns:
            None
        """
    requests.post(
        discord_webhook_url,
        json={'content': message},
        headers={'Content-Type': 'application/json'},
        timeout=10  # タイムアウトを10秒に設定
    )
