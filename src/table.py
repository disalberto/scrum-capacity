import wx
import wx.grid
import csv
from pydantic import BaseModel, ValidationError
from column import Columns
from member import Member, MemberList
from event import MemberUpdatedEvent, EVT_MEMBER_UPDATED
from common import Common

class MyGrid(wx.grid.Grid):
    """
    Class of type Grid, used to materialize the content
    of the JSON file (team members) in tabular form.
    """
    _list: MemberList = None

    def __init__(self, parent: wx.Panel, mList: MemberList):
        """
        Init method to initialize a Grid with the content of a given MemberList
        :param parent: the parent panel.
        :param mList: the input list of team members.
        """
        self._list = mList
        self.parentPanel = parent

        wx.grid.Grid.__init__(self, self.parentPanel)
        self.SetDefaultColSize (130)
        self.CreateGrid(len(mList), len(Columns))
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.update_member_list)

        for col in Columns:
            self.SetColLabelValue(int(col), col.name)

        for member in mList:
            self.SetCellValue(self._list.index(member), int(Columns.NAME), member.name)
            self.SetCellValue(self._list.index(member), int(Columns.DAYS_OFF), str(member.days_off))
            self.SetCellValue(self._list.index(member), int(Columns.TRAINING_DAYS), str(member.training_days))
            self.SetCellValue(self._list.index(member), int(Columns.ACTIVITY), str(member.activity))

    def update_member_list(self, event):
        """
        Method to update a given element of the list (row) with the modified content,
        from the corresponding cell (col)
        :param event: the event wx.grid.EVT_GRID_CELL_CHANGED.
        :return: nothing.
        """
        row = event.GetRow()
        col = event.GetCol()

        if int(Columns.NAME) == col:
            cell_input = self.GetCellValue(row, col)
        else:
            # Not column Name
            cell_input = self.GetCellValue(row, col)
            if not cell_input.isnumeric():
                Common.pop_wrong_input_num(self.GetParent())
                cell_input = "0"
                self.SetCellValue(row, col, cell_input)

        self._list[row].set_value(col, cell_input)

        print(str(self._list))

        # Send event for updating the capacity
        wx.PostEvent(self, MemberUpdatedEvent())

    def later(self):
        """
        To warn the user that an invalid content has been put in a given cell.
        :return: nothing.
        """
        msg_box = wx.MessageBox('Invalid Input!', 'Error', wx.OK | wx.ICON_HAND | wx.CENTRE)
