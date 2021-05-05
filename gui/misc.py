# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-05 10:24:37
Modified : 2021-05-05 10:59:18

Comments : miscellaneous functions, that would not fit anywhere else
"""

# %% IMPORTS
from PyQt5.QtCore import Qt


# %% KEY MANAGEMENT

# -- ACTIONS
def _konami(self):
    print("KONAMI !!!!!")


def _dave(self):
    print("I'm sorry Dave, I'm affraid I can't do that.")


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
    """ Analyse key log and trigger actions"""
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
        if kl[lkl - lseq:] == seq:
            KEY_SEQUENCES[seq](self)  # trigger action
            self._kl = []  # reset
            break