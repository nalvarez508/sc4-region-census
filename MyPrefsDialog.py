# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: MyPrefsDialog.pyc
# Compiled at: 2004-02-05 20:30:08
from wxPython.wx import *

class MyPrefsDialog(wxDialog):
    __module__ = __name__

    def __init__(self, *args, **kwds):
        kwds['style'] = wxDIALOG_MODAL | wxCAPTION | wxRESIZE_BORDER | wxSYSTEM_MENU | wxTHICK_FRAME
        wxDialog.__init__(self, *args, **kwds)
        self.label_6 = wxStaticText(self, -1, 'Simcity Directory:')
        self.text_simcityDir = wxTextCtrl(self, -1, '')
        self.button_browse = wxButton(self, -1, 'Browse...')
        self.label_7 = wxStaticText(self, -1, 'Jpg Quality:')
        self.spin_quality = wxSpinCtrl(self, -1, '', min=0, max=100)
        self.checkbox_HideEmpty = wxCheckBox(self, -1, 'Hide Empty Cities')
        self.button_ok = wxButton(self, wxID_OK, 'Ok')
        self.button_cancel = wxButton(self, wxID_CANCEL, 'Cancel')
        self.__set_properties()
        self.__do_layout()
        EVT_BUTTON(self, self.button_browse.GetId(), self.onBrowse)

    def __set_properties(self):
        self.SetTitle('Preferences')
        self.checkbox_HideEmpty.SetToolTipString('Hide cities without a mayor name.  These are not yet established.')
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_9 = wxBoxSizer(wxVERTICAL)
        sizer_10 = wxBoxSizer(wxHORIZONTAL)
        grid_sizer_1 = wxFlexGridSizer(3, 3, 2, 2)
        grid_sizer_1.Add(self.label_6, 0, wxALL | wxALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.text_simcityDir, 1, wxALL | wxEXPAND, 5)
        grid_sizer_1.Add(self.button_browse, 0, wxALL, 5)
        grid_sizer_1.Add(self.label_7, 0, wxALL | wxALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.spin_quality, 0, wxALL, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.checkbox_HideEmpty, 0, wxALL | wxALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add((300, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.AddGrowableCol(1)
        sizer_9.Add(grid_sizer_1, 1, wxEXPAND, 0)
        sizer_10.Add((20, 20), 1, wxEXPAND, 0)
        sizer_10.Add(self.button_ok, 0, wxALIGN_RIGHT, 0)
        sizer_10.Add((20, 20), 0, wxALIGN_RIGHT, 0)
        sizer_10.Add(self.button_cancel, 0, wxALIGN_RIGHT, 0)
        sizer_9.Add(sizer_10, 0, wxEXPAND | wxALIGN_RIGHT, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_9)
        sizer_9.Fit(self)
        sizer_9.SetSizeHints(self)
        self.Layout()

    def onBrowse(self, event):
        dlg = wxDirDialog(self, 'Select Simcity 4 Folder', self.text_simcityDir.GetValue())
        if dlg.ShowModal() == wxID_OK:
            self.text_simcityDir.SetValue(dlg.GetPath())
