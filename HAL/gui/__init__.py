# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19

Comments :
"""

# %% IMPORTS

import json
from pathlib import Path

# %% LOAD OPENING LINES
try:
    local_folder = __path__[0]
    json_file = Path(local_folder) / "quotes.json"
    if json_file.is_file():
        quotes = json.loads(json_file.read_text())
    else:
        quotes = [
            "Good morning, Dave.",
        ]
        print(f"Error loading quotes from {json_file}")
except Exception as e:
    quotes = [
        "Good morning, Dave.",
    ]
    print(f"Error loading quotes : {e}")
