from entities.image import ImageP
import os

class Menu:
	def __init__(self) :
		try :
			# self.image = ImageP(self.inputImagePath("Enter image file path: "))
			# self.dirName = self.inputDirName("Enter path where processed images will be stored: ")
			os.system("clear")

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

	def inputDirName(self, message) :
		outPath = str(input(message))

		isDir = os.path.isdir(outPath)

		if(not isDir) :
			os.makedirs(outPath)

		return outPath

	def options(self) :
		op = self.imageOps()
		if(op == 1) :
			op = self.oneImgOps()
			if(op == 1) :
				print("Constant operations")
			if(op == 2) :
				print("Rotation")
			if(op == 3) :
				print("Mirroring")
		elif(op == 2):
			op = self.twoImgOps()
			if(op == 1) :
				print("Sum")
			if(op == 2) :
				print("Subtraction")
			if(op == 3) :
				print("Multiplication")
			if(op == 4) :
				print("Division")
			if(op == 5) :
				print("3D Anaglyph")
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