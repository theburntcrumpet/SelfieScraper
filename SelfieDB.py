import sqlite3
TEST = False
class SelfieDB:
	def __init__(self,sqliteFile="Selfies.db"):
		self.db = sqlite3.connect(sqliteFile)

	def CreateDatabase(self):
		c = self.db.cursor()
		c.execute("CREATE TABLE hashtags (hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,hashtag TEXT)")
		c.execute("CREATE TABLE selfies (selfie_id INTEGER PRIMARY KEY AUTOINCREMENT,selfie_url TEXT)")
		c.execute("CREATE TABLE selfie_hashtag (selfie_hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,selfie_id INTEGER,hashtag_id INTEGER)")
		self.db.commit()

	def GetHashtagId(self,hashtag):
		c = self.db.cursor()
		hashtagIds = c.execute("SELECT hashtag_id FROM hashtags WHERE hashtag = ?",(hashtag,))
		id = hashtagIds.fetchone()
		if len(id) == 0:
			return None
		return id[0]

	def GetSelfieId(self,selfieUrl):
		c = self.db.cursor()
		selfieIds = c.execute("SELECT selfie_id FROM selfies WHERE selfie_url=?",(selfieUrl,))
		id = selfieIds.fetchone()
		if len(id) == 0:
			return None
		return id[0]

	def CheckHashtagExists(self,hashtag):
		c = self.db.cursor()
		existing = c.execute("SELECT COUNT(*) FROM hashtags WHERE hashtag=?", (hashtag,))
		nExisting = existing.fetchone()
		if(nExisting[0] > 0):
			return True
		return False

	def InsertHashtag(self,hashtag):
		if(self.CheckHashtagExists(hashtag)):
			return
		c = self.db.cursor()
		c.execute("INSERT INTO hashtags (hashtag) VALUES (?)", (hashtag,))
		self.db.commit()

	def CheckSelfieExists(self,selfieUrl):
		c = self.db.cursor()
		existing = c.execute("SELECT COUNT(*) FROM selfies WHERE selfie_url=?", (selfieUrl,))
		nExisting = existing.fetchone()
		if(nExisting[0] > 0):
			return True
		return False

	def InsertSelfie(self,selfieUrl):
		if(self.CheckSelfieExists(selfieUrl)):
			return
		c = self.db.cursor()
		c.execute("INSERT INTO selfies (selfie_url) VALUES (?)", (selfieUrl,))
		self.db.commit()

	def CheckMappingExists(self,hashtagId,selfieId):
		c = self.db.cursor()
		existing = c.execute("SELECT COUNT(*) FROM selfie_hashtag WHERE selfie_id = ? AND hashtag_id = ?", (selfieId,hashtagId))
		nExisting = existing.fetchone()
		if(nExisting[0] > 0):
			return True
		return False

	def InsertMapping(self,hashtagId,selfieId):
		if self.CheckMappingExists(hashtagId,selfieId):
			return
		c = self.db.cursor()
		c.execute("INSERT INTO selfie_hashtag (selfie_id,hashtag_id) VALUES (? , ?)", (selfieId,hashtagId))
		self.db.commit()
		
	def AddRecord(self,selfieUrl, hashtags):
		self.InsertSelfie(selfieUrl)
		selfieId = self.GetSelfieId(selfieUrl)
		for hashtag in hashtags:
			self.InsertHashtag(hashtag)
			currentId = self.GetHashtagId(hashtag)
			print(currentId)
			if currentId != None:
				self.InsertMapping(currentId,selfieId)

if __name__ == "__main__":
	myDB = SelfieDB()
	myDB.CreateDatabase()
	if not TEST:
		exit()
	myDB.InsertHashtag("funbuns")
	myDB.InsertHashtag("crumpy")
	myDB.InsertHashtag("funbuns")