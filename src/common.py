import wx

class Common():

    def pop_wrong_input_num(parent: wx.Window):
        """
        Method to show a popup to warn the user a wrong input has been entered.
        :return: nothing.
        """
        message = wx.MessageDialog(parent, "A number is required!", "ERROR", style=wx.OK|wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()