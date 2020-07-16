import argparse, os, sys, json

import tweepy
from decouple import config
from termcolor import colored
from colorama import init
import pandas as pd
init()

from twitterapp import TwitterApp
# Parse arguments

parser = argparse.ArgumentParser(
    description="Get profile and tweets of a Twitter user\nTwitter API key and secret can be given as\n\t1) .env file with \n\t\tKEY=<twitter_key>\n\t\tSECRET=<twitter_secret>\n\t\tACCESS_TOKEN=<access_token>\n\t\tACCESS_SECRET=<access_secret>\n\t2) commandline argument with --key and --secret", 
    formatter_class=argparse.RawTextHelpFormatter, 
    epilog="Example of usage:\npython profile.py github\n"
    )
parser.add_argument("folder", metavar="folder", help="[REQUIRED] Folder name of accounts")
parser.add_argument("-k", "--key", metavar="key", nargs="?", help="Twitter API Key")
parser.add_argument("-s", "--secret", metavar="secret", nargs="?", help="Twitter API Secret")
parser.add_argument("-at", "--access_token", metavar="atoken", nargs="?", help="Twitter API Access Token")
parser.add_argument("-as", "--access_secret", metavar="asecret", nargs="?", help="Twitter API Access Token Secret")
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

# Get Twitter instance

twitter = TwitterApp(args.verbose, api_key, api_secret, api_access_token, api_access_token_secret)

# LOOP

columns= ['screen_name', 'name', 'name_emojis', 'is_verified', 'is_locked', 'bio', 'bio_emojis', 'links', 'location']
df = pd.DataFrame(columns=columns)

if args.verbose:
    print("Reading files...", end='\r')
for file in os.listdir(args.folder):
    filename = os.path.join(args.folder, file)
    with open(filename) as f:
        data = json.load(f)["followers"]
        data_dict = {}
        i = 0
        for follower in data.values():
            data_dict[i] = follower
            i += 1
    df = pd.DataFrame.from_dict(data_dict, "index")
if args.verbose:
    print("Reading files..." + colored("Done", "green"))

df.to_csv(args.folder + ".csv")
if args.verbose:
    print(colored("Accounts.csv is created", "green"))
    print("Getting locations...")
# Get Locations

df["location"] = df["name"].apply(twitter.get_location)
if args.verbose:
    print("Getting locations..." + colored("Done", "green"))