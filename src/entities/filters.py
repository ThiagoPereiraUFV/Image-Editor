from PIL import Image
import numpy as np
import os

class Filters :
	def __init__(self, img):
		os.system("clear")
		print("Processing image...")

		self.Lmax = 255
		self.img = self.openImage(img1)
		self.imgArr = np.asarray(self.img, dtype=float)
		self.imgResultArr = np.zeros(img.shape, dtype=float)

	def openImage(self, path) :
		image = Image.open(path)

		if(image.mode != "RGB") :
			image = image.convert("RGB")

		return image

	def getKernel(kernel):
		kernels = {
			'gauss': [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]],
			'laplace': [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
			'sobel': [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
			'prewitt': [[], [], []],
			'robinson': [[], [], []],
		}

		return kernels[kernel]