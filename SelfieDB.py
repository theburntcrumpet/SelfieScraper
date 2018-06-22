from SqliteDB import *

class SelfieDB(SqliteDB):
	def __init__(self,sqliteFile="Selfies.db"):
		super().__init__(sqliteFile)
		self.IncrementalChanges()

	def IncrementalChanges(self):
		try:
			c = self.db.cursor()
			c.execute("ALTER TABLE selfies ADD ret_error TEXT")
			self.db.commit()
		except Exception as e:
			logging.debug(e)

	def CreateDatabase(self):
		c = self.db.cursor()
		c.execute("CREATE TABLE hashtags (hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,hashtag TEXT)")
		c.execute("CREATE TABLE selfies (selfie_id INTEGER PRIMARY KEY AUTOINCREMENT,selfie_url TEXT)")
		c.execute("CREATE TABLE selfie_hashtag (selfie_hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,selfie_id INTEGER,hashtag_id INTEGER)")
		self.db.commit()

	def CheckMappingExists(self,hashtagId,selfieId):
		c = self.db.cursor()
		existing = c.execute("SELECT COUNT(*) FROM selfie_hashtag WHERE selfie_id = ? AND hashtag_id = ?", (selfieId,hashtagId))
		nExisting = existing.fetchone()
		if(nExisting[0] > 0):
			return True
		return False

	def GetHashtagId(self,hashtag):
		return self.GetIdFromTable("hashtag_id","hashtag","hashtags",hashtag)
		
	def GetAllURLs(self):
			urls = set()
			c = self.db.cursor()
			results = c.execute("SELECT selfie_url FROM selfies")
			for result in results:
				if "403" not in result[0] and "404" not in result[0]:
					urls.add(result[0])
			return urls

	def GetSelfieId(self,selfieUrl):
		return self.GetIdFromTable("selfie_id","selfie_url","selfies",selfieUrl)

	def CheckHashtagExists(self,hashtag):
		return self.CheckSingleValueExistsInTable("hashtags","hashtag",hashtag)
	
	def CheckSelfieExists(self,selfieUrl):
		return self.CheckSingleValueExistsInTable("selfies","selfie_url",selfieUrl)

	def InsertHashtag(self,hashtag):
		if not self.CheckHashtagExists(hashtag):
			self.InsertValuesIntoTable("hashtags",["hashtag"],[hashtag])
	
	def InsertSelfie(self,selfieUrl):
		if not self.CheckSelfieExists(selfieUrl):
			self.InsertValuesIntoTable("selfies",["selfie_url"],[selfieUrl])

	def InsertMapping(self,hashtagId,selfieId):
		if not self.CheckMappingExists(hashtagId,selfieId):
			self.InsertValuesIntoTable("selfie_hashtag",["selfie_id","hashtag_id"],[selfieId,hashtagId])
			return True
		return False

	def UpdateErrorOnURL(self,url,err):
		c = self.db.cursor()
		c.execute("UPDATE selfies SET ret_error=? WHERE selfie_url=?",(err,url))
		self.db.commit()

	def AddRecord(self,selfieUrl, hashtags):
		if len(hashtags) == 0:
			return
		self.InsertSelfie(selfieUrl)
		selfieId = self.GetSelfieId(selfieUrl)
		if selfieId is None:
			return

		for hashtag in hashtags:
			self.InsertHashtag(hashtag)
			currentId = self.GetHashtagId(hashtag)
			if currentId is None:
				continue
			if self.InsertMapping(currentId,selfieId):
				logging.info("Hashtag ID: {} Selfie ID: {} Selfie URL: {} Hashtag: #{}".format(currentId,selfieId,selfieUrl,hashtag))

if __name__ == "__main__":
	myDB = SelfieDB()
	myDB.CreateDatabase()
