import tweepy, time
from credentials import *
from SelfieDB import *
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

while True:
	selfies = tweepy.Cursor(api.search,q="selfie").items()

	nCount = 0
	db = SelfieDB()

	for tweet in selfies:
		media = tweet.entities.get('media', [])
		hashtags =   []
		if len(media) < 1:
			continue

		for i in tweet.entities.get('hashtags'):
			hashtags.append(i["text"])
		print(media[0]['media_url'])
		db.AddRecord(media[0]['media_url'],hashtags)
		nCount +=1

	print("Tweets Collected")
	time.sleep(60)

