#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 11:49:40 2022

@author: martin
"""

from datetime import datetime
from utils.streakfields import Stages, Fields
import pandas as pd


def ConvertJSONToDataFrame(streak_data):
    columns = [field.name for field in list(Fields)]
    columns.append('STATUS')
    columns.append('OPTIEDATUM')
    g = {}

    for entry in streak_data:
        g[entry['name']] = [entry['fields'][field.value] if field.value in entry['fields'] else None for field in list(Fields) ]
        g[entry['name']].append(Stages(entry['stageKey']).name)
        g[entry['name']].append(entry['creationTimestamp'])



    df = pd.DataFrame.from_dict(g, columns=columns, orient='index')
    df.fillna("",inplace=True)

    df['DATUM'] = df['DATUM'].apply(lambda x: ConvertMiliSecondsToString(x))
    df['OPTIEDATUM'] = df['OPTIEDATUM'].apply(lambda x: ConvertMiliSecondsToString(x+1209600000)) #two weeks
    return df


def ConvertMiliSecondsToString(ms): #numpy.float64
    if not ms: #if string is empty
        return ''
    else:
        return datetime.fromtimestamp(ms/1000.0).strftime('%Y-%m-%d')
    
def ConvertToEvent(s):
    desc = f'''J: {s['BESCHIKBAAR']}\nN: {s['NIET_BESCHIKBAAR']}\n\nTijden: {s['TIJDEN']}\n\nTechniek: {s['TECHNIEK']}'''
    
    if s['STATUS'].capitalize() == 'Aanvraag':
        desc += f'''\n\nOptie tot {s['OPTIEDATUM']}''' 
    
    event = {
      'summary': f"{s['STATUS'].capitalize()} // {s.name}".replace("_"," "),
      'location': f"{s['STAD']} - {s['LOCATIE']}",
      'description': desc,
      'start': {
        'date': f"{s['DATUM']}",
      },
      'end': {
        'date': f"{s['DATUM']}",
      },
      'line-up': s['BESCHIKBAAR'].replace(" ","").split(',')
      
  }
    
    return event


    
    
