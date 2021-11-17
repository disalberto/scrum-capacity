import wx
from capacity import computeCapacity
from table import getTable
from member import MemberList

class MyFrame(wx.Frame):

    DAFAULT_SPRINT_DAYS = "15"
    filepath = ''

    def __init__(self):
        super().__init__(parent=None, title='oRatio - The Capacity Calculator')
        self.SetSize(wx.Size(600, 500))
        self.panel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # JSON part
        jsonSizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, "JSON")

        loadBtn = wx.Button(self.panel, label='Load JSON file')
        loadBtn.Bind(wx.EVT_BUTTON, self.loadFile)
        jsonSizer.Add(loadBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlJson = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_RIGHT, size=(450, -1))
        jsonSizer.Add(self.textCtrlJson, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(jsonSizer, 0, wx.ALL | wx.EXPAND, 5)

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
                                       "JSON files (*.json)|*.json",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()

        self.filepath = openFileDialog.GetPath()
        self.textCtrlJson.SetValue(self.filepath)

        openFileDialog.Destroy()

        self.mList = MemberList.parse_file(openFileDialog.GetPath()).__root__

        grid = getTable(self.panel, self.mList)
        self.mainSizer.Add(grid, 0, wx.ALL | wx.EXPAND, 5)

        # Compute capacity
        self.textCtrlCapa.SetValue(str(computeCapacity(self.mList, int(self.textCtrlDays.GetValue()))))

        # Refresh ui
        self.SetSizerAndFit(self.mainSizer)
        #self.GetParent().Fit()


    def compute(self, event):
        value = self.filepath
        if not value:
            print("Please load a csv file first!")
        else:
            self.textCtrlCapa.SetValue(str(computeCapacity(self.mList, int(self.textCtrlDays.GetValue()))))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
