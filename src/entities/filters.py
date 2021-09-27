from PIL import Image
import numpy as np
import os

class Filters :
	def __init__(self, img1, img2 = None):
		os.system("clear")
		print("Processing image...")
		self.Lmax = 255

		if(img2 is None) :
			self.img = self.openImage(img1)
		else :
			self.img = self.openImage(img1)
			self.imgAux = self.openImage(img2)

	def openImage(self, path) :
		image = Image.open(path)

		if(image.mode != "RGB") :
			image = image.convert("RGB")

		return image
