import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class FirstTest:

    service = 0

    def __init__(self):
        FLAGS = gflags.FLAGS

        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret can be found in Google Cloud Console
        FLOW = OAuth2WebServerFlow(
            client_id='693663834058-9rucffp9gvfk24iv05ougqa1f8p9315m.apps.googleusercontent.com',
            client_secret='cdxvYrRSuw11BmuwRo5C4hc8',
            scope='https://www.googleapis.com/auth/calendar',
            user_agent='SpikeCalendar')

        # To disable the local server feature, uncomment the following line:
        # FLAGS.auth_local_webserver = False

        # If the Credentials don't exist or are invalid, run through the native client
        # flow. The Storage object will ensure that if successful the good
        # Credentials will get written back to a file.
        storage = Storage('calendar.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
          credentials = run(FLOW, storage)

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API. Visit
        # the Google Cloud Console
        # to get a developerKey for your own application.
        global service
        service = build(serviceName='calendar', version='v3', http=http,
               developerKey='AIzaSyB54M42XSytsOX6YlECtO4o6JajAMH-iQg')

    def getEvent(self):
        page_token = None
        while True:
            events = service.events().list(calendarId='primary', pageToken=page_token).execute()
            if len(events['items']) == 0:
                print "Calendario vuoto!"
                break
            else:
                for event in events['items']:
                    print event
                    print event['summary']
                    print event['start']
                    print event['end']
                    print
                page_token = events.get('nextPageToken')
                if not page_token:
                    break

    def addEvent(self,summary,location,startTime,endTime):
        event = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': startTime
            },
            'end': {
                'dateTime': endTime
            }
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()

        print created_event['id']

    def deleteEvent(self,id):
        service.events().delete(calendarId='primary', eventId=id).execute()

    def deleteAllEvent(self):
        page_token = None
        while True:
            events = service.events().list(calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                id = event['id']
                self.deleteEvent(id)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

def main():
    prova = FirstTest()
    prova.getEvent()
    prova.addEvent("Primo evento API","Sul tuo PC","2013-12-05T23:00:00.000+01:00","2013-12-05T23:30:00.000+01:00")
    prova.getEvent()


if __name__ == '__main__':
    main()