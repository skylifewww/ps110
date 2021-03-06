from __future__ import print_function

import os, sys
base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

from django.core.management.base import BaseCommand, CommandError
import sys, os, time, random, time

from django.contrib.auth.models import User

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import warnings
warnings.filterwarnings("ignore")

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

flags = None

from event.models import Event

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

os.environ['DJANGO_SETTINGS_MODULE'] = ''
from django.conf import settings

class Command(BaseCommand):
    help = 'Example command taking an argument from the command line and with access to model '

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # delete existing events for this source
        Event.objects.filter(source='kathleen1').delete()
        
        eventsResult = service.events().list(
            calendarId='ps110pta.org_9cp0mb9jp5724em646ce7teark@group.calendar.google.com', timeMin=now, maxResults=1000, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')
        
        for event in events:

            """ GET EVENT START DATE """
            start = event['start'].get('dateTime', event['start'].get('date'))
            if len(start) < 15:
                start = start + " 00:00:00"
            if start[-6:][0] == '-' and start[-6:][3] == ':':
                start = start[:-6]


            """ GET EVENT END DATE """
            end = event['end'].get('dateTime', event['end'].get('date'))
            if len(end) < 15:
                end = end + " 00:00:00"
            if end[-6:][0] == '-' and end[-6:][3] == ':':
                end = end[:-6]        

            # reduce one day from end date     
            """
            if 'T' in end:
                pass
            else:
                end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)
            """


            """ GET EVENT DESCRIPTION """
            desc = ''
            try:
                desc = event['description']
            except KeyError:
                pass

            print("** EVENT **",start, event['summary'], desc, " start", start, "end", end, event['end'])

            try:
                event = Event.objects.get(location='', end_date=end, start_date=start, title=event['summary'])
            except Event.DoesNotExist:
                event = Event.objects.create(location='', end_date=end, start_date=start, title=event['summary'], description=desc)

            event.description = desc
            # add EVERYONE
            event.classroom.add(1)
            event.source = 'kathleen1'
            event.save()

            # create additional entries for this event to account for additional days coverage
            if event.days_hours_and_minutes()[0] > 1:
                day = 1
                while day < event.days_hours_and_minutes()[0]:              
                    event.pk = None
                    start_date = None
                    try:
                        start_date = datetime.datetime.strptime(str(event.start_date).replace('+00:00',''), '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(days=1)
                    except ValueError:
                        try:
                            start_date = datetime.datetime.strptime(str(event.start_date).replace('+00:00',''), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=1)
                        except ValueError:
                            start_date = None

                    event.start_date = start_date
                    event.save()
                    event.classroom.add(1)

                    

        print("finished")
