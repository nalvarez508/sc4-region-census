# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: MyAboutDialog.pyc
# Compiled at: 2004-02-05 20:31:56
from wxPython.wx import *

class MyAboutDialog(wxDialog):
    __module__ = __name__

    def __init__(self, *args, **kwds):
        kwds['style'] = wxDEFAULT_DIALOG_STYLE
        wxDialog.__init__(self, *args, **kwds)
        self.text_about = wxTextCtrl(self, -1, '', style=wxTE_MULTILINE | wxTE_READONLY | wxTE_CENTRE)
        self.button_1 = wxButton(self, wxID_OK, 'Ok')
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle('About Region Census')
        self.SetSize((250, 200))
        self.button_1.SetDefault()

    def __do_layout(self):
        sizer_14 = wxBoxSizer(wxVERTICAL)
        sizer_14.Add(self.text_about, 1, wxEXPAND, 0)
        sizer_14.Add(self.button_1, 0, wxALL | wxALIGN_CENTER_HORIZONTAL | wxALIGN_CENTER_VERTICAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_14)
        self.Layout()
