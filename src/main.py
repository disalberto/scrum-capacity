import wx
from capacity import computeCapacity
from table import getTable

class MyFrame(wx.Frame):

    DAFAULT_SPRINT_DAYS = "15"
    filepath = ''

    def __init__(self):
        super().__init__(parent=None, title='oRatio - The Capacity Calculator')
        self.SetSize(wx.Size(600, 500))
        self.panel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # CSV part
        csvSizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, "CSV")

        loadBtn = wx.Button(self.panel, label='Load CSV file')
        loadBtn.Bind(wx.EVT_BUTTON, self.loadFile)
        csvSizer.Add(loadBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlCsv = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_RIGHT, size=(450, -1))
        csvSizer.Add(self.textCtrlCsv, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(csvSizer, 0, wx.ALL | wx.EXPAND, 5)

        # Capacity part
        capaSizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, "Capacity")

        daysLabel = wx.StaticText(self.panel,-1,style = wx.ALIGN_RIGHT)
        daysLabel.SetLabel("Sprint Days:")
        capaSizer.Add(daysLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.textCtrlDays = wx.TextCtrl(self.panel)
        self.textCtrlDays.SetValue(self.DAFAULT_SPRINT_DAYS)
        self.textCtrlDays.Bind(wx.EVT_TEXT, self.compute)
        capaSizer.Add(self.textCtrlDays, 0, wx.ALL | wx.EXPAND, 5)

        capaLabel = wx.StaticText(self.panel,-1,style = wx.ALIGN_RIGHT)
        capaLabel.SetLabel("Capacity:")
        capaSizer.Add(capaLabel, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlCapa = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.textCtrlCapa.SetValue("0")
        capaSizer.Add(self.textCtrlCapa, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(capaSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.mainSizer)
        self.Show()


    def loadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Csv files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        openFileDialog.GetPath()

        self.filepath = openFileDialog.GetPath()
        self.textCtrlCsv.SetValue(self.filepath)

        openFileDialog.Destroy()

        grid = getTable(self.panel, self.filepath)
        self.mainSizer.Add(grid, 0, wx.ALL | wx.EXPAND, 5)

        # Compute capacity
        self.textCtrlCapa.SetValue(str(computeCapacity(self.filepath, int(self.textCtrlDays.GetValue()))))

        # Refresh ui
        self.SetSizerAndFit(self.mainSizer)
        #self.GetParent().Fit()


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
