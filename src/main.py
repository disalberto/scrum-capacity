import wx.adv
import datetime
import pandas as pd
import holidays
import jinja2 as jinja
import capacity as cp
import table
import member
import event
import estimation as est
import team_template as team
import common as cm


class MyFrame(wx.Frame):
    def __init__(self):
        """Initialize the main Frame with all the UI content."""
        super().__init__(parent=None, title="oRatio - The Capacity Calculator")
        self.save_btn = None
        self.team_size = None
        self.grid = None
        self._team_table = None

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._content_not_saved: bool = False
        self._estimation_ongoing: bool = False

        # JSON part
        json_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, "")

        new_btn = wx.Button(self, label="Start Estimation")
        new_btn.Bind(wx.EVT_BUTTON, self.new_est)
        json_sizer.Add(new_btn, 0, wx.ALL | wx.RIGHT, 5)

        load_btn = wx.Button(self, label="Load JSON file")
        load_btn.Bind(wx.EVT_BUTTON, self.load_file)
        json_sizer.Add(load_btn, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_json = wx.TextCtrl(
            self, style=wx.TE_READONLY | wx.TE_RIGHT, size=(600, -1)
        )
        json_sizer.Add(self.text_ctrl_json, 0, wx.ALL | wx.EXPAND, 5)

        countries_clean = [
            sub
            for sub in holidays.list_supported_countries()
            if not all(ele.isupper() for ele in sub)
        ]
        self.country = wx.Choice(self, -1, choices=countries_clean)
        self.country.SetStringSelection(cm.Common.DEFAULT_LOCATION)
        json_sizer.Add(self.country, 0, wx.ALL | wx.EXPAND, 4)

        self.main_sizer.Add(json_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Capacity part
        capa_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, "")

        date_from_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        date_from_label.SetLabel("Iteration start:")
        capa_sizer.Add(date_from_label, 0, wx.ALL | wx.EXPAND, 5)

        self.date_from = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime)
        capa_sizer.Add(self.date_from, 0, wx.ALL | wx.EXPAND, 5)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_from_changed, self.date_from)

        date_to_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        date_to_label.SetLabel("Iteration end:")
        capa_sizer.Add(date_to_label, 0, wx.ALL | wx.EXPAND, 5)

        self.date_to = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime)
        self.default_it_end: datetime = datetime.date.today() + datetime.timedelta(
            cm.Common.DEFAULT_SPRINT_DAYS_WEEKENDS
        )
        self.date_to.SetValue(self.default_it_end)
        capa_sizer.Add(self.date_to, 0, wx.ALL | wx.EXPAND, 5)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_to_changed, self.date_to)

        days_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        days_label.SetLabel("Sprint Days:")
        capa_sizer.Add(days_label, 0, wx.ALL | wx.EXPAND, 5)

        self.text_ctrl_days = wx.TextCtrl(self)
        self.text_ctrl_days.SetValue(str(cm.Common.DEFAULT_SPRINT_DAYS))
        self.text_ctrl_days.Bind(wx.EVT_TEXT, self.on_update_text_ctrl_sprint_days)
        self.text_ctrl_days.Disable()
        capa_sizer.Add(self.text_ctrl_days, 0, wx.ALL | wx.EXPAND, 5)

        s_factor_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        s_factor_label.SetLabel("Scrum Factor in %:")
        capa_sizer.Add(s_factor_label, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_s_factor = wx.TextCtrl(self)
        self.text_ctrl_s_factor.SetValue(str(cm.Common.DEFAULT_SCRUM_FACTOR))
        self.text_ctrl_s_factor.Bind(wx.EVT_TEXT, self.on_update_text_ctrl_scrum_factor)
        self.text_ctrl_s_factor.Disable()
        capa_sizer.Add(self.text_ctrl_s_factor, 0, wx.ALL | wx.EXPAND, 5)

        capa_label = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT)
        capa_label.SetLabel("Total Capacity:")
        capa_sizer.Add(capa_label, 0, wx.ALL | wx.RIGHT, 5)

        self.text_ctrl_capa = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.text_ctrl_capa.SetValue(str(cm.Common.DEFAULT_CAPACITY))
        self.text_ctrl_capa.SetForegroundColour(wx.RED)
        capa_sizer.Add(self.text_ctrl_capa, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(capa_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Table part
        self.table_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.table_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.main_sizer)

        self.main_sizer.Layout()

        # Refresh ui
        self.SetSizerAndFit(self.main_sizer)

        self.Show()

    def check_not_saved(self):
        """
        Check if the current content is not saved before allowing its replacement
        :return False-1 if the content is not saved and the user chose to undo
                True if either the content is updated or the user confirmed the action
        """
        return (
            self._content_not_saved
            and wx.MessageBox(
                "Current content has not been saved! Proceed?",
                "Please confirm",
                wx.ICON_QUESTION | wx.YES_NO,
                self,
            )
            == wx.NO
        )

    def new_est(self, _):
        """
        Method to initialize a new estimation with a given number of people in the team (rows)
        :param _: the event of pressing the dedicated button
        :return: nothing.
        """
        if self.check_not_saved():
            return

        dialog = wx.TextEntryDialog(
            self, "Size of the team:", "", style=wx.OK | wx.CANCEL
        )
        if dialog.ShowModal() == wx.ID_OK:

            if not cm.Common.is_number(dialog.GetValue()):
                cm.Common.pop_wrong_input(self, "A number is required!")
                return
            else:
                self.team_size = int(dialog.GetValue())
                # Empty the filepath in case there was some content before restarting with a new estimation
                self.text_ctrl_json.ChangeValue("")

                template: str = team.TEMPLATE

                resulting_json = jinja.Template(template).render(
                    date_from=cm.Common.get_date_value(self.date_from),
                    date_to=cm.Common.get_date_value(self.date_to),
                    range=range(self.team_size),
                    capacity=cm.Common.DEFAULT_CAPACITY,
                    sprint_days=str(self.text_ctrl_days.GetValue()),
                    scrum_factor=cm.Common.DEFAULT_SCRUM_FACTOR,
                )

                # Use the newly defined json to build the UI
                self.fill_content(resulting_json, False)

        dialog.Destroy()

    def load_file(self, _):
        """
        Method that:
            - opens a load file dialog if the corresponding button is pressed
            - sets the filepath in a dedicated text area
            - loads the file content in tabular form
            - triggers the capacity calculation with the original content
        :param _: the event of pressing the button: wx.EVT_BUTTON
        :return: nothing.
        """
        if self.check_not_saved():
            return

        with wx.FileDialog(
            self,
            "Open",
            "",
            "",
            "JSON files (*.json)|*.json",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            self.text_ctrl_json.ChangeValue(path_name)
            self.fill_content(path_name, True)

        self._content_not_saved = False

    def fill_content(self, obj: str, is_file: bool):
        """
        Used to populate a Grid with a json file content and attach it to the main sizer
        :param obj: path of the json file
        :param is_file: true if the input is a filepath, false if json
        :return: nothing.
        """
        try:
            estimation = (
                est.Estimation.parse_file(obj)
                if is_file
                else est.Estimation.parse_raw(obj)
            )
            self.grid = table.MyGrid(self, estimation)
            self._estimation_ongoing = True
        except IOError:
            wx.LogError("Error parsing or opening '%s'." % obj)
            return

        # Init Grid and Save button
        if self._team_table is not None:
            self.delete_all_children_from_sizer(self.table_sizer)

        self._team_table = self.table_sizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 5)
        self.save_btn = wx.Button(self, label="Save table to JSON file")
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_file)
        self.table_sizer.Add(self.save_btn, 0, wx.LEFT, 5)
        self.SetSizerAndFit(self.main_sizer)

        # Set capacity
        capacity: float = estimation.capacity
        self.text_ctrl_capa.ChangeValue(str(capacity))
        self.update_capacity_color(capacity)
        # Set scrum factor
        self.text_ctrl_s_factor.SetValue(str(estimation.scrum_factor))
        self.text_ctrl_s_factor.Enable()

        # Set Dates
        self.date_from.SetValue(
            datetime.datetime.fromisoformat(str(estimation.date_from))
        )
        self.date_to.SetValue(datetime.datetime.fromisoformat(str(estimation.date_to)))

        # Set sprint days
        self.text_ctrl_days.SetValue(str(estimation.sprint_days))
        self.text_ctrl_days.Enable()

        # Event binding
        self.grid.Bind(event.EVT_MEMBER_UPDATED, self.on_update_grid)

        # Refresh ui
        self.save_btn.Disable()
        self.main_sizer.Layout()
        self.SetSizerAndFit(self.main_sizer)

    def save_file(self, _):
        """
        Method used to save the current content of the table to a JSON file
        :param _: the event of pressing the button: wx.EVT_BUTTON
        :return: nothing.
        """

        estimation = est.Estimation(
            date_from=cm.Common.get_date_value(self.date_from),
            date_to=cm.Common.get_date_value(self.date_to),
            sprint_days=float(self.text_ctrl_days.GetValue()),
            scrum_factor=float(self.text_ctrl_s_factor.GetValue()),
            capacity=float(self.text_ctrl_capa.GetValue()),
            member_list=member.MemberList(__root__=self.grid.get_list()),
        ).json()

        with wx.FileDialog(
            self,
            "Save data to JSON file",
            wildcard="JSON files (*.json)|*.json",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path_name = file_dialog.GetPath()
            today: str = datetime.date.today().strftime(cm.Common.ISO_DATE_FORMAT)
            try:
                with open(f"{path_name}_{today}.json", "w") as file:
                    file.write(estimation)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % path_name)

        self.text_ctrl_json.ChangeValue(path_name)
        self.save_btn.Disable()
        self._content_not_saved = False

    @staticmethod
    def delete_all_children_from_sizer(sizer):
        """
        To delete all the children from a given sizer
        Used to avoid multiple table in the same sizer, if a file is loaded twice
        :param sizer: the input sizer to be cleaned
        :return: nothing.
        """
        for child in sizer.GetChildren():
            child.GetWindow().Destroy()

    def update_capacity(self, sprint_days: str = None, scrum_factor: str = None):
        """
        Method to update the capacity text area, and it's color and also the grid's local values.
        :return: nothing.
        """
        capacity = cp.compute_capacity(
            self.grid.get_list(), float(sprint_days), float(scrum_factor)
        )

        self.text_ctrl_capa.ChangeValue(str(capacity))

        self.update_capacity_color(capacity)

        self.save_btn.Enable()
        self._content_not_saved = True

    def update_capacity_color(self, capacity: float):
        """
        Method to update the capacity color in the UI depending on its value
        :param capacity: the computed or retrieved capacity
        :return: nothing.
        """
        if capacity > 40:
            self.text_ctrl_capa.SetForegroundColour(wx.GREEN)
        elif capacity > 20:
            self.text_ctrl_capa.SetForegroundColour(wx.YELLOW)
        else:
            self.text_ctrl_capa.SetForegroundColour(wx.RED)

    def update_sprint_days(self, df, dt):
        """
        Method to automatically update the number of sprint days to reflect
        the start and the end of the iteration
        The complete range of dates is initially computed from the input iteration start and end dates
        Then the weekends and bank holidays are removed
        The length of the resulting list is used to know the real number of days in the iteration
        :param df: the iteration start date
        :param dt: the iteration end date
        :return: nothing
        """
        # Days without weekends
        date_range = pd.date_range(df, dt, freq="B")
        sprint_dates: list[str] = [
            d.strftime(cm.Common.ISO_DATE_FORMAT) for d in date_range
        ]

        # Removing bank holidays
        years: list[int] = [df.year, dt.year]
        years_list: list[int] = list(set(years))

        bank_holidays_dict = dict(
            holidays.CountryHoliday(
                self.country.GetString(self.country.GetCurrentSelection()), years_list
            )
        )
        bank_holidays_dates: list[str] = [
            date.strftime(cm.Common.ISO_DATE_FORMAT)
            for date in bank_holidays_dict.keys()
        ]

        working_dates = [
            elem for elem in sprint_dates if elem not in bank_holidays_dates
        ]

        print("Initial Sprint Dates: " + str(sprint_dates))
        print("Bank Holidays Dates: " + str(bank_holidays_dates))
        print("Effective working days: " + str(working_dates))

        days: int = len(working_dates)
        self.text_ctrl_days.SetValue(str(days))

    def update_text_ctrl(self, evt: wx.Event, default: str):
        """
        If the content of the text boxes is updated:
            - recompute the capacity
            - enable the button save
            - set a boolean saying there is unsaved content
        In case of wrong input, default value is set
        :param evt: the triggered event
        :param default: default value of the text ctrl area
        :return: nothing
        """
        raw_value = evt.GetEventObject().GetValue()

        if cm.Common.is_number(raw_value):
            evt.GetEventObject().ChangeValue(str(float(raw_value)))
            evt.Skip()
        else:
            cm.Common.pop_wrong_input(self, "A number is required!")
            evt.GetEventObject().ChangeValue(default)

        if self._estimation_ongoing:
            self.update_capacity(
                sprint_days=self.text_ctrl_days.GetValue(),
                scrum_factor=self.text_ctrl_s_factor.GetValue(),
            )

    def on_update_text_ctrl_scrum_factor(self, evt):
        """
        Update the capacity if scrum factor changed
        :param evt: the triggered event
        :return: nothing
        """
        self.update_text_ctrl(evt, str(cm.Common.DEFAULT_SCRUM_FACTOR))

    def on_update_text_ctrl_sprint_days(self, evt):
        """
        Update the capacity if sprint days changed
        :param evt: the triggered event
        :return: nothing
        """
        self.update_text_ctrl(evt, str(cm.Common.DEFAULT_SPRINT_DAYS))

    def on_update_grid(self, _):
        """
        If the content of the grid is updated:
            - recompute the capacity
            - enable the button save
            - set a boolean saying there is unsaved content
        :param _: the custom event: EVT_MEMBER_UPDATED
        :return: nothing.
        """
        self.update_capacity(
            sprint_days=self.text_ctrl_days.GetValue(),
            scrum_factor=self.text_ctrl_s_factor.GetValue(),
        )

    def on_date_from_changed(self, evt):
        """
        Method to update the number of sprint days and, as a consequence, the capacity, when the iteration start date
        is modified. The chosen date cannot be later than the iteration end date. If so, a popup is shown and the
        iteration start date is set back to default (execution day)
        :param evt: the event triggering the method call
        :return: nothing
        """
        date_from: datetime = datetime.datetime.fromisoformat(
            cm.Common.get_date_value(evt)
        )

        if date_from > self.date_to.GetValue():
            cm.Common.pop_wrong_input(
                self.GetParent(),
                "The iteration start date cannot be after the end date!",
            )
            self.date_from.SetValue(date_from.today())

        self.update_sprint_days(
            date_from,
            datetime.datetime.fromisoformat(cm.Common.get_date_value(self.date_to)),
        )

    def on_date_to_changed(self, evt):
        """
        Method to update the number of sprint days and, as a consequence, the capacity, when the iteration end date
        is modified. The chosen date cannot be before the iteration start date. If so, a popup is shown and the
        iteration end date is set back to default (execution day + default sprint length)
        :param evt: the event triggering the method call
        :return: nothing
        """
        date_to: datetime = datetime.datetime.fromisoformat(
            cm.Common.get_date_value(evt)
        )

        if date_to < self.date_from.GetValue():
            cm.Common.pop_wrong_input(
                self.GetParent(),
                "The iteration end date cannot be before the start date!",
            )
            self.date_to.SetValue(self.default_it_end)

        self.update_sprint_days(
            datetime.datetime.fromisoformat(cm.Common.get_date_value(self.date_from)),
            date_to,
        )


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
