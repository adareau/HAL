# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07

Comments : Imports fit information, as saved by our former image analysis
           program HeV
"""
# %% IMPORTS

# -- global
from pathlib import Path
from scipy.io import loadmat

# -- local
from HAL.classes.metadata.abstract import AbstractMetaData


# %% TOOL
FIT_PARAM_CONVERSION = {
    "Gaussian": {"cx": 5, "cy": 6, "sx": 3, "sy": 4},
    "TF": {"cx": 5, "cy": 6, "sx": 3, "sy": 4},
}

CENTER_SIZE_FMT = "%.3g"


def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


# %% CLASS DEFINITION
class HevFitData(AbstractMetaData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "HeV-fit"
        self.path = path

    def analyze(self):
        # - init data
        data = []

        # - HeV generated .fit file
        # (this is actually a .mat file)
        # generate file path
        fit_file = self.path.with_suffix(".fit")
        # load and get params
        if fit_file.is_file():
            # - load
            fit_data = loadmat(str(fit_file), squeeze_me=True)
            saved = fit_data["tosave"]

            # - fit type
            fitType = saved["fitType"][()]
            param = {
                "name": "fit type",
                "value": fitType,
                "display": "%s",
                "unit": "",
                "comment": "fit type",
            }
            data.append(param)

            # - atom number
            # Nfit
            param = {
                "name": "Nfit",
                "value": saved["Nfit"][()],
                "display": "%.2g",
                "unit": "",
                "comment": "fitted atom number",
            }
            data.append(param)
            # Nint
            param = {
                "name": "Nint",
                "value": saved["Nint"][()],
                "display": "%.2g",
                "unit": "",
                "comment": "integrated atom number",
            }
            data.append(param)
            # Ncalc
            param = {
                "name": "Ncal",
                "value": saved["Ncalc"][()],
                "display": "%.2g",
                "unit": "",
                "comment": "calculated atom number",
            }
            data.append(param)

            # - size and position
            if fitType in FIT_PARAM_CONVERSION:
                # get conversion
                conv = FIT_PARAM_CONVERSION[fitType]

                # general parameters
                ROI = saved["ROI"][()]
                fitres = saved["fittedParam"][()]
                magnification = saved["magnification"][()]
                xcal = saved["xcal"][()]  # in µm
                ycal = saved["ycal"][()]  # in µm

                # cx (pixels)
                cx_px = fitres[conv["cx"] - 1] + ROI[2]
                param = {
                    "name": "cx",
                    "value": cx_px,
                    "display": CENTER_SIZE_FMT,
                    "unit": "pixels",
                    "comment": "center x (pixels)",
                }
                data.append(param)

                # cy (pixels)
                cy_px = fitres[conv["cy"] - 1] + ROI[0]
                param = {
                    "name": "cy",
                    "value": cy_px,
                    "display": CENTER_SIZE_FMT,
                    "unit": "pixels",
                    "comment": "center y (pixels)",
                }
                data.append(param)

                # sy (pixels)
                sx_px = fitres[conv["sx"] - 1]
                param = {
                    "name": "sx",
                    "value": sx_px,
                    "display": CENTER_SIZE_FMT,
                    "unit": "pixels",
                    "comment": "size x (pixels)",
                }
                data.append(param)

                # sy (pixels)
                sy_px = fitres[conv["sy"] - 1]
                param = {
                    "name": "st",
                    "value": sy_px,
                    "display": CENTER_SIZE_FMT,
                    "unit": "pixels",
                    "comment": "size y (pixels)",
                }
                data.append(param)

                # now in microns
                param = {
                    "name": "cx_µm",
                    "value": cx_px * xcal * magnification,
                    "display": CENTER_SIZE_FMT,
                    "unit": "µm",
                    "comment": "center x (microns)",
                }
                data.append(param)
                param = {
                    "name": "cy_µm",
                    "value": cy_px * ycal * magnification,
                    "display": CENTER_SIZE_FMT,
                    "unit": "µm",
                    "comment": "center y (microns)",
                }
                data.append(param)
                param = {
                    "name": "sx_µm",
                    "value": sx_px * xcal * magnification,
                    "display": CENTER_SIZE_FMT,
                    "unit": "µm",
                    "comment": "size x (microns)",
                }
                data.append(param)
                param = {
                    "name": "sy_µm",
                    "value": sy_px * ycal * magnification,
                    "display": CENTER_SIZE_FMT,
                    "unit": "µm",
                    "comment": "size y (microns)",
                }
                data.append(param)

        # - store
        self.data = data


# %% TEST
if __name__ == "__main__":
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = HevFitData(path)
    data.analyze()
    print(data.data)
