import os
import sys
import json

from qtpy import QtWidgets, QtGui

from ayon_common.resources import (
    get_icon_path,
    load_stylesheet,
)
from ayon_common.ui_utils import get_qt_app


class MessageWindow(QtWidgets.QDialog):
    default_width = 410
    default_height = 170

    def __init__(
        self, message, installer_path, parent=None
    ):
        super().__init__(parent)

        icon_path = get_icon_path()
        icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle("AYON-launcher distribution issue")

        self._first_show = True

        info_label = QtWidgets.QLabel(message, self)
        info_label.setWordWrap(True)

        installer_path_label = None
        if installer_path and os.path.exists(installer_path):
            installer_path_label = QtWidgets.QLabel(
                (
                    "NOTE: Setup can be found"
                    f" <a href=\"file:///{installer_path}\">"
                    f"{installer_path}</a>"
                ),
                self
            )

        btns_widget = QtWidgets.QWidget(self)
        confirm_btn = QtWidgets.QPushButton("Close", btns_widget)

        btns_layout = QtWidgets.QHBoxLayout(btns_widget)
        btns_layout.setContentsMargins(0, 0, 0, 0)
        btns_layout.addStretch(1)
        btns_layout.addWidget(confirm_btn, 0)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(info_label, 0)
        main_layout.addStretch(1)
        if installer_path_label:
            main_layout.addWidget(installer_path_label, 0)
        main_layout.addWidget(btns_widget, 0)

        confirm_btn.clicked.connect(self._on_confirm_click)

        self._confirm_btn = confirm_btn

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self._on_first_show()
        self._recalculate_sizes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recalculate_sizes()

    def _recalculate_sizes(self):
        hint = self._confirm_btn.sizeHint()
        new_width = max((hint.width(), hint.height() * 3))
        self._confirm_btn.setMinimumWidth(new_width)

    def _on_first_show(self):
        self.setStyleSheet(load_stylesheet())
        self.resize(self.default_width, self.default_height)

    def _on_confirm_click(self):
        self.accept()
        self.close()


def main():
    """Show message that server does not have set bundle to use.

    It is possible to pass url as argument to show it in the message. To use
        this feature, pass `--url <url>` as argument to this script.
    """

    filepath = sys.argv[-1]
    with open(filepath, "r") as stream:
        data = json.load(stream)

    app = get_qt_app()
    window = MessageWindow(data["message"], data["installer_path"])
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
