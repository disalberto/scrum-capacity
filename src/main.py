import wx
from capacity import computeCapacity

class MyFrame(wx.Frame):

    filepath=''

    def __init__(self):
        super().__init__(parent=None, title='Capacity Calculator')
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        loadBtn = wx.Button(panel, label='Load CSV file')
        loadBtn.Bind(wx.EVT_BUTTON, self.loadFile)
        sizer.Add(loadBtn, 0, wx.ALL | wx.CENTER, 5)

        self.textCtrlCsv = wx.TextCtrl(panel, style=wx.TE_READONLY)
        sizer.Add(self.textCtrlCsv, 0, wx.ALL | wx.EXPAND, 5)

        capaBtn = wx.Button(panel, label='Compute Capacity')
        capaBtn.Bind(wx.EVT_BUTTON, self.compute)
        sizer.Add(capaBtn, 0, wx.ALL | wx.CENTER, 5)

        self.textCtrlCapa = wx.TextCtrl(panel, style=wx.TE_READONLY)
        sizer.Add(self.textCtrlCapa, 0, wx.ALL | wx.EXPAND, 5)
        self.textCtrlCapa.SetValue("0")

        panel.SetSizer(sizer)
        self.Show()


    def loadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Csv files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        openFileDialog.GetPath()

        self.textCtrlCsv.SetValue(openFileDialog.GetPath())
        self.filepath = openFileDialog.GetPath()

        openFileDialog.Destroy()


    def compute(self, event):
        value = self.filepath
        if not value:
            print("Please load a csv file first!")
        else:
            print(self.filepath)
            self.textCtrlCapa.SetValue(str(computeCapacity(self.filepath)))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
