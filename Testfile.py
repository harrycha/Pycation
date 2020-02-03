#!/bin/env python

import os, sys, string, stat
from types import *

dir_path = path = os.getcwd()
sys.path.insert(0, path)
os.chdir(path)  # change working to file directory

dir_parts = string.splitfields(path, '\\')
cnt = len(dir_parts) - 1
dir_parts[cnt] = "Python"
pyth_dir = string.joinfields(dir_parts, '\\')

sys.path.insert(0, pyth_dir)

import wx
import wx.grid

from wxUtil import MessageDlg, OnFileDlg, OnFileDlgMulti
from wxUtil import SetToolPath

all_file = "All Files (*.*)|*.*"
text_file = "Text (*.txt)|*.txt|All Files (*.*)|*.*"
csv_file = "Comma Delimited(*.csv)|*.csv|All Files (*.*)|*.*"
excel_file = "Excel(*.xls)|*.xls|All Files (*.*)|*.*"

TRUE = 1
FALSE = 0

version = "0.1"


def MessageDlg(self, message, type="Message"):
    dlg = wx.MessageDialog(self, message, type, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


all_file = "All Files (*.*)|*.*"


def OnFileDlgSave(self, fpath, filename="", type=all_file, title="Save File"):
    dlg = wx.FileDialog(self, title, ".", "", type, wx.SAVE)
    if fpath != None:
        dlg.SetPath(fpath)
    dlg.SetFilename(filename)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    else:
        path = None
    return path


class SetFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.target = window

    def OnDropFiles(self, x, y, filenames):
        self.target.FileDrop(filenames)


class SetMenuBitmap:
    def __init__(self, parent, bmp_dir):
        global dir_path
        self.fullpath = os.path.join(dir_path, bmp_dir)

    def GetItem(self, menu, text, image, ext_text=""):
        mID = wx.NewId()
        item = wx.MenuItem(menu, mID, text, ext_text)

        bmp_file = os.path.join(self.fullpath, image)
        bmp = wx.Image(bmp_file, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        item.SetBitmap(bmp)
        return item, mID


def UniqueList(list):
    set = {}
    for val in list:
        set[val] = None

    result = set.keys()
    return result


class TableList(wx.Frame):
    def __init__(self, parent, vlist=[], ntitle="Values"):
        wx.Frame.__init__(self, parent, -1, ntitle, wx.DefaultPosition, wx.Size(400, 500))
        global dir_path
        self.SetMenu()
        icon_path = os.path.join(dir_path, "Icon")

        self.icon = wx.Icon(os.path.join(icon_path, "Text.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        wx.BeginBusyCursor()
        self.grid = grid = wx.Grid(self, -1)

        rtotal = len(vlist)
        try:
            ctotal = len(vlist[0])
        except:
            ctotal = 1

        grid.CreateGrid(rtotal, ctotal)

        grid.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)

        row = 0
        for val in vlist:
            col = 0
            for set in val:
                grid.SetCellValue(row, col, str(set))
                col += 1
            row += 1

        grid.AutoSizeRows()
        grid.Refresh()
        wx.EndBusyCursor()

    def SetFrameIcon(self):
        self.icon = wx.Icon('mondrian.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

    def SetMenu(self):
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()

        mID = wx.NewId()
        menu.Append(mID, 'Copy', 'Copy')
        EVT_MENU(self, mID, self.OnCopy)

        mID = wx.NewId()
        menu.Append(mID, 'Save', 'Save')
        EVT_MENU(self, mID, self.OnFileSave)

        mID = wx.NewId()
        menu.Append(mID, 'E&xit', 'Exit')
        EVT_MENU(self, mID, self.OnCloseWindow)

        self.mainmenu.Append(menu, '&File')
        self.SetMenuBar(self.mainmenu)

    def OnCopy(self, event):
        delimit = '\t'

        grid = self.grid
        col_total = grid.GetNumberCols()
        row_total = grid.GetNumberRows()

        row = 0
        wx.BeginBusyCursor()
        list = []
        while row < row_total:
            set = []
            col = 0
            while col < col_total:
                value = grid.GetCellValue(row, col)
                set.append(value)
                col += 1
            result = string.joinfields(set, delimit)
            list.append(result)
            row += 1
        wx.EndBusyCursor()

        result = string.joinfields(list, '\r')
        self.SetClipboard(result)

    def SetClipboard(self, ctext):
        self.do = wx.TextDataObject()
        self.do.SetText(ctext)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(self.do)
        wx.TheClipboard.Close()

    def OnFileSave(self, event):
        self.SaveTable("Serving Areas.txt")

    def SaveTable(self, title):
        global dir_path
        file_nm = OnFileDlgSave(self, dir_path, title, type=text_file, title="Save List")
        if file_nm is None:
            return

        file = open(file_nm, 'w')
        self.SaveFile(file)

    def SaveFile(self, file):
        delimit = '\t'

        grid = self.grid
        col_total = grid.GetNumberCols()
        row_total = grid.GetNumberRows()

        row = 0
        wx.BeginBusyCursor()
        while row < row_total:
            set = []
            col = 0
            while col < col_total:
                value = grid.GetCellValue(row, col)
                set.append(value)
                col += 1
            result = string.joinfields(set, delimit)
            file.write(result)
            file.write('\n')
            row += 1
        file.close()
        wx.EndBusyCursor()

    def OnCloseWindow(self, event):
        self.Destroy()


class VirtualList(wx.ListCtrl):
    def __init__(self, parent):
        lstyle = wx.LC_REPORT | wx.LC_VIRTUAL
        wx.ListCtrl.__init__(self, parent, -1, style=lstyle)

        self.parent = parent
        self.image_data = parent.image_data

        self.SetItemCount(0)

        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")

        EVT_LIST_ITEM_SELECTED(self, self.GetId(), self.OnItemSelected)
        EVT_LIST_ITEM_ACTIVATED(self, self.GetId(), self.OnItemActivated)
        EVT_LIST_COL_CLICK(self, self.GetId(), self.OnColClick)

    def SetSize(self, rows):
        self.SetItemCount(rows)

    def OnItemSelected(self, event):
        self.parent.currentItem = event.m_itemIndex

    def OnItemActivated(self, event):
        self.parent.currentItem = event.m_itemIndex

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnColClick(self, event):
        self.parent.sort = event.GetColumn()
        self.parent.Refresh()

    def FormatValue(self, col, val):
        result = val
        return result

    def OnGetItemText(self, item, col):
        try:
            data = self.image_data[item]
            value = self.FormatValue(col, data[col])
        except:
            value = ""
        return value

    def OnGetItemImage(self, item):
        return 0

    def OnGetItemAttr(self, item):
        return None


class App(wx.Frame):
    def __init__(self, parent, id, title):
        size = wx.Size(300, 300)
        style = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size, style)
        self.icon = wx.Icon('Icon/Text.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.data = []

        self.CreateStatusBar(1)

        self.mainmenu = wx.MenuBar()
        menu = wx.Menu()

        menu = self.MakeFileMenu()
        self.mainmenu.Append(menu, '&File')

        menu = self.MakeHelpMenu()
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        self.MakeToolMenu()  # toolbar

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.image_data = []

        self.nm = wx.TextCtrl(self, -1, "", wx.DefaultPosition, wx.Size(-1, -1),
                              wx.TE_MULTILINE | wx.SUNKEN_BORDER | wx.TE_READONLY)
        self.nm.SetValue("Concatenate Files")

        dt = SetFileDropTarget(self)  # drag and drop for files
        self.nm.SetDropTarget(dt)

        self.SetStatus()

    def MakeFileMenu(self):
        menu = wx.Menu()

        set_id = menu.Append(-1, 'Open Files\tCtrl-O')
        self.Bind(wx.EVT_MENU, self.OnOpen, set_id)

        menu.AppendSeparator()

        set_id = menu.Append(-1, 'Close')
        self.Bind(wx.EVT_MENU, self.OnFileExit, set_id)

        return menu

    def MakeHelpMenu(self):
        menu = wx.Menu()

        set_id = menu.Append(-1, 'About')
        self.Bind(wx.EVT_MENU, self.OnAbout, set_id)

        return menu

    def MakeToolMenu(self):
        global dir_path
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER)
        icon_path = os.path.join(dir_path, "Icon")
        tsize = (16, 16)
        chx, chy = tb.GetTextExtent("X")

        mID = wx.NewId()
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        tb.AddLabelTool(mID, "Open", new_bmp, shortHelp="Open File", longHelp="Open'")
        self.Bind(wx.EVT_TOOL, self.OnOpen, id=mID)

        tb.AddSeparator()

        tb.Realize()

    def SetStatus(self):
        self.total = len(self.image_data)
        self.SetStatusText("Total: " + str(self.total), 0)

    def Clean(self, value):
        set = str(value)
        if type(value) == FloatType:
            set = set[0:-2]

        return set

    def CleanString(self, text):
        new_text = ''
        for val in text:
            if val != '"':
                new_text += val
        return new_text

    def CleanFloat(self, text):
        new_text = ''
        for val in text:
            if val != '$':
                new_text += val
        try:
            result = float(new_text)
        except:
            result = 0.0
        return result

    def DateConvert(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        new_date = month + '/' + day + '/' + year
        return new_date

    def OnOpen(self, event):
        start_path = 'C:\\My Documents'

        file_list = OnFileDlgMulti(self, type=text_file, title="Choose Files to Concatenate",
                                   action=wx.OPEN | wx.MULTIPLE, filename="", directory=start_path)

        if file_list == []:
            return

        self.file_list = file_list
        self.ProcessFiles()

    def ProcessFiles(self):
        dir_path, fl_nm = os.path.split(self.file_list[0])

        file_nm = OnFileDlg(self, type=text_file, title="Master File", action=wx.SAVE, filename="EAS",
                            directory=dir_path)
        if file_nm == None:
            return

        fl_out = open(file_nm, 'w')

        total = len(self.file_list)

        dlg = wx.ProgressDialog(file_nm, "Processing Total Records: " + str(total),
                                total, self, wx.PD_CAN_ABORT | wx.PD_APP_MODAL)

        line_cnt = 0
        for file_in in self.file_list:
            fl_in = open(file_in)

            data = fl_in.readlines()

            for val in data:
                result = string.strip(val)
                Test = True
                if result == "":
                    Test = False
                elif result[0:3] == '---':
                    Test = False
                elif result[0:3] == 'SQL':
                    Test = False
                elif result[0:6] == 'U_NPAN':
                    Test = False

                if Test == True:
                    flds = string.splitfields(result, ' ')
                    try:
                        if flds[1] != 'rows':
                            nxx = result[0:6]
                            name = result[7:50]
                            name = string.strip(name)
                            prov = result[58:60]

                            out_val = [nxx, name, prov]
                            result = string.joinfields(out_val, '\t')
                            fl_out.write(result + '\n')
                    except:
                        pass

            wx.Yield()

            line_cnt += 1

            if dlg.Update(line_cnt) == FALSE:
                break

            fl_in.close()

        fl_out.close()
        dlg.Destroy()

    def Display(self):
        self.image_data = []
        for val in self.data[1:]:
            data = []
            cnt = 0
            for set in val:
                valid = self.fields[cnt]
                if self.valid.has_key(valid):
                    data.append(set)
                cnt += 1
            self.image_data.append(data)
        self.Refresh()

    def OnNewFile(self, event):
        global start_dir
        file_nm = OnFileDlg(self, text_file, "Select File for Conversion", directory=start_dir)
        if file_nm is None:
            return
        start_dir, fl_nm = os.path.split(file_nm)

        self.file_list = [file_nm]
        self.ProcessList()

    def Refresh(self):
        self.nm.DeleteAllItems()

        self.total = len(self.image_data)
        self.nm.SetSize(self.total)
        self.nm.image_data = self.image_data

        self.SetStatus()

    def CleanNumber(self, value):
        result = ""
        for val in value:
            if val >= '0' and val <= '9':
                result = result + val
        return result

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnFileExit(self, event):
        self.Close()

    def SetStatus(self):
        self.SetStatusText("", 0)

    def FileDrop(self, filenames):
        self.file_list = filenames
        self.ProcessFiles()

    def OnAbout(self, event):
        text = " Humbolt Summary Report: " + version + '\n\n'
        text = text + "Lorne White, TELUS, (780)+493+4722, Lorne.White@TELUS.com"

        MessageDlg(self, text, "About Program")

    def OnHelp(self, event):
        text = "Files Processing\n\n"
        MessageDlg(self, text, "Help")

    def OnFileExit(self, event):
        self.Close()


# ---------------------------------------------------------------------------


class MyApp(wx.App):
    def OnInit(self):
        frame = App(None, -1, "EAS File Concatenate")
        frame.Show(True)
        frame.Centre(wx.BOTH)
        self.SetTopWindow(frame)
        return True


# ---------------------------------------------------------------------------


def main():
    app = MyApp(0)
    app.MainLoop()


def t():
    import pdb
    pdb.run('main()')


if __name__ == '__main__':
    main()