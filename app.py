import argparse
from os import path
import sys
import json

import tweepy
from decouple import config
from termcolor import colored
from colorama import init
init()

# Parse arguments

parser = argparse.ArgumentParser(
    description="Get profile and tweets of a Twitter user\nTwitter API key and secret can be given as\n\t1) .env file with \n\t\tKEY=<twitter_key>\n\t\tSECRET=<twitter_secret>\n\t\tACCESS_TOKEN=<access_token>\n\t\tACCESS_SECRET=<access_secret>\n\t2) commandline argument wiht --key and --secret", 
    formatter_class=argparse.RawTextHelpFormatter, 
    epilog="Example of usage:\npython profile.py github\n"
    )
parser.add_argument("screen_name", metavar="screen_name", help="[REQUIRED] Screen name without @ of the user")
parser.add_argument("count", metavar="count", nargs="?", help="[OPTIONAL] Total amout of tweets to get from user timeline, default: 20", default=20)
parser.add_argument("-k", "--key", metavar="key", nargs="?", help="Twitter API Key")
parser.add_argument("-s", "--secret", metavar="secret", nargs="?", help="Twitter API Secret")
parser.add_argument("-at", "--access_token", metavar="atoken", nargs="?", help="Twitter API Access Token")
parser.add_argument("-as", "--access_secret", metavar="asecret", nargs="?", help="Twitter API Access Token Secret")
args = parser.parse_args()

if args.key is not None and args.secret is not None and args.atoken is not None and args.asecret is not None:
    api_key = args.key
    api_secret = args.secret
    api_access_token = args.atoken
    api_access_secret = args.asecret
elif args.key is None and args.secret is None:
    if path.exists('.env'):
        api_key = config('KEY')
        api_secret = config('SECRET')
        api_access_token = config('ACCESS_TOKEN')
        api_access_token_secret = config('ACCESS_TOKEN_SECRET')
    else:
        sys.exit(colored(".env file not found !", "red"))
else:
    sys.exit(colored("Either both parameters or .env file found!","red"))

# Auth with tweepy

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(api_access_token, api_access_token_secret)
api = tweepy.API(auth)

# Get Followers/Friends

name = args.screen_name
followers = api.followers(name)
friends = api.friends(name)

followers_l = [user._json for user in followers]
friends_l = [user._json for user in friends]

# Get User Timeline

user_timeline = api.user_timeline(name, count = args.count)
tweets_l = [status._json for status in user_timeline]
print(len(tweets_l))

# Write Followers/Friends

with open('followers_' + name + '.json', 'w') as followersjson:
    json.dump(followers_l, followersjson, indent=4)

with open('friends_' + name+ '.json', 'w') as friendsjson:
    json.dump(friends_l, friendsjson, indent=4)

with open('timeline_' + name+ '.json', 'w') as timelinejson:
    json.dump(tweets_l, timelinejson, indent=4)