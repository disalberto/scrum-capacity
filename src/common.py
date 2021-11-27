import wx

class Common():

    def check_int(self, to_check: str):
        try:
            ret = int(to_check)
        except:
            message = wx.MessageDialog(self, "An integer is required!", "ERROR", style=wx.OK|wx.ICON_ERROR)
            message.ShowModal()
            message.Destroy()
            ret = 0
        return ret