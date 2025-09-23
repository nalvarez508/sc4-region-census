# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: MyScrolledWindow.pyc
# Compiled at: 2004-02-05 21:48:37
from wxPython.wx import *

class MyScrolledWindow(wxScrolledWindow):
    __module__ = __name__

    def __init__(self, *args, **kwds):
        kwds['style'] = wxTAB_TRAVERSAL
        wxScrolledWindow.__init__(self, *args, **kwds)
        self.__set_properties()
        self.__do_layout()
        self.OriginalBuffer = wxEmptyImage(1, 1)
        self.SetVirtualSize((1, 1))
        EVT_PAINT(self, self.OnPaint)
        EVT_SIZE(self, self.OnResize)
        self.zoom = 1
        self.buffer = wxBitmapFromImage(self.OriginalBuffer)

    def __set_properties(self):
        self.SetScrollRate(0, 0)

    def __do_layout(self):
        pass

    def OnPaint(self, event):
        dc = wxBufferedPaintDC(self, self.buffer)

    def SetBuffer(self, img, zoomLevel=-1, refresh=True):
        """Pass an image in RGB format.  zoomLevel is < 0 for actual size,
        0 for fit to width, and greater than zero for increased zoom levels."""
        self.OriginalBuffer = img
        if zoomLevel < 0:
            self.buffer = wxBitmapFromImage(img)
            self.zoom = 1
        elif zoomLevel == 0:
            (sizeX, sizeY) = self.GetClientSizeTuple()
            print sizeX, sizeY
            if sizeX < img.GetWidth():
                self.zoom = 0
                newY = int(img.GetHeight() * (float(sizeX) / img.GetWidth()))
                self.buffer = wxBitmapFromImage(img.Scale(sizeX, newY))
            else:
                self.zoom = 1
                self.buffer = wxBitmapFromImage(img)
        else:
            newX = int(img.GetWidth() * zoomLevel)
            newY = int(img.GetHeight() * zoomLevel)
            if newX > 0 and newY > 0:
                self.buffer = wxBitmapFromImage(img.Scale(int(img.GetWidth() * zoomLevel), int(img.GetHeight() * zoomLevel)))
                self.zoom = zoomLevel
        print 'Buffer size:', self.buffer.GetWidth(), self.buffer.GetHeight()
        (posX, posY) = self.GetViewStart()
        (sizeX, sizeY) = (self.buffer.GetWidth(), self.buffer.GetHeight())
        self.SetScrollbars(1, 1, sizeX, sizeY, posX, posY)
        self.Refresh(refresh)

    def OnResize(self, event):
        print self.GetViewStart()
        if self.zoom == 0:
            self.SetBuffer(self.OriginalBuffer, self.zoom, refresh=false)
