# Pyside6CustomWidgets
Pyside6CustomWidgets Collect Custom widget in one place

### Install
```
pip install git+https://www.github.com/3mora2/Pyside6CustomWidgets@main
```

### Widgets

| Widget         |   |
|----------------|---|
| Toast          | ✔ |
| QToaster       | ✔ |
| AnimatedToggle | ✔ |



### Example:
```python
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

    def show_toast(self):
        Toast("Pyside6 Toast", parent=self, position="bottom").show()

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


```

Result:

![Result](https://raw.githubusercontent.com/3mora2/Pyside6CustomWidgets/main/doc/ezgif.com-video-to-gif.gif)
