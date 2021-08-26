from PIL import Image
import numpy as np

class Operations :
	def __init__(self, img1, img2 = None):
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

	def constSum(self, const = 0) :
		f = np.asarray(self.img, dtype=int)
		f = f + int(const)

		f[f > self.Lmax] = self.Lmax
		f[f < 0] = 0

		return Image.fromarray(np.uint8(f))
