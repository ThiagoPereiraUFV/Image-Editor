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

	def constMirror(self, axis) :
		f = np.asarray(self.img, dtype=int)

		return Image.fromarray(np.uint8(np.flip(f, axis=axis)))

	def imagesSum(self, w = -1) :
		w = w/100
		f = np.asarray(self.img, dtype=float)
		g = np.asarray(self.imgAux, dtype=float)

		if(w < 0 or w > 100) :
			f = f + g
		else :
			f = w*f + (1-w)*g

		f[f > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(np.round(f)))

	def imagesSub(self, w = -1) :
		w = w/100
		f = np.asarray(self.img, dtype=float)
		g = np.asarray(self.imgAux, dtype=float)

		if(w < 0 or w > 100) :
			f = f - g
		else :
			f = w*f - (1-w)*g

		f[f < 0] = 0

		return Image.fromarray(np.uint8(np.round(f)))

	def imagesMult(self) :
		f = np.asarray(self.img, dtype=float)
		g = np.asarray(self.imgAux, dtype=float)/self.Lmax

		f = f * g

		f[f > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(np.round(f)))

	def imagesDiv(self) :
		f = np.asarray(self.img, dtype=float)
		g = np.asarray(self.imgAux, dtype=float)/self.Lmax

		f = f / g

		f[np.isnan(f)] = self.Lmax
		f[f > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(np.round(f)))

	def images3D(self) :
		f = np.asarray(self.img, dtype=int)
		g = np.asarray(self.img, dtype=int)
		h = np.asarray(self.img, dtype=int)

		f[:,:,1] = 0
		f[:,:,2] = 0
		g[:,:,0] = 0

		disp = f.shape[1]*0.002

		f = np.roll(f, int(disp), axis=1)
		g = np.roll(g, -int(disp), axis=1)
		# h = f + g + 0.5*h
		h = f + g

		h[h > self.Lmax] = self.Lmax

		return Image.fromarray(np.uint8(h))