import wx
import os
import nibabel as nib
import utility_fx
import accuracy_eval
import ImageViewer

wildcard = 'Image source (*.nii, *nii.gz)|*.nii; *nii.gz|' \
           'All files (*.*)|*.*'


class ApplyTransfMatrix(wx.Frame):
    def __init__(self, parent, title):
        super(ApplyTransfMatrix, self).__init__(parent, title=title, size=wx.Size(1000, 500))

        self.panel = wx.Panel(self)
        self.SetBackgroundColour("WHEAT")

        self.currentDirectory = os.getcwd()

        self.tgt_img_label = wx.Button(self.panel, -1,
                                       label="Target Image",
                                       size=wx.Size(80, 30))

        self.tgt_img_path = wx.StaticText(self.panel, -1,
                                          style=wx.TE_CENTRE | wx.TE_READONLY,
                                          size=wx.Size(250, 30))
        self.tgt_img_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.ref_img_label1 = wx.Button(self.panel, -1,
                                        label="First Reference Image",
                                        size=wx.Size(80, 30))
        self.ref_img_label1.Enable(False)

        self.ref_img_path1 = wx.StaticText(self.panel, -1,
                                           style=wx.TE_CENTRE | wx.TE_READONLY,
                                           size=wx.Size(250, 30))
        self.ref_img_path1.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.ref_img_label2 = wx.Button(self.panel, -1,
                                        label="Second Reference Image",
                                        size=wx.Size(80, 30))
        self.ref_img_label2.Enable(False)

        self.ref_img_path2 = wx.StaticText(self.panel, -1,
                                           style=wx.TE_CENTRE | wx.TE_READONLY,
                                           size=wx.Size(250, 30))
        self.ref_img_path2.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.ref_img_label3 = wx.Button(self.panel, -1,
                                        label="Third Reference Image",
                                        size=wx.Size(80, 30))
        self.ref_img_label3.Enable(False)

        self.ref_img_path3 = wx.StaticText(self.panel, -1,
                                           style=wx.TE_CENTRE | wx.TE_READONLY,
                                           size=wx.Size(250, 30))
        self.ref_img_path3.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.ref_img_label4 = wx.Button(self.panel, -1,
                                        label="Fourth Reference Image",
                                        size=wx.Size(80, 30))
        self.ref_img_label4.Enable(False)

        self.ref_img_path4 = wx.StaticText(self.panel, -1,
                                           style=wx.TE_CENTRE | wx.TE_READONLY,
                                           size=wx.Size(250, 30))
        self.ref_img_path4.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.first_tfm = wx.Button(self.panel, -1,
                                   label="First tfm",
                                   size=wx.Size(80, 30))
        self.first_tfm.Enable(False)

        self.first_tfm_path = wx.StaticText(self.panel, -1,
                                            style=wx.TE_CENTRE | wx.TE_READONLY,
                                            size=wx.Size(280, 30))
        self.first_tfm_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.second_tfm = wx.Button(self.panel, -1,
                                    label="Second tfm",
                                    size=wx.Size(80, 30))
        self.second_tfm.Enable(False)

        self.second_tfm_path = wx.StaticText(self.panel, -1,
                                             style=wx.TE_CENTRE | wx.TE_READONLY,
                                             size=wx.Size(280, 30))
        self.second_tfm_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.third_tfm = wx.Button(self.panel, -1,
                                   label="Third tfm",
                                   size=wx.Size(80, 30))
        self.third_tfm.Enable(False)

        self.third_tfm_path = wx.StaticText(self.panel, -1,
                                            style=wx.TE_CENTRE | wx.TE_READONLY,
                                            size=wx.Size(280, 30))
        self.third_tfm_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.fourth_tfm = wx.Button(self.panel, -1,
                                    label="Fourth tfm",
                                    size=wx.Size(80, 30))
        self.fourth_tfm.Enable(False)

        self.fourth_tfm_path = wx.StaticText(self.panel, -1,
                                             style=wx.TE_CENTRE | wx.TE_READONLY,
                                             size=wx.Size(280, 30))
        self.fourth_tfm_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.first_inv_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Inverse", size=wx.Size(100, 20))
        self.first_inv_check.Enable(False)
        self.second_inv_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Inverse", size=wx.Size(100, 20))
        self.second_inv_check.Enable(False)
        self.third_inv_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Inverse", size=wx.Size(100, 20))
        self.third_inv_check.Enable(False)
        self.fourth_inv_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Inverse", size=wx.Size(100, 20))
        self.fourth_inv_check.Enable(False)

        self.first_lab_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Label", size=wx.Size(100, 20))
        self.first_lab_check.Enable(False)
        self.second_lab_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Label", size=wx.Size(100, 20))
        self.second_lab_check.Enable(False)
        self.third_lab_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Label", size=wx.Size(100, 20))
        self.third_lab_check.Enable(False)
        self.fourth_lab_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Label", size=wx.Size(100, 20))
        self.fourth_lab_check.Enable(False)

        self.first_def_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Nonrigid", size=wx.Size(100, 20))
        self.first_def_check.Enable(False)
        self.second_def_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Nonrigid", size=wx.Size(100, 20))
        self.second_def_check.Enable(False)
        self.third_def_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Nonrigid", size=wx.Size(100, 20))
        self.third_def_check.Enable(False)
        self.fourth_def_check = wx.CheckBox(self.panel, -1, style=wx.TE_CENTRE, label="Nonrigid", size=wx.Size(100, 20))
        self.fourth_def_check.Enable(False)

        self.save_tfm = wx.Button(self.panel, -1, label="Apply tfm and save")

        vbox_panel = wx.BoxSizer(wx.VERTICAL)
        hbox_tfm = wx.BoxSizer(wx.HORIZONTAL)
        vbox_col1 = wx.BoxSizer(wx.VERTICAL)
        vbox_col1.AddSpacer(10)
        vbox_col1.Add(self.tgt_img_label, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col1.Add(self.tgt_img_path, 1, wx.ALL | wx.EXPAND, 5)

        vbox_col2 = wx.BoxSizer(wx.VERTICAL)
        vbox_col2.AddSpacer(10)
        vbox_col2.Add(self.ref_img_label1, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col2.Add(self.ref_img_path1, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col2.AddSpacer(3)
        vbox_col2.Add(self.ref_img_label2, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col2.Add(self.ref_img_path2, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col2.AddSpacer(3)
        vbox_col2.Add(self.ref_img_label3, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col2.Add(self.ref_img_path3, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col2.AddSpacer(3)
        vbox_col2.Add(self.ref_img_label4, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col2.Add(self.ref_img_path4, 1, wx.ALL | wx.EXPAND, 5)

        vbox_col3 = wx.BoxSizer(wx.VERTICAL)
        vbox_col3.AddSpacer(10)
        vbox_col3.Add(self.first_tfm, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col3.Add(self.first_tfm_path, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col3.AddSpacer(3)
        vbox_col3.Add(self.second_tfm, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col3.Add(self.second_tfm_path, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col3.AddSpacer(3)
        vbox_col3.Add(self.third_tfm, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col3.Add(self.third_tfm_path, 1, wx.ALL | wx.EXPAND, 5)
        vbox_col3.AddSpacer(3)
        vbox_col3.Add(self.fourth_tfm, 1, wx.ALL | wx.EXPAND, 3)
        vbox_col3.Add(self.fourth_tfm_path, 1, wx.ALL | wx.EXPAND, 5)

        vbox_col4 = wx.BoxSizer(wx.VERTICAL)
        vbox_col4.AddSpacer(20)
        vbox_col4.Add(self.first_inv_check)
        vbox_col4.Add(self.first_def_check)
        vbox_col4.Add(self.first_lab_check)
        vbox_col4.AddSpacer(21)
        vbox_col4.Add(self.second_inv_check)
        vbox_col4.Add(self.second_def_check)
        vbox_col4.Add(self.second_lab_check)
        vbox_col4.AddSpacer(22)
        vbox_col4.Add(self.third_inv_check)
        vbox_col4.Add(self.third_def_check)
        vbox_col4.Add(self.third_lab_check)
        vbox_col4.AddSpacer(23)
        vbox_col4.Add(self.fourth_inv_check)
        vbox_col4.Add(self.fourth_def_check)
        vbox_col4.Add(self.fourth_lab_check)

        hbox_tfm.AddMany([(vbox_col1, 1, wx.ALL, 5), (vbox_col2, 1, wx.ALL, 5), (vbox_col3, 1, wx.ALL, 5),
                          (vbox_col4, 1, wx.ALL, 15)])
        vbox_panel.AddMany([(hbox_tfm, 1, wx.ALL, 10), (self.save_tfm, 0, wx.ALIGN_CENTRE, 5)])
        vbox_panel.AddStretchSpacer()

        self.panel.SetSizer(vbox_panel)

        self.Centre()
        self.Show(True)

        self.tgt_img_label.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 0))
        self.ref_img_label1.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 1.1))
        self.first_tfm.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 1.2))
        self.ref_img_label2.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 2.1))
        self.second_tfm.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 2.2))
        self.ref_img_label3.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 3.1))
        self.third_tfm.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 3.2))
        self.ref_img_label4.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 4.1))
        self.fourth_tfm.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 4.2))
        self.save_tfm.Bind(wx.EVT_BUTTON, self.on_save)

    def onOpenFile(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        wildcardtfm = 'Image source (*.nii, *nii.gz, *tfm)|*.nii; *nii.gz; *tfm|' \
                      'All files (*.*)|*.*'
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcardtfm,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 0:
                self.tgt_img_path.SetLabelText(str(paths[0]))
                self.ref_img_label1.Enable(True)
                self.first_tfm.Enable(True)
                self.first_inv_check.Enable(True)
                self.first_def_check.Enable(True)
                self.first_lab_check.Enable(True)
            elif which_file == 1.1:
                self.ref_img_path1.SetLabelText(str(paths[0]))
                if self.first_tfm_path.GetLabelText() != u'':
                    self.ref_img_label2.Enable(True)
                    self.second_tfm.Enable(True)
                    self.second_inv_check.Enable(True)
                    self.second_def_check.Enable(True)
                    self.second_lab_check.Enable(True)
            elif which_file == 2.1:
                self.ref_img_path2.SetLabelText(str(paths[0]))
                if self.second_tfm_path.GetLabelText() != u'':
                    self.ref_img_label3.Enable(True)
                    self.third_tfm.Enable(True)
                    self.third_inv_check.Enable(True)
                    self.third_def_check.Enable(True)
                    self.third_lab_check.Enable(True)
            elif which_file == 3.1:
                self.ref_img_path3.SetLabelText(str(paths[0]))
                if self.third_tfm_path.GetLabelText() != u'':
                    self.ref_img_label3.Enable(True)
                    self.fourth_tfm.Enable(True)
                    self.fourth_inv_check.Enable(True)
                    self.fourth_def_check.Enable(True)
                    self.fourth_lab_check.Enable(True)
            elif which_file == 4.1:
                self.ref_img_path4.SetLabelText(str(paths[0]))
            elif which_file == 1.2:
                self.first_tfm_path.SetLabelText(str(paths[0]))
                if self.ref_img_path1.GetLabelText() != u'':
                    self.ref_img_label2.Enable(True)
                    self.second_tfm.Enable(True)
                    self.second_inv_check.Enable(True)
                    self.second_def_check.Enable(True)
                    self.second_lab_check.Enable(True)
            elif which_file == 2.2:
                self.second_tfm_path.SetLabelText(str(paths[0]))
                if self.ref_img_path2.GetLabelText() != u'':
                    self.ref_img_label3.Enable(True)
                    self.third_tfm.Enable(True)
                    self.third_inv_check.Enable(True)
                    self.third_def_check.Enable(True)
                    self.third_lab_check.Enable(True)
            elif which_file == 3.2:
                self.third_tfm_path.SetLabelText(str(paths[0]))
                if self.ref_img_path3.GetLabelText() != u'':
                    self.ref_img_label4.Enable(True)
                    self.fourth_tfm.Enable(True)
                    self.fourth_inv_check.Enable(True)
                    self.fourth_def_check.Enable(True)
                    self.fourth_lab_check.Enable(True)
            elif which_file == 4.2:
                self.fourth_tfm_path.SetLabelText(str(paths[0]))
        dlg.Destroy()

    def on_save(self, event):
        img_applied = None
        if self.tgt_img_path.GetLabelText() != u'' and self.ref_img_path1.GetLabelText() != u'' \
                and self.first_tfm_path.GetLabelText() != u'':
            img_applied = utility_fx.apply_tfm_matrix(self.tgt_img_path.GetLabelText(),
                                                      self.ref_img_path1.GetLabelText(),
                                                      self.first_tfm_path.GetLabelText(),
                                                      is_inverse=self.first_inv_check.GetValue(),
                                                      is_label=self.first_lab_check.GetValue(),
                                                      is_def=self.first_def_check.GetValue())

        if self.ref_img_path2.GetLabelText() != u'' and self.second_tfm_path.GetLabelText() != u'':
            img_applied = utility_fx.apply_tfm_matrix(img_applied,
                                                      self.ref_img_path2.GetLabelText(),
                                                      self.second_tfm_path.GetLabelText(),
                                                      is_inverse=self.second_inv_check.GetValue(),
                                                      is_label=self.second_lab_check.GetValue(),
                                                      is_def=self.second_def_check.GetValue())

        if self.ref_img_path3.GetLabelText() != u'' and self.third_tfm_path.GetLabelText() != u'':
            img_applied = utility_fx.apply_tfm_matrix(img_applied,
                                                      self.ref_img_path3.GetLabelText(),
                                                      self.third_tfm_path.GetLabelText(),
                                                      is_inverse=self.third_inv_check.GetValue(),
                                                      is_label=self.third_lab_check.GetValue(),
                                                      is_def=self.third_def_check.GetValue())

        if self.ref_img_path4.GetLabelText() != u'' and self.fourth_tfm_path.GetLabelText() != u'':
            img_applied = utility_fx.apply_tfm_matrix(img_applied,
                                                      self.ref_img_path4.GetLabelText(),
                                                      self.fourth_tfm_path.GetLabelText(),
                                                      is_inverse=self.fourth_inv_check.GetValue(),
                                                      is_label=self.fourth_lab_check.GetValue(),
                                                      is_def=self.fourth_def_check.GetValue())

        with wx.FileDialog(self, "Save Image", wildcard="Nifti files (*.nii)|*.nii",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(str(pathname), 'w') as file:
                    utility_fx.save_file(img_applied, str(pathname))
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % str(pathname))


class MetricCfr(wx.Frame):
    def __init__(self, parent, title, img1, img2):
        super(MetricCfr, self).__init__(parent, title=title, size=(1000, 600))

        # images path
        self.img1 = img1
        self.img2 = img2

        self.panel = wx.Panel(self)
        # Labels for already chosen images
        img1_label = wx.StaticText(self.panel, -1,
                                   style=wx.TE_CENTRE | wx.TE_READONLY,
                                   label="Image 1",
                                   size=wx.Size(80, 30))
        img1_path = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label=str(os.path.basename(self.img1)),
                                  size=wx.Size(280, 30))
        img1_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        img2_label = wx.StaticText(self.panel, -1,
                                   style=wx.TE_CENTRE | wx.TE_READONLY,
                                   label="Image 2",
                                   size=wx.Size(80, 30))
        img2_path = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label=str(os.path.basename(self.img2)),
                                  size=wx.Size(280, 30))
        img2_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        hbox_img1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_img1.Add(img1_label, 0, wx.ALIGN_CENTER, 5)
        hbox_img1.Add(img1_path, 0, wx.ALIGN_CENTER, 5)
        hbox_img2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_img2.Add(img2_label, 0, wx.ALIGN_CENTER, 5)
        hbox_img2.Add(img2_path, 0, wx.ALIGN_CENTER, 5)

        vbox_layout = wx.BoxSizer(wx.HORIZONTAL)
        vbox_layout.Add(hbox_img1, 0, wx.ALIGN_CENTER, 5)
        vbox_layout.Add(hbox_img2, 0, wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(vbox_layout)

        self.Centre()
        self.Show(True)

    def onOpenFile(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        if which_file == 1:
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        else:
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 1:
                self.ref_img_path.SetLabelText(str(paths[0]))
                self.path_ref = str(paths[0])
            elif which_file == 2:
                for i in paths:
                    self.tgts_img_path.AppendText(str(i) + "\n")
                    self.path_tgts.append(str(i))
                self.copy_btn.Enable(True)
        dlg.Destroy()


# TODO aggiungere opzione file 4d
class StatCalculator(wx.Frame):
    def __init__(self, parent, title):
        super(StatCalculator, self).__init__(parent, title=title, size=(800, 600))

        self.panel = wx.Panel(self)
        self.SetBackgroundColour("THISTLE")

        self.currentDirectory = os.getcwd()
        self.path_ref = None
        self.img = None
        self.img_panel = 1

        self.median_img_view = ImageViewer.ImageViewer(parent=self.panel, name="Median")
        self.mean_img_view = ImageViewer.ImageViewer(parent=self.panel, name="Mean")
        self.mean_img_view.Hide()
        self.stdev_img_view = ImageViewer.ImageViewer(parent=self.panel, name="Standard Dev")
        self.stdev_img_view.Hide()

        self.dir_button = wx.Button(self.panel, -1, "Select Directory", size=wx.Size(130, 30))
        self.dir_path = wx.TextCtrl(self.panel, -1,
                                    style=wx.TE_CENTRE | wx.TE_READONLY,
                                    size=wx.Size(600, 30))
        self.dir_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        n_bins = wx.StaticText(self.panel, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Number of bins",
                               size=wx.Size(100, 30))
        self.number_bins = wx.SpinCtrl(self.panel, size=wx.Size(80, 20))
        self.number_bins.SetRange(1, 100)
        self.number_bins.SetValue(50)
        self.number_bins.Enable(False)

        self.shift_plus_button = wx.Button(self.panel, -1, " > ", size=wx.Size(50, 50))
        self.shift_plus_button.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                               False))
        self.shift_minus_button = wx.Button(self.panel, -1, " < ", size=wx.Size(50, 50))
        self.shift_minus_button.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                                False))
        self.shift_minus_button.Enable(False)

        self.calc_btn = wx.Button(self.panel, -1, "Calculate", size=wx.Size(100, 30))
        self.calc_btn.Enable(False)

        fixed_hbox = wx.BoxSizer(wx.HORIZONTAL)
        fixed_hbox.Add(self.dir_button, 0, wx.ALIGN_CENTER, 10)
        fixed_hbox.Add(self.dir_path, 0, wx.ALIGN_CENTER, 10)

        bins_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bins_hbox.Add(n_bins, 0, wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, 10)
        bins_hbox.Add(self.number_bins, 0, wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, 10)
        bins_hbox.AddStretchSpacer(1)
        bins_hbox.Add(self.shift_minus_button, 0, wx.ALIGN_CENTRE_VERTICAL | wx.RIGHT, 10)
        bins_hbox.Add(self.shift_plus_button, 0, wx.ALIGN_CENTRE_VERTICAL | wx.RIGHT, 10)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(fixed_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(bins_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.median_img_view, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.mean_img_view, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.stdev_img_view, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.calc_btn, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        self.panel.SetSizer(panel_sizer)

        self.dir_button.Bind(wx.EVT_BUTTON, self.on_open_dir)
        self.shift_plus_button.Bind(wx.EVT_BUTTON, self.navigate_img)
        self.shift_minus_button.Bind(wx.EVT_BUTTON, self.navigate_img)
        self.calc_btn.Bind(wx.EVT_BUTTON, self.calc_img_stat)

        self.Centre()
        self.Show(True)

    def on_open_dir(self, event):
        dlg = wx.DirDialog(
            self, message="Choose a directory",
            defaultPath=self.currentDirectory,
            style=wx.DD_CHANGE_DIR | wx.DD_DIR_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPath()
            self.dir_path.SetLabelText(str(paths))
            self.number_bins.Enable(True)
            self.calc_btn.Enable(True)
            for p in os.listdir(paths):
                if os.path.isfile(os.path.join(str(paths), str(p))):
                    self.path_ref = os.path.join(str(paths), str(p))
                    break
        dlg.Destroy()

    def onView(self, path_img, img):
        """
        View image when it is first selected by user
        """
        self.median_img_view.populate_view(path_img=path_img, img=img[0])
        self.mean_img_view.populate_view(path_img=path_img, img=img[1])
        self.stdev_img_view.populate_view(path_img=path_img, img=img[2])
        self.panel.Refresh()

    def calc_img_stat(self, event):
        niblist = []
        for fl in os.listdir(str(self.dir_path.GetLabelText())):
            if os.path.isfile(os.path.join(str(self.dir_path.GetLabelText()), fl)):
                niblist.append(os.path.join(str(self.dir_path.GetLabelText()), fl))
        img_data, img_header, img = utility_fx.read_image(niblist[0])
        self.img = img
        median_im, mean_im, stdev_im = utility_fx.median_approx_fits(niblist, int(self.number_bins.GetValue()))
        median_img = nib.Nifti1Image(median_im, img.affine, header=img.header)
        mean_img = nib.Nifti1Image(mean_im, img.affine, header=img.header)
        stdev_img = nib.Nifti1Image(stdev_im, img.affine, header=img.header)
        self.onView(path_img=self.path_ref, img=[median_im, mean_im, stdev_im])
        nib.save(median_img, os.path.join(str(self.dir_path.GetLabelText()), "median.nii.gz"))
        nib.save(mean_img, os.path.join(str(self.dir_path.GetLabelText()), "mean.nii.gz"))
        nib.save(stdev_img, os.path.join(str(self.dir_path.GetLabelText()), "stdev.nii.gz"))

    def navigate_img(self, event):
        if event.GetEventObject().GetLabel() == " > ":
            self.img_panel += 1
        elif event.GetEventObject().GetLabel() == " < ":
            self.img_panel -= 1
        if self.img_panel == 1:
            self.median_img_view.Show()
            self.mean_img_view.Hide()
            self.stdev_img_view.Hide()
            self.shift_plus_button.Enable(True)
            self.shift_minus_button.Enable(False)
        elif self.img_panel == 2:
            self.median_img_view.Hide()
            self.mean_img_view.Show()
            self.stdev_img_view.Hide()
            self.shift_plus_button.Enable(True)
            self.shift_minus_button.Enable(True)
        elif self.img_panel == 3:
            self.median_img_view.Hide()
            self.mean_img_view.Hide()
            self.stdev_img_view.Show()
            self.shift_plus_button.Enable(False)
            self.shift_minus_button.Enable(True)
        else:
            raise IndexError("Image index Out of Range")

        self.panel.Layout()


class AccuracyCalc(wx.Frame):
    def __init__(self, parent, title):
        super(AccuracyCalc, self).__init__(parent, title=title, size=(1000, 600))

        self.currentDirectory = os.getcwd()
        self.SetBackgroundColour("THISTLE")
        self.img_mae = None

        self.panel = wx.Panel(self)

        label_font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        # Labels for images
        self.img1_button = wx.Button(self.panel, -1, label="Image 1", size=wx.Size(80, 30))
        self.img1_path = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(280, 30))
        self.img1_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.img2_button = wx.Button(self.panel, -1, label="Image 2", size=wx.Size(80, 30))
        self.img2_path = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(280, 30))
        self.img2_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.abs_err_view = ImageViewer.ImageViewer(parent=self.panel, name="Absolute Error")

        mae_label = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Mean Absolute Error (MAE)",
                                  size=wx.Size(280, 30))
        mae_label.SetFont(label_font)

        self.mae_value = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(50, 30))
        self.mae_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.calc_btn_img = wx.Button(self.panel, -1, "Calculate", size=wx.Size(100, 30))

        # Labels for rois
        self.roi1_button = wx.Button(self.panel, -1, label="Roi 1", size=wx.Size(80, 30))
        self.roi1_path = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(280, 30))
        self.roi1_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.roi2_button = wx.Button(self.panel, -1, label="Roi 2", size=wx.Size(80, 30))
        self.roi2_path = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(280, 30))
        self.roi2_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        jac_label = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Jaccard",
                                  size=wx.Size(280, 30))
        jac_label.SetFont(label_font)

        self.jac_value = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(50, 30))
        self.jac_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        dice_label = wx.StaticText(self.panel, -1,
                                   style=wx.TE_CENTRE | wx.TE_READONLY,
                                   label="Dice",
                                   size=wx.Size(280, 30))
        dice_label.SetFont(label_font)

        self.dice_value = wx.StaticText(self.panel, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        size=wx.Size(50, 30))
        self.dice_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        vs_label = wx.StaticText(self.panel, -1,
                                 style=wx.TE_CENTRE | wx.TE_READONLY,
                                 label="Volume Similarity",
                                 size=wx.Size(280, 30))
        vs_label.SetFont(label_font)

        self.vs_value = wx.StaticText(self.panel, -1,
                                      style=wx.TE_CENTRE | wx.TE_READONLY,
                                      size=wx.Size(50, 30))
        self.vs_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        fn_label = wx.StaticText(self.panel, -1,
                                 style=wx.TE_CENTRE | wx.TE_READONLY,
                                 label="False Negative",
                                 size=wx.Size(280, 30))
        fn_label.SetFont(label_font)

        self.fn_value = wx.StaticText(self.panel, -1,
                                      style=wx.TE_CENTRE | wx.TE_READONLY,
                                      size=wx.Size(50, 30))
        self.fn_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        fp_label = wx.StaticText(self.panel, -1,
                                 style=wx.TE_CENTRE | wx.TE_READONLY,
                                 label="False Positive",
                                 size=wx.Size(280, 30))
        fp_label.SetFont(label_font)

        self.fp_value = wx.StaticText(self.panel, -1,
                                      style=wx.TE_CENTRE | wx.TE_READONLY,
                                      size=wx.Size(50, 30))
        self.fp_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        hd_label = wx.StaticText(self.panel, -1,
                                 style=wx.TE_CENTRE | wx.TE_READONLY,
                                 label="Hausdorff Distance",
                                 size=wx.Size(280, 30))
        hd_label.SetFont(label_font)

        self.hd_value = wx.StaticText(self.panel, -1,
                                      style=wx.TE_CENTRE | wx.TE_READONLY,
                                      size=wx.Size(50, 30))
        self.hd_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        msd_label = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Mean Surface Distance",
                                  size=wx.Size(280, 30))
        msd_label.SetFont(label_font)

        self.msd_value = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(50, 30))
        self.msd_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        mesd_label = wx.StaticText(self.panel, -1,
                                   style=wx.TE_CENTRE | wx.TE_READONLY,
                                   label="Median Surface Distance",
                                   size=wx.Size(280, 30))
        mesd_label.SetFont(label_font)

        self.mesd_value = wx.StaticText(self.panel, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        size=wx.Size(50, 30))
        self.mesd_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        std_label = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Std Surface Distance",
                                  size=wx.Size(280, 30))
        std_label.SetFont(label_font)

        self.std_value = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(50, 30))
        self.std_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        max_label = wx.StaticText(self.panel, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Max Surface Distance",
                                  size=wx.Size(280, 30))
        max_label.SetFont(label_font)

        self.max_value = wx.StaticText(self.panel, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY,
                                       size=wx.Size(50, 30))
        self.max_value.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.calc_btn_roi = wx.Button(self.panel, -1, "Calculate", size=wx.Size(100, 30))

        hbox_img = wx.BoxSizer(wx.HORIZONTAL)
        hbox_img.Add(self.img1_button, 0, wx.ALIGN_CENTER, 5)
        hbox_img.Add(self.img1_path, 0, wx.ALIGN_CENTER, 5)
        hbox_img.Add(self.img2_button, 0, wx.ALIGN_CENTER, 5)
        hbox_img.Add(self.img2_path, 0, wx.ALIGN_CENTER, 5)

        hbox_mae = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mae.Add(mae_label, 0, wx.ALIGN_CENTER, 5)
        hbox_mae.Add(self.mae_value, 0, wx.ALIGN_CENTER, 5)

        hbox_roi = wx.BoxSizer(wx.HORIZONTAL)
        hbox_roi.Add(self.roi1_button, 0, wx.ALIGN_CENTER, 5)
        hbox_roi.Add(self.roi1_path, 0, wx.ALIGN_CENTER, 5)
        hbox_roi.Add(self.roi2_button, 0, wx.ALIGN_CENTER, 5)
        hbox_roi.Add(self.roi2_path, 0, wx.ALIGN_CENTER, 5)

        hbox_jacc = wx.BoxSizer(wx.HORIZONTAL)
        hbox_jacc.Add(jac_label, 0, wx.ALIGN_CENTER, 5)
        hbox_jacc.Add(self.jac_value, 0, wx.ALIGN_CENTER, 5)

        hbox_dice = wx.BoxSizer(wx.HORIZONTAL)
        hbox_dice.Add(dice_label, 0, wx.ALIGN_CENTER, 5)
        hbox_dice.Add(self.dice_value, 0, wx.ALIGN_CENTER, 5)

        hbox_vs = wx.BoxSizer(wx.HORIZONTAL)
        hbox_vs.Add(vs_label, 0, wx.ALIGN_CENTER, 5)
        hbox_vs.Add(self.vs_value, 0, wx.ALIGN_CENTER, 5)

        hbox_fn = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fn.Add(fn_label, 0, wx.ALIGN_CENTER, 5)
        hbox_fn.Add(self.fn_value, 0, wx.ALIGN_CENTER, 5)

        hbox_fp = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fp.Add(fp_label, 0, wx.ALIGN_CENTER, 5)
        hbox_fp.Add(self.fp_value, 0, wx.ALIGN_CENTER, 5)

        vbox_over = wx.BoxSizer(wx.VERTICAL)
        vbox_over.Add(hbox_jacc, 0, wx.ALIGN_CENTER, 5)
        vbox_over.Add(hbox_dice, 0, wx.ALIGN_CENTER, 5)
        vbox_over.Add(hbox_vs, 0, wx.ALIGN_CENTER, 5)
        vbox_over.Add(hbox_fn, 0, wx.ALIGN_CENTER, 5)
        vbox_over.Add(hbox_fp, 0, wx.ALIGN_CENTER, 5)

        hbox_hd = wx.BoxSizer(wx.HORIZONTAL)
        hbox_hd.Add(hd_label, 0, wx.ALIGN_CENTER, 5)
        hbox_hd.Add(self.hd_value, 0, wx.ALIGN_CENTER, 5)

        hbox_msd = wx.BoxSizer(wx.HORIZONTAL)
        hbox_msd.Add(msd_label, 0, wx.ALIGN_CENTER, 5)
        hbox_msd.Add(self.msd_value, 0, wx.ALIGN_CENTER, 5)

        hbox_mesd = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mesd.Add(mesd_label, 0, wx.ALIGN_CENTER, 5)
        hbox_mesd.Add(self.mesd_value, 0, wx.ALIGN_CENTER, 5)

        hbox_std = wx.BoxSizer(wx.HORIZONTAL)
        hbox_std.Add(std_label, 0, wx.ALIGN_CENTER, 5)
        hbox_std.Add(self.std_value, 0, wx.ALIGN_CENTER, 5)

        hbox_max = wx.BoxSizer(wx.HORIZONTAL)
        hbox_max.Add(max_label, 0, wx.ALIGN_CENTER, 5)
        hbox_max.Add(self.max_value, 0, wx.ALIGN_CENTER, 5)

        vbox_surf = wx.BoxSizer(wx.VERTICAL)
        vbox_surf.Add(hbox_hd, 0, wx.ALIGN_CENTER, 5)
        vbox_surf.Add(hbox_msd, 0, wx.ALIGN_CENTER, 5)
        vbox_surf.Add(hbox_mesd, 0, wx.ALIGN_CENTER, 5)
        vbox_surf.Add(hbox_std, 0, wx.ALIGN_CENTER, 5)
        vbox_surf.Add(hbox_max, 0, wx.ALIGN_CENTER, 5)

        hbox_index = wx.BoxSizer(wx.HORIZONTAL)
        hbox_index.Add(vbox_over, 0, wx.ALIGN_CENTER, 5)
        hbox_index.Add(vbox_surf, 0, wx.ALIGN_CENTER, 5)

        vbox_layout = wx.BoxSizer(wx.VERTICAL)
        vbox_layout.AddSpacer(5)
        vbox_layout.Add(hbox_img, 0, wx.ALIGN_CENTER, 10)
        vbox_layout.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 10)
        vbox_layout.Add(self.abs_err_view, 0, wx.ALIGN_CENTER, 15)
        vbox_layout.Add(hbox_mae, 0, wx.ALIGN_CENTER, 15)
        vbox_layout.AddSpacer(5)
        vbox_layout.Add(self.calc_btn_img, 0, wx.ALIGN_CENTER, 15)
        vbox_layout.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 10)
        vbox_layout.Add(hbox_roi, 0, wx.ALIGN_CENTER, 10)
        vbox_layout.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 10)
        vbox_layout.Add(hbox_index, 0, wx.ALIGN_CENTER, 10)
        vbox_layout.AddSpacer(5)
        vbox_layout.Add(self.calc_btn_roi, 0, wx.ALIGN_CENTER, 15)

        self.panel.SetSizer(vbox_layout)

        self.Centre()
        self.Show(True)

        self.calc_btn_img.Bind(wx.EVT_BUTTON, self.on_calc_img)
        self.calc_btn_roi.Bind(wx.EVT_BUTTON, self.on_calc_roi)
        self.img1_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 1))
        self.img2_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 2))
        self.roi1_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 3))
        self.roi2_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 4))

    def onOpenFile(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        wildcardtfm = 'Image source (*.nii, *nii.gz, *tfm)|*.nii; *nii.gz; *tfm|' \
                      'All files (*.*)|*.*'
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcardtfm,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 1:
                self.img1_path.SetLabelText(str(paths[0]))
            elif which_file == 2:
                self.img2_path.SetLabelText(str(paths[0]))
            elif which_file == 3:
                self.roi1_path.SetLabelText(str(paths[0]))
            elif which_file == 4:
                self.roi2_path.SetLabelText(str(paths[0]))
        dlg.Destroy()

    def onView(self, path_img, img):
        """
        View image when it is first selected by user
        """
        self.abs_err_view.populate_view(path_img=path_img, img=img)
        self.panel.Refresh()

    # TODO ricambiare funzioni per mandare img e non path
    def on_calc_img(self, event):
        path1 = self.img1_path.GetLabelText()
        path2 = self.img2_path.GetLabelText()
        mae_img, mae_val = utility_fx.calculate_mae(im1_path=path1, im2_path=path2)
        self.mae_value.SetLabelText(str(mae_val))
        self.img_mae = mae_img
        self.onView(path_img=path1, img=mae_img)

    def on_calc_roi(self, event):
        path1 = self.roi1_path.GetLabelText()
        path2 = self.roi2_path.GetLabelText()

        overlap, surface = accuracy_eval.accuracy_calc(roi1=path1, roi2=path2)
        self.jac_value.SetLabelText(str(overlap[0]))
        self.dice_value.SetLabelText(str(overlap[1]))
        self.vs_value.SetLabelText(str(overlap[2]))
        self.fn_value.SetLabelText(str(overlap[3]))
        self.fp_value.SetLabelText(str(overlap[4]))
        self.hd_value.SetLabelText(str(surface[0]))
        self.msd_value.SetLabelText(str(surface[1]))
        self.mesd_value.SetLabelText(str(surface[2]))
        self.std_value.SetLabelText(str(surface[3]))
        self.max_value.SetLabelText(str(surface[4]))


class CopyHeader(wx.Frame):
    """
    Loads one reference image and copies its header on one or more target images
    """

    def __init__(self, parent, title):
        super(CopyHeader, self).__init__(parent, title=title, size=(800, 400))

        self.panel = wx.Panel(self)
        self.SetBackgroundColour("THISTLE")

        self.currentDirectory = os.getcwd()
        self.path_ref = None
        self.path_tgts = []

        self.ref_img_button = wx.Button(self.panel, -1, "Select Reference Image", size=wx.Size(130, 30))
        self.ref_img_path = wx.TextCtrl(self.panel, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        size=wx.Size(600, 30))
        self.ref_img_path.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.tgts_img_button = wx.Button(self.panel, -1, "Select Targets Images", size=wx.Size(130, 30))
        self.tgts_img_path = wx.TextCtrl(self.panel, -1,
                                         style=wx.TE_CENTRE | wx.TE_READONLY | wx.TE_MULTILINE,
                                         size=wx.Size(600, 130))
        self.tgts_img_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.copy_btn = wx.Button(self.panel, -1, "Copy Header", size=wx.Size(100, 30))
        self.copy_btn.Enable(False)

        fixed_hbox = wx.BoxSizer(wx.HORIZONTAL)
        fixed_hbox.Add(self.ref_img_button, 0, wx.ALIGN_CENTER, 10)
        fixed_hbox.Add(self.ref_img_path, 0, wx.ALIGN_CENTER, 10)
        moving_hbox = wx.BoxSizer(wx.HORIZONTAL)
        moving_hbox.Add(self.tgts_img_button, 0, wx.ALIGN_CENTER, 10)
        moving_hbox.Add(self.tgts_img_path, 0, wx.ALIGN_CENTER, 10)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.AddSpacer(10)
        panel_sizer.Add(fixed_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(moving_hbox, 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.copy_btn, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        self.panel.SetSizer(panel_sizer)

        self.ref_img_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 1))
        self.tgts_img_button.Bind(wx.EVT_BUTTON, lambda event: self.onOpenFile(event, 2))
        self.copy_btn.Bind(wx.EVT_BUTTON, self.make_header_copy)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Ready')

        self.Centre()
        self.Show(True)

    def onOpenFile(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        if which_file == 1:
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        else:
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 1:
                self.ref_img_path.SetLabelText(str(paths[0]))
                self.path_ref = str(paths[0])
            elif which_file == 2:
                for i in paths:
                    self.tgts_img_path.AppendText(str(i) + "\n")
                    self.path_tgts.append(str(i))
                self.copy_btn.Enable(True)
        dlg.Destroy()

    def make_header_copy(self, event):
        utility_fx.correct_header(img_list=self.path_tgts, img_ref_path=self.path_ref)
        self.statusbar.SetStatusText('Done!')
