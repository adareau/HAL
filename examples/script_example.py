# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2021-06-24 16:47:55

Comments : copy this script to the user script folder (~/.HAL/user_scripts)
"""

# the script is a standard python file
# you can import global python modules
import logging
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import Qt

# and also local modules from HAL
from HAL.gui.dataexplorer import getSelectionMetaDataFromCache

# you can of course write some python
logger = logging.getLogger(__name__)

# /!\/!\/!\
# in order to be imported as a user script, two "global" variables
# have to be defined: NAME and CATEGORY
NAME = "hello"  # display name, used in menubar and command palette
CATEGORY = "example"  # category (note that CATEGORY="" is a valid choice)


def main(self):
    """
    the script also have to define a `main` function. When playing a script,
    HAL runs `main` passes one (and only one) argument "self" that is the
    HAL mainwindow object (granting access to all the gui attributes and methods)
    """
    # - you have access to all the gui attributes
    version = self._version
    name = self._name
    url = self._url
    logger.warning(f"you're running {name} (v{version}), from {url}")

    # - you can ask user input via dialogs
    user_name, ok = QInputDialog.getText(
        self, "Hello there", "what's your name ?", text="Dave"
    )

    # - you can call methods from 'self'
    # go to today folder
    self._todayButtonClicked()

    # - you have access to all the gui elements !
    # the run list for instance (that's a QListWidget)
    runList = self.runList
    runList.blockSignals(True)  # block signals to prevent triggering callback
    for i in range(runList.count()):
        item = runList.item(i)  # get the items
        data = item.data(Qt.UserRole)  # the file path is stored in item.data()
        if data.is_file():  # data can be a folder or a file
            item.setSelected(True)  # if it is a file, selected it
    runList.blockSignals(False)  # unblock signals
    # lets toggle the last item now to trigger the "runListSelectionChanged" callback
    if runList.count() > 0:
        item.setSelected(False)
        item.setSelected(True)

    # - you can also call methods / functions imported from HAL
    # get metadata from current selection
    metadata = getSelectionMetaDataFromCache(self, update_cache=True)
    # let's plot file size vs file timestamp
    if metadata:
        fig = plt.figure()
        for dset, data in metadata.items():
            if "file" in data and {"timestamp", "size"} <= data["file"].keys():
                x = data["file"]["timestamp"]
                x = np.array([datetime.fromtimestamp(xx) for xx in x])
                y = data["file"]["size"]
                plt.plot(x, y, ":o", label=dset)
        plt.legend()
        plt.grid()
        plt.ylabel("file size")
        plt.xlabel("timestamp")
        plt.title(f"A nice figure for {user_name}")
        fig.autofmt_xdate()
        plt.show()
