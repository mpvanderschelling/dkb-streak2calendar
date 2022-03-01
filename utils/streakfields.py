#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:26:13 2022

@author: martin
"""

from enum import Enum

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
    
    
class Emails(Enum):
    MCtest = 'dkbstreakcalendar@gmail.com'