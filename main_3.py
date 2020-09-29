import os
import wx
import registration_frame
import ImageViewer
import menubar_wins

wildcard = 'Image source (*.nii, *nii.gz)|*.nii; *nii.gz|' \
           'All files (*.*)|*.*'


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600))

        self.panel = wx.Panel(self)

        self.panel.SetBackgroundColour('WHEAT')

        self.currentDirectory = os.getcwd()

        self.fixed_img_button = wx.Button(self.panel, -1, "Select Fixed Image", size=wx.Size(130, 30))
        self.fixed_img_path = wx.TextCtrl(self.panel, -1,
                                          style=wx.TE_CENTRE | wx.TE_READONLY,
                                          size=wx.Size(600, 30))
        self.fixed_img_path.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.moving_img_button = wx.Button(self.panel, -1, "Select Moving Image", size=wx.Size(130, 30))
        self.moving_img_path = wx.TextCtrl(self.panel, -1,
                                           style=wx.TE_CENTRE | wx.TE_READONLY,
                                           size=wx.Size(600, 30))
        self.moving_img_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.img_view_fix = ImageViewer.ImageViewer(parent=self.panel, name="Fixed")
        self.img_view_mvg = ImageViewer.ImageViewer(parent=self.panel, name="Moving")

        self.registration_btn = wx.Button(self.panel, -1, "Registration", size=wx.Size(130, 30))
        self.segmentation_btn = wx.Button(self.panel, -1, "Segmentation", size=wx.Size(130, 30))
        self.segmentation_btn.Enable(False)
        self.metric_cfr_btn = wx.Button(self.panel, -1, "Metric Cfr", size=wx.Size(130, 30))
        self.costfunt_btn = wx.Button(self.panel, -1, "Accuracy", size=wx.Size(130, 30))

        fixed_hbox = wx.BoxSizer(wx.HORIZONTAL)
        fixed_hbox.Add(self.fixed_img_button, 0, wx.ALIGN_CENTER, 10)
        fixed_hbox.Add(self.fixed_img_path, 0, wx.ALIGN_CENTER, 10)
        moving_hbox = wx.BoxSizer(wx.HORIZONTAL)
        moving_hbox.Add(self.moving_img_button, 0, wx.ALIGN_CENTER, 10)
        moving_hbox.Add(self.moving_img_path, 0, wx.ALIGN_CENTER, 10)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_hbox.Add(self.registration_btn, 0, wx.ALIGN_CENTER, 10)
        btn_hbox.Add(self.segmentation_btn, 0, wx.ALIGN_CENTER, 10)
        btn_hbox.Add(self.metric_cfr_btn, 0, wx.ALIGN_CENTER, 10)
        btn_hbox.Add(self.costfunt_btn, 0, wx.ALIGN_CENTER, 10)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(fixed_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(moving_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.img_view_fix, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.img_view_mvg, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.AddStretchSpacer()
        panel_sizer.Add(btn_hbox, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(panel_sizer)

        self.fixed_img_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 1))
        self.moving_img_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 2))
        self.fixed_img_path.Bind(wx.EVT_TEXT, lambda event: self.on_view(event, 1))
        self.moving_img_path.Bind(wx.EVT_TEXT, lambda event: self.on_view(event, 2))

        self.registration_btn.Bind(wx.EVT_BUTTON, self.on_open_reg_frame)
        self.metric_cfr_btn.Bind(wx.EVT_BUTTON, self.on_open_metric)
        self.costfunt_btn.Bind(wx.EVT_BUTTON, self.on_open_cf)

        self.CreateStatusBar()  # A status bar in the bottom of the window

        # Creating the menubar.
        self.make_menu_bar()

        self.Centre()
        self.Show(True)

    def make_menu_bar(self):  # TODO vedere se e utile e sostituire funzioni placeholder
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        file_menu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        hello_item = file_menu.Append(-1, "&Hello...\tCtrl-H",
                                      "Help string shown in status bar for this menu item")
        file_menu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exit_item = file_menu.Append(wx.ID_EXIT)

        # Help menu for the about item
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)

        # Image functions menu
        image_menu = wx.Menu()
        tfms_item = image_menu.Append(-1, "Apply Tfm",
                                      "Apply transformation to a set of images")
        image_menu.AppendSeparator()
        stat_item = image_menu.Append(-1, "Stat Calculator",
                                      "Calculate Mean, Median and Standard Deviation of a set of images")
        image_menu.AppendSeparator()
        header_item = image_menu.Append(-1, "Copy Header",
                                        "Broadcast Image header from a reference to a set of targets")

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")
        menu_bar.Append(image_menu, "Image proc")

        # Give the menu bar to the frame
        self.SetMenuBar(menu_bar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        self.Bind(wx.EVT_MENU, self.on_apply_tfm, tfms_item)
        self.Bind(wx.EVT_MENU, self.on_calc_stat, stat_item)
        self.Bind(wx.EVT_MENU, self.on_copy_header, header_item)

    def onOpenFile(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 1:
                self.fixed_img_path.SetLabelText(str(paths[0]))
            elif which_file == 2:
                self.moving_img_path.SetLabelText(str(paths[0]))
        dlg.Destroy()

    def on_open_reg_frame(self, event):
        registration_window = registration_frame.RegistrationFrame(parent=None, title="Registration Frame",
                                                                   path_fix=self.fixed_img_path.GetLabelText(),
                                                                   path_mov=self.moving_img_path.GetLabelText())
        registration_window.Show()

    def on_open_cf(self, event):
        cf_window = menubar_wins.AccuracyCalc(parent=None, title="Accuracy evaluation")
        cf_window.Show()

    def on_open_metric(self, event):
        mc_window = menubar_wins.MetricCfr(parent=None, title="Metric confront",
                                           img1=self.fixed_img_path.GetLabelText(),
                                           img2=self.moving_img_path.GetLabelText())
        mc_window.Show()

    def on_view(self, event, which_panel):
        """
        View image when it is first selected by user get_bitmap(data=img1, index=int(img1.shape[2] / 2), dim=2)
        """
        if which_panel == 1:
            self.img_view_fix.populate_view(path_img=self.fixed_img_path.GetLabelText())
        elif which_panel == 2:
            self.img_view_mvg.populate_view(path_img=self.moving_img_path.GetLabelText())
        self.panel.Refresh()

    def on_apply_tfm(self, event):
        apply_tfm_win = menubar_wins.ApplyTransfMatrix(parent=None, title="Apply Transformations")
        apply_tfm_win.Show()

    def on_copy_header(self, event):
        copy_head_window = menubar_wins.CopyHeader(parent=None, title="Copy Image Header")
        copy_head_window.Show()

    def on_calc_stat(self, event):
        stat_calc_window = menubar_wins.StatCalculator(parent=None, title="Calculation of mean, median ad stdev")
        stat_calc_window.Show()

    # TODO vedere se e utile - placeholder
    def on_hello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def on_about(self, event):
        """Display an About Dialog. List of dependencies"""
        wx.MessageBox(' * numpy \n * scipy \n * os \n * wx \n * math \n * nibabel \n * nilearn \n * scikit-image \n '
                      '* matplotlib \n * SimpleITK',
                      'Requirements',
                      wx.OK | wx.ICON_INFORMATION)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


app = wx.App(False)
frame = MainWindow(None, "Image Registration Window")
app.MainLoop()
