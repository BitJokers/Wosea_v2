import requests
import sys
import os
import shutil
from PySide6 import QtWidgets
import zipfile


def download(remote_path: str, local_path: str) -> bool:
    """下载文件"""
    res = requests.get(remote_path)
    if not res.status_code == 200:
        return False
    else:
        with open(local_path, "wb") as f:
            f.write(res.content)
        return True


def download_new_version(remote_path) -> bool:
    """下载新版本文件"""
    return download(remote_path + "/version.txt", "./version.txt") and download(
        remote_path + "/new_version.zip", "./new_version.zip"
    )


def update(remote_path) -> bool:
    """更新版本"""
    if not download_new_version(remote_path):
        dlg = QtWidgets.QMessageBox(None)
        dlg.setWindowTitle("错误")
        dlg.setText("下载新版本文件失败")
        dlg.exec()
        os.remove("./version.txt")
        os.remove("./new_version.zip")
        return False
    shutil.rmtree("./bin")
    os.mkdir("./bin/")
    zip = zipfile.ZipFile("./new_version.zip")
    for file in zip.filelist:
        zip.extract(file, "./bin/")
    zip.close()
    os.remove("./new_version.zip")
    return True


def start():
    """启动主程序"""
    os.execl("./bin/wosea.exe", "./bin/wosea.exe", "")


def to_int(data: list[str]) -> list[int]:
    """转换版本号"""
    for i in range(0, len(data)):
        data[i] = int(data[i])
    return data


def get_local_version() -> list[int]:
    """获取本地版本号"""
    local_version = []
    try:
        with open("./version.txt", "r") as f:
            tmp = f.readline().strip()
            local_version = tmp.split(".")
    except FileNotFoundError:
        # 如果找不到版本文件就直接下载最新版本
        return [0, 0, 0]
    return to_int(local_version)


def get_remote_version(remote_path) -> list[int]:
    """获取服务器版本号"""
    res = requests.get(remote_path + "/version.txt")
    if not res.status_code == 200:
        # 如果版本检查失败就直接返回本地版本
        return get_local_version()
    else:
        return to_int(res.content.decode("utf-8").strip().split("."))


def main(remote_path):
    # 获取版本号
    local_version = get_local_version()
    remote_version = get_remote_version(remote_path)
    # 检查是否有更新
    flag = False
    for i in range(0, 3):
        if remote_version[i] > local_version[i]:
            flag = True
    # 更新
    if flag:
        dlg = QtWidgets.QMessageBox(None)
        dlg.setWindowTitle("有新的版本")
        dlg.setText("有新的版本可用,点击确认开始更新")
        dlg.exec()
        if update():
            dlg = QtWidgets.QMessageBox(None)
            dlg.setWindowTitle("消息")
            dlg.setText("更新成功")
            dlg.exec()
            start()
        else:
            dlg = QtWidgets.QMessageBox(None)
            dlg.setWindowTitle("错误")
            dlg.setText("更新失败,请联系开发者")
            dlg.exec()
            sys.exit(1)
    else:
        start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    os.mkdir("./bin")
    remote_path = None
    with open("dev_remote_path.txt", "r") as f:
        remote_path = f.readline().strip()
    main(remote_path)
