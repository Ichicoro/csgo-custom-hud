import sys
from enum import Enum
import yaml

from PyQt5 import QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar

from gsi.gsi_server import GSIDaemon

from utils import resource_path

config = {}
try:
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    config.setdefault("opacity", 0.4)
    config.setdefault("offset", 0)
except FileNotFoundError:
    print("No config.yaml found. Loading default config")


class WeaponState(Enum):
    ACTIVE = 1
    RELOADING = 2
    NO_AMMO_LEFT = 3
    NOT_GUN = 4


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(resource_path("overlay.ui"), self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        rect = QtWidgets.qApp.desktop().availableGeometry()
        rect.moveTop(200 + config["offset"])
        self.setWindowOpacity(config["opacity"])
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.size(), rect)
        )
        self.thread = GSIDaemon()
        self.thread._signal.connect(self.update_stats)
        self.thread.start()

    def update_stats(self, gamestate):
        self.set_current_hp(gamestate.player.state.health)
        self.set_current_armor(gamestate.player.state.armor, gamestate.player.state.helmet)

        weapon_state: WeaponState = WeaponState.NOT_GUN
        weapon_name: str = ""
        weapon_ammo_clip: int = 0
        weapon_clip_size: int = 0
        weapon_reserve: int = 0
        for weapon in gamestate.player.weapons.values():
            if weapon["state"] == "holstered":
                continue

            if weapon["type"] == "Knife":
                weapon_state = WeaponState.NOT_GUN
                weapon_name = "Knife"
            elif weapon["type"] == "C4":
                weapon_state = WeaponState.NOT_GUN
                weapon_name = "C4"
            else:
                weapon_name = weapon["name"]
                weapon_ammo_clip = weapon["ammo_clip"]
                weapon_clip_size = weapon["ammo_clip_max"]
                weapon_reserve = weapon["ammo_reserve"]
                weapon_state = WeaponState.NO_AMMO_LEFT if weapon_reserve == 0 else {
                    "reloading": WeaponState.RELOADING,
                    "active": WeaponState.ACTIVE
                }[weapon["state"]]

        self.set_weapon_data(weapon_state, weapon_name, weapon_ammo_clip, weapon_clip_size, weapon_reserve)

        self.repaint()

    def mousePressEvent(self, event):
        sys.exit(0)

    def set_current_hp(self, hp: int) -> None:
        currHP_label = self.findChild(QLabel, "currHP_label")
        currHP_label.setText(f"{hp}")
        HP_progressBar = self.findChild(QProgressBar, "HP_progressBar")
        HP_progressBar.setValue(hp)

    def set_current_armor(self, armor: int, has_helmet: bool = False) -> None:
        currarmor_label = self.findChild(QLabel, "currarmor_label")
        currarmor_label.setText(f"{armor}{' (H)' if has_helmet else ''}")
        armor_progressBar = self.findChild(QProgressBar, "armor_progressBar")
        armor_progressBar.setValue(armor)

    def set_weapon_data(self, state: WeaponState, weapon_label: str, clip: int, clip_max: int, reserve: int):
        self.setUpdatesEnabled(False)
        weapon_name_label = self.findChild(QLabel, "weapon_name_label")
        magammo_label = self.findChild(QLabel, "magammo_label")
        magsize_label = self.findChild(QLabel, "magsize_label")
        ammo_progressBar = self.findChild(QProgressBar, "ammo_progressBar")

        if state == WeaponState.ACTIVE:
            weapon_label = weapon_label.replace("weapon_", "").replace("_", " ").upper()
            weapon_name_label.setText(f"{weapon_label}")
            magammo_label.setText(f"{clip}")
            magsize_label.setText(f"{clip_max}")
            ammo_progressBar.setValue(clip)
            ammo_progressBar.setMaximum(clip_max)
        elif state == WeaponState.RELOADING:
            weapon_name_label.setText("[reloading]")
            magammo_label.setText("")
            magsize_label.setText("")
            ammo_progressBar.setValue(0)
            ammo_progressBar.setMaximum(0)
        elif state == WeaponState.NO_AMMO_LEFT:
            weapon_name_label.setText("[no ammo]")
            magammo_label.setText("")
            magsize_label.setText("")
            ammo_progressBar.setValue(100)
            ammo_progressBar.setMaximum(100)
        elif state == WeaponState.NOT_GUN:
            weapon_name_label.setText(weapon_label)
            magammo_label.setText("")
            magsize_label.setText("")
            ammo_progressBar.setValue(100)
            ammo_progressBar.setMaximum(100)
        self.setUpdatesEnabled(True)

    def set_teams_alive(self, ct_alive: int, t_alive: int):
        alive_t_label = self.findChild(QLabel, "alive_t_label")
        alive_ct_label = self.findChild(QLabel, "alive_ct_label")

        alive_t_label.setText(f"{t_alive} ALIVE")
        alive_ct_label.setText(f"{ct_alive} ALIVE")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec()
