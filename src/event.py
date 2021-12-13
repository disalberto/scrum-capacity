import wx.lib.newevent

"""
Custom event to be triggered when an element of the main table is updated.
"""
MemberUpdatedEvent, EVT_MEMBER_UPDATED = wx.lib.newevent.NewEvent()
