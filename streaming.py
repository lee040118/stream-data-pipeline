import json
import tweepy

from google.cloud import pubsub_v1
from google.oauth2 import service_account
key_path = "stream-pj-32067718f958.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
) 

client = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = client.topic_path('stream-pj', 'tweeets')

with open("twitter.json", "r") as tw_json:
    api_keys = json.load(tw_json)


twitter_api_key = api_keys['twitter_api_key']
twitter_api_secret_key =  api_keys['twitter_api_secret_key']
twitter_access_token =  api_keys['twitter_access_token']
twitter_access_token_secret =  api_keys['twitter_access_token_secret']


class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)
        tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
        client.publish(topic_path, data=tweet.encode('utf-8'))
    
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

stream_listener = SimpleStreamListener()

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['Bitcoin'])
