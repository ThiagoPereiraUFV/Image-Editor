from entities.image import ImageP
import os

class Menu:
	def __init__(self) :
		try :
			image = ImageP(self.inputImagePath("Enter image file path: "))

			self.options()
		except Exception :
			print("An error occurred, try again!")

	def inputImagePath(self, message) :
		imagePath = str(input(message))

		isFile = os.path.isfile(imagePath)

		while(not isFile) :
			print("Invalid path, try again!\n")

			imagePath = str(input(message))
			isFile = os.path.isfile(imagePath)

		return imagePath

	def options(self) :
		print("")