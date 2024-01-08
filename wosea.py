from PySide6 import QtCore, QtWidgets, QtGui
import time


class MainWindow(QtWidgets.QWidget):
    window_locked = False

    def __init__(self):
        """构造函数."""
        super().__init__()
        self.init_widget()
        self.init_tray_menu()

        # 移动窗口至左上角并锁定
        self.move(0, 0)
        self.window_locked = True

        # 创建计时器
        self.timer = QtCore.QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(self.update_time)

        # 设置窗口属性
        # 窗口透明度
        self.setWindowOpacity(0.8)
        # 窗口标志(始终位于顶层,无边框,工具层)
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
        )

    def init_widget(self):
        """初始化控件."""
        # 布局
        self.layout = QtWidgets.QVBoxLayout(self)
        # 控件
        # 时间Label
        self.time_label = QtWidgets.QLabel(
            "", self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.time_label.setFont(QtGui.QFont("Microsoft YaHei", 20))
        # 添加控件
        self.layout.addWidget(self.time_label)

    def init_tray_menu(self):
        self.tray = QtWidgets.QSystemTrayIcon(self)
        self.tray.setIcon(QtGui.QIcon(":/logo/icon.png"))
        self.tray_menu = QtWidgets.QMenu()
        # TODO: 完成托盘菜单
        self.tray.setContextMenu(self.tray_menu)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """鼠标移动事件"""
        if self.window_locked:
            return
        if self._tracking:
            self._endPos = event.position().toPoint() - self._startPos
            self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """鼠标释放事件"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """鼠标按下事件"""
        # 保存位置
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._startPos = QtCore.QPoint(event.position().x(), event.position().y())
            self._tracking = True
        # 显示主菜单
        # TODO: 完成菜单显示

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        """双击窗口时锁定窗口"""
        self.window_locked = not self.window_locked

    def show(self):
        super().show()
        self.tray.show()

    def update_time(self):
        self.time_label.setText(time.strftime("%H:%M:%S"))


def main():
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
