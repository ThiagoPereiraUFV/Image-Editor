class ImageP :
	def __init__(self, path) :
		imageFullName = path.split("/")[len(path.split("/"))-1]
		self.imageName = imageFullName.split(".")[0]
		self.imageExtension = imageFullName.split(".")[1]

	def getImageName(self) :
		return self.imageName

	def getImageExtension(self) :
		return self.imageExtension