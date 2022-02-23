#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 11:49:40 2022

@author: martin
"""

import numpy as np
from datetime import datetime

def ConvertMiliSecondsToString(ms): #numpy.float64
    if not ms: #if string is empty
        return ''
    else:
        return datetime.fromtimestamp(ms/1000.0).strftime('%Y-%m-%d')
    
    
if __name__ == '__main__':
    pass
    

def ConvertToEvent(s):
    event = {
      'summary': f"{s['STATUS'].capitalize()}: {s.name}",
      'location': f"{s['STAD']}, {s['LOCATIE']}",
      'description': f'''J: {s['BESCHIKBAAR']}\nN: {s['NIET_BESCHIKBAAR']}\n?: {s['GEEN_ANTWOORD']}\n\n{s['TIJDEN']}\n\n{s['LOG']}''',
      'start': {
        'date': f"{s['DATUM']}",
      },
      'end': {
        'date': f"{s['DATUM']}",
      },
      
  }
    
    return event
    
    
    
