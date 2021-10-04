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

	def getKernelGauss(self, kSize, sigma):
		if kSize % 2 == 0:
      raise Exception('\n\n\nKernel size must be odd\n\n\n')

    x = np.arange(-(kSize-1)/2, (kSize-1)/2+1)
    y = np.arange(-(kSize-1)/2, (kSize-1)/2+1)

    h1, h2 = np.meshgrid(x,y)

    hg = np.exp(-(h1**2 + h2**2) / (2*sigma**2))

    return hg / np.sum(hg)

	def getKernel(self, kernel, kSize=9, sigma=1):
		kernels = {
			'gauss': [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]],
			'gaussCustom': self.getKernelGauss(kSize, sigma),
			'laplaceSmooth1': [[-1,-1,-1], [-1,9,-1], [-1,-1,-1]],
			'laplaceSmooth2': [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
			'laplaceEdge1': [[-1,-1,-1], [-1,8,-1], [-1,-1,-1]],
			'laplaceEdge2': [[0,-1,0], [-1,4,-1], [0,-1,0]],
			'emboss1': [[-1, -1, 0], [-1, 1, 1], [0, 1, 1]],
			'emboss2': [[1, 1, 0], [1, 1, -1], [0, -1, -1]],
			'embossEdge': [[-1, -1, 0], [-1, 0, 1], [0, 1, 1]],
			'relief1': [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]],
			'relief2': [[2, 1, 0], [1, 1, -1], [0, -1, -2]],
			'reliefEdge': [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]],
			'sobel1': [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
			'sobel2': [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
			'prewitt1': [[1, 0, -1], [1, 0, -1], [1, 0, -1]],
			'prewitt2': [[1, 1, 1], [0, 0, 0], [-1, -1, -1]],
			'roberts1': [[1,0], [0,-1]],
			'roberts2': [[0,1], [-1,0]],
			'scharr1': [[3, 10, 3], [0, 0, 0], [-3, -10, -3]],
			'scharr2': [[3, 0, -3], [10, 0, -10], [3, 0, -3]]
		}

		return kernels[kernel]