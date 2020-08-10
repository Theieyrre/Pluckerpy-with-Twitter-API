import tweepy
from tweepy import TweepError
from termcolor import colored
from colorama import init
init()
import sys, time

class TwitterApp:
    def __init__(self, verbose, api_key, api_secret, api_access_token, api_access_token_secret):
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(api_access_token, api_access_token_secret)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.verbose = verbose
        self.count = 0
    def get_user(self, name, count):
        user_l = {}
        if self.verbose:
            print("Getting user data...", end='\r')
        try:
            user = self.api.get_user(name)._json
        except TweepError as te:
            sys.exit(colored(te,"red"))
            
        user_l["main_name"] = user["name"]
        user_l["main_screen_name"] = name
        user_l["main_location"] = user["location"]
        user_l["main_is_locked_account"] = user["protected"]
        user_l["main_created_at"] = user["created_at"]
        user_l["main_is_verified"] = user["verified"]
        user_l["main_language"] = user["lang"]
        max_tweet = user["statuses_count"]

        count = max_tweet if count == '-1' else count
        if self.verbose:
            print("Getting user data..." + colored("Done", "green"))
        return user_l, count
    
    def get_followers(self, name):
        followers_l = []
        for follower in tweepy.Cursor(self.api.followers, id=name).items():
            f = {}
            f["name"] = follower._json["name"]
            f["screen_name"] = follower._json["screen_name"]
            f["location"] = follower._json["location"]
            f["description"] = follower._json["description"]
            f["is_locked"] = follower._json["protected"]
            f["created_at"] = follower._json["created_at"]
            f["is_verified"] = follower._json["verified"]
            f["language"] = follower._json["lang"]
            followers_l.append(f)
            if self.verbose:
                print("Current follower count: " + colored(len(followers_l),"yellow"), end='\r')
        if self.verbose:
            print()
            print("Getting Followers..." + colored("Done", "green"))
        return followers_l
    def get_friends(self, name):
        friends_l = []
        if self.verbose:
            print("Getting Friends...", end='\r')
        for friend in tweepy.Cursor(self.api.friends, id=name).items():
            f = {}
            f["name"] = friend._json["name"]
            f["screen_name"] = friend._json["screen_name"]
            f["location"] = friend._json["location"]
            f["description"] = friend._json["description"]
            f["is_locked"] = friend._json["protected"]
            f["created_at"] = friend._json["created_at"]
            f["is_verified"] = friend._json["verified"]
            f["language"] = friend._json["lang"]
            friends_l.append(f)
            if self.verbose:
                print("Current friend count: " + colored(len(friends_l),"yellow"), end='\r')
        if self.verbose:
            print()
            print("Getting Friends..." + colored("Done", "green"))
        return friends_l
    def get_tweets(self, name, count):
        if self.verbose:
            print("Getting user timeline...", end='\r')
        tweets_l = []
        for status in tweepy.Cursor(self.api.user_timeline, id=name, count = count).items():
            t = {}
            t["created_at"] = status._json["created_at"]
            t["text"] = status._json["text"]
            t["hashtags"] = ",".join([ h["text"] for h in status._json["entities"]["hashtags"]])
            t["symbols"] = status._json["entities"]["symbols"]
            t["urls"] = ",".join([u["url"] for u in status._json["entities"]["urls"]])
            t["is_retweet"] = status._json["retweeted"]
            t["language"] = status._json["lang"]
            t["name"] = status._json["user"]["name"]
            t["screen_name"] = status._json["user"]["screen_name"]
            t["is_quote"] = status._json["is_quote_status"]
            t["is_reply"] = 0 if status._json["in_reply_to_status_id"] else status._json["in_reply_to_status_id"]
            t["source"] = status._json["source"]
            tweets_l.append(t)
            if self.verbose:
                print("Current tweets count: " + colored(len(tweets_l),"yellow"), end='\r')
        return tweets_l
    def get_location(self, name):
        try:
            user = self.api.get_user(name)
            self.count += 1
            time.sleep(1)
            return user._json['location']
        except TweepError as te:
            print(colored(te.args[0][0]['message'],"red"))
            return "<ERROR>"
    def get_rate_limit_status(self, category):
        if category == "users":
            return self.api.rate_limit_status()["resources"]["users"]['/users/show/:id']
        elif category == "friends":
            return self.api.rate_limit_status()["resources"]["friends"]['/friends/list']
        elif category == "followers":
            return self.api.rate_limit_status()["resources"]["followers"]['/followers/list']
        elif category == "tweets":
            return self.api.rate_limit_status()["resources"]["statuses"]['/statuses/user_timeline']
        elif category == "location":
            return self.api.rate_limit_status()["resources"]["users"]['/users/:id']
        else:
            return self.api.rate_limit_status()