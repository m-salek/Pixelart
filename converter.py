import sys
from PIL import Image, ImageOps, ImageDraw

WHITE = 255

def load(imgAdrs):
    try:
        img = Image.open(imgAdrs)
    except IOError:
        print("Error: I/O => Image loading")
        sys.exit(0)
    img = ImageOps.grayscale(img)
    img = ImageOps.equalize(img)
    return img

def save(newImg, imgAdrs):
    newAdrs = ""
    array = imgAdrs.split('.')
    for i in range(len(array)):
        if i == len(array) - 1:
            newAdrs += '_new'
            newAdrs += '.'
        newAdrs += array[i]
    try:
        newImg.save(newAdrs)
    except IOError:
        print("Error: I/O => Image save")

def createTileColorArray(img, colors, tilesInWidth, tilesInHeight, tileSize):
    tilesColors = [[WHITE for x in range(0, img.width - tileSize, tileSize)] 
            for y in range(0, img.height - tileSize, tileSize)]
    for y in range(0, img.height - tileSize, tileSize):
        for x in range(0, img.width - tileSize, tileSize):
            colorSum = 0
            for tileX in range(tileSize):
                for tileY in range(tileSize):
                    colorSum += img.getpixel((x + tileX, y + tileY))
            colorAvg = int(colorSum / (tileSize * tileSize))
            colorIndx = int((WHITE - colorAvg) * colors / WHITE + 1)
            newColor = int(WHITE * colorIndx / colors)
            tilesColors[int(y / tileSize)][int(x / tileSize)] = newColor
    return tilesColors

def createTileImage(size, tilesNewColor, tileSize):
    newImg = Image.new('L', size, WHITE)
    drawImg = ImageDraw.Draw(newImg)
    for y in range(len(tilesNewColor)):
        for x in range(len(tilesNewColor[0])):
            newX = x * tileSize
            newY = y * tileSize
            drawImg.rectangle([(newX, newY), 
                (newX + tileSize, newY + tileSize)], 
                tilesNewColor[y][x])
    return newImg

def main():       

    imgAdrs = 'image.jpg' #image address
    tilesInWidth = 100 #tiles in a row
    colors = 5 #number of colors

    img = load(imgAdrs)
    if tilesInWidth > img.width:
        tilesInWidth = img.width
        print("Error: Tiles number > Picture pixels! (row)")
        print("Solved: \"tilesInWidth\" changed to pixels in a row(=%d)."%(tilesInWidth))
    tileSize = int(img.width / tilesInWidth)
    tilesInHeight = int(img.height / tileSize)
    tilesColors = createTileColorArray(img, colors, tilesInWidth, tilesInHeight, tileSize)
    newImg = createTileImage((img.width, img.height), tilesColors, tileSize)
    #newImg.show()
    save(newImg, imgAdrs)

if __name__ == "__main__":
    main()
