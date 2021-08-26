class ImageP :
	def __init__(self, imageName) :
		self.imageFullName = imageName
		self.imageName = self.imageFullName.split(".")[0]
		self.imageExtension = self.imageFullName.split(".")[1]

	def getImageName(self) :
		return self.imageName

	def getImageExtension(self) :
		return self.imageExtension

	def getImageFullName(self) :
		return self.imageFullName