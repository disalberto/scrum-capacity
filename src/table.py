import wx
import wx.grid
import csv

from pydantic import BaseModel, ValidationError
from member import Member, MemberList, Columns

def getTable(panel: wx.Panel, inputFile: str):
    grid = wx.grid.Grid(panel)
    grid.SetDefaultColSize (130)

    mList = MemberList.parse_file("team.json").__root__

    grid.CreateGrid(len(mList), len(Columns))

    for col in Columns:
        grid.SetColLabelValue(int(col), col.name)

    for member in mList:
        grid.SetCellValue(mList.index(member), int(Columns.NAME), member.name)
        grid.SetCellValue(mList.index(member), int(Columns.DAYS_OFF), str(member.daysOff))
        grid.SetCellValue(mList.index(member), int(Columns.TRAINING_DAYS), str(member.trainingDays))
        grid.SetCellValue(mList.index(member), int(Columns.ACTIVITY), str(member.activity))

    return grid

