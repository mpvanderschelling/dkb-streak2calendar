#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 16:55:13 2022

@author: martin
"""

from utils.google_apis import create_service

class GoogleAPI():
    def __init__(self, CLIENT_SECRET_FILE='client_secret_GoogleCloudDemo.json',
                 API_NAME='calendar',
                 API_VERSION='v3',
                 SCOPES=['https://www.googleapis.com/auth/calendar']):
        
        self.service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        self.calendar_id = '138rjpv797dnj06tbggu8m0l1g@group.calendar.google.com' #DKB Streak-Calendar
        
    
    def addNewEvent(self,event):
         if event['start']['date']:
             self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
             return   

    def deleteEvent(self, event):
        #retrieve eventdata
        if not event['start']['date']:
            return
        
        eventId = self.getEventID(event['summary'].split(' // ')[1])
        
        if eventId is None:
            #do nothing
            return
        
        self.service.events().delete(calendarId=self.calendar_id, eventId=eventId).execute()


    def getEventID(self, name):
        events = self.getAllEvents()
        for event in events:
            if event['summary'].split(' // ')[1] == name:
                return event['id']
            
        return None
    
    def getAllEvents(self):
        page_token = None
        while True:
          events = self.service.events().list(calendarId=self.calendar_id, pageToken=page_token).execute()
          page_token = events.get('nextPageToken')
          if not page_token:
            break    
        return events['items']
    
    def updateEvent(self, event):
        #retrieve eventdata
        if not event['start']['date']:
            return
        
        eventId = self.getEventID(event['summary'].split(' // ')[1])
        
        #afgezegde gigs automatisch verwijderen uit agenda
        if 'Afgezegd' in event['summary'].split(' // ')[0] and eventId is not None:
            self.deleteEvent(event)
            return
        
        if eventId is None:
            #make a new event
            self.addNewEvent(event)
            return
        else:
            #update event    
            self.service.events().update(calendarId=self.calendar_id, eventId=eventId, body=event).execute()
        
        
if __name__ == '__main__':
    pass
        