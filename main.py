
from PIL import Image
import math
import os, sys

formatFileDir = ""

resolution = (400, 400)

if len(sys.argv) < 2:
	print("input format file")
	formatFileDir = input()
elif len(sys.argv) == 3:
	formatFileDir = sys.argv[1]
	resolution = (int(sys.argv[2]), int(sys.argv[2]))
elif len(sys.argv) == 4:
	formatFileDir = sys.argv[1]
	resolution = (int(sys.argv[2]), int(sys.argv[3]))

print(sys.argv[1])

if not os.path.exists(formatFileDir):
	print(f"!! file \"{formatFileDir}\" does not exist")
	input("enter to exit\n")
	exit()
	
imageList = []
formatArr = []
cellSize = (0, 0)

formatPadding = 2

# ~~ parse format file ~~

with open(formatFileDir, "r") as f:
	# get image list
	s = f.readline()
	while not s == "\n":
		imageDirString = s.strip()
		imageDirOpen = Image.open(imageDirString)
		imageList.append(imageDirOpen)
		s = f.readline()
	
	# get format string
	formatStr = ""
	s = f.readline().rstrip()
	cellSize = (int(len(s) / formatPadding), 0)
	while not s == "":
		formatStr += s
		cellSize = (cellSize[0], cellSize[1] + 1)
		s = f.readline().rstrip()
		
	# set up format array
	formatArr = []
	for x in range(cellSize[0]):
		formatArr.append([])
		for y in range(cellSize[1]):
			formatArr[len(formatArr) - 1].append('-')

	# populate format array
	for i in range(int(len(formatStr) / formatPadding)):
		istr = ""
		for j in range(formatPadding):
			if not formatStr[i * formatPadding + j] == ' ':
				istr += formatStr[i * formatPadding + j]
		formatArr[i % cellSize[0]][math.floor(i / cellSize[0])] = istr
		

if cellSize == (0, 0):
	print("!! invalid cell format: format cannot be empty")

# ~~ set up cells ~~

class Cell:
	def __init__(self, image):
		self.image = image
		self.width = 1
		self.height = 1

	def size(self, size):
		self.width = size[0]
		self.height = size[1]
		return self


for x in range(len(formatArr)):
	for y in range(len(formatArr[x])):

		char = formatArr[x][y]

		if char == '|' or char == '-':
			formatArr[x][y] = None
			continue
		
		if not char.isnumeric():
			formatArr[x][y] = None
			continue
		
		cellImageIndex = int(char)
		if cellImageIndex > len(imageList):
			print(f"!! invalid image index: {str(cellImageIndex)} at ({x}, {y})")
			formatArr[x][y] = None
			continue

		cellWidth = 0
		cellHeight = 0

		# ugh		
		if x < len(formatArr) - 1:
			i = 0
			checkChar = formatArr[x + 1][y]
			while x + i < len(formatArr) and checkChar == '-':
				checkChar = formatArr[x + i][y]
				i += 1
			cellWidth = i
		
		if y < len(formatArr[x]) - 1:
			i = 0
			checkChar = formatArr[x][y + 1]
			while y + i < len(formatArr[x]) and checkChar == '|':
				checkChar = formatArr[x][y + i]
				i += 1
			cellHeight = i
		
		cell = Cell(imageList[cellImageIndex])
		cell.size((cellWidth + 1, cellHeight + 1))
		formatArr[x][y] = cell



# ~~ draw cells ~~

collageImage = Image.new("RGB", resolution)

from progress.bar import Bar
bar = Bar('processing', max= len(formatArr) * len(formatArr[0]))

for x in range(len(formatArr)):
	for y in range(len(formatArr[x])):

		cell = formatArr[x][y]

		if cell == None: 
			bar.next()
			continue

		thumbImage: Image.Image = cell.image.copy()

		# calc

		resImageCellSize = (
			int(resolution[0] / cellSize[0]), 
			int(resolution[1] / cellSize[1])
			)
		collageImageCellSize = (
			resImageCellSize[0] * cell.width, 
			resImageCellSize[1] * cell.height
			)
		collageImageAspectRatio = collageImageCellSize[1] / collageImageCellSize[0]

		collageSizeSelect = 0
		if collageImageCellSize[1] > collageImageCellSize[0]:
			collageSizeSelect = 1

		# resize image

		imageAspectRatio = thumbImage.height / thumbImage.width
		
		if thumbImage.width < thumbImage.height:
			ratioAdjuster = (collageImageCellSize[collageSizeSelect], collageImageCellSize[collageSizeSelect] * imageAspectRatio)
		else:
			ratioAdjuster = (collageImageCellSize[collageSizeSelect] / imageAspectRatio, collageImageCellSize[collageSizeSelect])
		
		ratioAdjuster = (int(ratioAdjuster[0]), int(ratioAdjuster[1]))
		thumbImage = cell.image.resize(ratioAdjuster)
			
		# crop image
		cropOrigin = (
			(thumbImage.width - collageImageCellSize[0]) / 2,
			(thumbImage.height - collageImageCellSize[1]) / 2
			)
		thumbImage = thumbImage.crop(
			cropOrigin + (
				cropOrigin[0] + collageImageCellSize[0], 
				cropOrigin[1] + collageImageCellSize[1]
				)
			)

		collageImage.paste(thumbImage, (x * resImageCellSize[0], y * resImageCellSize[1]))

		bar.next()

	

bar.finish()

# ~~ save file ~~

print("saving...")
collageImage.save('output.png')
print("complete!! (enter to exit)")
#input()
exit()

from tkinter.filedialog import asksaveasfilename

path = asksaveasfilename(
	initialfile = 'Untitled.png',
	defaultextension=".png",
	filetypes=[("All Files","*.*"),("Images","*.png *.jpg *.jpeg")]
	)

collageImage.save(path)
