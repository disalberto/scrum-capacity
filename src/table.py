import wx.grid
from column import Columns
from member import Member
from estimation import Estimation
from event import MemberUpdatedEvent
from common import *
from capacity import member_capacity


class MyGrid(wx.grid.Grid):
    """
    Class of type Grid, used to materialize the content
    of the JSON file (team members) in tabular form.
    """

    _list: list[Member] = None
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
        self.SetDefaultColSize(130)
        self.CreateGrid(len(self._list), len(Columns))
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.update_member_list)

        for col in Columns:
            self.SetColLabelValue(int(col), col.name)

        for member in self._list:
            self.SetCellValue(self._list.index(member), int(Columns.NAME), member.name)
            self.SetCellValue(
                self._list.index(member), int(Columns.DAYS_OFF), str(member.days_off)
            )
            self.SetCellValue(
                self._list.index(member),
                int(Columns.TRAINING_DAYS),
                str(member.training_days),
            )
            self.SetCellValue(
                self._list.index(member),
                int(Columns.SUPPORT_DAYS),
                str(member.support_days),
            )
            self.SetCellValue(
                self._list.index(member), int(Columns.ACTIVITY), str(member.activity)
            )

            # Initial capacity computation
            capacity = member_capacity(member, self._sprint_days, self._scrum_factor)
            member.capacity = capacity
            self.SetCellValue(
                self._list.index(member), int(Columns.CAPACITY), str(capacity)
            )
            self.SetReadOnly(self._list.index(member), int(Columns.CAPACITY), True)

            self.SetCellValue(
                self._list.index(member), int(Columns.NOTES), member.notes
            )
            self.SetColSize(int(Columns.NOTES), 250)
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

        if int(Columns.NAME) == col or int(Columns.NOTES) == col:
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
            self._list[row].set_value(int(Columns.CAPACITY), new_capacity)
            self.SetCellValue(row, int(Columns.CAPACITY), str(new_capacity))

        print(str(self._list))

        # Send event for updating the TOTAL capacity and the related text box
        wx.PostEvent(self, MemberUpdatedEvent())
