from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QListWidget, QListWidgetItem
from pathlib import Path

ICON_ROOT = Path(__file__).parent / "icons"
STYLES = r"""
    QListWidget{
        min-width: 294;
        background: none;
        font-size: 8pt;
        color: #eee;
    }
    QListWidget::item {
        width: 68;
        height: 68;
        border-radius: 2;
        margin: 4;
        padding: 8;
        background: #414851;
    }
    QListWidget::item::hover {
        background: #5A626C;
    }
"""


class ButtonGrid(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMovement(self.Static)  # The items cannot be moved by the user.
        self.setViewMode(self.IconMode)  # make items icons
        self.setResizeMode(self.Adjust)  # relayout when view is resized.
        self.setUniformItemSizes(True)  # better performance
        self.setIconSize(QSize(36, 36))
        self.setWordWrap(True)
        self.setStyleSheet(STYLES)

    def _get_icon(self, name):
        path = ICON_ROOT / f'{name.lower().replace(" ", "_")}.png'
        if not path.exists():
            return ""
        return str(path)

    def addItem(self, label: str):
        if isinstance(label, QListWidgetItem):
            super().addItem(label)
        super().addItem(QListWidgetItem(QIcon(self._get_icon(label)), label))

    def addItems(self, labels) -> None:
        for label in labels:
            self.addItem(label)
