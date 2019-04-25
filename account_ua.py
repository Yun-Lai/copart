import csv
import io
import json
import random

import requests


# Script to map account to a user agent

def read_accounts():
    with open('./accounts.json', 'r') as f:
        return json.load(f)


def write_accounts(accounts):
    with open('./accounts_new.json', 'w') as f:
        f.write(json.dumps(accounts, indent=4))


def read_user_agents_csv():
    url = "https://raw.githubusercontent.com/N0taN3rd/userAgentLists/master/csv/chrome.csv"
    response = requests.get(url)
    response.encoding = 'utf-8'  # useful if encoding is not sent (or not sent properly) by the server
    csvio = io.StringIO(response.text, newline="")
    data = []
    for row in csv.DictReader(csvio):
        data.append(row)

    return data


def run():
    uas = read_user_agents_csv()
    accounts = read_accounts()

    for account in accounts:
        if 'ua' not in account:
            account['ua'] = random.sample(uas, 1)[0]['ua']

    write_accounts(accounts)


if __name__ == '__main__':
    run()
