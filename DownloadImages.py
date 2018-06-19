from SelfieDB import *
from Requester import * 

import os

class MissingImages:
	def __init__(self,mediaDirectory):
		self.mediaDirectory = mediaDirectory
		self.requester = Requester(self.mediaDirectory)
		self.db = SelfieDB()

	def __GetURLs(self):
		return self.db.GetAllURLs()

	def Get(self):
		existing = os.listdir(self.mediaDirectory)
		for i in self.__GetURLs():
			if i.split("/").pop() not in existing:
				logging.debug("Fetching Image at URL: {}".format(i))
				self.requester.Download(i)

if __name__ == "__main__":
	m = MissingImages("media/")
	m.Get()



