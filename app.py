import argparse, os, sys, json

import tweepy
from decouple import config
from termcolor import colored
from colorama import init
init()

from twitterapp import TwitterApp

# Parse arguments

parser = argparse.ArgumentParser(
    description="Get profile and tweets of a Twitter user\nTwitter API key and secret can be given as\n\t1) .env file with \n\t\tKEY=<twitter_key>\n\t\tSECRET=<twitter_secret>\n\t\tACCESS_TOKEN=<access_token>\n\t\tACCESS_SECRET=<access_secret>\n\t2) commandline argument with --key and --secret", 
    formatter_class=argparse.RawTextHelpFormatter, 
    epilog="Example of usage:\npython profile.py github\n"
    )
parser.add_argument("screen_name", metavar="screen_name", help="[REQUIRED] Screen name without @ of the user")
parser.add_argument("count", metavar="count", nargs="?", help="[OPTIONAL] Total amout of tweets to get from user timeline, default: 20", default=20)
parser.add_argument("-k", "--key", metavar="key", nargs="?", help="Twitter API Key")
parser.add_argument("-s", "--secret", metavar="secret", nargs="?", help="Twitter API Secret")
parser.add_argument("-at", "--access_token", metavar="atoken", nargs="?", help="Twitter API Access Token")
parser.add_argument("-as", "--access_secret", metavar="asecret", nargs="?", help="Twitter API Access Token Secret")
parser.add_argument("-d", "--dir", metavar="dir", nargs="?", help="Directory name to write outputs to", default='output')
parser.add_argument("--csv", action='store_true', help="Format output in csv file")
parser.add_argument("-v", "--verbose", action='store_true', help="Extra prints")
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

# Get Twitter instance

twitter = TwitterApp(args.verbose, api_key, api_secret, api_access_token, api_access_token_secret)
# Get profile data

name = args.screen_name
user_l, count = twitter.get_user(name, args.count)

# Get Followers/Friends

followers_l = twitter.get_followers(name)
friends_l = twitter.get_friends(name)

# Get User Timeline

tweets_l = twitter.get_tweets(name, count)

if args.verbose:
    print()
    print("Getting user timeline..." + colored("Done", "green"))
    print("Total number of followers collected: " + colored(len(followers_l), "yellow"))
    print("Total number of friends collected: " + colored(len(friends_l), "yellow"))
    print("Total number of tweets collected: " + colored(len(tweets_l), "yellow"))

# Write Followers/Friends

if not os.path.exists(args.dir):
    os.makedirs(args.dir)

if not args.csv:
    with open(args.dir + '/followers_' + name + '.json', 'w') as followersjson:
        json.dump(followers_l, followersjson, indent=4)

    with open(args.dir + '/friends_' + name+ '.json', 'w') as friendsjson:
        json.dump(friends_l, friendsjson, indent=4)

    with open(args.dir + '/timeline_' + name+ '.json', 'w') as timelinejson:
        json.dump(tweets_l, timelinejson, indent=4)
else:
    df_followers = pd.DataFrame(columns = user_l.keys())
    df_friends = pd.DataFrame(columns = user_l.keys())
    df_tweets = pd.DataFrame(columns = user_l.keys())
    for i in range(len(followers_l)):
        dict_to_append = dict(**user_l, **followers_l[i])
        df_followers = df_followers.append(dict_to_append, ignore_index=True)
    for i in range(len(friends_l)):
        dict_to_append = dict(**user_l, **friends_l[i])
        df_friends = df_friends.append(dict_to_append, ignore_index=True)
    for i in range(len(tweets_l)):
        dict_to_append = dict(**user_l, **tweets_l[i])
        df_tweets = df_tweets.append(dict_to_append, ignore_index=True)

    if args.verbose:
        print("Followers DataFrame")
        print(df_followers.head(5))
        print("Friends DataFrame")
        print(df_friends.head(5))
        print("Tweets DataFrame")
        print(df_tweets.head(5))

    df_followers.to_csv(args.dir + '/followers_' + name+ '.csv')
    df_friends.to_csv(args.dir + '/friends_' + name+ '.csv')
    df_tweets.to_csv(args.dir + '/tweets_' + name+ '.csv')