import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from Pyside6CustomWidgets import Toast, QToaster, AnimatedToggle


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('show Toast', self, clicked=self.show_toast))
        layout.addWidget(QPushButton('show Toaster', self, clicked=self.show_toaster))

        self.mainToggle = AnimatedToggle()
        self.mainToggle.setFixedSize(self.mainToggle.sizeHint())
        self.mainToggle.clicked.connect(lambda x: print("- checked"))
        layout.addWidget(self.mainToggle)
        self.lines = ["Pyside6 Toast"]

    def show_toast(self):
        Toast("\n".join(self.lines), parent=self, position="center").show()
        self.lines.append(f"line {len(self.lines)}"*len(self.lines))

    def show_toaster(self):
        t = QToaster()
        t.showMessage(
            self, "Pyside6 Toaster",
            QtWidgets.QStyle.SP_MessageBoxCritical,
            timeout=1000
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
