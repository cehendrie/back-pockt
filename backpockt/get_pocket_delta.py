import datetime
import json
import os

from argparse import ArgumentParser

import requests


def arg_parser():
    argparser = ArgumentParser()
    argparser.add_argument(
        '-k', 
        '--key', 
        required=True, 
        help='a pocket consumer key')
    argparser.add_argument(
        '-t', 
        '--token', 
        required=True,
        help='a pocket access token')
    argparser.add_argument(
        '-s', 
        '--since',
        type=int, 
        required=True,
        help='unix timestamp of last retrieval data')
    args = argparser.parse_args()
    return args

def get_pocket_data(consumer_key, access_token, since):
    headers = {
        'X-Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF8'
    }
    payload = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'sort': 'oldest',
        'since': since,
        'detailType': 'simple'
    }
    r = requests.post(
        'https://getpocket.com/v3/get', 
        headers=headers, 
        data=json.dumps(payload))
    return r.json()

def generate_article_data(json_data):
    articles = []
    for id, data in json_data["list"].items():
        if 'resolved_title' in data and 'resolved_url' in data:
            article = {
                "id": id, 
                "resolved_title": data["resolved_title"],
                "resolved_url": data["resolved_url"],
                "excerpt": data["excerpt"],
                "time_added": data["time_added"]
            }
        else:
            print(f"missing title and url... id: {id}")
        articles.append(json.dumps(article))
    return articles

def save_article_data(articles):
    file = os.path.join(os.getcwd(), f"back-pockt-db.txt")
    with open(file, 'a') as f:
        for article in articles:
            f.write(article + "\n")

def main(consumer_key, access_token, since):
    json_data = get_pocket_data(consumer_key, access_token, since)
    data = generate_article_data(json_data)
    save_article_data(data)
    print(f"data: {data}")
    print(f"number articles retrieved: {len(data)}")
    print(f"store since value for next run... {json_data['since']}")

if __name__ == '__main__':
    args = arg_parser()
    main(args.key, args.token, args.since)
