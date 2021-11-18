import wx
import wx.grid
import csv

from pydantic import BaseModel, ValidationError
from member import Member, MemberList, Columns
from event import MemberUpdatedEvent

class MyGrid(wx.grid.Grid):

    list = []

    def __init__(self, parent: wx.Panel, mList: MemberList):

        self.list = mList

        wx.grid.Grid.__init__(self, parent)
        self.SetDefaultColSize (130)
        self.CreateGrid(len(mList), len(Columns))
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.update_member_list)

        for col in Columns:
            self.SetColLabelValue(int(col), col.name)

        for member in mList:
            self.SetCellValue(self.list.index(member), int(Columns.NAME), member.name)
            self.SetCellValue(self.list.index(member), int(Columns.DAYS_OFF), str(member.daysOff))
            self.SetCellValue(self.list.index(member), int(Columns.TRAINING_DAYS), str(member.trainingDays))
            self.SetCellValue(self.list.index(member), int(Columns.ACTIVITY), str(member.activity))


    def update_member_list(self, event):
        row = event.GetRow()
        col = event.GetCol()

        if int(Columns.NAME) == col:
            cell_input = self.GetCellValue(row, col)
        else:
            try:
                cell_input = int(self.GetCellValue(row, col))
            except:
                self.SetCellValue(row, col, '')
                wx.CallAfter(self.Later)

        self.list[row].set_value(col, cell_input)

        wx.PostEvent(self, MemberUpdatedEvent())

        print(self.list)


    def Later(self):
        msgbox = wx.MessageBox('Invalid Input!', 'Error', wx.OK | wx.ICON_HAND | wx.CENTRE)

