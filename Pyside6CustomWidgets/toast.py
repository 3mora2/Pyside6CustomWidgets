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
        # self.setMinimumSize(QSize(*self.MinimumSize))
        # self.setMaximumSize(QSize(*self.MaximumSize))

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

    @property
    def layout_height(self):
        return self.layout.minimumSize().height()

    @property
    def layout_width(self):
        return self.layout.minimumSize().width()

    def center(self):
        if self.parent:

            toast_x = self.parent.x() + int((self.parent.width() - self.layout_width) / 2)
            toast_y = self.parent.y() + int((self.parent.height() - self.layout_height) / 2 + 40)
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      int((screen.height() - size.height()) / 2) + 40)

    def bottom(self):
        if self.parent:
            toast_x = self.parent.x() + int((self.parent.width() - self.layout_width) / 2)
            toast_y = self.parent.y() + int((self.parent.height() - self.layout_height))
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      int((screen.height() - size.height())))

    def top(self):
        if self.parent:
            toast_x = self.parent.x() + int((self.parent.width() - self.layout_width) / 2)
            toast_y = self.parent.y() + 40
            self.move(toast_x, toast_y)
        else:
            screen = QGuiApplication.primaryScreen().size()
            size = self.geometry()
            self.move(int((screen.width() - size.width()) / 2),
                      40)

    def init_ui(self, message):
        self.message_label = QLabel()
        if self.parent:
            self.message_label.setMaximumSize(self.parent.size())
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.size_policy = QSizePolicy()
        self.size_policy.setHorizontalStretch(0)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setHeightForWidth(self.message_label.sizePolicy().hasHeightForWidth())
        self.message_label.setSizePolicy(self.size_policy)
        self.message_label.setWordWrap(True)
        self.message_label.setText(message)
        self.message_label.setTextFormat(Qt.AutoText)
        self.message_label.setScaledContents(True)
        self.message_label.setObjectName("LabelMessage")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message_label)

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
