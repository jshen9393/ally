import sys
import json
from datetime import datetime

import requests

command = sys.argv[1]
invalid_input = 'Please enter the argument of \'loc\', \'pass\', or \'people\' '
error_message = 'Unable to retrieve information, please try again later.'


def unix_to_date(unix):
    return datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')


def location():

    result = requests.get('http://api.open-notify.org/iss-now.json')
    j = json.loads(result.text)
    if result.status_code not in (200,400):
        print(error_message)
    elif j['message'] == 'failure':
        print(result.text['reason'] + ', please try again')
    else:
        time = unix_to_date(j['timestamp'])
        LAT = j['iss_position']['latitude']
        LONG = j['iss_position']['longitude']
        print(f'The ISS current location at {time} is {LAT, LONG}')


def pass_iss():
    latitude = input('Please enter your latitude: ')
    longitude = input('Please enter your longitude: ')
    params = {'lat': latitude,
              'lon': longitude}
    result = requests.get('http://api.open-notify.org/iss-pass.json?', params=params)
    j = json.loads(result.text)
    if result.status_code not in (200, 400):
        print(error_message)
    elif j['message'] == 'failure':
        print(j['reason'] + ', please try again')
    else:
        LAT = j['request']['latitude']
        LONG = j['request']['longitude']
        time = unix_to_date(j['response'][0]['risetime'])
        duration = j['response'][0]['duration']
        print(f'The ISS will be overhead {LAT, LONG} at {time} for {duration}')


def people():
    result = requests.get('http://api.open-notify.org/astros.json')
    j = json.loads(result.text)
    if result.status_code not in (200, 400):
        print(error_message)
    elif j['message'] == 'failure':
        print(j['reason'] + ', please try again')
    else:
        people_list = j['people']
        number = len(people_list)
        craft_set = set(x['craft'] for x in j['people'])
        for craft in craft_set:
            name_list = [x['name'] for x in j['people'] if x['craft'] == craft]
            name_list[-1] = 'and ' + name_list[-1]
            names = ', '.join(name_list)
            print(f'There are {number} people aboard the {craft}. They are {names}')


if not command:
    print(invalid_input)
elif command == 'loc':
    location()
elif command == 'pass':
    pass_iss()
elif command == 'people':
    people()
else:
    print(invalid_input)
