from entities.image import ImageP
from entities.operations import Operations
import os

class Menu:
	def __init__(self) :
		try :
			self.samplesFolder = "samples"
			self.dirName = "result"
			self.image = ImageP(self.inputImageName("Enter image file name in " + self.samplesFolder + " folder: "))
			os.system("clear")

			self.options()
		except Exception as err :
			print(str(err))
		finally :
			exit(0)

	def inputImageName(self, message) :
		imageName = str(input(message))

		isFile = os.path.isfile(self.samplesFolder + "/" + imageName)

		while(not isFile) :
			print("Invalid path, try again!\n")

			imageName = str(input(message))
			isFile = os.path.isfile(self.samplesFolder + "/" + imageName)

		return imageName

	def inputDirName(self, message) :
		outPath = str(input(message))

		isDir = os.path.isdir(outPath)

		if(not isDir) :
			os.makedirs(outPath)

		return outPath

	def getResultImagePath(self, name) :
		return self.dirName + "/" + self.image.getImageName() + "-" + name + "." + self.image.getImageExtension()

	def options(self) :
		imagePath = self.samplesFolder + "/" + self.image.getImageFullName()
		op = self.imageOps()
		if(op == 1) :
			op = self.oneImgOps()
			if(op == 1) :
				op = self.constImgOps()
				if(op == 1) :
					factor = int(input('Type a brighness factor between -255 and 255: '))
					while(factor < -255 or factor > 255) :
						factor = int(input('Invalid value, try again: '))

					result = Operations(imagePath).constSum(factor)
					imageSavePath = self.getResultImagePath("const-brightness")
					result.save(imageSavePath)
					result.show()
				elif(op == 2) :
					factor = float(input('Type a brighness factor between 0 and 100: '))
					while(factor < 0 or factor > 100) :
						factor = float(input('Invalid value, try again: '))

					result = Operations(imagePath).constMult(factor)
					imageSavePath = self.getResultImagePath("const-contrast")
					result.save(imageSavePath)
					result.show()
				elif(op == 3) :
					result = Operations(imagePath).constNegative()
					imageSavePath = self.getResultImagePath("const-negative")
					result.save(imageSavePath)
					result.show()
				elif(op == 4) :
					result = Operations(imagePath).constMono()
					imageSavePath = self.getResultImagePath("const-mono")
					result.save(imageSavePath)
					result.show()
			elif(op == 2) :
				result = Operations(imagePath).constRot()
				imageSavePath = self.getResultImagePath("const-rotate")
				result.save(imageSavePath)
				result.show()
			elif(op == 3) :
				axis = int(input('Type 0 to mirror around horizontal axis, 1 to mirror around vertical axis or 2 to mirror around color axis: '))
				while(axis != 0 and axis != 1 and axis != 2) :
					axis = int(input('Invalid value, try again: '))

				result = Operations(imagePath).constMirror(axis)
				imageSavePath = self.getResultImagePath("const-mirror")
				result.save(imageSavePath)
				result.show()
		elif(op == 2):
			imageAux = ImageP(self.inputImageName("Enter second image file name in " + self.samplesFolder + " folder: "))
			imageAuxPath = self.samplesFolder + "/" + imageAux.getImageFullName()
			op = self.twoImgOps()
			if(op == 1) :
				w = int(input('Type a transparency value to image 1 over image 2 between 0 and 100 (Type -1 to not apply transparency): '))
				while(w < -1 or w > 100) :
					w = int(input('Invalid value, try again: '))

				result = Operations(imagePath, imageAuxPath).imagesSum(w)
				imageSavePath = self.getResultImagePath("images-sum")
				result.save(imageSavePath)
				result.show()
			elif(op == 2) :
				w = int(input('Type a transparency value to image 1 over image 2 between 0 and 100 (Type -1 to not apply transparency): '))
				while(w < -1 or w > 100) :
					w = int(input('Invalid value, try again: '))

				result = Operations(imagePath, imageAuxPath).imagesSub(w)
				imageSavePath = self.getResultImagePath("images-sub")
				result.save(imageSavePath)
				result.show()
			elif(op == 3) :
				result = Operations(imagePath, imageAuxPath).imagesMult()
				imageSavePath = self.getResultImagePath("images-mult")
				result.save(imageSavePath)
				result.show()
			elif(op == 4) :
				result = Operations(imagePath, imageAuxPath).imagesDiv()
				imageSavePath = self.getResultImagePath("images-div")
				result.save(imageSavePath)
				result.show()
			elif(op == 5) :
				result = Operations(imagePath).images3D()
				imageSavePath = self.getResultImagePath("images-3d")
				result.save(imageSavePath)
				result.show()
		elif(op == 0) :
			exit(0)

	def imageOps(self) :
		print("Image operations:")
		print("1 - One image operations")
		print("2 - Two images operations")
		print("0 - Exit")
		op = int(input("Type the corresponding operation number: "))

		while(op < 0 or op > 2) :
			op = int(input("Invalid operation, type again: "))

		os.system("clear")

		return op

	def oneImgOps(self) :
		print("One image operations:")
		print("1 - Constant operations")
		print("2 - Rotation")
		print("3 - Mirroring")
		op = int(input("Type the corresponding operation number: "))

		while(op < 1 or op > 3) :
			op = int(input("Invalid operation, type again: "))

		os.system("clear")

		return op

	def twoImgOps(self) :
		print("Two image operations:")
		print("1 - Sum")
		print("2 - Subtraction")
		print("3 - Multiplication")
		print("4 - Division")
		print("5 - 3D Anaglyph")
		op = int(input("Type the corresponding operation number: "))

		while(op < 1 or op > 5) :
			op = int(input("Invalid operation, type again: "))

		os.system("clear")

		return op

	def constImgOps(self) :
		print("Constant image operations:")
		print("1 - Brigthness")
		print("2 - Contrast")
		print("3 - Negative")
		print("4 - Shades of gray")
		op = int(input("Type the corresponding operation number: "))

		while(op < 1 or op > 4) :
			op = int(input("Invalid operation, type again: "))

		os.system("clear")

		return op