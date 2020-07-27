from application.popos.charity import Charity
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def return_charities(search_term):
    charities = charity_objects(charity_list(search_term))

    return charities

def charity_objects(response):
    parsed = response.json()
    charity_list = []
    for charity in parsed:
        id = charity["ein"]
        name = charity["charityName"]
        url = charity["charityNavigatorURL"]
        rating = charity["currentRating"]["rating"]
        rating_image = charity["currentRating"]["ratingImage"]["large"]
        charity_list.append(Charity(id, name, url, rating, rating_image))

    return charity_list

def charity_list(search_term):
    payload = {
                'app_id': os.getenv('CHARITY_APP_ID'),
                'app_key': os.getenv('CHARITY_APP_KEY'),
                'rated': 'TRUE',
                'minRating': 3,
                'sort': 'RATING:DESC',
                'search': search_term
               }

    response = requests.get(
                            'https://api.data.charitynavigator.org/v2/organizations',
                            params=payload
                            )

    return response
