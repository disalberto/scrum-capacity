# pylint: disable=function-redefined

from datetime import datetime
import wx
import wx.adv
import multipledispatch as md


class Common:
    """Class Common for constants and functions"""

    DEFAULT_SPRINT_DAYS: float = 15.0
    DEFAULT_SPRINT_DAYS_WEEKENDS: float = 21.0
    DEFAULT_CAPACITY: float = 0.0
    DEFAULT_SCRUM_FACTOR: float = 20.0
    DEFAULT_LOCATION: str = "France"
    DEFAULT_ITERATION_DEPTH: int = 3
    ISO_DATE_FORMAT: str = "%Y-%m-%d"
    ROUND_PRECISION = 2

    @staticmethod
    def pop_wrong_input(parent: wx.Window, message: str):
        """
        Method to show a popup to warn the user a wrong input has been entered.
        :return: nothing.
        """
        message = wx.MessageDialog(
            parent, message, "ERROR", style=wx.OK | wx.ICON_ERROR
        )
        message.ShowModal()
        message.Destroy()

    @staticmethod
    def is_number(par: str):
        """
        Method to check if the passed argument is numeric or not
        :param par: input param
        :return: True if input param is a number, False otherwise
        """
        try:
            float(par)
            return True
        except ValueError:
            return False

    @staticmethod
    @md.dispatch(wx.adv.DatePickerCtrl)
    def get_date_value(date: wx.adv.DatePickerCtrl):
        """
        Method to return a string representing the input date in ISO format
        :param date: input date of type DatePickerCtrl (from UI)
        :return: the ISO formatted date
        """
        return str(date.GetValue().Format(Common.ISO_DATE_FORMAT))

    @staticmethod
    @md.dispatch(wx.adv.DateEvent)
    def get_date_value(evt: wx.adv.DateEvent):
        """
        Method to return a string representing the input date in ISO format
        :param evt: input date wrapped in a DateEvent (date changed)
        :return: the ISO formatted date
        """
        return str(evt.GetDate().Format(Common.ISO_DATE_FORMAT))

    @staticmethod
    def get_str_from_datetime(date: datetime) -> str:
        """
        Method to convert a datetime into string with the ISO format
        :param date input date
        :return: the corresponding ISO formatted string
        """
        return str(date.strftime(Common.ISO_DATE_FORMAT))

    @staticmethod
    def get_datetime_from_string(date: str) -> datetime:
        """
        Method to convert a string into datetime
        :param date input date in string ISO format
        :return: the corresponding datetime
        """
        return datetime.strptime(date, Common.ISO_DATE_FORMAT)
