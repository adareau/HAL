# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03

Comments : Functions related to quick data analysis
"""

# %% IMPORTS
# -- global
import typing
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import interpolate
from datetime import datetime
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QAbstractItemView,
    QStyle,
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QAction,
    QActionGroup,
    QToolButton,
    QWidget,
)
import PySimpleGUI as sg

# -- local
from . import dataexplorer
from .PlottingOptionsUI import Ui_plottingOptionsWindow

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
class PlottingOptionsWindow(QMainWindow, Ui_plottingOptionsWindow):
    def __init__(self) -> None:
        super(PlottingOptionsWindow, self).__init__()

        self.setupUi(self)


sg.theme("LightGrey1")


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

    # - Plotby
    # define menu and selection group
    menuPlotby = QMenu()
    actionGroupPlotby = QActionGroup(menuPlotby)
    actionGroupPlotby.setExclusive(True)
    # store for future access
    self.quickPlotPlotbyToolButtonActionGroup = actionGroupPlotby
    self.quickPlotPlotbyToolButton.actionGroup = actionGroupPlotby
    # associate the menu with the corresponding toolbutton
    self.quickPlotPlotbyToolButton.setMenu(menuPlotby)
    self.quickPlotPlotbyToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotPlotbyLabel.setText("no selection")
    self.quickPlotPlotbyToolButton.label = self.quickPlotPlotbyLabel

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
        self.quickPlotPlotbyToolButton,
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
        self.quickPlotPlotbyToolButton,
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
            button.label.setText(f"{name} ⏵ {par_name}")


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

    if self.quickPlotPlotByBox.isChecked():
        plot_by = True
        checkedDataPlotBy = self.quickPlotPlotbyToolButton.actionGroup.checkedAction()
        if checkedDataPlotBy is None:
            logger.warning("plotData() : data selection missing")
            return
        (category, variable) = checkedDataPlotBy.data()
        subsets_values = np.unique(metadata["current selection"][category][variable])
        number_of_subsets = len(subsets_values)
    else:
        plot_by = False

    # sequences_list = np.unique(metadata["current selection"]["file"]["parent"])
    # number_of_sequences = len(sequences_list)

    for set, data in metadata.items():
        # - filter data
        # get data
        if plot_by is False:
            x_raw = [data[x_data_name[0]][x_data_name[1]]]
            y_raw = [data[y_data_name[0]][y_data_name[1]]]
        elif plot_by is True:
            x_raw = [[]] * number_of_subsets
            y_raw = [[]] * number_of_subsets
            for k in range(number_of_subsets):
                x_raw[k] = np.array(data[x_data_name[0]][x_data_name[1]])[
                    np.array(data[category][variable]) == subsets_values[k]
                ]
                y_raw[k] = np.array(data[y_data_name[0]][y_data_name[1]])[
                    np.array(data[category][variable]) == subsets_values[k]
                ]
            pass

        # remove non numeric values
        x_filtered = [[]] * len(x_raw)
        y_filtered = [[]] * len(x_raw)
        for k in range(len(x_raw)):
            x_filtered[k] = []
            y_filtered[k] = []

            for i, (x, y) in enumerate(zip(x_raw[k], y_raw[k])):
                if not _isnumber(x) or not _isnumber(y):
                    continue
                x_filtered[k].append(float(x))
                y_filtered[k].append(float(y))

        # if empty : continue
        isort = [[]] * len(x_raw)
        for k in range(len(x_raw)):
            if not x_filtered[k]:
                continue
            x_filtered[k] = np.array(x_filtered[k])
            y_filtered[k] = np.array(y_filtered[k])

            # sort
            isort[k] = np.argsort(x_filtered[k])
            x_filtered[k] = x_filtered[k][isort[k]]
            y_filtered[k] = y_filtered[k][isort[k]]

        # - is x a timestamp ?
        x_meta, x_name = x_data_name
        x_info = data[x_meta].get("_%s_info" % x_name, None)
        if x_info is not None:
            special = x_info.get("special", None)
            if special == "timestamp":
                for k in range(len(x_raw)):
                    x_filtered[k] = [datetime.fromtimestamp(t) for t in x_filtered[k]]
                x_timestamp = True

        # - plot
        if self.quickPlotEnableFitBox.isChecked():
            fmt = "o"
        else:
            fmt = ":o"
        for k in range(len(x_raw)):
            if plot_by is False:
                plot_label = set
                if set == "current selection":
                    y_meta, y_name = y_data_name
                    plot_label = y_name

            elif plot_by is True:
                plot_label = str(variable) + " " + str(subsets_values[k])
            (line,) = ax.plot(x_filtered[k], y_filtered[k], fmt, label=plot_label)

        # - fit
        if self.quickPlotEnableFitBox.isChecked():
            # get current fit class
            current_action = self.quickPlotFitToolButtonActionGroup.checkedAction()

            if len(x_raw) == 1:
                x_filtered = x_filtered[0]
                y_filtered = y_filtered[0]
            elif len(x_raw) != 1:
                logger.warning("Select one sequence or disable plot by seq")
                return

            if current_action is not None:
                # init the fit object
                _, _, FitClass = current_action.data()
                fit = FitClass(x=x_filtered, z=y_filtered)
                # do the fit
                fit.do_guess()
                if self.settings.config["fit"]["custom guess"] == "true":
                    p0guess = "not used"
                    p1guess = "not used"
                    p2guess = "not used"
                    p3guess = "not used"
                    p4guess = "not used"
                    l1 = [
                        [
                            sg.Text("Fit name", font="Helvetica 10 bold"),
                            sg.Text("gaussian", font="Helvetica 10", key="fit name"),
                        ],
                        [
                            sg.Text("Fit formula", font="Helvetica 10 bold"),
                            sg.Text("f(x) = 0", font="Helvetica 10", key="fit formula"),
                        ],
                        [
                            sg.Text("Fit parameters", font="Helvetica 10 bold"),
                            sg.Text(
                                "[a,b,c]", font="Helvetica 10", key="fit parameters"
                            ),
                        ],
                    ]

                    l2 = [
                        [
                            sg.Text("p[0]"),
                            sg.Input(size=(25, 1), default_text=p0guess, key="p0"),
                        ],
                        [
                            sg.Text("p[1]"),
                            sg.Input(size=(25, 1), default_text=p1guess, key="p1"),
                        ],
                        [
                            sg.Text("p[2]"),
                            sg.Input(size=(25, 1), default_text=p2guess, key="p2"),
                        ],
                        [
                            sg.Text("p[3]"),
                            sg.Input(size=(25, 1), default_text=p3guess, key="p3"),
                        ],
                        [
                            sg.Text("p[4]"),
                            sg.Input(size=(25, 1), default_text=p4guess, key="p4"),
                        ],
                    ]

                    l3 = [[sg.Button("Ok"), sg.Button("Cancel")]]

                    layout = [
                        [
                            sg.Frame(layout=l1, title="", size=(600, 100)),
                        ],
                        [
                            sg.Frame(layout=l2, title="", size=(600, 200)),
                        ],
                        [
                            sg.Frame(layout=l3, title="", size=(600, 50)),
                        ],
                    ]
                    guess = fit.guess
                    window = sg.Window(
                        "Custom guess window",
                        layout,
                        finalize=True,
                    )
                    window["fit name"].update(fit.name)
                    window["fit formula"].update(fit.formula_help)
                    window["fit parameters"].update(fit.parameters_help)
                    if len(guess) >= 1:
                        p0guess = str(guess[0])
                        window["p0"].update(p0guess)
                    if len(guess) >= 2:
                        p1guess = str(guess[1])
                        window["p1"].update(p1guess)
                    if len(guess) >= 3:
                        p2guess = str(guess[2])
                        window["p2"].update(p2guess)
                    if len(guess) >= 4:
                        p3guess = str(guess[3])
                        window["p3"].update(p3guess)
                    if len(guess) >= 5:
                        p4guess = str(guess[4])
                        window["p4"].update(p4guess)
                    window.refresh()
                    while True:
                        event, values = window.read()
                        if (
                            event == sg.WIN_CLOSED or event == "Cancel"
                        ):  # if user closes window or clicks cancel
                            break
                        if event == "Ok":
                            new_guess = [
                                values["p0"],
                                values["p1"],
                                values["p2"],
                                values["p3"],
                                values["p4"],
                            ]
                            for k in range(len(new_guess)):
                                if new_guess[len(new_guess) - 1 - k] == "not used":
                                    new_guess.pop()
                                else:
                                    new_guess[len(new_guess) - 1 - k] = float(
                                        new_guess[len(new_guess) - 1 - k]
                                    )
                            fit.guess = new_guess
                            break

                    window.close()
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
    # parameters loaded from the options window
    cmap = self.quickplotOptionsWindow.cmapComboBox.currentText()
    RBFI_kwargs = {
        "kernel": self.quickplotOptionsWindow.radialFunctionsBasisComboBox.currentText(),
    }
    try:
        RBFI_kwargs["epsilon"] = float(
            self.quickplotOptionsWindow.epsilonValueLineEdit.text()
        )
    except:
        pass
    try:
        RBFI_kwargs["degree"] = int(self.quickplotOptionsWindow.degreeLineEdit.text())
    except:
        pass

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

    if not self.quickplotOptionsWindow.interpolationEnabledCheckBox.isChecked():

        data_avg_pivotted = data_stacked.pivot(ylabel, xlabel, zlabel)
        data_std_pivotted = data_stacked.pivot(ylabel, xlabel, "std")
        data_fmt_std_pivotted = data_stacked.pivot(ylabel, xlabel, "fmt_std")

        if self.quickplotOptionsWindow.showStdDevCheckBox.isChecked():
            # probably exists a cleaner way to manage the 1 subplot / 2 subplots cases
            if len(data_stacked.groupby(xlabel)) >= len(data_stacked.groupby(ylabel)):
                fig, axs = plt.subplots(2, 1)
            else:
                fig, axs = plt.subplots(1, 2)
            sns.heatmap(
                data_avg_pivotted,
                cmap=cmap,
                annot=True,
                linewidths=0.5,
                cbar=False,
                ax=axs[0],
            )
            axs[0].set_title(data_stacked[zlabel].name, fontweight="bold")

            sns.heatmap(
                data_std_pivotted,
                cmap=cmap,
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
                cmap=cmap,
                annot=data_fmt_avg_pivotted,
                fmt="",
                linewidths=0.5,
                cbar=False,
                ax=ax,
            )
            ax.set_title(data_stacked[zlabel].name, fontweight="bold")

    else:

        xy_obs = data_stacked[[xlabel, ylabel]].to_numpy()
        z_obs = data_stacked[[zlabel]].to_numpy()
        interpolation_func = interpolate.RBFInterpolator(xy_obs, z_obs, **RBFI_kwargs)

        xmin = float(data_stacked[[xlabel]].min())
        xmax = float(data_stacked[[xlabel]].max())
        ymin = float(data_stacked[[ylabel]].min())
        ymax = float(data_stacked[[ylabel]].max())

        xmargin = 0.05 * (xmax - xmin)
        ymargin = 0.05 * (ymax - ymin)

        xy_grid = np.mgrid[
            xmin - xmargin : xmax + xmargin : 100j,
            ymin - ymargin : ymax + ymargin : 100j,
        ]

        xy_flat = xy_grid.reshape(2, -1).T

        z_flat = interpolation_func(xy_flat)
        z_grid = z_flat.reshape(100, 100)

        if self.quickplotOptionsWindow.showStdDevCheckBox.isChecked():
            std_obs = data_stacked[["std"]].to_numpy()
            interpolation_std_func = interpolate.RBFInterpolator(
                xy_obs, std_obs, **RBFI_kwargs
            )
            std_flat = interpolation_std_func(xy_flat)
            std_grid = std_flat.reshape(100, 100)

            fig, axs = plt.subplots(1, 2)

            im_avg = axs[0].pcolormesh(*xy_grid, z_grid, shading="gouraud", cmap=cmap)
            if self.quickplotOptionsWindow.showNodesCheckBox.isChecked():
                p_avg = axs[0].scatter(*xy_obs.T, c=z_obs, s=20, ec="k")
            plt.colorbar(im_avg, ax=axs[0], orientation="horizontal")

            axs[0].set_xlabel(data_stacked[xlabel].name)
            axs[0].set_ylabel(data_stacked[ylabel].name)
            axs[0].set_title(data_stacked[zlabel].name, fontweight="bold")

            im_std = axs[1].pcolormesh(*xy_grid, std_grid, shading="gouraud", cmap=cmap)
            if self.quickplotOptionsWindow.showNodesCheckBox.isChecked():
                p_std = axs[1].scatter(*xy_obs.T, c=std_obs, s=20, ec="k")
            plt.colorbar(im_std, ax=axs[1], orientation="horizontal")

            axs[1].set_xlabel(data_stacked[xlabel].name)
            axs[1].set_ylabel(data_stacked[ylabel].name)
            axs[1].set_title(
                "standart deviation",
                fontweight="bold",
            )

        else:
            fig, ax = plt.subplots()
            im = ax.pcolormesh(*xy_grid, z_grid, shading="gouraud", cmap=cmap)
            if self.quickplotOptionsWindow.showNodesCheckBox.isChecked():
                p = ax.scatter(*xy_obs.T, c=z_obs, s=20, ec="k")
            fig.colorbar(im)
            ax.set_xlabel(data_stacked[xlabel].name)
            ax.set_ylabel(data_stacked[ylabel].name)
            ax.set_title(data_stacked[zlabel].name, fontweight="bold")

    fig.suptitle(
        f"Dataset: {datasize} runs | Average data/cell: {round(datasize/data_stacked.notna()[zlabel].sum(),2)}",
        fontweight="bold",
    )

    plt.tight_layout()
    plt.show()
