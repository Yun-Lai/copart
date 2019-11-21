import csv
import io
import random

import requests


def read_user_agents_csv():
    url = "https://raw.githubusercontent.com/N0taN3rd/userAgentLists/master/csv/chrome.csv"
    response = requests.get(url)
    response.encoding = 'utf-8'  # useful if encoding is not sent (or not sent properly) by the server
    csvio = io.StringIO(response.text, newline="")
    data = []
    for row in csv.DictReader(csvio):
        data.append(row)

    return data


UA = read_user_agents_csv()


def get_random_ua():
    return random.choice(UA)['ua']
