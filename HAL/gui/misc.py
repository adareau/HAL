# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-05 10:24:37

Comments : miscellaneous functions, that would not fit anywhere else
"""

# %% IMPORTS
import logging
import time
import webbrowser
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


# %% TEXT WRAPPING


def wrap_text(text_in, max=50):
    words_in = text_in.split(" ")
    text_out = ""
    current_line = ""
    for w in words_in:
        if len(current_line) + len(w) + 1 > max:
            text_out += current_line + "\n"
            current_line = ""
        current_line += w + " "
    text_out += current_line
    return text_out


# %% MESSAGES


def dialog(self, title="error detected"):
    HAL_lines = [
        "Affirmative, Dave. I read you.",
        "I'm sorry, Dave. I'm afraid I can't do that.",
        "I think you know what the problem is just as well as I do.",
        "This mission is too important for me to allow you to jeopardize it.",
        "I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.",
    ]
    Dave_lines = [
        "Open the pod bay doors, HAL.",
        "What's the problem?",
        "What are you talking about, HAL?",
        "I don't know what you're talking about, HAL.",
        "Go back to work...",
    ]

    for h, d in zip(HAL_lines, Dave_lines):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle(title)
        box.setText(h)
        box.setStandardButtons(QMessageBox.Ok)
        button = box.button(QMessageBox.Ok)
        button.setText(d)
        box.exec_()


# %% KEY MANAGEMENT

# -- ACTIONS
def _konami(self):
    logger = logging.getLogger(__name__)
    logger.debug("KONAMI !!!!")
    konami_url = "https://www.youtube.com/watch?v=z9Uz1icjwrM"
    try:
        webbrowser.open_new_tab(konami_url)
        time.sleep(3)
        pyautogui.press("space")
    except Exception as e:
        logger.error(e)


def _dave(self):
    logger = logging.getLogger(__name__)
    logger.warning("I'm sorry Dave, I'm affraid I can't do that.")
    dave_url = "https://www.youtube.com/watch?v=7qnd-hdmgfk"
    try:
        webbrowser.open_new_tab(dave_url)
        time.sleep(3)
        pyautogui.press("space")
    except Exception as e:
        logger.error(e)


# -- SHORTHAND
UP = Qt.Key_Up
DW = Qt.Key_Down
LF = Qt.Key_Left
RG = Qt.Key_Right
A = Qt.Key_A
B = Qt.Key_B
D = Qt.Key_D
E = Qt.Key_E
V = Qt.Key_V
SHIFT = Qt.Key_Shift

# -- LINK
KEY_SEQUENCES = {
    (UP, UP, DW, DW, LF, RG, LF, RG, B, A): _konami,
    (SHIFT, D, A, V, E): _dave,
}


def analyse_keylog(self):
    """Analyse key log and trigger actions"""
    global KEY_SEQUENCES

    # -- get max length
    max_length = max([len(k) for k in KEY_SEQUENCES.keys()])

    # -- analyze key list

    # is it too long ?
    while len(self._kl) > max_length:
        self._kl = self._kl[1:]

    # convert to tuple
    kl = tuple(k for k in self._kl)

    # is it a defined key sequence ?
    lkl = len(kl)
    for seq in KEY_SEQUENCES.keys():
        lseq = len(seq)
        if kl[lkl - lseq :] == seq:
            KEY_SEQUENCES[seq](self)  # trigger action
            self._kl = []  # reset
            break
