from wxPython.wx import *
from MyFrame import MyFrame

class MyApp(wxApp):
    def OnInit(self):
        frame = MyFrame(None, -1, "Region Census")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()