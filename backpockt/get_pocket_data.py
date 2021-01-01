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
    print(f"retrieving next articles: {offset}")
    count = 50
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
    file = os.path.join(os.getcwd(), f"back-pockt-db-{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.txt")
    with open(file, 'w+') as f:
        for article in articles:
            f.write(article + "\n")

def is_more_articles(num_articles, num_request):
    return num_articles == num_request

def main(consumer_key, access_token):
    more_articles = True
    offset = 0
    data = []
    since = []
    while more_articles:
        json_data = get_pocket_data(consumer_key, access_token, offset)
        articles = generate_article_data(json_data)
        data.extend(articles)
        since.append(json_data["since"])
        offset += 1
        more_articles = is_more_articles(len(json_data["list"].items()), 50)
    save_article_data(data)
    print(f"store latest value for next run... {since}")

if __name__ == '__main__':
    args = arg_parser()
    main(args.consumerkey, args.accesstoken)
