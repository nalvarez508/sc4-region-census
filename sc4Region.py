# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: sc4Region.pyc
# Compiled at: 2004-02-06 09:33:30
import cStringIO, sc4Dat, glob, os, Image, ImageDraw, ImageFont, PngImagePlugin, JpegImagePlugin, BmpImagePlugin, copy, ConfigParser
from struct import *

class sc4City:
    __module__ = __name__

    def __init__(self, sc4File):
        datFile = sc4Dat.sc4Dat(sc4File)
        rvFile = cStringIO.StringIO(datFile.getDecompressedData(3389161179L, 3389161185L, 0L))
        self.Filename = os.path.split(sc4File)[1]
        (self.VersionMajor, self.VersionMinor) = unpack('<hh', rvFile.read(calcsize('<hh')))
        (self.CityX, self.CityY) = unpack('<LL', rvFile.read(calcsize('<LL')))
        (self.SizeX, self.SizeY) = unpack('<LL', rvFile.read(calcsize('<LL')))
        self.TileSize = ('', 'Small', 'Medium', '', 'Large')[self.SizeX]
        self.Residential = unpack('<L', rvFile.read(calcsize('<L')))[0]
        self.Commercial = unpack('<L', rvFile.read(calcsize('<L')))[0]
        self.Industrial = unpack('<L', rvFile.read(calcsize('<L')))[0]
        print sc4File, self.VersionMajor, self.VersionMinor
        if self.VersionMajor == 1 and self.VersionMinor <= 9:
            rvFile.read(calcsize('<LLLLLLBBB'))
        elif self.VersionMajor == 1 and self.VersionMinor <= 10:
            rvFile.read(calcsize('<LLLLLLLBBB'))
        else:
            rvFile.read(calcsize('<LLLLLLLL'))
        sLen = unpack('<L', rvFile.read(calcsize('<L')))[0]
        fmt = '<%ds' % sLen
        if sLen:
            self.CityName = unpack(fmt, rvFile.read(calcsize(fmt)))[0]
        else:
            self.CityName = ''
        rvFile.read(calcsize('<L'))
        sLen = unpack('<L', rvFile.read(calcsize('<L')))[0]
        fmt = '<%ds' % sLen
        if sLen:
            self.MayorName = unpack(fmt, rvFile.read(calcsize(fmt)))[0]
        else:
            self.MayorName = ''
        self.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2317648569L, 1243906747L, 0L)))
        self.cityMask = Image.open(cStringIO.StringIO(datFile.getRawData(2317648569L, 1243906747L, 2L)))
        try:
            self.trafficPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2317648569L, 1243906747L, 4L)))
        except TypeError:
            self.trafficPNG = None

        try:
            self.trafficMask = Image.open(cStringIO.StringIO(datFile.getRawData(2317648569L, 1243906747L, 6L)))
        except TypeError:
            self.trafficMask = None

        try:
            fundsFile = cStringIO.StringIO(datFile.getDecompressedData(3918577153L, 698035483L, 0L))
            fundsFile.read(calcsize('<LLLh'))
            self.CityFunds = unpack('<q', fundsFile.read(calcsize('<q')))[0]
            self.CityFunds2 = unpack('<q', fundsFile.read(calcsize('<q')))[0]
        except:
            self.CityFunds = 'N/A'
            self.CityFunds2 = 'N/A'

        return


class sc4EmptyTile:
    __module__ = __name__

    def __init__(self, tileSize):
        self.cityPNG = None
        self.cityMask = None
        self.trafficPNG = None
        self.trafficMask = None
        self.SizeX = tileSize
        self.SizeY = tileSize
        self.CityX = 0
        self.CityY = 0
        self.CityName = ''
        self.MayorName = ''
        return


