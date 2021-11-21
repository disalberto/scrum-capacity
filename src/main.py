import wx
from capacity import compute_capacity
from table import MyGrid
from member import MemberList
from event import EVT_MEMBER_UPDATED

class MyFrame(wx.Frame):

    DAFAULT_SPRINT_DAYS = "15"

    def __init__(self):
        super().__init__(parent=None, title='oRatio - The Capacity Calculator')
        self.SetSize(wx.Size(600, 500))
        self.panel = wx.Panel(self)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self._team_table: wx.SizerItem = None
        self._content_not_saved: bool = False

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
        self.textCtrlDays.Bind(wx.EVT_TEXT, self.on_update_days)
        capaSizer.Add(self.textCtrlDays, 0, wx.ALL | wx.EXPAND, 5)

        capaLabel = wx.StaticText(self.panel,-1,style = wx.ALIGN_RIGHT)
        capaLabel.SetLabel("Capacity:")
        capaSizer.Add(capaLabel, 0, wx.ALL | wx.RIGHT, 5)

        self.textCtrlCapa = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.textCtrlCapa.SetValue("0")
        capaSizer.Add(self.textCtrlCapa, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(capaSizer, 0, wx.ALL | wx.EXPAND, 5)

        # Table part
        self.tableSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.tableSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.mainSizer)
        self.Show()


    def loadFile(self, event):

        if self._content_not_saved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        with wx.FileDialog(self, "Open", "", "", "JSON files (*.json)|*.json",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.textCtrlJson.SetValue(pathname)
            try:
                self.grid = MyGrid(self.panel, MemberList.parse_file(pathname).__root__)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

            self.grid.Bind(EVT_MEMBER_UPDATED, self.on_update_table)

            if self._team_table != None:
                self.delete_all_children_from_sizer(self.tableSizer)

            self._team_table = self.tableSizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 5)
            self.add_button_save()

            self.mainSizer.Layout()

            # Compute capacity
            self.textCtrlCapa.SetValue(str(compute_capacity(MemberList.parse_file(pathname).__root__,
                                                            int(self.textCtrlDays.GetValue()))))
            # Refresh ui
            self.SetSizerAndFit(self.mainSizer)


    def save_file(self, event):
        mlist: MemberList = MemberList(__root__ = self.grid._list)
        new_json = mlist.json()

        with wx.FileDialog(self, "Save table to JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    file.write(new_json)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

        self._content_not_saved = False


    def on_update_table(self, event):
        self.textCtrlCapa.SetValue(str(compute_capacity(self.grid._list, int(self.textCtrlDays.GetValue()))))
        self.saveBtn.Enable()
        self._content_not_saved = True

    def on_update_days(self, event):
        self.textCtrlCapa.SetValue(str(compute_capacity(self.grid._list, int(self.textCtrlDays.GetValue()))))


    def delete_all_children_from_sizer(self, sizer):
        for child in sizer.GetChildren():
            child.GetWindow().Destroy()


    def add_button_save(self):
        self.saveBtn = wx.Button(self.panel, label='Save table to JSON file')
        self.saveBtn.Disable()
        self.saveBtn.Bind(wx.EVT_BUTTON, self.save_file)
        self.tableSizer.Add(self.saveBtn, 0, wx.LEFT, 5)
        self.SetSizerAndFit(self.mainSizer)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
