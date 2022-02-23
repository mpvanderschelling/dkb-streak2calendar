#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 16:55:13 2022

@author: martin
"""

#from pprint import pprint
from utils.google_apis import create_service

CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

calendar_id = '138rjpv797dnj06tbggu8m0l1g@group.calendar.google.com' #DKB Streak-Calendar


## LIST ALL EVENTS

page_token = None
while True:
  events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
  for event in events['items']:
    print(event['summary'])
  page_token = events.get('nextPageToken')
  if not page_token:
    break


def getAllEvents(calendar_id):
    page_token = None
    while True:
      events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
      # for event in events['items']:
      #   print(event['summary'])
      page_token = events.get('nextPageToken')
      if not page_token:
        break    
    return events['items']


def giveEventID(name, calendar_id):
    events = getAllEvents(calendar_id)
    for event in events:
        if event['summary'] == name:
            break
        
    #include something if nothing is found
    return event['id'] #, event['summary']

## UPDATE AN EVENT

#First retrieve the event from the API.
event = service.events().get(calendarId=calendar_id, eventId=giveEventID('Appointment at Somewhere', calendar_id)).execute()

event['summary'] = 'Google API'

updated_event = service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()

# Print the updated date.
print(updated_event['updated'])


## ADD NEW EVENT
# event = {
#   'summary': 'Google API',
#   'location': 'Thuis',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'date': '2022-05-28',
#     'timeZone': 'Europe/Amsterdam',
#   },
#   'end': {
#     'date': '2022-05-28',
#     'timeZone': 'Europe/Amsterdam',
#   },

# }

# event = service.events().insert(calendarId=calendar_id, body=event).execute()
#print 'Event created: %s' % (event.get('htmlLink'))


event = {
  'summary': 'Google API',
  'location': 'Thuis',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'date': '2022-05-28',
  },
  'end': {
    'date': '2022-05-28',
  },
  
}