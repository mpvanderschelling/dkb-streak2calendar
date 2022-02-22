#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 16:55:13 2022

@author: martin
"""

from pprint import pprint
from utils.google_apis import create_service

CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)