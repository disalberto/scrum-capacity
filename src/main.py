from jinja2 import Template
from capacity import compute_capacity
from table import MyGrid
from member import MemberList
from event import EVT_MEMBER_UPDATED
from estimation import Estimation
from team_template import TEMPLATE
from common import *


class MyFrame(wx.Frame):

    def __init__(self):
        """ Initialize the main Frame with all the UI content. """
        super().__init__(parent=None, title='oRatio - The Capacity Calculator')
        self.save_btn = None
        self.team_size = None
        self.grid = None
        self._team_table = None

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._content_not_saved: bool = False

        # JSON part
        json_sizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self, "")

        new_btn = wx.Button(self, label='Start Estimation')
        new_btn.Bind(wx.EVT_BUTTON, self.new_est)
        json_sizer.Add(new_btn, 0, wx.ALL | wx.RIGHT, 5)

        load_btn = wx.Button(self, label='Load JSON file')
        load_btn.Bind(wx.EVT_BUTTON, self.load_file)
        json_sizer.Add(load_btn, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_json = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_RIGHT, size=(500, -1))
        json_sizer.Add(self.text_ctrl_json, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(json_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Capacity part
        capa_sizer = sz = wx.StaticBoxSizer(wx.HORIZONTAL, self, "")

        days_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        days_label.SetLabel("Sprint Days:")
        capa_sizer.Add(days_label, 0, wx.ALL | wx.EXPAND, 5)

        self.text_ctrl_days = wx.TextCtrl(self)
        self.text_ctrl_days.SetValue(str(Common.DEFAULT_SPRINT_DAYS))
        self.text_ctrl_days.Bind(wx.EVT_TEXT, self.on_update_text_ctrl)
        self.text_ctrl_days.Disable()
        capa_sizer.Add(self.text_ctrl_days, 0, wx.ALL | wx.EXPAND, 5)

        sfactor_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        sfactor_label.SetLabel("Scrum Factor in %:")
        capa_sizer.Add(sfactor_label, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_sfactor = wx.TextCtrl(self)
        self.text_ctrl_sfactor.SetValue(str(Common.DEFAULT_SCRUM_FACTOR))
        self.text_ctrl_sfactor.Bind(wx.EVT_TEXT, self.on_update_text_ctrl)
        self.text_ctrl_sfactor.Disable()
        capa_sizer.Add(self.text_ctrl_sfactor, 0, wx.ALL | wx.EXPAND, 5)

        capa_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        capa_label.SetLabel("Total Capacity:")
        capa_sizer.Add(capa_label, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_capa = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.text_ctrl_capa.SetValue(str(Common.DEFAULT_CAPACITY))
        self.text_ctrl_capa.SetForegroundColour(wx.RED)
        capa_sizer.Add(self.text_ctrl_capa, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(capa_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Table part
        self.table_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.table_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.main_sizer)

        self.main_sizer.Layout()

        # Refresh ui
        self.SetSizerAndFit(self.main_sizer)

        self.Show()

    def check_not_saved(self):
        """
        Check if the current content is not saved before allowing its replacement.
        :return False-1 if the content is not saved and the user chose to undo,
                True if either the content is updated or the user confirmed the action.
        """
        return self._content_not_saved and \
               wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO

    def new_est(self, event):
        """
        Method to initialize a new estimation with a given number of people in the team (rows).
        :param event: the event of pressing the dedicated button.
        :return: nothing.
        """
        if self.check_not_saved():
            return

        dialog = wx.TextEntryDialog(self, "Size of the team:", "", style=wx.OK | wx.CANCEL)
        if dialog.ShowModal() == wx.ID_OK:

            if not Common.is_number(dialog.GetValue()):
                Common.pop_wrong_input_num(self)
                return
            else:
                self.team_size = int(dialog.GetValue())
                # Empty the filepath in case there was some content before restarting with a new estimation
                self.text_ctrl_json.ChangeValue("")

                template: str = TEMPLATE
                resulting_json = Template(template).render(range=range(self.team_size),
                                                           capacity=Common.DEFAULT_CAPACITY,
                                                           sprint_days=Common.DEFAULT_SPRINT_DAYS,
                                                           scrum_factor=Common.DEFAULT_SCRUM_FACTOR)

                # Use the newly defined json to build the UI
                self.fill_content(resulting_json, False)

        dialog.Destroy()

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
        if self.check_not_saved():
            return

        with wx.FileDialog(self, "Open", "", "", "JSON files (*.json)|*.json",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            self.text_ctrl_json.ChangeValue(path_name)
            self.fill_content(path_name, True)

        self._content_not_saved = False

    def fill_content(self, obj: str, is_file: bool):
        """
        Used to populate a Grid with a json file content and attach it to the main sizer.
        :param obj: path of the json file.
        :param is_file: true if the input is a filepath, false if json
        :return: nothing.
        """
        try:
            estimation = Estimation.parse_file(obj) if is_file else Estimation.parse_raw(obj)
            self.grid = MyGrid(self, estimation)
        except IOError:
            wx.LogError("Error parsing or opening '%s'." % obj)
            return

        # Init Grid and Save button
        if self._team_table is not None:
            self.delete_all_children_from_sizer(self.table_sizer)

        self._team_table = self.table_sizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 5)
        self.save_btn = wx.Button(self, label='Save table to JSON file')
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_file)
        self.table_sizer.Add(self.save_btn, 0, wx.LEFT, 5)
        self.SetSizerAndFit(self.main_sizer)

        # Set capacity
        capacity: float = estimation.capacity
        self.text_ctrl_capa.ChangeValue(str(capacity))
        self.update_capacity_color(capacity)
        # Set scrum factor
        self.text_ctrl_sfactor.SetValue(str(estimation.scrum_factor))
        self.text_ctrl_sfactor.Enable()
        # Set sprint days
        self.text_ctrl_days.SetValue(str(estimation.sprint_days))
        self.text_ctrl_days.Enable()

        # Event binding
        self.grid.Bind(EVT_MEMBER_UPDATED, self.on_update_grid)

        # Refresh ui
        self.save_btn.Disable()
        self.main_sizer.Layout()
        self.SetSizerAndFit(self.main_sizer)

    def save_file(self, event):
        """
        Method used to save the current content of the table to a JSON file.
        :param event: the event of pressing the button: wx.EVT_BUTTON.
        :return: nothing.
        """

        estimation = Estimation(sprint_days=float(self.text_ctrl_days.GetValue()),
                                scrum_factor=float(self.text_ctrl_sfactor.GetValue()),
                                capacity=float(self.text_ctrl_capa.GetValue()),
                                member_list=MemberList(__root__=self.grid._list)).json()

        with wx.FileDialog(self, "Save data to JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            try:
                with open(path_name, 'w') as file:
                    file.write(estimation)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % path_name)

        self.text_ctrl_json.ChangeValue(path_name)
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

    def update_capacity(self, sprint_days: str = None, scrum_factor: str = None):
        """
        Method to update the capacity text area and it's color and also the grid's local values.
        :return: nothing.
        """
        capacity = compute_capacity(self.grid._list, float(sprint_days), float(scrum_factor))

        self.text_ctrl_capa.ChangeValue(str(capacity))

        self.update_capacity_color(capacity)

        self.save_btn.Enable()
        self._content_not_saved = True

    def update_capacity_color(self, capacity: float):
        """
        Method to update the capacity color in the UI depending on its value.
        :param capacity: the computed or retrieved capacity.
        :return: nothing.
        """
        if capacity > 40:
            self.text_ctrl_capa.SetForegroundColour(wx.GREEN)
        elif capacity > 20:
            self.text_ctrl_capa.SetForegroundColour(wx.YELLOW)
        else:
            self.text_ctrl_capa.SetForegroundColour(wx.RED)

    ################################################# Events Handling ##################################################

    def on_update_text_ctrl(self, event):
        """
        If the content of the text boxes is updated:
            - recompute the capacity,
            - enable the button save,
            - set a boolean saying there is unsaved content.
        :param event: the custom event: EVT_MEMBER_UPDATED.
        :return: nothing.
        """
        raw_value = event.GetEventObject().GetValue()

        if Common.is_number(raw_value):
            event.GetEventObject().ChangeValue(str(float(raw_value)))
            event.Skip()
        else:
            Common.pop_wrong_input_num(self)
            event.GetEventObject().ChangeValue("0.0")

        self.update_capacity(sprint_days=self.text_ctrl_days.GetValue(),
                             scrum_factor=self.text_ctrl_sfactor.GetValue())

    def on_update_grid(self, event):
        """
        If the content of the grid is updated:
            - recompute the capacity,
            - enable the button save,
            - set a boolean saying there is unsaved content.
        :param event: the custom event: EVT_MEMBER_UPDATED.
        :return: nothing.
        """
        self.update_capacity(sprint_days=self.text_ctrl_days.GetValue(),
                             scrum_factor=self.text_ctrl_sfactor.GetValue())


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