class sc4Region:
    __module__ = __name__

    def __init__(self, simcity4Location=''):
        self.RegionLoaded = False
        self.BlanksLoaded = False
        self.LoadBlankTiles(simcity4Location)
        return None
        return

    def Load(self, location):
        self.RegionPath = location
        self.RegionDirName = os.path.split(location)[1]
        self.ConfigBMP = Image.open(os.path.join(location, 'config.bmp')).convert('RGB')
        (self.SizeX, self.SizeY) = self.ConfigBMP.size
        self.RegionINI = ConfigParser.ConfigParser()
        self.RegionINI.read(os.path.join(location, 'region.ini'))
        try:
            self.RegionName = self.RegionINI.get('Regional Settings', 'name')
        except:
            self.RegionName = self.RegionDirName

        self.TerrainType = self.RegionINI.get('Regional Settings', 'terrain type')
        self.Cities = []
        for sc4File in glob.glob(os.path.join(location, '*.sc4')):
            self.Cities.append(sc4City(os.path.join(location, sc4File)))

        self.ComputeRegionStats()
        self.RegionPNG = Image.new('RGB', (1, 1))
        self.RegionLoaded = True

    def ComputeRegionStats(self):
        self.Residential = 0
        self.Commercial = 0
        self.Industrial = 0
        for city in self.Cities:
            self.Residential += city.Residential
            self.Commercial += city.Commercial
            self.Industrial += city.Industrial

    def GenerateRegionImage(self, traffic=False, borders=False, cityNames=False, mayorNames=False, fillEmptyTiles=True):

        def tileCheck(x, y, xSize, ySize, configBMP, imageData):
            (imageX, imageY) = configBMP.size
            if y > 0:
                for n in range(xSize):
                    if imageData[x + n + (y - 1) * imageX] != (0, 0, 0):
                        return False

            if x > 0:
                for n in range(ySize):
                    if imageData[x - 1 + (y + n) * imageX] != (0, 0, 0):
                        return False

            if x > 0 and y > 0:
                if imageData[x - 1 + (y - 1) * imageX] != (0, 0, 0):
                    return False
            for imgX in range(x, x + xSize):
                for imgY in range(y, y + ySize):
                    imageData[imgX + imgY * imageX] = (
                     0, 0, 0)

            configBMP.putdata(imageData)
            return True

        regionBMP = Image.new('RGB', (self.SizeX + 4, self.SizeY + 4), (0, 0, 0))
        regionBMP.paste(self.ConfigBMP, (0, 0))
        newRegionBMP = Image.new('RGB', (self.SizeX + 4, self.SizeY + 4), (0, 0, 0))
        bmpData = list(regionBMP.getdata())
        bmpWidth = regionBMP.size[0]
        bmpHeight = regionBMP.size[1]
        newbmpData = list(newRegionBMP.getdata())
        for city in self.Cities:
            print 'Size: ', city.SizeX, city.SizeY, city.CityX, city.CityY
            for y in range(city.CityY, city.SizeY + city.CityY):
                for x in range(city.CityX, city.SizeX + city.CityX):
                    if city.CityX + city.SizeX <= bmpWidth and city.CityX >= 0 and city.SizeX > 0 and city.CityY + city.SizeY <= bmpHeight and city.CityY >= 0 and city.SizeY > 0:
                        bmpData[x + y * bmpWidth] = (
                         0, 0, 0)
                        newbmpData[x + y * bmpWidth] = (255, 255, 255)

        regionBMP.putdata(bmpData)
        newRegionBMP.putdata(newbmpData)
        emptyList = []
        if regionBMP.getbbox():
            if fillEmptyTiles and self.BlanksLoaded:
                print 'Blank Tiles!'
                for y in range(self.ConfigBMP.size[1]):
                    for x in range(bmpWidth):
                        (r, g, b) = bmpData[x + y * bmpWidth]
                        if r == 255 and g < 255 and b < 255:
                            if self.TerrainType:
                                city = copy.copy(self.SmallWater)
                            else:
                                city = copy.copy(self.SmallLand)
                            city.CityX = x
                            city.CityY = y
                            emptyList.append(city)
                            bmpData[x + y * bmpWidth] = (0, 0, 0)
                            newbmpData[x + y * bmpWidth] = (255, 255, 255)
                        elif r < 255 and g == 255 and b < 255:
                            if self.TerrainType == 0:
                                city = copy.copy(self.MediumLand)
                            else:
                                city = copy.copy(self.MediumWater)
                            city.CityX = x
                            city.CityY = y
                            emptyList.append(city)
                            for imgY in range(2):
                                for imgX in range(2):
                                    bmpData[x + imgX + (y + imgY) * bmpWidth] = (
                                     0, 0, 0)
                                    newbmpData[x + imgX + (y + imgY) * bmpWidth] = (255, 255, 255)

                        elif r < 255 and g < 255 and b == 255:
                            if self.TerrainType == 0:
                                city = copy.copy(self.LargeLand)
                            else:
                                city = copy.copy(self.LargeWater)
                            city.CityX = x
                            city.CityY = y
                            emptyList.append(city)
                            for imgX in range(4):
                                for imgY in range(4):
                                    bmpData[x + imgX + (y + imgY) * bmpWidth] = (
                                     0, 0, 0)
                                    newbmpData[x + imgX + (y + imgY) * bmpWidth] = (255, 255, 255)

                regionBMP.putdata(bmpData)
                newRegionBMP.putdata(newbmpData)
        else:
            print 'No Blank Tiles!'
        regionBMPData = newbmpData
        print 'Region BMP Sizes'
        print regionBMP.size
        print len(regionBMPData)
        fileList = list(range(len(self.Cities)))
        drawList = []
        print len(emptyList)
        print len(drawList)
        f = 0
        while fileList or emptyList:
            tilePlaced = False
            for (i, data) in enumerate(fileList):
                item = self.Cities[data]
                if tileCheck(item.CityX, item.CityY, item.SizeX, item.SizeY, regionBMP, regionBMPData):
                    tilePlaced = True
                    drawList.append(item)
                    fileList.pop(i)

            for item in emptyList:
                if tileCheck(item.CityX, item.CityY, item.SizeX, item.SizeY, regionBMP, regionBMPData):
                    tilePlaced = True
                    drawList.append(item)
                    emptyList.remove(item)

            if not tilePlaced:
                print 'Error:  No placable tile found.'
                break

        outPNG = Image.new('RGBA', (regionBMP.size[0] * 135 + 200, regionBMP.size[1] * 120))
        pushLeft = outPNG.size[0] / 3
        imgDraw = ImageDraw.Draw(outPNG)
        try:
            textFont = ImageFont.truetype('arialbd.ttf', 12)
        except:
            textFont = ImageFont.load_default()

        textDraw = []
        textColor = (
         220, 220, 220)
        XOffset = (0, 0, -37, 0, -112)
        YOffset = (0, 0, 64, 0, 192)
        for i in drawList:
            srcImg = i.cityPNG.copy()
            srcMask = i.cityMask.copy()
            if traffic:
                if i.trafficPNG and i.trafficMask:
                    srcImg = i.trafficPNG.copy()
                    srcMask = i.trafficMask.copy()
            posLeft = 90 * i.CityX + -37 * i.CityY + XOffset[i.SizeX] + pushLeft
            yOff = srcImg.size[1]
            posTop = 19 * i.CityX + 45 * i.CityY - yOff + YOffset[i.SizeY] + 250
            mask = srcMask.split()[2].point((lambda i: i == 255 and 255))
            if borders:
                srcImg.paste((128, 128, 128), mask=i.cityMask.split()[0])
            if srcImg.mode != 'RGBA':
                srcImg = srcImg.convert('RGBA')
            srcImg.putalpha(srcMask.split()[2])
            outPNG.paste(srcImg, (posLeft, posTop), mask)
            if cityNames and i.CityName and i.CityName != 'New City':
                textSize = textFont.getsize(i.CityName)
                textLeft = srcImg.size[0] / 2 - textSize[0] / 2 + posLeft
                textTop = i.SizeY * 62 / 2 - textSize[1] - 4 + posTop
                textDraw.append((textLeft, textTop, i.CityName))
            if mayorNames and i.MayorName:
                textSize = textFont.getsize(i.MayorName)
                textLeft = posLeft + srcImg.size[0] / 2 - textSize[0] / 2
                textTop = i.SizeY * 62 / 2 - 5 + posTop
                textDraw.append((textLeft, textTop, i.MayorName))

        for (x, y, text) in textDraw:
            imgDraw.text((x, y), text, font=textFont, fill=textColor)

        outPNG = outPNG.crop(outPNG.getbbox())
        self.RegionPNG = outPNG
        return outPNG

    def LoadBlankTiles(self, simcity1DatLocation='c:/program files/maxis/simcity 4'):
        try:
            if self.BlanksLoaded:
                print 'Blanks Already Loaded'
                return
        except:
            pass

        try:
            datFile = sc4Dat.sc4Dat(os.path.join(simcity1DatLocation, 'simcity_1.dat'))
            print 'Loading Blank Tiles...'
            self.SmallLand = sc4EmptyTile(1)
            self.SmallWater = sc4EmptyTile(1)
            self.MediumLand = sc4EmptyTile(2)
            self.MediumWater = sc4EmptyTile(2)
            self.LargeLand = sc4EmptyTile(4)
            self.LargeWater = sc4EmptyTile(4)
            self.SmallLand.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 1785505950L)))
            self.SmallWater.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 1780685126L)))
            self.SmallLand.cityMask = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 1780685127L)))
            self.SmallWater.cityMask = self.SmallLand.cityMask
            if self.SmallLand.cityPNG.size != self.SmallLand.cityMask.size:
                self.SmallLand.cityMask = self.SmallLand.cityMask.resize(self.SmallLand.cityPNG.size)
            if self.SmallWater.cityPNG.size != self.SmallWater.cityMask.size:
                self.SmallWater.cityMask = self.SmallWater.cityMask.resize(self.SmallWater.cityPNG.size)
            self.MediumLand.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 1785505503L)))
            self.MediumWater.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 3928168797L)))
            self.MediumLand.cityMask = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 3928168798L)))
            self.MediumWater.cityMask = self.MediumLand.cityMask
            if self.MediumLand.cityPNG.size != self.MediumLand.cityMask.size:
                self.MediumLand.cityMask = self.MediumLand.cityMask.resize(self.MediumLand.cityPNG.size)
            if self.MediumWater.cityPNG.size != self.MediumWater.cityMask.size:
                self.MediumWater.cityMask = self.MediumWater.cityMask.resize(self.MediumWater.cityPNG.size)
            self.LargeLand.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 174893961L)))
            self.LargeWater.cityPNG = Image.open(cStringIO.StringIO(datFile.getRawData(2238569388L, 1780411692L, 170070745L)))
            self.LargeLand.cityMask = Image.open(cStringIO.StringIO(datFile.getDecompressedData(2238569388L, 1780411692L, 170070744L)))
            self.LargeWater.cityMask = self.LargeLand.cityMask
            if self.LargeLand.cityPNG.size != self.LargeLand.cityMask.size:
                self.LargeLand.cityMask = self.LargeLand.cityMask.resize(self.LargeLand.cityPNG.size)
            if self.LargeWater.cityPNG.size != self.LargeWater.cityMask.size:
                self.LargeWater.cityMask = self.LargeWater.cityMask.resize(self.LargeWater.cityPNG.size)
            print self.LargeWater.cityPNG.mode
            print self.LargeWater.cityMask.mode
            self.BlanksLoaded = True
            print 'Done loading blank tiles!'
        except:
            self.BlanksLoaded = False
