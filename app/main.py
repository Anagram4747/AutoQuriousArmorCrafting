"""
このモジュールは、GUIアプリケーションを起動するエントリーポイントを提供します。
"""

from app.gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
