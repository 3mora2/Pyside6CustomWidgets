# from http://www.liuyangdeboke.cn/?post=37

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import QTimer, Qt, QSize, QPropertyAnimation
from PySide6.QtGui import QGuiApplication, QPaintEvent, QPainter, QBrush


class Toast(QWidget):
    style = """#LabelMessage{color:white;font-family:Microsoft YaHei;}"""
    MinimumSize = (220, 100)
    MaximumSize = (220, 180)
    ContentsMargins = (20, -1, 20, -1)

    def __init__(self, message='', timeout=1500, parent=None, position="center", minimum_size=None, maximum_size=None,
                 contents_margins=None, **kwargs):
        """
        @param message: prompt message
        @param timeout: window display time
        @param parent: parent window control
        @param position: position of toast ("center", "top", "bottom")
        """
        super().__init__(parent)
        if minimum_size:
            self.MinimumSize = minimum_size
        if maximum_size:
            self.MaximumSize = maximum_size
        if contents_margins:
            self.ContentsMargins = contents_margins

        self.parent = parent
        self.timer = QTimer()
        # Since I don't know the end event of the animation, I use QTimer to close the window,
        # and close the window when the animation ends, so the event here should be the same as the animation time
        self.timer.singleShot(timeout, self.close)  # singleShot means that the timer will only start once
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Set the window to be transparent
        # ToDo: Adjust Size to message
        self.setMinimumSize(QSize(*self.MinimumSize))
        self.setMaximumSize(QSize(*self.MaximumSize))
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(*self.ContentsMargins)
        self.setLayout(self.layout)
        self.animation = None
        self.init_ui(message)
        self.create_animation(timeout)
        self.setStyleSheet(Toast.style)
        # Adjust position
        if position == "bottom":
            self.bottom()
        elif position == "top":
            self.top()
        else:
            self.center()

    def center(self):
        if self.parent:
            toast_x = self.parent.x() + int((self.parent.width() - self.width()) / 2)
            toast_y = self.parent.y() + int((self.parent.height() - self.height()) / 2 + 40)
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      int((screen.height() - size.height()) / 2) + 40)

    def bottom(self):
        if self.parent:
            toast_x = self.parent.x() + int((self.parent.width() - self.width()) / 2)
            toast_y = self.parent.y() + int((self.parent.height() - self.height()))
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      int((screen.height() - size.height())))

    def top(self):
        if self.parent:
            toast_x = self.parent.x() + int((self.parent.width() - self.width()) / 2)
            toast_y = self.parent.y() + 40
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      40)

    def init_ui(self, message):
        message_label = QLabel()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(message_label.sizePolicy().hasHeightForWidth())
        message_label.setSizePolicy(size_policy)
        message_label.setWordWrap(True)
        message_label.setText(message)
        message_label.setTextFormat(Qt.AutoText)
        message_label.setScaledContents(True)
        message_label.setObjectName("LabelMessage")
        message_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message_label)

    def create_animation(self, timeout):
        # 1. Define an animation
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setTargetObject(self)
        # 2. Set the attribute value
        self.animation.setStartValue(0)
        self.animation.setKeyValueAt(0.2, 0.7)  # 设置插值0.3 表示单本次动画时间的0.3处的时间点
        self.animation.setKeyValueAt(0.8, 0.7)  # 设置插值0.8 表示单本次动画时间的0.3处的时间点
        self.animation.setEndValue(0)
        # 3. Set the duration
        self.animation.setDuration(timeout)
        # 4. Start animation
        self.animation.start()

    def paintEvent(self, a0: QPaintEvent):
        qp = QPainter()
        qp.begin(self)  # Can't drop, otherwise it won't work
        qp.setRenderHints(QPainter.Antialiasing, True)  # anti-aliasing
        qp.setBrush(QBrush(Qt.black))
        qp.setPen(Qt.transparent)
        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        qp.drawRoundedRect(rect, 15, 15)
        qp.end()
