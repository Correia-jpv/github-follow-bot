import requests
import json
import argparse
import tqdm
import time
from base64 import b64encode
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--token', help="Your GitHub Personal Access Token", required=True)
parser.add_argument('-m', '--my-username', help="Your GitHub Username", required=True)
parser.add_argument('-f', '--file', help="Followers File to Unfollow")
parser.add_argument('-a', '--all', help="Unfollow all your followers", action="store_true")
parser.add_argument('-mu', '--max-unfollow', help="Max Number of People to Unfollow")
args = parser.parse_args()

HEADERS = {"Authorization": "Basic " + b64encode(str(args.my_username + ":" + args.token).encode('utf-8')).decode('utf-8')}
sesh = requests.session()
sesh.headers.update(HEADERS)
users_to_unfollow = []
mnof = args.max_followers
if args.all:
    res = sesh.get("https://api.github.com/users/" + args.my_username + "/followers")
    links_array = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    last_link = links_array[1]['url']
    last_page = last_link.split('=')[-1]
    print('Grabbing People to Unfollow\nThis may take a while... there are ' + str(last_page) + ' pages to go through.')
    for page in tqdm.tqdm(range(1, int(last_page)), ncols=35, smoothing=True, bar_format='[PROGRESS] {n_fmt}/{total_fmt} | {bar}'):
        res = sesh.get('https://api.github.com/users/' + args.my_username + "/followers?limit=100&page=" + str(page)).json()
        for user in res:
            users_to_unfollow.append(user['login'])
        if mnof != None:
            if len(users_to_unfollow) >= int(mnof):
                break
    print("Unfollowing Users... This WILL take a while!")
    for user in tqdm.tqdm(users_to_unfollow, ncols=35, smoothing=True, bar_format='[PROGRESS] {n_fmt}/{total_fmt} | {bar}'):
        while True:
            time.sleep(5)
            res = sesh.delete('https://api.github.com/user/following/' + user)
            if res.status_code != 204:
                print(res.status_code)
                print("We may have been rate-limited, waiting until it stops!")
                time.sleep(60)
            else:
                break
else:
    if not args.file:
        print("Please pass a file to unfollow from with -f or use -a to unfollow everybody! Limit with -mu INT")
    with open(args.file, 'r+') as f:
        counter = 0
        obj = json.load(f)
        print("Unfollowing Users... This WILL take a while!")
        for user in tqdm.tqdm(obj, ncols=35, smoothing=True, bar_format='[PROGRESS] {n_fmt}/{total_fmt} | {bar}'):
            if mnof != None:
                if counter >= int(mnof):
                    break
            while True:
                time.sleep(5)
                res = sesh.delete('https://api.github.com/user/following/' + user)
                if res.status_code != 204:
                    print(res.status_code)
                    print("We may have been rate-limited, waiting until it stops!")
                    time.sleep(60)
                else:
                    break
            counter += 1
            
