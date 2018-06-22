from SelfieDB import *
from Requester import * 
from threading import Thread
import threading
import os,time,copy

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
				r = self.requester.Download(i)
				if r != True:
					try:
						self.db.UpdateErrorOnURL(i,r)
					except Exception as e:
						logging.debug(e)

class MissingImagesWorker(Thread):
	def __init__(self,missingImagesObject):
		super().__init__()
		self.missingImagesObject = missingImagesObject 
	
	def run(self):
		self.missingImagesObject = MissingImages(self.missingImagesObject.mediaDirectory)
		while True:
			try:
				self.missingImagesObject.Get()
				time.sleep(600)
			except Exception as e:
				logging.error(e)
