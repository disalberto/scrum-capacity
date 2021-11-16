import wx
import wx.grid
import csv

def getTable(panel: wx.Panel, inputFile: str):
    grid = wx.grid.Grid(panel)
    grid.SetDefaultColSize (120)
    with open("team.csv", 'r') as team:
        reader = csv.reader(team,delimiter=",")
        columns: [] = next(reader)
        ncol = len(columns)
        #team.seek(0)
        rows: List = list(reader)
        nrow = len(rows)

        grid.CreateGrid(nrow, ncol)

        for i in range(ncol):
            grid.SetColLabelValue(i, columns[i])

        for j in range(nrow):
            jrow = rows[j]
            #grid.SetRowLabelValue(j, jrow[0])
            for k in range(len(jrow)):
                grid.SetCellValue(j,k,jrow[k])
    return grid

