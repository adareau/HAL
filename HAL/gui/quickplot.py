# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03

Comments : Functions related to quick data analysis
"""

# %% IMPORTS

# -- global
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QInputDialog,
    QAbstractItemView,
    QStyle,
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QAction,
    QActionGroup,
    QToolButton,
)

# -- local
from . import dataexplorer

# -- logger
logger = logging.getLogger(__name__)


# %% TOOLS


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% SETUP FUNCTIONS


def setupUi(self):
    # -- data selection in quickplot
    # - X
    # define menu and selection group
    menuX = QMenu()
    actionGroupX = QActionGroup(menuX)
    actionGroupX.setExclusive(True)
    # store for future access
    self.quickPlotXToolButtonActionGroup = actionGroupX
    self.quickPlotXToolButton.actionGroup = actionGroupX
    # associate the menu with the corresponding toolbutton
    self.quickPlotXToolButton.setMenu(menuX)
    self.quickPlotXToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotXLabel.setText("no selection")
    self.quickPlotXToolButton.label = self.quickPlotXLabel

    # - Y
    # define menu and selection group
    menuY = QMenu()
    actionGroupY = QActionGroup(menuY)
    actionGroupY.setExclusive(True)
    # store for future access
    self.quickPlotYToolButtonActionGroup = actionGroupY
    self.quickPlotYToolButton.actionGroup = actionGroupY
    # associate the menu with the corresponding toolbutton
    self.quickPlotYToolButton.setMenu(menuY)
    self.quickPlotYToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotYLabel.setText("no selection")
    self.quickPlotYToolButton.label = self.quickPlotYLabel

    # - 2D X
    # define menu and selection group
    menu2DX = QMenu()
    actionGroup2DX = QActionGroup(menu2DX)
    actionGroup2DX.setExclusive(True)
    # store for future access
    self.quickPlot2DXToolButtonActionGroup = actionGroup2DX
    self.quickPlot2DXToolButton.actionGroup = actionGroup2DX
    # associate the menu with the corresponding toolbutton
    self.quickPlot2DXToolButton.setMenu(menu2DX)
    self.quickPlot2DXToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlot2DXLabel.setText("no selection")
    self.quickPlot2DXToolButton.label = self.quickPlot2DXLabel

    # - 2D Y
    # define menu and selection group
    menu2DY = QMenu()
    actionGroup2DY = QActionGroup(menu2DY)
    actionGroup2DY.setExclusive(True)
    # store for future access
    self.quickPlot2DYToolButtonActionGroup = actionGroup2DY
    self.quickPlot2DYToolButton.actionGroup = actionGroup2DY
    # associate the menu with the corresponding toolbutton
    self.quickPlot2DYToolButton.setMenu(menu2DY)
    self.quickPlot2DYToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlot2DYLabel.setText("no selection")
    self.quickPlot2DYToolButton.label = self.quickPlot2DYLabel

    # - 2D Z
    # define menu and selection group
    menu2DZ = QMenu()
    actionGroup2DZ = QActionGroup(menu2DZ)
    actionGroup2DZ.setExclusive(True)
    # store for future access
    self.quickPlot2DZToolButtonActionGroup = actionGroup2DZ
    self.quickPlot2DZToolButton.actionGroup = actionGroup2DZ
    # associate the menu with the corresponding toolbutton
    self.quickPlot2DZToolButton.setMenu(menu2DZ)
    self.quickPlot2DZToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlot2DZLabel.setText("no selection")
    self.quickPlot2DZToolButton.label = self.quickPlot2DZLabel

    # - FIT
    # define menu and selection group
    menuFit = QMenu()
    actionGroupFit = QActionGroup(menuFit)
    actionGroupFit.setExclusive(True)
    # populate menu
    submenu_dic = {}
    default_cat_name = "other"
    checked = True
    for fitClass in self.fit_classes_1D:
        # get fit category
        category = fitClass().category
        fitname = fitClass().short_name
        if category is None:
            category = default_cat_name
        # get or create submenu
        if category in submenu_dic:
            submenu = submenu_dic[category]
        else:
            submenu = menuFit.addMenu(category)
            submenu_dic[category] = submenu
        # add the corresponding action
        action = QAction(
            fitname,
            menuFit,
            checkable=True,
            checked=checked,
        )
        checked = False
        action.setData((category, fitname, fitClass))
        submenu.addAction(action)
        actionGroupFit.addAction(action)
    # update label
    current_action = actionGroupFit.checkedAction()
    if current_action is None:
        self.quickPlotFitLabel.setText("no selection")
    else:
        cat, name, _ = current_action.data()
        self.quickPlotFitLabel.setText(f"{cat} ⏵ {name}")
    # store for future access
    self.quickPlotFitToolButtonActionGroup = actionGroupFit
    self.quickPlotFitToolButton.actionGroup = actionGroupFit
    # associate the menu with the corresponding toolbutton
    self.quickPlotFitToolButton.setMenu(menuFit)
    self.quickPlotFitToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotFitToolButton.label = self.quickPlotFitLabel


# %% CALLBACKS


def quickPlotSelectionChanged(self):
    """Called when the quickPlot ToolButtons selection is changed"""
    # -- refresh string
    tool_buttons = [
        self.quickPlotXToolButton,
        self.quickPlotYToolButton,
        self.quickPlot2DXToolButton,
        self.quickPlot2DYToolButton,
        self.quickPlot2DZToolButton,
    ]
    for button in tool_buttons:
        # get action group
        actionGroup = button.actionGroup
        # currently checked action
        current_action = actionGroup.checkedAction()
        if current_action is None:
            button.label.setText("no selection")
        else:
            name, par_name = current_action.data()
            button.label.setText(f"{name} ⏵ {par_name}")


def quickPlotFitSelectionChanged(self):
    """Called when the quickPlotFitToolButton selection is changed"""
    # -- refresh string
    button = self.quickPlotFitToolButton
    # get action group
    actionGroup = button.actionGroup
    # currently checked action
    current_action = actionGroup.checkedAction()
    if current_action is None:
        button.label.setText("no selection")
    else:
        cat, name, _ = current_action.data()
        button.label.setText(f"{cat} ⏵ {name}")


def refreshMetaDataList(self):
    """
    Updates all the quickplot elements that allow the selection of metadata
    """
    # -- get data
    metadata_list = self.available_numeric_metadata

    # -- tool buttons
    tool_buttons = [
        self.quickPlotXToolButton,
        self.quickPlotYToolButton,
        self.quickPlot2DXToolButton,
        self.quickPlot2DYToolButton,
        self.quickPlot2DZToolButton,
    ]
    for button in tool_buttons:
        # get action group
        actionGroup = button.actionGroup
        # currently checked action
        current_action = actionGroup.checkedAction()
        if current_action is not None:
            current_data = current_action.data()
        else:
            current_data = ("", "")
        # get menu and clear
        menu = button.menu()
        menu.clear()
        # remove all actions
        for action in actionGroup.actions():
            actionGroup.removeAction(action)
        # populate
        for name, param_list in metadata_list.items():
            # if empty list : stop
            if not param_list:
                continue
            # add submenu, and populate
            submenu = menu.addMenu(name)
            for par_name in sorted(param_list):
                action = QAction(
                    par_name,
                    menu,
                    checkable=True,
                    checked=current_data == (name, par_name),
                )
                action.setData((name, par_name))
                submenu.addAction(action)
                actionGroup.addAction(action)
        # update label
        current_action = actionGroup.checkedAction()
        if current_action is None:
            button.label.setText("no selection")
        else:
            name, par_name = current_action.data()
            button.label.setText("%s ⏵ %s" % (name, par_name))


# %% PLOT FUNCTIONS


def plotData(self):
    """
    PLACEHOLDER : Plotting the selected metadata
    """
    # -- load metadata
    # get selected metadata fields
    checkedDataX = self.quickPlotXToolButton.actionGroup.checkedAction()
    checkedDataY = self.quickPlotYToolButton.actionGroup.checkedAction()
    if None in [checkedDataX, checkedDataY]:
        logger.debug("plotData() : data selection missing")
        return

    # get data names
    # it is stored in the data() field of the quickPlot ToolButtons actions
    # in the form (meta_data_name, parameter_name)
    x_data_name = checkedDataX.data()
    y_data_name = checkedDataY.data()

    # load metadata
    metadata = dataexplorer.getSelectionMetaDataFromCache(self)
    if len(metadata) == 0:
        logger.debug("plotData() : no dataset selected")
        return

    # -- PLOT
    # - prepare figure
    # FIXME : allow for new figure / hold on control via GUI
    if self.current_fig is None:
        fig, ax = plt.subplots(1, 1)
        self.current_fig = (fig, ax)
    else:
        fig, ax = self.current_fig
        if not plt.fignum_exists(fig.number):
            fig, ax = plt.subplots(1, 1)
            self.current_fig = (fig, ax)

    # - loop on sets
    x_timestamp = False
    fit_results = {}
    for set, data in metadata.items():
        # - filter data
        # get data
        x_raw = data[x_data_name[0]][x_data_name[1]]
        y_raw = data[y_data_name[0]][y_data_name[1]]
        # remove non numeric values
        x_filtered = []
        y_filtered = []
        for i, (x, y) in enumerate(zip(x_raw, y_raw)):
            if not _isnumber(x) or not _isnumber(y):
                continue
            x_filtered.append(float(x))
            y_filtered.append(float(y))

        # if empty : continue
        if not x_filtered:
            continue

        x_filtered = np.array(x_filtered)
        y_filtered = np.array(y_filtered)

        # sort
        isort = np.argsort(x_filtered)
        x_filtered = x_filtered[isort]
        y_filtered = y_filtered[isort]

        # - is x a timestamp ?
        x_meta, x_name = x_data_name
        x_info = data[x_meta].get("_%s_info" % x_name, None)
        if x_info is not None:
            special = x_info.get("special", None)
            if special == "timestamp":
                x_filtered = [datetime.fromtimestamp(t) for t in x_filtered]
                x_timestamp = True

        # - plot
        if self.quickPlotEnableFitBox.isChecked():
            fmt = "o"
        else:
            fmt = ":o"
        (line,) = ax.plot(x_filtered, y_filtered, fmt, label=set)

        # - fit
        if self.quickPlotEnableFitBox.isChecked():
            # get current fit class
            current_action = self.quickPlotFitToolButtonActionGroup.checkedAction()
            if current_action is not None:
                # init the fit object
                _, _, FitClass = current_action.data()
                fit = FitClass(x=x_filtered, z=y_filtered)
                # do the fit
                fit.do_guess()
                fit.do_fit()
                # prepare to plot
                xfit = np.linspace(x_filtered.min(), x_filtered.max(), 500)
                yfit = fit.eval(xfit)
                color = line.get_color()
                # plot
                ax.plot(xfit, yfit, color=color, label=None)
                # get x information
                x_meta, x_name = x_data_name
                x_info = data[x_meta].get("_%s_info" % x_name, None)
                if x_info is not None:
                    unit = x_info.get("unit", "")
                    fit.x_unit = unit

                # get y information
                y_meta, y_name = y_data_name
                y_info = data[y_meta].get("_%s_info" % y_name, None)
                if y_info is not None:
                    unit = y_info.get("unit", "")
                    fit.z_unit = unit

                # store results
                fit.compute_values()
                fit_results[set] = fit.values
                fit_results["__fit__"] = fit

    # - figure setup
    # x label
    x_meta, x_name = x_data_name
    x_label = "%s - %s" % x_data_name
    x_info = data[x_meta].get("_%s_info" % x_name, None)
    if x_info is not None:
        unit = x_info.get("unit", "")
        if unit:
            x_label += " (%s)" % unit
    ax.set_xlabel(x_label)

    # y label
    y_meta, y_name = y_data_name
    y_label = "%s - %s" % y_data_name
    y_info = data[y_meta].get("_%s_info" % y_name, None)
    if y_info is not None:
        unit = y_info.get("unit", "")
        if unit:
            y_label += " (%s)" % unit
    ax.set_ylabel(y_label)

    # timestamps ?
    if x_timestamp:
        fig.autofmt_xdate()

    # grid and legend
    plt.grid()
    plt.legend()

    # show
    fig.canvas.draw()
    plt.show()

    # -- print fit results
    dataexplorer.display1DFitResults(self, fit_results)


def plotData2D(self):
    """
    PLACEHOLDER : Plotting the selected metadata
    """
    # -- load metadata
    # get selected metadata fields
    checkedDataX = self.quickPlot2DXToolButton.actionGroup.checkedAction()
    checkedDataY = self.quickPlot2DYToolButton.actionGroup.checkedAction()
    checkedDataZ = self.quickPlot2DZToolButton.actionGroup.checkedAction()
    if None in [checkedDataX, checkedDataY, checkedDataZ]:
        logger.debug("plotData() : data selection missing")
        return

    # get data names
    # it is stored in the data() field of the quickPlot ToolButtons actions
    # in the form (meta_data_name, parameter_name)
    x_data_name = checkedDataX.data()
    y_data_name = checkedDataY.data()
    z_data_name = checkedDataZ.data()

    # load metadata
    metadata = dataexplorer.getSelectionMetaDataFromCache(self)
    if len(metadata) == 0:
        logger.debug("plotData() : no dataset selected")
        return

    # -- PLOT

    # - loop on sets
    x_timestamp = False

    for set, data in metadata.items():
        # - filter data
        # get data
        x_raw = data[x_data_name[0]][x_data_name[1]]
        y_raw = data[y_data_name[0]][y_data_name[1]]
        z_raw = data[z_data_name[0]][z_data_name[1]]
        # remove non numeric values
        x_filtered = []
        y_filtered = []
        z_filtered = []
        for i, (x, y, z) in enumerate(zip(x_raw, y_raw, z_raw)):
            if not _isnumber(x) or not _isnumber(y) or not _isnumber(z):
                continue
            x_filtered.append(float(x))
            y_filtered.append(float(y))
            z_filtered.append(float(z))

        # if empty : continue
        if not x_filtered:
            continue

        x_filtered = np.array(x_filtered)
        y_filtered = np.array(y_filtered)
        z_filtered = np.array(z_filtered)

        # - is x a timestamp ?
        x_meta, x_name = x_data_name
        x_info = data[x_meta].get(f"_{x_name}_info", None)
        if x_info is not None:
            special = x_info.get("special", None)
            if special == "timestamp":
                x_filtered = [datetime.fromtimestamp(t) for t in x_filtered]
                x_timestamp = True

        # - plot
        df_raw = pd.DataFrame()

        x_meta, x_name = x_data_name
        xlabel = f"{x_meta} - {x_name}"
        x_info = data[x_meta].get(f"_{x_name}_info", None)
        if x_info is not None:
            unit = x_info.get("unit", "")
            if unit:
                xlabel += f" ({unit})"

        y_meta, y_name = y_data_name
        ylabel = f"{y_meta} - {y_name}"
        y_info = data[y_meta].get(f"_{y_name}_info", None)
        if y_info is not None:
            unit = y_info.get("unit", "")
            if unit:
                ylabel += f" ({unit})"

        z_meta, z_name = z_data_name
        zlabel = f"{z_meta} - {z_name}"
        z_info = data[z_meta].get(f"_{z_name}_info", None)
        if z_info is not None:
            unit = z_info.get("unit", "")
            if unit:
                zlabel += f" ({unit})"

        df_raw[xlabel] = x_filtered
        df_raw[ylabel] = y_filtered
        df_raw[zlabel] = z_filtered
        datasize = len(df_raw)

        data_stacked = df_raw.groupby([xlabel, ylabel], as_index=False).mean()
        data_stacked["std"] = (
            df_raw.groupby([xlabel, ylabel], as_index=False).std()[zlabel]
            / data_stacked[zlabel]
        )
        data_stacked["size"] = df_raw.groupby([xlabel, ylabel], as_index=False).size()[
            "size"
        ]
        data_stacked["fmt_std"] = data_stacked["std"].combine(
            data_stacked["size"],
            lambda std, num: f"{round(100*std,1)} ({num})",
        )
        data_stacked = data_stacked.round(3)

        data_avg_pivotted = data_stacked.pivot(ylabel, xlabel, zlabel)

        data_std_pivotted = data_stacked.pivot(ylabel, xlabel, "std")
        data_fmt_std_pivotted = data_stacked.pivot(ylabel, xlabel, "fmt_std")

    if self.quickPlot2DEnableStdBox.isChecked():
        # probably exists a cleaner way to manage the 1 subplot / 2 subplots cases
        if len(data_stacked.groupby(xlabel)) >= len(data_stacked.groupby(ylabel)):
            fig, axs = plt.subplots(2, 1)
        else:
            fig, axs = plt.subplots(1, 2)
        sns.heatmap(
            data_avg_pivotted,
            cmap="mako",
            annot=True,
            linewidths=0.5,
            cbar=False,
            ax=axs[0],
        )
        axs[0].set_title(data_stacked[zlabel].name, fontweight="bold")

        sns.heatmap(
            data_std_pivotted,
            cmap="mako",
            annot=data_fmt_std_pivotted,
            fmt="",
            linewidths=0.5,
            cbar=False,
            ax=axs[1],
        )
        axs[1].set_title(
            data_stacked["std"].name + " in % (sample size)",
            fontweight="bold",
        )

    else:

        def formater(avg, std):
            if not np.isnan(std):
                return format(avg, ".2E") + f" ({round(100*std,1)}%)"
            else:
                return format(avg, ".2E")

        data_stacked["fmt_avg"] = data_stacked[zlabel].combine(
            data_stacked["std"],
            formater,
        )
        data_fmt_avg_pivotted = data_stacked.pivot(ylabel, xlabel, "fmt_avg")
        fig, ax = plt.subplots()
        sns.heatmap(
            data_avg_pivotted,
            cmap="mako",
            annot=data_fmt_avg_pivotted,
            fmt="",
            linewidths=0.5,
            cbar=False,
            ax=ax,
        )
        ax.set_title(data_stacked[zlabel].name, fontweight="bold")

    fig.suptitle(
        f"Dataset: {datasize} runs | Average data/cell: {round(datasize/data_stacked.notna()[zlabel].sum(),2)}",
        fontweight="bold",
    )

    plt.tight_layout()
    plt.show()
