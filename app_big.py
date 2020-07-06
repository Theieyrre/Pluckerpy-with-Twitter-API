import argparse, os, sys, json

import tweepy
from decouple import config
from termcolor import colored
from colorama import init
from tqdm import tqdm
init()

from twitterapp import TwitterApp

# Parse arguments

parser = argparse.ArgumentParser(
    description="Get profiles and tweets of Twitter users in JSON array\nTwitter API key and secret can be given as\n\t1) .env file with \n\t\tKEY=<twitter_key>\n\t\tSECRET=<twitter_secret>\n\t\tACCESS_TOKEN=<access_token>\n\t\tACCESS_SECRET=<access_secret>\n\t2) commandline argument with --key and --secret", 
    formatter_class=argparse.RawTextHelpFormatter, 
    epilog="Example of usage:\npython profile.py name.json\n"
    )
parser.add_argument("file_name", metavar="file_name", help="[REQUIRED] JSON file with JSON array including screen names")
parser.add_argument("count", metavar="count", nargs="?", help="[OPTIONAL] Total amout of tweets to get from user timeline, default: 20", default=20)
parser.add_argument("-k", "--key", metavar="key", nargs="?", help="Twitter API Key")
parser.add_argument("-s", "--secret", metavar="secret", nargs="?", help="Twitter API Secret")
parser.add_argument("-at", "--access_token", metavar="atoken", nargs="?", help="Twitter API Access Token")
parser.add_argument("-as", "--access_secret", metavar="asecret", nargs="?", help="Twitter API Access Token Secret")
parser.add_argument("-d", "--dir", metavar="dir", nargs="?", help="Directory name to write outputs to", default='output')
parser.add_argument("--csv", action='store_true', help="Format output in csv file")
parser.add_argument("-v", "--verbose", action='store_true', help="Extra prints")
parser.add_argument("--all", action='store_true', help="Concatenates different users dataframes to yield three csv files instead")
args = parser.parse_args()

if args.key is not None and args.secret is not None and args.atoken is not None and args.asecret is not None:
    api_key = args.key
    api_secret = args.secret
    api_access_token = args.atoken
    api_access_token_secret = args.asecret
elif args.key is None and args.secret is None:
    if os.path.exists('.env'):
        api_key = config('KEY')
        api_secret = config('SECRET')
        api_access_token = config('ACCESS_TOKEN')
        api_access_token_secret = config('ACCESS_TOKEN_SECRET')
    else:
        sys.exit(colored(".env file not found !", "red"))
else:
    sys.exit(colored("Either both parameters or .env file found!","red"))

if args.csv:
    import pandas as pd

if not os.path.exists(args.dir):
        os.makedirs(args.dir)

# Get profiles

profiles = []
try:
    print("Loading and removing duplicates from JSON File: " + args.file_name)
    with open(args.file_name, 'r') as jsonfile:
        profiles_json = json.load(jsonfile)
        for profile in profiles_json:
            p = {'name': profile["followerName"], 'label': profile["label"]}
            if p not in profiles:
                profiles.append(p)
        if args.verbose:
            print(colored("Data loaded !","green"))
            print("Total profile count: " + colored(len(profiles), "yellow"))
except FileNotFoundError:
    sys.exit(colored("File not Found!", "red"))

for profile in tqdm(profiles):
    twitter = TwitterApp(args.verbose, api_key, api_secret, api_access_token, api_access_token_secret)
    name = profile["name"]
    user, count = twitter.get_user(name, args.count)
    user["label"] = profile["label"]
    followers = twitter.get_followers(name)
    friends = twitter.get_friends(name)
    tweets = twitter.get_tweets(name, count)

    if args.csv:
        df_followers = pd.DataFrame(columns = user.keys())
        df_friends = pd.DataFrame(columns = user.keys())
        df_tweets = pd.DataFrame(columns = user.keys())
        for i in range(len(followers)):
            dict_to_append = dict(**user, **followers[i])
            df_followers = df_followers.append(dict_to_append, ignore_index=True)
        for i in range(len(friends)):
            dict_to_append = dict(**user, **friends[i])
            df_friends = df_friends.append(dict_to_append, ignore_index=True)
        for i in range(len(tweets)):
            dict_to_append = dict(**user, **tweets[i])
            df_tweets = df_tweets.append(dict_to_append, ignore_index=True)

        if args.verbose:
            print("Followers DataFrame")
            print(df_followers.head(5))
            print("Friends DataFrame")
            print(df_friends.head(5))
            print("Tweets DataFrame")
            print(df_tweets.head(5))

    if not args.csv:
        with open(args.dir + '/followers_' + name + '.json', 'w') as followersjson:
            json.dump(followers, followersjson, indent=4)

        with open(args.dir + '/friends_' + name+ '.json', 'w') as friendsjson:
            json.dump(friends, friendsjson, indent=4)

        with open(args.dir + '/timeline_' + name+ '.json', 'w') as timelinejson:
            json.dump(tweets, timelinejson, indent=4)

    elif not args.all:
        df_followers.to_csv(args.dir + '/followers_' + name+ '.csv')
        df_friends.to_csv(args.dir + '/friends_' + name+ '.csv')
        df_tweets.to_csv(args.dir + '/tweets_' + name+ '.csv')

    else:
        df_followers_all = pd.DataFrame(columns = user.keys())
        df_friends_all = pd.DataFrame(columns = user.keys())
        df_tweets_all = pd.DataFrame(columns = user.keys())
        df_followers_all = pd.concat(df_followers_all, df_followers)
        df_friends_all = pd.concat(df_friends_all, df_friends)
        df_tweets_all = pd.concat(df_tweets_all, df_tweets)

if args.all:
    df_followers_all.to_csv(args.dir + '/followers_all.csv')
    df_friends_all.to_csv(args.dir + '/friends_all.csv')
    df_tweets_all.to_csv(args.dir + '/tweets_all.csv')

        
