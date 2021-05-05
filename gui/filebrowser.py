# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-08 09:51:10
Modified : 2021-05-05 17:04:22

Comments : Functions related to file browsing, i.e. select the right year,
           month, day folders, and list the files inside.
"""

# %% IMPORTS

# -- global
import pysnooper
import locale
from datetime import datetime, date
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidgetItem, QStyle, QAbstractItemView

# -- local
import HAL.gui.fitting as fitting


# %% GLOBAL VARIABLES

YEAR_DISPLAY_FMT = "%Y"
MONTH_DISPLAY_FMT = "%m"
DAY_DISPLAY_FMT = "%d"
DEFAULT_LOCALE = "en_GB.UTF-8"

# %% TOOLS


class EmptyIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, _):
        return QtGui.QIcon()


def validateDateFormat(date_string, date_format):
    try:
        # temporary switch of time locale
        stored_locale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, DEFAULT_LOCALE)
        # if this fails, then format is bad
        date_object = datetime.strptime(date_string, date_format)
        # string back
        date_string_back = date_object.strftime(date_format)
        # restore
        locale.setlocale(locale.LC_TIME, stored_locale)
        # this is to ensuire zero paddings
        if date_string != date_string_back:
            raise ValueError
        return True
    except ValueError:
        locale.setlocale(locale.LC_TIME, stored_locale)
        return False


def convertDateFormat(date_string, date_format_in, date_format_out):
    # temporary switch of time locale
    stored_locale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, DEFAULT_LOCALE)
    # convert to date object
    date_object = datetime.strptime(date_string, date_format_in)
    # convert back to string
    date_string_out = date_object.strftime(date_format_out)
    # restore
    locale.setlocale(locale.LC_TIME, stored_locale)
    return date_string_out


# %% LOW LEVEL FUNCTIONS


def getSubfolders(folder_path, date_format):
    """
    analyzes folder, looking for subfolders with the right date format
    folder_path needs to be a pathlib.Path() object
    """
    # if the path does no correspond to a directory : return
    if not folder_path.is_dir():
        return []

    # browse folder content
    selected_content = []
    for content in folder_path.iterdir():
        if content.is_dir() and validateDateFormat(content.name, date_format):
            selected_content.append(content)

    return selected_content


def refreshListContent(list, folder, date_format, display_format):
    """
    Low-level function to refresh the content of the
    year / month / day lists
    """
    # clear current content
    list.clear()

    # analyze folder
    subdir_list = getSubfolders(folder, date_format)
    subdir_list.sort(reverse=False)

    # populate list
    for subdir in subdir_list:
        name = convertDateFormat(subdir.name, date_format, display_format)
        item = QListWidgetItem()
        item.setText(name)
        item.setData(Qt.UserRole, subdir)
        list.addItem(item)


def exploreDayFolder(folder):
    # -- check that a directory is provided
    if not folder.is_dir():
        return []

    # -- explore
    # get list of files and subdirs
    file_list = []
    subdir_list = []
    for content in folder.iterdir():
        if content.is_dir():
            # ignore hidden folders
            if content.name.startswith("."):
                continue
            # otherwise, append
            subdir_list.append(content)
        elif content.is_file():
            file_list.append(content)
    # sort
    file_list.sort(reverse=True)
    subdir_list.sort(reverse=True)
    # get subdirs content
    dir_content = []
    # include current dir
    dir_content.append({"name": ".", "path": folder, "file_list": file_list})
    # loop on subdirs
    for subdir in subdir_list:
        content = {"name": subdir.name, "path": subdir}
        file_list = []
        for file in subdir.iterdir():
            if file.is_file():
                # TODO : implement filer per type here !!
                # right now, only dummy filtering
                if file.suffix in [".png", ".atoms"]:
                    file_list.append(file)
        file_list.sort(reverse=True)
        content["file_list"] = file_list
        dir_content.append(content)

    return dir_content


# %% SETUP FUNCTIONS


def setupFileListBrowser(self):
    """Setup the file list browser (year, month, day)"""

    # -- definitions : setup root
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()

    # -- year
    # initialize year list
    year_fmt = conf["data"]["year folder"]
    refreshListContent(self.yearList, root, year_fmt, YEAR_DISPLAY_FMT)

    # scrollbar
    self.yearList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.yearList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- month
    # scrollbar
    self.monthList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.monthList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- day
    # scrollbar
    self.dayList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dayList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- run & seq list
    # selection mode
    self.runList.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.seqList.setSelectionMode(QAbstractItemView.ExtendedSelection)
    # icon size
    self.runList.setIconSize(QSize(15, 15))

    # -- calendar
    self.dateEdit.setCalendarPopup(True)
    self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
    self.dateEdit.setDisplayFormat("yyyy/MM/dd")


# %%  CALLBACKS


def yearListSelectionChanged(self):
    # if nothing seleted, return
    if not self.yearList.selectedItems():
        return
    # get selected year
    year = self.yearList.selectedItems()[0]
    year_dir = year.data(Qt.UserRole)
    # get month formatting
    conf = self.settings.config
    month_fmt = conf["data"]["month folder"]
    # refresh month list
    refreshListContent(self.monthList, year_dir, month_fmt, MONTH_DISPLAY_FMT)
    # clear day list
    self.dayList.clear()


def monthListSelectionChanged(self):
    # if nothing seleted, return
    if not self.monthList.selectedItems():
        return
    # get selected month
    month = self.monthList.selectedItems()[0]
    month_dir = month.data(Qt.UserRole)
    # get day formatting
    conf = self.settings.config
    day_fmt = conf["data"]["day folder"]
    # refresh day list
    refreshListContent(self.dayList, month_dir, day_fmt, DAY_DISPLAY_FMT)


def dayListSelectionChanged(self):
    # if nothing seleted, return
    if not self.dayList.selectedItems():
        return
    # -- get selected day
    day = self.dayList.selectedItems()[0]
    day_dir = day.data(Qt.UserRole)

    # -- update current folder
    refreshCurrentFolder(self, day_dir)

    # -- update calendar date
    # get selected
    year_str = self.yearList.selectedItems()[0].text()
    month_str = self.monthList.selectedItems()[0].text()
    day_str = self.dayList.selectedItems()[0].text()
    # get date
    year = datetime.strptime(year_str, YEAR_DISPLAY_FMT).year
    month = datetime.strptime(month_str, MONTH_DISPLAY_FMT).month
    day = datetime.strptime(day_str, DAY_DISPLAY_FMT).day
    # update
    new_date = QDate(year, month, day)
    self.dateEdit.blockSignals(True)
    self.dateEdit.setDate(new_date)
    self.dateEdit.blockSignals(False)


def runListSelectionChanged(self):
    """
    ATTENTION : this is just to handle the case where a sequence is selected,
    so that the whole sequence is then selected. File content should be handled
    by another function !
    """
    self.runList.blockSignals(True)
    # get selected
    selection = self.runList.selectedItems()
    # find dirs
    subdir_list = []
    for item in selection:
        data = item.data(Qt.UserRole)
        if data.is_dir():
            subdir_list.append(data)
            # unselect
            item.setSelected(False)

    # select dir content
    for i in range(self.runList.count()):
        item = self.runList.item(i)
        data = item.data(Qt.UserRole)
        if data.parent in subdir_list:
            item.setSelected(True)

    self.runList.blockSignals(False)


def todayButtonClicked(self):
    selected_date = date.today()
    updateDayBrowser(self, selected_date)


def dateEditClicked(self):
    # -- get selected date
    selected_date = self.dateEdit.date()  # QDate format
    selected_date = selected_date.toPyDate()  # datetime.date format
    updateDayBrowser(self, selected_date)


def updateDayBrowser(self, selected_date):
    """
    update the day browser by first changing year, month and day.
    """
    # -- update current path
    # get config
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()
    year_fmt = conf["data"]["year folder"]
    month_fmt = conf["data"]["month folder"]
    day_fmt = conf["data"]["day folder"]

    # new path
    year = selected_date.strftime(year_fmt)
    month = selected_date.strftime(month_fmt)
    day = selected_date.strftime(day_fmt)
    day_dir = root / year / month / day

    # -- update current folder
    refreshCurrentFolder(self, day_dir)

    # -- update file browser
    # year
    year_items = self.yearList.findItems(year, Qt.MatchExactly)
    if year_items:
        # note : the month list will automatically update !!
        self.dayList.blockSignals(True)
        self.yearList.setCurrentItem(year_items[0])
        self.dayList.blockSignals(False)
    else:
        # if year not found, we stop here !
        return

    # month
    month_items = self.monthList.findItems(month, Qt.MatchExactly)
    if month_items:
        # note : the day list will automatically update !!
        self.dayList.blockSignals(True)
        self.monthList.setCurrentItem(month_items[0])
        self.dayList.blockSignals(False)
    else:
        # if month not found, we stop here !
        return

    # day
    day_items = self.dayList.findItems(day, Qt.MatchExactly)
    if day_items:
        # note : we prevent the dayListSelectionChanged to be trigged
        self.dayList.blockSignals(True)
        self.dayList.setCurrentItem(day_items[0])
        self.dayList.blockSignals(False)


def refreshCurrentFolder(self, new_folder=None):
    # -- set new current folder
    if new_folder is not None:
        self.current_folder = new_folder
    if self.current_folder is None:
        return

    # -- get selected sequences and runs
    selected_sequences = [item.text() for item in self.seqList.selectedItems()]
    selected_runs = [
        item.data(Qt.UserRole) for item in self.runList.selectedItems()
    ]
    # handle case where "all" is selected
    if "[all]" in selected_sequences:
        selected_sequences = []

    # -- reset lists
    # block callbacks
    self.seqList.blockSignals(True)
    # clear
    self.runList.clear()
    self.seqList.clear()
    # add "all" to seqlist
    item = QListWidgetItem()
    item.setText("[all]")
    item.setData(Qt.UserRole, None)
    self.seqList.addItem(item)
    # unblock
    self.seqList.blockSignals(False)

    # -- check that the folder exists
    if not self.current_folder.is_dir():
        self.runList.addItems(["Folder does not exists"])
        return

    # -- get content and update list
    dir_content = exploreDayFolder(self.current_folder)

    for content in dir_content:
        # - skip if empty
        if not content["file_list"]:
            continue

        # - add subdir item
        # normal formatting > for seqList
        item = QListWidgetItem()
        item.setText(content["name"])
        item.setData(Qt.UserRole, content["path"])
        self.seqList.addItem(item)

        # stop here if not selected
        if selected_sequences and content["name"] not in selected_sequences:
            continue

        # special formatting > for runList
        item = QListWidgetItem()
        item.setText(content["name"])
        item.setData(Qt.UserRole, content["path"])
        item.setForeground(QColor(0, 0, 255))
        # https://joekuan.files.wordpress.com/2015/09/screen3.png
        item.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.runList.addItem(item)

        # - add files items
        n_files = len(content["file_list"])
        for i, file in enumerate(content["file_list"]):
            # good prefix
            if i == n_files - 1:
                prefix = "└─ "
            else:
                prefix = "├─ "

            # is there a fit ?
            suffix = ""
            if fitting.saved_fit_exist(self, file):
                # ideas for markers :
                # 🟩, ✳️ ✔️
                # see https://emojipedia.org
                suffix += " ✔️"

            # add item
            item = QListWidgetItem()
            # NB: use file.stem to remove ext
            item.setText(prefix + file.stem + suffix)
            item.setData(Qt.UserRole, file)
            self.runList.addItem(item)

    # -- restore selections
    for i in range(self.runList.count()):
        data = self.runList.item(i).data(Qt.UserRole)
        if data in selected_runs:
            self.runList.item(i).setSelected(True)
    self.seqList.blockSignals(True)
    for i in range(self.seqList.count()):
        name = self.seqList.item(i).text()
        if name in selected_sequences:
            self.seqList.item(i).setSelected(True)
    self.seqList.blockSignals(False)
