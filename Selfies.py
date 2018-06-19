import tweepy, time
from credentials import *
from SelfieDB import *
from DownloadImages import *

MEDIA_DIRECTORY = "media/"
DOWNLOAD_ON_COLLECTION = True

logging.basicConfig(level=logging.INFO)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = None
try:
	api = tweepy.API(auth,wait_on_rate_limit=True)
	logging.info("Authenticed using provided credentials")
except Exception as e:
	logging.error("An error occured during authentication")
	exit()

db = SelfieDB()
missingImages = MissingImages(MEDIA_DIRECTORY)

logging.info("Beginning main data harvesting loop")
while True:
	try:
		selfies = tweepy.Cursor(api.search,q="selfie").items()
		
		for tweet in selfies:
			media = tweet.entities.get('media', [])
			hashtags =   []
			if len(media) < 1:
				continue

			for i in tweet.entities.get('hashtags'):
				hashtags.append(i["text"])
			
			db.AddRecord(media[0]['media_url'],hashtags)
			
			if DOWNLOAD_ON_COLLECTION:
				missingImages.Get()
		logging.info("Retrieving any missing images")
		missingImages.Get()
		logging.info("Sleeping for 60 seconds")
		time.sleep(60)
	except Exception as e:
		continue

