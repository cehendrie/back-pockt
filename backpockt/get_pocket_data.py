import json

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

def get_pocket_data(consumer_key, access_token):
    headers = {
        'X-Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF8'
    }
    payload = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'count': '5',
        'detailType': 'simple'
    }
    r = requests.get(
        'https://getpocket.com/v3/get', 
        headers=headers, 
        data=json.dumps(payload))
    return r.json()

def main(consumer_key, access_token):
    data = get_pocket_data(consumer_key, access_token)
    print(data)

if __name__ == '__main__':
    args = arg_parser()
    main(args.consumerkey, args.accesstoken)
