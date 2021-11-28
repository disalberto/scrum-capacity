import wx

class Common():

    DAFAULT_SPRINT_DAYS: float = 15
    DEFAULT_CAPACITY: float = 0.0
    DAFAULT_SCRUM_FACTOR: float = 80.0

    def pop_wrong_input_num(parent: wx.Window):
        """
        Method to show a popup to warn the user a wrong input has been entered.
        :return: nothing.
        """
        message = wx.MessageDialog(parent, "A number is required!", "ERROR", style=wx.OK|wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()

    def is_number(s: str):
        try:
            float(s)
            return True
        except ValueError:
            return False