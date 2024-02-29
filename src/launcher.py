import requests as re
import simplejson as json
from PySide6 import QtGui, QtWidgets, QtCore
import rtoml


def download_file(remote_path: str, local_path: str) -> (int, bool):
    """下载文件,并返回响应码和是否成功下载的指示."""
    try:
        # 远程部分
        response = re.get(remote_path)
        if not response.status_code == 200:
            return (response.status_code, False)
        data = response.content
        response.close()
        # 本地部分
        with open(local_path, "wb") as f:
            f.write(data)
    except Exception:
        return (-1, False)
    finally:
        response.close()
        f.close()


def load_config(config_path: str) -> (dict[str, any], bool):
    """加载并检查配置文件项"""
    try:
        config = rtoml.load(config_path)
        # TODO: 检查配置项
        return (config, True)
    except Exception:
        return (None, False)


def check_update(remote_path: str, local_version: list[int]) -> (list[int], bool):
    """检查更新"""
    pass


def start():
    """启动主程序"""
    pass


def main(config_path: str):
    config = load_config(config_path)
    # 检查更新
    if config["core"]["update"]["enable"]:
        result = check_update(config["core"]["update"]["remote_path"])
        if result[1]:
            dlg = QtWidgets.QMessageBox(None)
            dlg.setWindowTitle("自动更新")
            dlg.setText(
                '发现新的版本"{}",点击确定开始更新.'.format(
                    "{0}.{1}.{2}".format(result[0][0], result[0][1], result[0][1])
                )
            )
            dlg.exec()
        else:
            start()
