import wx


class Common():
    DEFAULT_SPRINT_DAYS: float = 15
    DEFAULT_CAPACITY: float = 0.0
    DEFAULT_SCRUM_FACTOR: float = 80.0

    def pop_wrong_input_num(self: wx.Window):
        """
        Method to show a popup to warn the user a wrong input has been entered.
        :return: nothing.
        """
        message = wx.MessageDialog(self, "A number is required!", "ERROR", style=wx.OK | wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()

    def is_number(val: str):
        try:
            float(val)
            return True
        except ValueError:
            return False
