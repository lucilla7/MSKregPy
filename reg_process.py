import wx


# import time


class RegistrationProcess(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        self.SetTitle("Registration Progress")
        panel = wx.Panel(self, wx.ID_ANY)
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, u'Consolas')

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.log = wx.TextCtrl(panel, wx.ID_ANY, size=(300, 100), style=style)
        self.log.SetFont(font)

        # self.reg_gauge = wx.Gauge(panel, wx.ID_ANY, 50, (20, 50), (250, 25), style=wx.GA_HORIZONTAL).Pulse()

        sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        # sizer.Add(self.reg_gauge, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)

    def update_list(self, listprog):
        self.log.write(listprog)
        self.log.write('\n')
