import wx
from capacity import compute_capacity
from table import MyGrid
from member import MemberList
from event import EVT_MEMBER_UPDATED

class MyFrame(wx.Frame):

    DAFAULT_SPRINT_DAYS = "15"
    DEFAULT_EMPTY_TEAM_PATH = "../src/default_team.json"

    def __init__(self):
        """ Initialize the main Frame with all the UI content. """
        super().__init__(parent=None, title='oRatio - The Capacity Calculator')
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._team_table: wx.SizerItem = None
        self._content_not_saved: bool = False

        # JSON part
        json_sizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self, "JSON")

        load_btn = wx.Button(self, label='Load JSON file')
        load_btn.Bind(wx.EVT_BUTTON, self.load_file)
        json_sizer.Add(load_btn, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_json = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_RIGHT, size=(450, -1))
        json_sizer.Add(self.text_ctrl_json, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(json_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Capacity part
        capa_sizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self, "Capacity")

        days_label = wx.StaticText(self, -1, style = wx.ALIGN_RIGHT)
        days_label.SetLabel("Sprint Days:")
        capa_sizer.Add(days_label, 0, wx.ALL | wx.EXPAND, 5)

        self.text_ctrl_days = wx.TextCtrl(self)
        self.text_ctrl_days.SetValue(self.DAFAULT_SPRINT_DAYS)
        self.text_ctrl_days.Bind(wx.EVT_TEXT, self.on_update_days)
        capa_sizer.Add(self.text_ctrl_days, 0, wx.ALL | wx.EXPAND, 5)

        capa_label = wx.StaticText(self, -1, style = wx.ALIGN_RIGHT)
        capa_label.SetLabel("Capacity:")
        capa_sizer.Add(capa_label, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_capa = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.text_ctrl_capa.SetValue("0")
        capa_sizer.Add(self.text_ctrl_capa, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(capa_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Table part
        self.table_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.table_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.fill_grid(self.DEFAULT_EMPTY_TEAM_PATH)

        self.SetSizer(self.main_sizer)
        self.Show()

    def load_file(self, event):
        """
        Method that:
            - opens a load file dialog if the corresponding button is pressed,
            - sets the filepath in a dedicated text area,
            - loads the file content in tabular form,
            - triggers the capacity calculation with the original content.
        :param event: the event of pressing the button: wx.EVT_BUTTON.
        :return: nothing.
        """
        if self._content_not_saved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        with wx.FileDialog(self, "Open", "", "", "JSON files (*.json)|*.json",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            self.text_ctrl_json.SetValue(path_name)
            self.fill_grid(path_name)

            # Compute capacity
            self.text_ctrl_capa.SetValue(str(compute_capacity(MemberList.parse_file(path_name).__root__,
                                                              int(self.text_ctrl_days.GetValue()))))


    def fill_grid(self, path_name: str):
        """
        Used to populate a Grid with a json file content and attach it to the main sizer.
        :param path_name: path of the json file.
        :return: nothing.
        """
        try:
            self.grid = MyGrid(self, MemberList.parse_file(path_name).__root__)
        except IOError:
            wx.LogError("Cannot open file '%s'." % path_name)

        self.grid.Bind(EVT_MEMBER_UPDATED, self.on_update_table)

        if self._team_table != None:
            self.delete_all_children_from_sizer(self.table_sizer)

        self._team_table = self.table_sizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 5)
        self.add_button_save()

        self.main_sizer.Layout()

        # Refresh ui
        self.SetSizerAndFit(self.main_sizer)

    def save_file(self, event):
        """
        Method used to save the current content of the table to a JSON file.
        :param event: the event of pressing the button: wx.EVT_BUTTON.
        :return: nothing.
        """
        new_json = MemberList(__root__ = self.grid._list).json()

        with wx.FileDialog(self, "Save table to JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            try:
                with open(path_name, 'w') as file:
                    file.write(new_json)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % path_name)

        self.text_ctrl_json.SetValue(path_name)
        self.save_btn.Disable()
        self._content_not_saved = False

    def delete_all_children_from_sizer(self, sizer):
        """
        To delete all the children from a given sizer.
        Used to avoid multiple table in the same sizer, if a file is loaded twice.
        :param sizer: the input sizer to be cleaned.
        :return: nothing.
        """
        for child in sizer.GetChildren():
            child.GetWindow().Destroy()

    def add_button_save(self):
        """
        Method to append a save button to a the table sizer.
        :return: nothing.
        """
        self.save_btn = wx.Button(self, label='Save table to JSON file')
        self.save_btn.Disable()
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_file)
        self.table_sizer.Add(self.save_btn, 0, wx.LEFT, 5)
        self.SetSizerAndFit(self.main_sizer)

    # Events Handling
    def on_update_table(self, event):
        """
        If the content of the dable is updated:
            - recompute the capacity,
            - enable the button save,
            - set a boolean saying there is unsaved content.
        :param event: the custom event: EVT_MEMBER_UPDATED.
        :return: nothing.
        """
        self.text_ctrl_capa.SetValue(str(compute_capacity(self.grid._list, int(self.text_ctrl_days.GetValue()))))
        self.save_btn.Enable()
        self._content_not_saved = True

    def on_update_days(self, event):
        """
        To recompute the capacity if the number of days in the selected sprint have changed.
        :param event: an event of changing the text: wx.EVT_TEXT.
        :return: nothing.
        """
        self.text_ctrl_capa.SetValue(str(compute_capacity(self.grid._list, int(self.text_ctrl_days.GetValue()))))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
