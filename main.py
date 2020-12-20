import tweepy
import time

import make_tweet
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def reply_to(tweet):
    text = make_tweet.get_municipality(list(tweet.text))

    api.update_status(
        status=text,
        in_reply_to_status_id=tweet.id,
        auto_populate_reply_metadata=True
    )

def check_mentions(api, since_id):
    print("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,
            since_id=since_id).items():

        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        print(f"Answering to {tweet.user.name}")

        try:
            reply_to(tweet)
        except tweepy.TweepError as e:
            print(e.reason)
            break
        
    return new_since_id

since_id = 1

while True:
    print(since_id)
    since_id = check_mentions(api, since_id)
    print("Waiting...")
    time.sleep(15)
    print("15")
    time.sleep(15)