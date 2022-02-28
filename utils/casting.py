#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 11:49:40 2022

@author: martin
"""

from datetime import datetime
from utils.streakfields import Stages, Fields, Emails
import pandas as pd


def ConvertJSONToDataFrame(streak_data):
    columns = [field.name for field in list(Fields)]
    columns.append('STATUS')
    g = {}

    for entry in streak_data:
        g[entry['name']] = [entry['fields'][field.value] if field.value in entry['fields'] else None for field in list(Fields) ]
        g[entry['name']].append(Stages(entry['stageKey']).name)



    df = pd.DataFrame.from_dict(g, columns=columns, orient='index')
    df.fillna("",inplace=True)

    df['DATUM'] = df['DATUM'].apply(lambda x: ConvertMiliSecondsToString(x))
    return df


def ConvertMiliSecondsToString(ms): #numpy.float64
    if not ms: #if string is empty
        return ''
    else:
        return datetime.fromtimestamp(ms/1000.0).strftime('%Y-%m-%d')
    
def ConvertToEvent(s):
    event = {
      'summary': f"{s['STATUS'].capitalize()} // {s.name}".replace("_"," "),
      'location': f"{s['STAD']} - {s['LOCATIE']}",
      'description': f'''J: {s['BESCHIKBAAR']}\nN: {s['NIET_BESCHIKBAAR']}\n?: {s['GEEN_ANTWOORD']}\n\n{s['TIJDEN']}\n\n{s['LOG']}''',
      'start': {
        'date': f"{s['DATUM']}",
      },
      'end': {
        'date': f"{s['DATUM']}",
      },
      'attendees': ConvertToAttendees(s['BESCHIKBAAR'].replace(" ","").split(','))
      
  }
    
    return event
    


def ConvertToAttendees(names: list):
    return [{'email': Emails[name].value, 'responseStatus': 'needsAction'} for name in names if name in Emails.__members__]


    #a.replace(" ","").split(',')
    
if __name__ == '__main__':
    pass
    


    
    
