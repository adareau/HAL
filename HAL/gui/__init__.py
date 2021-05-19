# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-05-19 16:29:45

Comments :
'''

# %% IMPORTS

import json
from pathlib import Path

# %% LOAD OPENING LINES

json_file = Path('quotes.json')
if json_file.is_file():
    quotes = json.loads(json_file.read_text())
else:
    quotes = ["Good morning, Dave."]