import wx
import wx.adv
from multipledispatch import dispatch

"""Module to group commonly used constants and functions"""


class Common:
    DEFAULT_SPRINT_DAYS: float = 15.0
    DEFAULT_SPRINT_DAYS_WEEKENDS: float = 21.0
    DEFAULT_CAPACITY: float = 0.0
    DEFAULT_SCRUM_FACTOR: float = 80.0
    DEFAULT_LOCATION: str = "France"
    ISO_DATE_FORMAT: str = "%Y-%m-%d"

    def pop_wrong_input(self: wx.Window, message: str):
        """
        Method to show a popup to warn the user a wrong input has been entered.
        :return: nothing.
        """
        message = wx.MessageDialog(self, message, "ERROR", style=wx.OK | wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()

    def is_number(self: str):
        try:
            float(self)
            return True
        except ValueError:
            return False

    @dispatch(wx.adv.DatePickerCtrl)
    def get_date_value(self, date: wx.adv.DatePickerCtrl):
        """
        Method to return a string representing the input date in ISO format
        :param date: input date of type DatePickerCtrl (from UI)
        :return: the ISO formatted date
        """
        return str(date.GetValue().Format(Common.ISO_DATE_FORMAT))

    @dispatch(wx.adv.DateEvent)
    def get_date_value(self, evt: wx.adv.DateEvent):
        """
        Method to return a string representing the input date in ISO format
        :param evt: input date wrapped in a DateEvent (date changed)
        :return: the ISO formatted date
        """
        return str(evt.GetDate().Format(Common.ISO_DATE_FORMAT))
