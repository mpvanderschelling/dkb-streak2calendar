# DKB Streak-Calendar script
Application to automatically export Streak data to Google Calendar.

Gigs that are labelled 'Afgezegd' will not be synched and removed from the calendar.

## Getting started

1. Make a new Python environment based on the `requirements.txt`

2. Files you have to add yourself locally:
  * `client_secret_GoogleCloudDemo.json`: OAuth file from Google
  * `streak_apikey.txt`: API key retrieved from Streak.
  * `token_calendar_v3.pickle`: Sign-in token file retrieved from Google
  * `/utils/emails.py`: Emailadresses of external members of the calendar

3. Execute script by calling `main.py`

_&copy; De Klittenband_
