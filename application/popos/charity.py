import requests
import os
from dotenv import load_dotenv
load_dotenv()

def charitites(search_term):
    charity_objects(charity_list(search_term))

def charity_objects(response):
    parsed = response.json()
    charity_list = []
    for charity in parsed:
        id = "ein"
        name = "charityName"
        url = charity["charityNavigatorURL"]
        rating = charity["currentRating"]["rating"]
        charity_list.append(Charity(id, name, url, rating))

    return charity_list

def charity_list(search_term):
    search_term  = search_term if search_term else ""
    payload = {
                'app_id': os.getenv('CHARITY_APP_ID'),
                'app_key': os.getenv('CHARITY_APP_KEY'),
                'rated': 'TRUE',
                'minRating': 3,
                'sort': 'RATING:DESC',
                'search': search_term
               }
    response = requests.get(
                            'https://api.data.charitynavigator.org/v2',
                            params=payload
                            )

    return response

class Charity:
    def __init__(id, name, url, rating):
        self.id = id
        self.url = url
        self.name = name
        self.rating = rating
