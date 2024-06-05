"""
このモジュールは、Discord Web hookへのリクエスト送信処理を提供します
"""

import requests


def send_to_discord(discord_webhook_url, file_path, message="send_to_discord"):
    """
    画像をDiscordに送信するメソッド

    Args:
        discord_webhook_url (str): Discord Web hook のURL
        file_path (str): 送信する画像ファイルのパス。
        message (str): 送信するメッセージ。
    Returns:
        None
    """
    with open(file_path, 'rb') as f:
        requests.post(
            discord_webhook_url,
            files={'file': f},
            data={'content': message},
            timeout=30  # タイムアウトを30秒に設定
        )


def send_discord_message(discord_webhook_url, message="send_discord_message"):
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
        timeout=30  # タイムアウトを10秒に設定
    )
