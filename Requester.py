import urllib.request,os

class Requester:
	def __init__(self,storageDirectory):
		self.storageDirectory = storageDirectory
		if not os.path.exists(storageDirectory):
			os.makedirs(storageDirectory)

	def Download(self,url,filename=None):
		if not filename:
			filename = url.split("/").pop()
		try:
			data = urllib.request.urlopen(url).read()
			file = open(self.storageDirectory+filename,"wb")
			file.write(data)
			file.close()
			return True
		except Exception as e:
			return False


if __name__ == "__main__":
	r = Requester("media/")
	r.Download("http://pbs.twimg.com/media/DgEAdruWAAIvXbs.jpg")

