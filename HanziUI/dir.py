import os, sys
import inspect

PROJECT_NAME = 'HanziUI'
MODULE_ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.dirname(MODULE_ROOT))

    return os.path.join(base_path, PROJECT_NAME, relative_path)


def database_path(database):
    return resource_path(os.path.join('database', database))


def user_path(database):
    return resource_path(os.path.join('user_home', database))


def ui_path(ui):
    return resource_path(os.path.join('templates', ui))
