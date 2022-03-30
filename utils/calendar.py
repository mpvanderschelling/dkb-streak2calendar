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
        
        
        self.calendars = {'DKB': 'primary',
                     'MC': 'j2tdkt9j8nnorudcvdr1vqio24@group.calendar.google.com',
                     'Jatoch': '5dl5bf22mhu420dib8p2gtbjqc@group.calendar.google.com',
                     'Swart': 'mlqia1sp3nrq251k9o9dti7fi4@group.calendar.google.com',
                     'Tina': '6bfi0494fvd6d9iai21sj58koo@group.calendar.google.com',
                     'Mazin': 'ri9skhmif7huivrqb6e8n4kvso@group.calendar.google.com',
                     'Akker': 'iv5boq1g3v9sf0vng7ms53fis8@group.calendar.google.com',
                     'Lloyd': 'mcolkur10fp0jgofkkgpq70q04@group.calendar.google.com',
                     'Boris': 'aomobmn7pme0oc6ou7qcmr5u30@group.calendar.google.com',
                     'Eli': 'eu38pnlbp89ua67r698nna9ht4@group.calendar.google.com',
                     'Thomas': 'o3o6vphbt11khijbnh7k988hc8@group.calendar.google.com'}
        
        
        
        self.service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        #self.calendar_id = '138rjpv797dnj06tbggu8m0l1g@group.calendar.google.com' #DKB Streak-Calendar
        #self.calendar_id = 'primary'
        
    
    def addNewEvent(self, event, calendar):
        self.service.events().insert(calendarId=calendar, body=event, sendUpdates='all').execute()
        return   

    def deleteEvent(self, eventId, calendar):       
        self.service.events().delete(calendarId=calendar, eventId=eventId, sendUpdates='all').execute()
        return

    def deleteAllEvents(self, calendar):
        events = self.getAllEvents(calendar)
        for event in events:
            self.deleteEvent(event['id'], calendar)
            
        return


    def getEventID(self, name, calendar):
        events = self.getAllEvents(calendar)
        myCalendar = filter(lambda x: name == x['summary'].split(' // ')[1], events )
        try:
            f = next(myCalendar)
        except StopIteration:
            return None
        
        return f['id']
        
    def getAllEvents(self, calendar):

        response = self.service.events().list(
          maxResults=250,
          showDeleted=False,
          # showHidden=False,
          calendarId=calendar, 
          ).execute()
        
        calendarItems = response.get('items')
        nextPageToken = response.get('nextPageToken')
        
        while nextPageToken:
          response = self.service.events().list(
              maxResults=250,
              showDeleted=False,
              # showHidden=False,
              calendarId=calendar, 
              pageToken=nextPageToken
          ).execute()
          
          calendarItems.extend(response.get('items'))
          nextPageToken = response.get('nextPageToken')
          

        return calendarItems
    
    def getAttendees(self, event_id, calendar):
        event = self.service.events().get(calendarId=calendar, eventId=event_id).execute()
        if not 'attendees' in event:
            return []
        
        return event['attendees']
        
    def updateAttendees(self, event, event_id, calendar):
        list_google = self.getAttendees(event_id, calendar)
        list_streak = event['attendees']
        list_new = []
        
        
        for att_streak in list_streak:
            if att_streak['email'] in [att_google['email'] for att_google in list_google]:
                list_new.append(next(x for x in list_google if x['email'] == att_streak['email']))
                
            if att_streak['email'] not in [att_google['email']for att_google in list_google]:
                list_new.append(att_streak)
        
        return list_new

    def updateEvent(self, event, calendarname='DKB'):
        calendar = self.calendars[calendarname]
        #retrieve eventdata
        if not event['start']['date']:
            return
        
        print(f'check event for {calendarname}: {event["summary"]}')
        eventId = self.getEventID(event['summary'].split(' // ')[1], calendar)
        
        if calendarname not in event['line-up'] and calendarname != 'DKB':
            if eventId is not None:
                self.deleteEvent(eventId, calendar)
                print(f'delete event for {calendarname}: {eventId} : {event["summary"]}')
                
            return
        
        #afgezegde gigs automatisch verwijderen uit agenda
        if 'Afgezegd' in event['summary'].split(' // ')[0] and eventId is not None:
                        
            self.deleteEvent(eventId, calendar)
            print(f'delete event for {calendarname}: {eventId} : {event["summary"]}')
            return
        
        if 'Afgezegd' not in event['summary'].split(' // ')[0] and eventId is None:
            #make a new event
            self.addNewEvent(event, calendar)
            print(f'add event for {calendarname}: {event["summary"]}')
            return
        
        if eventId is None:
            return
        

        
        #update event
        event['attendees'] = self.updateAttendees(event, eventId, calendar)
        self.service.events().patch(calendarId=calendar, eventId=eventId, body=event, sendUpdates='externalOnly').execute()
        
    def run(self, event):
        for name in list(self.calendars.keys()):
            self.updateEvent(event, calendarname=name)     



