import wx.grid
from column import TeamColumns
from member import Member
from estimation import Estimation
from event import MemberUpdatedEvent
from common import *
from capacity import member_capacity
from typing import List


class TeamGrid(wx.grid.Grid):
    """
    Class of type Grid, used to materialize the content
    of the JSON file (team members) in tabular form.
    """

    _list: List[Member] = []
    _sprint_days: float = Common.DEFAULT_SPRINT_DAYS
    _scrum_factor: float = Common.DEFAULT_SCRUM_FACTOR

    def get_list(self):
        return self._list

    def __init__(self, parent: wx.Frame, estimation: Estimation):
        """
        Init method to initialize a Grid with the content of a given MemberList
        :param parent: the parent panel
        :param estimation: the Estimation (list and other info)
        """
        self._list = estimation.member_list.__root__
        self._sprint_days = estimation.sprint_days
        self._scrum_factor = estimation.scrum_factor

        self.parentPanel = parent

        wx.grid.Grid.__init__(self, self.parentPanel)
        self.SetDefaultColSize(160)
        self.CreateGrid(len(self._list), len(TeamColumns))
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.update_member_list)

        for col in TeamColumns:
            self.SetColLabelValue(col.index, col.label)

        for member in self._list:
            self.SetCellValue(
                self._list.index(member), TeamColumns.NAME.index, member.name
            )
            self.SetCellValue(
                self._list.index(member),
                TeamColumns.DAYS_OFF.index,
                str(member.days_off),
            )
            self.SetCellValue(
                self._list.index(member),
                TeamColumns.TRAINING_DAYS.index,
                str(member.training_days),
            )
            self.SetCellValue(
                self._list.index(member),
                TeamColumns.SUPPORT_DAYS.index,
                str(member.support_days),
            )
            self.SetCellValue(
                self._list.index(member),
                TeamColumns.ACTIVITY.index,
                str(member.activity),
            )

            # Initial capacity computation
            capacity = member_capacity(member, self._sprint_days, self._scrum_factor)
            member.capacity = capacity
            self.SetCellValue(
                self._list.index(member), TeamColumns.CAPACITY.index, str(capacity)
            )
            self.SetReadOnly(self._list.index(member), TeamColumns.CAPACITY.index, True)

            self.SetCellValue(
                self._list.index(member), TeamColumns.NOTES.index, member.notes
            )
            self.SetColSize(TeamColumns.NOTES.index, 250)
            self.ForceRefresh()

    def update_member_list(self, event):
        """
        Method to update a given element of the list (row) with the modified content,
        from the corresponding cell (col)
        :param event: the event wx.grid.EVT_GRID_CELL_CHANGED.
        :return: nothing.
        """
        row = event.GetRow()
        col = event.GetCol()
        updated: bool = False

        if TeamColumns.NAME.index == col or TeamColumns.NOTES.index == col:
            cell_input = self.GetCellValue(row, col)
            updated = True
        else:
            # Not column Name
            cell_input = self.GetCellValue(row, col)
            if not Common.is_number(cell_input):
                Common.pop_wrong_input(self.GetParent(), "A number is required!")
                # Back to the original value
                cell_input = str(self._list[row].get_value(col))
                self.SetCellValue(row, col, cell_input)
            else:
                self.SetCellValue(row, col, str(float(cell_input)))
                updated = True

        if updated:
            self._list[row].set_value(col, cell_input)

            # Update LOCAL capacity
            new_capacity = member_capacity(
                self._list[row], self._sprint_days, self._scrum_factor
            )
            self._list[row].set_value(TeamColumns.CAPACITY.index, new_capacity)
            self.SetCellValue(row, TeamColumns.CAPACITY.index, str(new_capacity))

        print(str(self._list))

        # Send event for updating the TOTAL capacity and the related text box
        wx.PostEvent(self, MemberUpdatedEvent())
