from PIL import Image
import numpy as np
import os

class Operations :
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

	def constSum(self, const = 0) :
		f = np.asarray(self.img, dtype=int)
		f = f + int(const)

		f[f > self.Lmax] = self.Lmax
		f[f < 0] = 0

		return Image.fromarray(np.uint8(f))

	def constMult(self, const = 1) :
		f = np.asarray(self.img, dtype=float)
		f = float(const)*f

		f[f > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(np.round(f)))

	def constNegative(self) :
		f = np.asarray(self.img, dtype=int)
		f = self.Lmax - f

		return Image.fromarray(np.uint8(f))

	def constMono(self) :
		f = np.asarray(self.img, dtype=int)
		f = 0.299 * f[:,:,0] + 0.587 * f[:,:,1] + 0.114 * f[:,:,2]

		return Image.fromarray(np.uint8(f))

	def constRot(self, rotation = 1) :
		f = np.asarray(self.img, dtype=int)

		return Image.fromarray(np.uint8(np.rot90(f, rotation)))

	def imagesSum(self, w = 1) :
		w = w/100
		f = np.asarray(self.img, dtype=float)
		g = np.asarray(self.imgAux, dtype=float)
		f = w*f + (1-w)*g

		f[f > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(np.round(f)))