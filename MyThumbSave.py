# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: MyThumbSave.pyc
# Compiled at: 2004-02-05 20:30:08
from wxPython.wx import *

class MyThumbSave(wxDialog):
    __module__ = __name__

    def __init__(self, *args, **kwds):
        kwds['style'] = wxDIALOG_MODAL | wxCAPTION | wxSYSTEM_MENU
        wxDialog.__init__(self, *args, **kwds)
        self.label_1 = wxStaticText(self, -1, 'Image Width:')
        self.slider_width = wxSlider(self, -1, -2147483648, 1, 100, style=wxSL_HORIZONTAL | wxSL_AUTOTICKS)
        self.label_size = wxStaticText(self, -1, 'label_size')
        self.button_ok = wxButton(self, wxID_OK, 'Ok')
        self.button_cancel = wxButton(self, wxID_CANCEL, 'Cancel')
        self.__set_properties()
        self.__do_layout()
        EVT_COMMAND_SCROLL(self, self.slider_width.GetId(), self.onSlide)

    def __set_properties(self):
        self.SetTitle('Save Thumbnail Settings')
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_11 = wxBoxSizer(wxVERTICAL)
        sizer_12 = wxBoxSizer(wxHORIZONTAL)
        sizer_13 = wxStaticBoxSizer(wxStaticBox(self, -1, 'Output size (pixels):'), wxVERTICAL)
        grid_sizer_2 = wxBoxSizer(wxHORIZONTAL)
        grid_sizer_2.Add(self.label_1, 0, wxALL | wxALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.slider_width, 1, wxALL | wxALIGN_CENTER_VERTICAL, 5)
        sizer_11.Add(grid_sizer_2, 0, wxEXPAND, 0)
        sizer_13.Add(self.label_size, 1, wxALL | wxEXPAND, 3)
        sizer_11.Add(sizer_13, 0, wxALL | wxEXPAND, 5)
        sizer_11.Add(20, 20, 0, 0, 0)
        sizer_12.Add(20, 20, 1, 0, 0)
        sizer_12.Add(self.button_ok, 0, wxALL, 2)
        sizer_12.Add(10, 10, 0, 0, 0)
        sizer_12.Add(self.button_cancel, 0, wxALL, 2)
        sizer_11.Add(sizer_12, 0, wxEXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_11)
        sizer_11.Fit(self)
        sizer_11.SetSizeHints(self)
        self.Layout()

    def onSlide(self, event):
        self.calcOutputSize()

    def calcOutputSize(self):
        if self.imgHeight and self.imgWidth:
            self.outW = self.slider_width.GetValue()
            self.outH = int(self.imgHeight * (float(self.outW) / self.imgWidth))
            self.label_size.SetLabel('(%d, %d)' % (self.outW, self.outH))
        else:
            self.label_size.SetLabel('(x, y)')
