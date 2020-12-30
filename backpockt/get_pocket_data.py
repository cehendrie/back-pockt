import datetime
import json
import os

from argparse import ArgumentParser

import requests


def arg_parser():
    argparser = ArgumentParser()
    argparser.add_argument(
        '-c', 
        '--consumerkey', 
        required=True, 
        help='consumer key')
    argparser.add_argument(
        '-a', 
        '--accesstoken', 
        required=True,
        help='access token')
    args = argparser.parse_args()
    return args

def get_pocket_data(consumer_key, access_token, offset):
    count = 3
    headers = {
        'X-Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF8'
    }
    payload = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'sort': 'newest',
        'count': count,
        'offset': (count * offset),
        'detailType': 'simple'
    }
    r = requests.get(
        'https://getpocket.com/v3/get', 
        headers=headers, 
        data=json.dumps(payload))
    return r.json()

def generate_article_data(json_data):
    articles = []
    for id, data in json_data["list"].items():
        article = {
            "id": id, 
            "resolved_title": data["resolved_title"],
            "resolved_url": data["resolved_url"],
            "excerpt": data["excerpt"],
            "time_added": data["time_added"]
        }
        articles.append(json.dumps(article))
    return articles

def save_article_data(articles):
    # build path to current directory and filename
    file = os.path.join(os.getcwd(), f"back-pockt-db-{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.txt")
    with open(file, 'w+') as f:
        for article in articles:
            f.write(article + "\n")

def main(consumer_key, access_token):
    data = []
    for offset in range(2):
        json_data = get_pocket_data(consumer_key, access_token, offset)
        articles = generate_article_data(json_data)
        data.extend(articles)
    print(data)
    save_article_data(data)

if __name__ == '__main__':
    args = arg_parser()
    main(args.consumerkey, args.accesstoken)
