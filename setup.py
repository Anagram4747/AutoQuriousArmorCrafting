"""
このモジュールは、セットアップスクリプトを提供し、パッケージのメタデータとインストール設定を定義します。
"""

from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'configparser',
    ],
    entry_points={
        'console_scripts': [
            'app = app.main:main'
        ]
    },
)
