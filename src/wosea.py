from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QMouseEvent
import time
import sys
import images


class MainWindow(QtWidgets.QWidget):
    # 窗口是否被锁定
    window_locked = True

    def __init__(self):
        """初始化窗口"""
        super().__init__()
        self.init_widget()
        self.init_tray_menu()
        # 创建定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(250)
        # 配置窗口属性
        self.setWindowOpacity(0.8)
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
        )

    def init_widget(self):
        """初始化窗口组件"""
        # 时间显示label
        self.time_label = QtWidgets.QLabel(
            "", self, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.time_label.setFont(QtGui.QFont("Microsoft YaHei", 18))
        # 窗口布局管理
        self.layout = QtWidgets.QVBoxLayout(self)
        # 安装组件
        self.layout.addWidget(self.time_label)

    def init_tray_menu(self):
        """初始化工具栏菜单"""
        # 菜单栏图标
        self.tray = QtWidgets.QSystemTrayIcon(self)
        self.tray.setIcon(QtGui.QIcon(":/icon.png"))
        # 菜单
        self.tray_menu = QtWidgets.QMenu()
        self.addTrayMenuAction("退出", self.exit)
        self.tray.setContextMenu(self.tray_menu)

    def addTrayMenuAction(self, text, callback):
        """添加托盘选项"""
        action = QtGui.QAction(text, self)
        action.triggered.connect(callback)
        self.tray_menu.addAction(action)

    def mouseMoveEvent(self, event: QMouseEvent):
        """跟踪鼠标移动"""
        # 如果窗口锁定就直接返回
        if self.window_locked:
            return
        if self._tracking:
            self._endPos = event.position().toPoint() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, event: QMouseEvent):
        """跟踪鼠标按下"""
        # 保存位置
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._startPos = QtCore.QPoint(event.position().x(), event.position().y())
            self._tracking = True
        # todo: 完成菜单显示

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """跟踪鼠标释放"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, _event: QMouseEvent):
        """双击窗口时锁定窗口"""
        self.window_locked = not self.window_locked

    @QtCore.Slot()
    def update_time(self):
        """更新时间"""
        self.time_label.setText(str(time.strftime("%H:%M:%S")))

    def show(self):
        """显示主窗口以及托盘图标"""
        self.tray.show()
        self.move(0, 0)
        super().show()

    def exit(self):
        self.close()
        self.destroy()
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
