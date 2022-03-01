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
        self.service.events().insert(calendarId=self.calendar_id, body=event, sendUpdates='all').execute()
        return   

    def deleteEvent(self, eventId):       
        self.service.events().delete(calendarId=self.calendar_id, eventId=eventId, sendUpdates='all').execute()
        return

    def deleteAllEvents(self):
        events = self.getAllEvents()
        for event in events:
            self.deleteEvent(event['id'])
            
        return


    def getEventID(self, name):
        events = self.getAllEvents()
        myCalendar = filter(lambda x: name == x['summary'].split(' // ')[1], events )
        try:
            f = next(myCalendar)
        except StopIteration:
            return None
        
        return f['id']
        
    def getAllEvents(self):

        response = self.service.events().list(
          maxResults=250,
          showDeleted=False,
          # showHidden=False,
          calendarId=self.calendar_id, 
          ).execute()
        
        calendarItems = response.get('items')
        nextPageToken = response.get('nextPageToken')
        
        while nextPageToken:
          response = self.service.events().list(
              maxResults=250,
              showDeleted=False,
              # showHidden=False,
              calendarId=self.calendar_id, 
              pageToken=nextPageToken
          ).execute()
          
          calendarItems.extend(response.get('items'))
          nextPageToken = response.get('nextPageToken')
          

        return calendarItems
    
    def getAttendees(self, event_id):
        event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        if not 'attendees' in event:
            return []
        
        return event['attendees']
        
    def updateAttendees(self, event, event_id):
        list_google = self.getAttendees(event_id)
        list_streak = event['attendees']
        list_new = []
        
        
        for att_streak in list_streak:
            if att_streak['email'] in [att_google['email'] for att_google in list_google]:
                list_new.append(next(x for x in list_google if x['email'] == att_streak['email']))
                
            if att_streak['email'] not in [att_google['email']for att_google in list_google]:
                list_new.append(att_streak)
        
        return list_new

    def updateEvent(self, event):
        #retrieve eventdata
        if not event['start']['date']:
            return
        print(f'check event: {event["summary"]}')
        eventId = self.getEventID(event['summary'].split(' // ')[1])
        
        #afgezegde gigs automatisch verwijderen uit agenda
        if 'Afgezegd' in event['summary'].split(' // ')[0] and eventId is not None:
                        
            self.deleteEvent(eventId)
            print(f'delete event: {eventId} : {event["summary"]}')
            return
        
        if 'Afgezegd' not in event['summary'].split(' // ')[0] and eventId is None:
            #make a new event
            self.addNewEvent(event)
            print(f'add event: {event["summary"]}')
            return
        
        if eventId is None:
            return
        
        #update event
        event['attendees'] = self.updateAttendees(event, eventId)
        self.service.events().patch(calendarId=self.calendar_id, eventId=eventId, body=event, sendUpdates='externalOnly').execute()
        
     



