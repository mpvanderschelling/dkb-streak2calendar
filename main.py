#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:11:39 2022

@author: martin
"""

from utils.streak import StreakAPI
from utils.calendar import GoogleAPI
from utils.casting import ConvertToEvent, ConvertJSONToDataFrame

if __name__ == '__main__':
    s = StreakAPI()
    g = GoogleAPI()
    
    df = ConvertJSONToDataFrame(s.getPipelineData())
    
    events = [ConvertToEvent(df.iloc[i]) for i in range(len(df))]

    # g.deleteAllEvents()
    
    for event in events:
        g.updateEvent(event)