# uncompyle6 version 3.9.2
# Python bytecode version base 2.3 (62011)
# Decompiled from: Python 3.11.5 (v3.11.5:cce6ba91b3, Aug 24 2023, 10:50:31) [Clang 13.0.0 (clang-1300.0.29.30)]
# Embedded file name: MyFrame.pyc
# Compiled at: 2004-02-05 21:22:02
from __future__ import print_function
from wxPython.wx import *
import os, sc4Region
from MyScrolledWindow import MyScrolledWindow

class MyFrame(wxFrame):
    __module__ = __name__

    def __init__(self, *args, **kwds):
        global MNU_EDIT_PREFS
        global MNU_FILE_EXIT
        global MNU_FILE_OPEN
        global MNU_FILE_SAVE_DATA
        global MNU_FILE_SAVE_IMAGE
        global MNU_FILE_THUMB
        global MNU_HELP_ABOUT
        kwds['style'] = wxDEFAULT_FRAME_STYLE
        wxFrame.__init__(self, *args, **kwds)
        self.splitter = wxSplitterWindow(self, -1)
        self.splitter_pane_notebook = wxPanel(self.splitter, -1)
        self.notebook = wxNotebook(self.splitter_pane_notebook, -1, style=0)
        self.notebook_image = wxPanel(self.notebook, -1)
        self.notebook_city_info = wxPanel(self.notebook, -1)
        self.notebook_region_info = wxPanel(self.notebook, -1)
        self.splitter_pane_tree = wxPanel(self.splitter, -1)
        self.frame_region_census_menubar = wxMenuBar()
        self.SetMenuBar(self.frame_region_census_menubar)
        MNU_FILE_OPEN = wxNewId()
        MNU_FILE_SAVE_IMAGE = wxNewId()
        MNU_FILE_THUMB = wxNewId()
        MNU_FILE_SAVE_DATA = wxNewId()
        MNU_FILE_EXIT = wxNewId()
        MNU_EDIT_PREFS = wxNewId()
        MNU_HELP_ABOUT = wxNewId()
        self.mnuFile = wxMenu()
        self.mnuFile.Append(MNU_FILE_OPEN, 'Open Region...\tCtrl-O', '', wxITEM_NORMAL)
        self.mnuFile.Append(MNU_FILE_SAVE_IMAGE, 'Save Image\tCtrl-S', '', wxITEM_NORMAL)
        self.mnuFile.Append(MNU_FILE_THUMB, 'Save Thumbnail', '', wxITEM_NORMAL)
        self.mnuFile.Append(MNU_FILE_SAVE_DATA, 'Save Data', '', wxITEM_NORMAL)
        self.mnuFile.Append(MNU_FILE_EXIT, 'Exit', '', wxITEM_NORMAL)
        self.frame_region_census_menubar.Append(self.mnuFile, 'File')
        self.mnuEdit = wxMenu()
        self.mnuEdit.Append(MNU_EDIT_PREFS, 'Preferences...', '', wxITEM_NORMAL)
        self.frame_region_census_menubar.Append(self.mnuEdit, 'Edit')
        self.mnuHelp = wxMenu()
        self.mnuHelp.Append(MNU_HELP_ABOUT, 'About...', '', wxITEM_NORMAL)
        self.frame_region_census_menubar.Append(self.mnuHelp, 'Help')
        self.tree_region = wxTreeCtrl(self.splitter_pane_tree, -1, style=wxTR_HAS_BUTTONS | wxTR_LINES_AT_ROOT | wxSUNKEN_BORDER)
        self.list_region_info = wxListCtrl(self.notebook_region_info, -1, style=wxLC_REPORT | wxSUNKEN_BORDER)
        self.list_city_info = wxListCtrl(self.notebook_city_info, -1, style=wxLC_REPORT | wxSUNKEN_BORDER)
        self.checkbox_shrink = wxCheckBox(self.notebook_image, -1, 'Shrink to fit')
        self.checkbox_borders = wxCheckBox(self.notebook_image, -1, 'Show borders')
        self.checkbox_traffic = wxCheckBox(self.notebook_image, -1, 'Traffic View')
        self.checkbox_cityNames = wxCheckBox(self.notebook_image, -1, 'Show City Names')
        self.checkbox_mayorNames = wxCheckBox(self.notebook_image, -1, 'Show Mayor Names')
        self.checkbox_fillEmpty = wxCheckBox(self.notebook_image, -1, 'Fill Empty Tiles')
        self.button_zoom1to1 = wxButton(self.notebook_image, -1, '1:1')
        self.button_zoomOut = wxButton(self.notebook_image, -1, 'Zoom Out')
        self.button_zoomIn = wxButton(self.notebook_image, -1, 'Zoom In')
        self.panel_image = MyScrolledWindow(self.notebook_image, -1)
        self.__set_properties()
        self.__do_layout()
        self.Region = None
        EVT_MENU(self, MNU_FILE_OPEN, self.mnuFileOpen)
        EVT_MENU(self, MNU_FILE_SAVE_IMAGE, self.mnuFileSave)
        EVT_MENU(self, MNU_FILE_THUMB, self.mnuSaveThumbnail)
        EVT_MENU(self, MNU_FILE_SAVE_DATA, self.SaveToCSV)
        EVT_MENU(self, MNU_FILE_EXIT, self.mnuFileExit)
        EVT_MENU(self, MNU_EDIT_PREFS, self.mnuPrefs)
        EVT_MENU(self, MNU_HELP_ABOUT, self.mnuAbout)
        EVT_TREE_SEL_CHANGED(self, self.tree_region.GetId(), self.onTreeSelChanged)
        EVT_BUTTON(self, self.button_zoomIn.GetId(), self.onButtonZoomIn)
        EVT_BUTTON(self, self.button_zoomOut.GetId(), self.onButtonZoomOut)
        EVT_BUTTON(self, self.button_zoom1to1.GetId(), self.onButtonZoom1to1)
        EVT_CHECKBOX(self, self.checkbox_shrink.GetId(), self.onCheckboxShrink)
        EVT_CHECKBOX(self, self.checkbox_borders.GetId(), self.onCheckboxRefreshImage)
        EVT_CHECKBOX(self, self.checkbox_traffic.GetId(), self.onCheckboxRefreshImage)
        EVT_CHECKBOX(self, self.checkbox_cityNames.GetId(), self.onCheckboxRefreshImage)
        EVT_CHECKBOX(self, self.checkbox_mayorNames.GetId(), self.onCheckboxRefreshImage)
        EVT_CHECKBOX(self, self.checkbox_fillEmpty.GetId(), self.onCheckboxRefreshImage)
        self.LoadPrefs()
        self.Region = sc4Region.sc4Region(self.simcityDir)
        return

    def mnuFileOpen(self, event):
        dlg = wxDirDialog(self, 'Choose a Region Folder', self.lastRegionDir)
        print( self.simcityDir)
        if dlg.ShowModal() == wxID_OK:
            print( 'Ok')
            busy = None
            try:
                wxBeginBusyCursor()
                busy = wxBusyInfo("Loading region...\n\nThis may take a moment.", self)
                wxYield()

                try:
                    self.Region.Load(dlg.GetPath())
                    try:
                        self.lastRegionDir = os.path.split(dlg.GetPath())[0]
                        self.SavePrefs()
                    except:
                        pass

                except StandardError, e:
                    msg = wxMessageDialog(self, 'Error loading region.\n%s' % e, 'Error', wxOK)
                    msg.ShowModal()
                    msg.Destroy()
                    return
                else:
                    print( 'Region has %d cities.' % len(self.Region.Cities))
                    self.PopulateRegionTree()
                    self.PopulateRegionSummary()
                    self.GenerateRegionImage()
            finally:
                if busy is not None:
                    busy.Destroy()
                if wxIsBusy():
                    wxEndBusyCursor()

    def mnuFileSave(self, event):
        import os, datetime
        from PIL import Image

        wildcard = 'PNG File (*.png)|*.png|JPG File (*.jpg)|*.jpg'
        outFile = ''
        if self.Region.RegionLoaded:
            i = self.tree_region.GetSelection()
            if i:
                data = self.tree_region.GetPyData(i)
            if data == None:
                outImg = self.Region.RegionPNG
                outFile = "{}-{}".format(self.Region.RegionName, datetime.datetime.now().strftime("%y%m%d"))
            else:
                outImg = data.cityPNG
                if self.checkbox_traffic.IsChecked():
                    if data.trafficPNG:
                        outImg = data.trafficPNG
                outFile = os.path.splitext(data.Filename)[0]
            dlg = wxFileDialog(self, 'Save file as...', os.getcwd(), outFile, wildcard, wxSAVE | wxOVERWRITE_PROMPT)
            if dlg.ShowModal() == wxID_OK:
                busy = None
                try:
                    wxBeginBusyCursor()
                    busy = wxBusyInfo("Saving image...\n\nThis may take a moment.", self)
                    wxYield()

                    path = dlg.GetPath()
                    ext = os.path.splitext(path)[1].lower()
                        
                    print( 'Path:', path)
                    print( self.jpgQuality)
                    if ext in ('.jpg', '.jpeg'):
                        if outImg.mode in ('RGBA', 'LA') or (outImg.mode == 'p' and 'transparency' in outImg.info):
                            bg = Image.new('RGB', outImg.size, (255, 255, 255))
                            bg.paste(outImg, mask=outImg.split()[-1])
                            outImg = bg
                        else:
                            outImg = outImg.convert('RGB')
                        outImg.save(path, 'JPEG', quality=int(self.jpgQuality), optimize=True)
                    else:
                        outImg.save(dlg.GetPath(), 'PNG')
                finally:
                    if busy is not None:
                        busy.Destroy()
                    if wxIsBusy():
                        wxEndBusyCursor()
            dlg.Destroy()
        else:
            msg = wxMessageDialog(self, 'No region open.  Nothing to save.', 'Cannot save', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
        return

    def mnuFileExit(self, event):
        print( 'File Exit!')
        self.Close()

    def __set_properties(self):
        self.SetTitle('Region Census')
        self.SetSize((1200, 800))
        self.checkbox_shrink.SetToolTipString('If the image is larger than the current view this option will make it fit.  It will not expand an image to fit to width.')
        self.checkbox_shrink.SetValue(1)
        self.checkbox_borders.SetToolTipString('An option to show city tile borders.')
        self.checkbox_fillEmpty.SetValue(1)
        self.button_zoom1to1.Enable(0)
        self.button_zoomOut.Enable(0)
        self.button_zoomIn.Enable(0)
        self.splitter.SplitVertically(self.splitter_pane_tree, self.splitter_pane_notebook, 157)

    def __do_layout(self):
        sizer_1 = wxBoxSizer(wxVERTICAL)
        sizer_3 = wxBoxSizer(wxHORIZONTAL)
        sizer_6 = wxBoxSizer(wxVERTICAL)
        sizer_7 = wxStaticBoxSizer(wxStaticBox(self.notebook_image, -1, ''), wxHORIZONTAL)
        sizer_8 = wxBoxSizer(wxVERTICAL)
        sizer_15 = wxBoxSizer(wxVERTICAL)
        sizer_5 = wxBoxSizer(wxHORIZONTAL)
        sizer_4 = wxBoxSizer(wxHORIZONTAL)
        sizer_2 = wxBoxSizer(wxHORIZONTAL)
        sizer_2.Add(self.tree_region, 1, wxEXPAND, 0)
        self.splitter_pane_tree.SetAutoLayout(1)
        self.splitter_pane_tree.SetSizer(sizer_2)
        sizer_2.Fit(self.splitter_pane_tree)
        sizer_2.SetSizeHints(self.splitter_pane_tree)
        sizer_4.Add(self.list_region_info, 1, wxEXPAND, 0)
        self.notebook_region_info.SetAutoLayout(1)
        self.notebook_region_info.SetSizer(sizer_4)
        sizer_4.Fit(self.notebook_region_info)
        sizer_4.SetSizeHints(self.notebook_region_info)
        sizer_5.Add(self.list_city_info, 1, wxEXPAND, 0)
        self.notebook_city_info.SetAutoLayout(1)
        self.notebook_city_info.SetSizer(sizer_5)
        sizer_5.Fit(self.notebook_city_info)
        sizer_5.SetSizeHints(self.notebook_city_info)
        sizer_6.Add((10, 6), 0, 0, 0)
        sizer_15.Add(self.checkbox_shrink, 0, 0, 0)
        sizer_15.Add((10, 5), 0, 0, 0)
        sizer_15.Add(self.checkbox_borders, 0, 0, 0)
        sizer_15.Add((20, 5), 0, 0, 0)
        sizer_15.Add(self.checkbox_traffic, 0, 0, 0)
        sizer_7.Add(sizer_15, 0, wxEXPAND, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_8.Add(self.checkbox_cityNames, 0, 0, 0)
        sizer_8.Add((20, 5), 0, 0, 0)
        sizer_8.Add(self.checkbox_mayorNames, 0, 0, 0)
        sizer_8.Add((20, 5), 0, 0, 0)
        sizer_8.Add(self.checkbox_fillEmpty, 0, 0, 0)
        sizer_7.Add(sizer_8, 0, wxEXPAND, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_7.Add(self.button_zoom1to1, 0, wxALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_7.Add(self.button_zoomOut, 0, wxALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_7.Add(self.button_zoomIn, 0, wxALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7, 0, wxEXPAND, 0)
        sizer_6.Add(self.panel_image, 1, wxEXPAND, 0)
        self.notebook_image.SetAutoLayout(1)
        self.notebook_image.SetSizer(sizer_6)
        sizer_6.Fit(self.notebook_image)
        sizer_6.SetSizeHints(self.notebook_image)
        self.notebook.AddPage(self.notebook_region_info, 'Region Info')
        self.notebook.AddPage(self.notebook_city_info, 'City Info')
        self.notebook.AddPage(self.notebook_image, 'Image')
        sizer_3.Add(self.notebook, 1, wxEXPAND, 0)
        self.splitter_pane_notebook.SetAutoLayout(1)
        self.splitter_pane_notebook.SetSizer(sizer_3)
        sizer_3.Fit(self.splitter_pane_notebook)
        sizer_3.SetSizeHints(self.splitter_pane_notebook)
        sizer_1.Add(self.splitter, 1, wxEXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()
        self.splitter.SetSashPosition(self.splitter.GetSashPosition())

    def onTreeSelChanged(self, event):
        print( 'Tree selection Changed!')
        i = event.GetItem()
        print( '%s' % self.tree_region.GetItemText(i))
        print( '%s' % self.tree_region.GetPyData(i))
        self.PopulateCityInfo(self.tree_region.GetPyData(i))
        self.PopulateImage(self.tree_region.GetPyData(i), self.panel_image.zoom)

    def onCheckboxShrink(self, event):
        if event.Checked():
            self.button_zoomIn.Enable(0)
            self.button_zoomOut.Enable(0)
            self.button_zoom1to1.Enable(0)
            i = self.tree_region.GetSelection()
            if i:
                self.PopulateImage(self.tree_region.GetPyData(i), 0)
        else:
            self.button_zoomIn.Enable(1)
            self.button_zoomOut.Enable(1)
            self.button_zoom1to1.Enable(1)
            i = self.tree_region.GetSelection()
            if i:
                self.PopulateImage(self.tree_region.GetPyData(i), 1)

    def onCheckboxRefreshImage(self, event):
        if self.Region and self.Region.RegionLoaded:
            try:
                wxBeginBusyCursor()
                wxYield()

                i = self.tree_region.GetSelection()
                self.GenerateRegionImage()
                print( 'selection:', i)
                print( self.tree_region.GetPyData(i))
                if i:
                    self.PopulateImage(self.tree_region.GetPyData(i), self.panel_image.zoom)
            finally:
                if wxIsBusy():
                    wxEndBusyCursor()

    def onButtonZoomIn(self, event):
        print( 'Zoom In!')
        print( self.panel_image.zoom)
        zoom = self.panel_image.zoom + 0.2
        if zoom > 4:
            zoom = 4
        i = self.tree_region.GetSelection()
        if i:
            self.PopulateImage(self.tree_region.GetPyData(i), zoom)

    def onButtonZoomOut(self, event):
        zoom = self.panel_image.zoom - 0.2
        if zoom <= 0:
            zoom = 0.2
        i = self.tree_region.GetSelection()
        if i:
            self.PopulateImage(self.tree_region.GetPyData(i), zoom)

    def onButtonZoom1to1(self, event):
        i = self.tree_region.GetSelection()
        if i:
            self.PopulateImage(self.tree_region.GetPyData(i), 1)

    def PopulateRegionTree(self):
        tree = self.tree_region
        tree.DeleteAllItems()
        root = tree.AddRoot(self.Region.RegionName)
        tree.SetPyData(root, None)
        self.SetTitle('Region Census -- %s' % self.Region.RegionName)
        for city in self.Region.Cities:
            if self.hideEmptyCities and not city.MayorName:
                pass
            else:
                item = tree.AppendItem(root, city.Filename)
                tree.SetPyData(item, city)

        tree.Expand(root)
        tree.SelectItem(root)
        return

    def PopulateRegionSummary(self):
        lst = self.list_region_info
        if lst.GetItemCount():
            lst.ClearAll()
        lst.InsertColumn(0, 'Attribute')
        lst.InsertColumn(1, 'Value', width=-1, format=wxLIST_FORMAT_RIGHT)
        i = lst.InsertStringItem(1, 'Residential Population')
        lst.SetStringItem(i, 1, '%d' % self.Region.Residential)
        i = lst.InsertStringItem(2, 'Commercial Population')
        lst.SetStringItem(i, 1, '%d' % self.Region.Commercial)
        i = lst.InsertStringItem(3, 'Industrial Population')
        lst.SetStringItem(i, 1, '%d' % self.Region.Industrial)
        lst.SetColumnWidth(0, wxLIST_AUTOSIZE)
        lst.SetColumnWidth(1, -1)

    def PopulateCityInfo(self, city):
        lst = self.list_city_info
        myCity = city
        lst.ClearAll()
        if myCity:
            lst.InsertColumn(0, 'Attribute')
            lst.InsertColumn(1, 'Value', width=-1, format=wxLIST_FORMAT_RIGHT)
            i = lst.InsertStringItem(1, 'City Name')
            lst.SetStringItem(i, 1, '%s' % myCity.CityName)
            i = lst.InsertStringItem(2, 'Residential Population')
            lst.SetStringItem(i, 1, '%d' % myCity.Residential)
            i = lst.InsertStringItem(3, 'Commercial Population')
            lst.SetStringItem(i, 1, '%d' % myCity.Commercial)
            i = lst.InsertStringItem(4, 'Industrial Population')
            lst.SetStringItem(i, 1, '%d' % myCity.Industrial)
            i = lst.InsertStringItem(5, 'City Funds')
            lst.SetStringItem(i, 1, '%s' % myCity.CityFunds)
            i = lst.InsertStringItem(6, 'Mayor Name')
            lst.SetStringItem(i, 1, '%s' % myCity.MayorName)
            lst.SetColumnWidth(0, wxLIST_AUTOSIZE)
        else:
            lst.InsertColumn(0, 'City')
            lst.InsertColumn(1, 'Res. Pop', width=-1, format=wxLIST_FORMAT_RIGHT)
            lst.InsertColumn(2, 'Com. Pop', width=-1, format=wxLIST_FORMAT_RIGHT)
            lst.InsertColumn(3, 'Ind. Pop', width=-1, format=wxLIST_FORMAT_RIGHT)
            lst.InsertColumn(4, 'City Funds', width=-1, format=wxLIST_FORMAT_RIGHT)
            lst.InsertColumn(5, 'Mayor Name', width=-1, format=wxLIST_FORMAT_RIGHT)
            lst.InsertColumn(6, 'Tile Size', width=-1, format=wxLIST_FORMAT_RIGHT)
            count = 0
            for (index, myCity) in enumerate(self.Region.Cities):
                if self.hideEmptyCities and not myCity.MayorName:
                    pass
                else:
                    i = lst.InsertStringItem(index, myCity.CityName)
                    lst.SetStringItem(i, 1, '%d' % myCity.Residential)
                    lst.SetStringItem(i, 2, '%d' % myCity.Commercial)
                    lst.SetStringItem(i, 3, '%d' % myCity.Industrial)
                    lst.SetStringItem(i, 4, '%s' % myCity.CityFunds)
                    lst.SetStringItem(i, 5, '%s' % myCity.MayorName)
                    lst.SetStringItem(i, 6, '%s' % myCity.TileSize)

    def PopulateImage(self, city, zoom=0):
        if self.checkbox_shrink.IsChecked():
            zoom = 0
        if city:
            if self.checkbox_traffic.IsChecked():
                if city.trafficPNG:
                    cityBMP = city.trafficPNG.convert('RGB')
            else:
                cityBMP = city.cityPNG.convert('RGB')
        else:
            cityBMP = self.Region.RegionPNG.convert('RGB')
        print( 'Populate image', cityBMP)
        img = wxEmptyImage(cityBMP.size[0], cityBMP.size[1])
        img.SetData(cityBMP.tobytes())
        self.panel_image.SetBuffer(img, zoom)

    def GenerateRegionImage(self):
        print( 'GenerateRegionImage')
        if self.Region:
            print( self.Region.RegionPNG)
            self.Region.GenerateRegionImage(traffic=self.checkbox_traffic.IsChecked(), borders=self.checkbox_borders.IsChecked(), cityNames=self.checkbox_cityNames.IsChecked(), mayorNames=self.checkbox_mayorNames.IsChecked(), fillEmptyTiles=self.checkbox_fillEmpty.IsChecked())
            print( 'End GenerateRegionImage')
            i = self.tree_region.GetSelection()
            self.PopulateImage(self.tree_region.GetPyData(i), self.panel_image.zoom)

    def SaveToCSV(self, event):
        import datetime
        if self.Region.RegionLoaded:
            outFile = "{}-{}".format(self.Region.RegionName, datetime.datetime.now().strftime("%y%m%d"))
            dlg = wxFileDialog(self, 'Save file as...', os.getcwd(), outFile, 'CSV File (Comma Seperated Values)|*.csv', wxSAVE | wxOVERWRITE_PROMPT)
            if dlg.ShowModal() == wxID_OK:
                try:
                    wxBeginBusyCursor()
                    wxYield()

                    outFile = open(dlg.GetPath(), 'w')
                    outFile.write('"City Name","Mayor Name","Residential Pop.","Commercial Pop.","Industrial Pop.","Funds","Tile Size"\n')
                    for city in self.Region.Cities:
                        if self.hideEmptyCities == True and not city.MayorName:
                            pass
                        else:
                            outFile.write('"%s",' % city.CityName)
                            outFile.write('"%s",' % city.MayorName)
                            outFile.write('"%s",' % city.Residential)
                            outFile.write('"%s",' % city.Commercial)
                            outFile.write('"%s",' % city.Industrial)
                            outFile.write('"%s",' % city.CityFunds)
                            outFile.write('"%s"\n' % city.TileSize)
                finally:
                    if wxIsBusy():
                        wxEndBusyCursor()

        else:
            msg = wxMessageDialog(self, 'No region open.  Nothing to save.', 'Cannot save', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

    def mnuPrefs(self, event):
        from MyPrefsDialog import MyPrefsDialog
        dlg = MyPrefsDialog(self, -1, '')
        dlg.text_simcityDir.SetValue(os.path.normpath(self.simcityDir))
        dlg.spin_quality.SetValue(self.jpgQuality)
        dlg.checkbox_HideEmpty.SetValue(self.hideEmptyCities)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wxID_OK:
            self.simcityDir = dlg.text_simcityDir.GetValue()
            if -1 < dlg.spin_quality.GetValue() < 101:
                self.jpgQuality = dlg.spin_quality.GetValue()
            if self.hideEmptyCities != dlg.checkbox_HideEmpty.IsChecked():
                self.hideEmptyCities = dlg.checkbox_HideEmpty.IsChecked()
                if self.Region.RegionLoaded:
                    self.PopulateRegionTree()
            self.checkSimcity_1Dat()
            self.SavePrefs()

    def mnuSaveThumbnail(self, event):
        import os, datetime
        from PIL import Image
        wildcard = 'PNG File (*.png)|*.png|JPG File (*.jpg)|*.jpg'
        if self.Region.RegionLoaded:
            from MyThumbSave import MyThumbSave
            dlg = MyThumbSave(self, -1, '')
            (dlg.imgWidth, dlg.imgHeight) = self.Region.RegionPNG.size
            dlg.slider_width.SetRange(10, self.Region.RegionPNG.size[0])
            dlg.slider_width.SetValue(self.thumbnailWidth)
            dlg.calcOutputSize()
            if dlg.ShowModal() == wxID_OK:
                self.thumbnailWidth = dlg.outW
                self.SavePrefs()
                outFile = "{}-{}_thumb".format(self.Region.RegionName, datetime.datetime.now().strftime("%y%m%d"))
                saveDlg = wxFileDialog(self, 'Save file as...', os.getcwd(), outFile, wildcard, wxSAVE | wxOVERWRITE_PROMPT)
                if saveDlg.ShowModal() == wxID_OK:
                    try:
                        wxBeginBusyCursor()
                        wxYield()

                        path = saveDlg.GetPath()
                        ext = os.path.splitext(path)[1].lower()
                        
                        print( 'Path:', path)
                        print( self.jpgQuality)
                        outImg = self.Region.RegionPNG.copy()
                        outImg.thumbnail((dlg.outW, dlg.outH), Image.ANTIALIAS)

                        if ext in ('.jpg', '.jpeg'):
                            if outImg.mode in ('RGBA', 'LA') or (outImg.mode == 'p' and 'transparency' in outImg.info):
                                bg = Image.new('RGB', outImg.size, (255, 255, 255))
                                bg.paste(outImg, mask=outImg.split()[-1])
                                outImg = bg
                            else:
                                outImg = outImg.convert('RGB')
                            outImg.save(path, 'JPEG', quality=int(self.jpgQuality), optimize=True)
                        else:
                            outImg.save(saveDlg.GetPath(), 'PNG')
                    finally:
                        if wxIsBusy():
                            wxEndBusyCursor()
            saveDlg.Destroy()
            dlg.Destroy()
        else:
            msg = wxMessageDialog(self, 'No region open.  Nothing to save.', 'Cannot save', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

    def LoadPrefs(self):
        import ConfigParser
        try:
            config = ConfigParser.ConfigParser()
            config.add_section('options')
            config.set('options', 'simcityDir', 'c:/program files/maxis/simcity 4')
            config.set('options', 'lastRegionDir', '')
            config.set('options', 'jpgQuality', '75')
            config.set('options', 'thumbnailWidth', '700')
            config.set('options', 'hideEmptyCities', '0')
            config.read('regioncensus.ini')
            self.simcityDir = config.get('options', 'simcityDir')
            self.lastRegionDir = config.get('options', 'lastregionDir')
            self.jpgQuality = config.getint('options', 'jpgQuality')
            self.thumbnailWidth = config.getint('options', 'thumbnailWidth')
            self.hideEmptyCities = config.getboolean('options', 'hideEmptyCities')
            print( 'Config read:', self.simcityDir)
            self.checkSimcity_1Dat()
            self.SavePrefs()
        except ConfigParser.Error, e:
            msg = wxMessageDialog(self, 'Problem reading regioncensus.ini\n%s\nUsing default configuration.' % e, 'Warning', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

    def SavePrefs(self):
        import ConfigParser
        try:
            config = ConfigParser.ConfigParser()
            config.add_section('options')
            config.set('options', 'simcityDir', '%s' % self.simcityDir)
            config.set('options', 'lastRegionDir', '%s' % self.lastRegionDir)
            config.set('options', 'jpgQuality', '%s' % self.jpgQuality)
            config.set('options', 'thumbnailWidth', '%s' % self.thumbnailWidth)
            config.set('options', 'hideEmptyCities', self.hideEmptyCities)
            ini = open('regioncensus.ini', 'w')
            config.write(ini)
            ini.close()
        except ConfigParser.Error, e:
            msg = wxMessageDialog(self, 'Problem writing regioncensus.ini\n%s' % e, 'Warning', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()

    def checkSimcity_1Dat(self):
        self.simcity1Dat = os.path.join(self.simcityDir, 'simcity_1.dat')
        if not os.path.exists(self.simcity1Dat):
            msg = wxMessageDialog(self, '%s was not found.\nFill empty tiles will not be available.\nUse Edit->Preferences to set your simcity install location.' % os.path.normpath(self.simcity1Dat), 'Warning', wxOK | wxICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
            self.checkbox_fillEmpty.SetValue(False)
            self.checkbox_fillEmpty.Disable()
            return
        else:
            self.checkbox_fillEmpty.Enable(True)
        if self.Region and self.Region.BlanksLoaded == False:
            self.Region.LoadBlankTiles(self.simcityDir)

    def mnuAbout(self, event):
        from MyAboutDialog import MyAboutDialog
        dlg = MyAboutDialog(self, -1, '')
        dlg.text_about.SetValue('Region Census\n=========================\nOriginal Author:  sawtooth\nRecompiled by: panthercoffee72\nVersion: 0.8.3\n')
        dlg.ShowModal()
