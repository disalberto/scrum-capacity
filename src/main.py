import wx
from capacity import computeCapacity

class MyFrame(wx.Frame):

    DAFAULT_SPRINT_DAYS="15"
    filepath=''

    def __init__(self):
        super().__init__(parent=None, title='Orazio - The Capacity Calculator')
        self.SetSize(wx.Size(600, -1))
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # CSV part
        csvSizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, panel, "CSV")

        loadBtn = wx.Button(panel, label='Load CSV file')
        loadBtn.Bind(wx.EVT_BUTTON, self.loadFile)
        csvSizer.Add(loadBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlCsv = wx.TextCtrl(panel, style=wx.TE_READONLY|wx.TE_RIGHT, size=(450, -1))
        csvSizer.Add(self.textCtrlCsv, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(csvSizer, 0, wx.ALL | wx.EXPAND, 5)

        # Capacity part
        capaSizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, panel, "Capacity")

        daysLabel = wx.StaticText(panel,-1,style = wx.ALIGN_RIGHT)
        daysLabel.SetLabel("Sprint Days:")
        capaSizer.Add(daysLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.textCtrlDays = wx.TextCtrl(panel)
        self.textCtrlDays.SetValue(self.DAFAULT_SPRINT_DAYS)
        capaSizer.Add(self.textCtrlDays, 0, wx.ALL | wx.EXPAND, 5)

        capaBtn = wx.Button(panel, label='Compute')
        capaBtn.Bind(wx.EVT_BUTTON, self.compute)
        capaSizer.Add(capaBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlCapa = wx.TextCtrl(panel, style=wx.TE_READONLY)
        capaSizer.Add(self.textCtrlCapa, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(capaSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.textCtrlCapa.SetValue("0")

        panel.SetSizer(mainSizer)
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
            self.textCtrlCapa.SetValue(str(computeCapacity(self.filepath, int(self.textCtrlDays.GetValue()))))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
