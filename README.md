# SelfieScraper
Scrape Selfies from Twitter, storing the associated hashtags

## What this does
Using a keyword (in the example provided here, "selfie") as the query, this makes requests to the twitter api.
Using the data returned by the twitter api, a sqlite 3 database is populated. The database contains
- A table of unique "hashtags"
- A table of unique "selfies" (or atleast, the url to the selfies)
- A table of mappings between the selfies and hashtags where each mapped pair is unique

## Using the scraper
To use this, you'll need some magical twitter developer credentials, python (I'm using python 3.6) and tweepy.
You'll need to create a file named "credentials.py". This file should contain 4 variables:
``` python
  # credentials.py
  consumer_key = "YOUR CONSUMER KEY HERE"
  consumer_secret = "YOUR CONSUMER SECRET HERE"
  access_token = "AN ACCESS TOKEN HERE"
  access_token_secret = "AN ACCESS TOKEN SECRET HERE" 
```
Once you've created this file, you'll need to create an instance of the database. You can do this by running:
``` bash
  python SelfieDB.py
```

Then check that the file, "Selfies.db", has been created within your working directory. Great. Now its just a case of:
``` bash
  python Selfies.py
```

I plan to have the database automatically created if the specified file name doesn't exist. I also intend to revise the database code.
It grew as I was writing it and I'm not happy with what seems to be duplication between functions.

Be warned, this doesn't filter NSFW content! There is a lot of it scraped. This is hopefully going to be part of a bigger project which I intend to use to learn a little about TensorFlow and deep learning technologies.

## Platforms
This should be supported by any platform supporting python3 and tweepy, however having said this, I've only tested on Arch Linux, using the latest version of python from the arch repositories.
