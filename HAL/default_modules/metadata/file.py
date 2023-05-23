# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
from pathlib import Path
from datetime import datetime
import re

# -- local
from HAL.classes.metadata.abstract import AbstractMetaData


# %% CLASS DEFINITION
class FileData(AbstractMetaData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "file"
        self.path = path

    def analyze(self):
        # check that file exists !
        if not self.path.is_file():
            return
        data = []

        #  name
        param = {
            "name": "file name",
            "value": self.path.name,
            "display": "%s",
            "unit": "",
            "comment": "file name",
        }
        data.append(param)

        # folder
        param = {
            "name": "parent",
            "value": self.path.parent.name,
            "display": "%s",
            "unit": "",
            "comment": "parent folder",
        }
        data.append(param)
        parsed_name = [
            int(s) for s in re.findall(r"\d+", self.path.parent.name)
        ]
        if parsed_name:
            #sequence folder int
            param = {
                "name": "Seq Folder integer",
                "value": parsed_name[0],
                "display": "%s",
                "unit": "",
                "comment": "parent folder",
            }
            data.append(param)

        # parsing filename with regex
        parsed_name = [
            int(s) for s in re.findall(r"\d+", self.path.name)
        ]  # === [#seq number , #run num]

        # sequence
        param = {
            "name": "sequence",
            "value": parsed_name[0],
            "display": "%s",
            "unit": "",
            "comment": "sequence number",
        }
        data.append(param)

        # cycle
        param = {
            "name": "cycle",
            "value": parsed_name[1],
            "display": "%s",
            "unit": "",
            "comment": "cycle",
        }
        data.append(param)

        # -- modification time
        tmstp = self.path.stat().st_mtime

        # store in "strings" for display
        mtime = datetime.fromtimestamp(tmstp)
        param = {
            "name": "date",
            "value": mtime.strftime("%Y-%m-%d"),
            "display": "%s",
            "unit": "",
            "comment": "last modification date",
        }
        data.append(param)

        param = {
            "name": "time",
            "value": mtime.strftime("%H:%M:%S"),
            "display": "%s",
            "unit": "",
            "comment": "last modification date",
        }
        data.append(param)

        # store timestamp for plotting / analysis (but 'hidden' !)
        param = {
            "name": "timestamp",
            "value": tmstp,
            "display": "%i",
            "unit": "",
            "hidden": True,
            "special": "timestamp",
            "comment": "last modification date",
        }
        data.append(param)

        # size
        size = self.path.stat().st_size
        b_to_Mb = 1 / 1024 ** 2
        param = {
            "name": "size",
            "value": size * b_to_Mb,
            "display": "%.3g",
            "unit": "Mb",
            "comment": "size in mega bytes",
        }
        data.append(param)
        #  store
        self.data = data


# %% TEST
if __name__ == "__main__":
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = FileData(path)
    data.analyze()
    print([d["name"] for d in data.data])
    print("---")
    # print(data.data)
    print(data.get_numeric_keys())
