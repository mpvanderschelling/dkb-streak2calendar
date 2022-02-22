#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:11:39 2022

@author: martin
"""


import pandas as pd
from enum import Enum

from utils.request import getPipelineData

class Stages(Enum):
    AANVRAAG = '5001'
    BEVESTIGD = '5002'
    AFGEZEGD_KLANT = '5008'
    AFGEZEGD_DKB = '5010'
    WACHTEN_OP_BETALING = '5003'
    AFHANDELING = '5006'
    AFGEROND = '5007'
    PRIJSINDICATIE = '5009'
    AFGEHANDELD = '5011'

class Fields(Enum):
    DATUM = '1001'
    STAD = '1002'
    LOCATIE = '1007'
    BESCHIKBAAR = '1011'
    NIET_BESCHIKBAAR = '1014'
    GEEN_ANTWOORD = '1015'
    TIJDEN = '1013'
    LOG = '1016'


aanvragen = getPipelineData()


columns = [field.name for field in list(Fields)]
columns.append('STATUS')
g = {}
for entry in aanvragen:
    g[entry['name']] = [entry['fields'][field.value] if field.value in entry['fields'] else None for field in list(Fields) ]
    g[entry['name']].append(Stages(entry['stageKey']).name)

df = pd.DataFrame.from_dict(g, columns=columns, orient='index')
df = df.replace('',None)
df['DATUM'] = df['DATUM'].astype('datetime64[ms]')

df.to_csv('test.csv')