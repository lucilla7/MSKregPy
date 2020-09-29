import wx
import os
import wx.lib.agw.floatspin as fs
import wx.lib.scrolledpanel as sp
import matplotlib.pyplot as plt
import ImageViewer
import registration_pipeline
import utility_fx
# import error_window

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


class RegistrationControl(wx.Panel):
    """
    Panel for registration step control
    """

    def __init__(self, parent, name):
        super(RegistrationControl, self).__init__(parent, name="Default")

        self.controls_font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)

        self.box = wx.StaticBox(self, -1, "Parameters")
        self.box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        # Metric Control
        metric_choices = ['Mean Squares', 'Correlation', 'Mattes MI']  # list of possible metrics
        # n_choices = len(metric_choices)
        default_metric = metric_choices[2]  # default metric set in comboBox to avoid errors
        # TODO aggiungere altre e differenziare (MI con bin ad es)
        box_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)

        # Registration widgets
        self.tfm_check = wx.CheckBox(self, -1, style=wx.TE_CENTRE, label=name, size=wx.Size(100, 50))
        self.tfm_check.SetFont(box_font)

        metric_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Metric",
                                     size=wx.Size(120, 30))
        metric_label.SetFont(self.controls_font)
        self.metric_combo = wx.ComboBox(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY | wx.CB_DROPDOWN,
                                        choices=metric_choices, size=wx.Size(100, 30))
        self.metric_combo.SetValue(default_metric)
        sampl_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Sampling %",
                                    size=wx.Size(120, 30))
        sampl_label.SetFont(self.controls_font)
        self.sampling_sc = wx.SpinCtrl(self, size=wx.Size(100, 20))
        lr_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Learning rate",
                                 size=wx.Size(120, 30))
        lr_label.SetFont(self.controls_font)
        self.lr_ctrl = fs.FloatSpin(self, -1, style=wx.TE_CENTRE, value=1, min_val=0.1, max_val=100)
        self.lr_ctrl.SetDigits(1)

        it_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="N. iterations",
                                 size=wx.Size(120, 30))
        it_label.SetFont(self.controls_font)
        self.it_ctrl = wx.SpinCtrl(self, size=wx.Size(100, 20))
        self.it_ctrl.SetRange(1, 10000)

        mv_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Conv Min Value",
                                 size=wx.Size(120, 30))
        mv_label.SetFont(self.controls_font)
        ex_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="10e-",
                                 size=wx.Size(30, 30))
        ex_label.SetFont(self.controls_font)
        self.mv_ctrl = wx.SpinCtrl(self, size=wx.Size(50, 20))
        self.mv_ctrl.SetRange(1, 8)

        ws_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Window Size",
                                 size=wx.Size(120, 30))
        ws_label.SetFont(self.controls_font)
        self.ws_ctrl = wx.SpinCtrl(self, size=wx.Size(100, 20))
        self.ws_ctrl.SetRange(2, 1000)

        sf_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Shrink Factors",
                                 size=wx.Size(120, 30))
        sf_label.SetFont(self.controls_font)
        sf_label.SetToolTip("Factors to apply when moving from one level \n"
                            "of the multiresolution pyramid to the next\n"
                            "Required format: int int int")
        self.sf_ctrl = wx.TextCtrl(self, -1, style=wx.TE_LEFT, size=wx.Size(80, 20))

        ss_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY, label="Smoothing Sigmas",
                                 size=wx.Size(120, 30))
        ss_label.SetFont(self.controls_font)
        ss_label.SetToolTip("Sigmas to use for smoothing when moving \n"
                            "from level to level \n"
                            "Required format: int int int")
        self.ss_ctrl = wx.TextCtrl(self, -1, style=wx.TE_LEFT, size=wx.Size(80, 20))

        mesh_label = wx.StaticText(self, -1, style=wx.TE_CENTRE | wx.TE_READONLY,
                                   label="Mesh Size",
                                   size=wx.Size(120, 30))
        mesh_label.SetToolTip("The mesh size is the number of polynomial patches comprising the finite domain of "
                              "support.\n "
                              "The relationship between the mesh size (number of polynomical pieces) \n"
                              "and the number of control points in any given dimension is: \n "
                              "mesh size = number of control points - spline order)")

        mesh_label.SetFont(self.controls_font)
        self.mesh1 = wx.SpinCtrl(self, size=wx.Size(50, 20))
        self.mesh1.SetRange(1, 100)

        self.mesh2 = wx.SpinCtrl(self, size=wx.Size(50, 20))
        self.mesh2.SetRange(1, 100)

        self.mesh3 = wx.SpinCtrl(self, size=wx.Size(50, 20))
        self.mesh3.SetRange(1, 100)

        self.vbox_tfm = wx.BoxSizer(wx.VERTICAL)

        hbox_metric = wx.BoxSizer(wx.HORIZONTAL)
        hbox_metric.Add(metric_label, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox_metric.Add(self.metric_combo, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 10)

        hbox_sr = wx.BoxSizer(wx.HORIZONTAL)
        hbox_sr.Add(sampl_label, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox_sr.Add(self.sampling_sc, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 10)

        hbox_lr = wx.BoxSizer(wx.HORIZONTAL)
        hbox_lr.Add(lr_label, 0, wx.ALIGN_CENTER, 10)
        hbox_lr.Add(self.lr_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_it = wx.BoxSizer(wx.HORIZONTAL)
        hbox_it.Add(it_label, 0, wx.ALIGN_CENTER, 10)
        hbox_it.Add(self.it_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_mv = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mv.Add(mv_label, 0, wx.ALIGN_CENTER, 10)
        hbox_mv.Add(ex_label, 0, wx.ALIGN_CENTER, 10)
        hbox_mv.Add(self.mv_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_ws = wx.BoxSizer(wx.HORIZONTAL)
        hbox_ws.Add(ws_label, 0, wx.ALIGN_CENTER, 10)
        hbox_ws.Add(self.ws_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_sf = wx.BoxSizer(wx.HORIZONTAL)
        hbox_sf.Add(sf_label, 0, wx.ALIGN_CENTER, 10)
        hbox_sf.Add(self.sf_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_ss = wx.BoxSizer(wx.HORIZONTAL)
        hbox_ss.Add(ss_label, 0, wx.ALIGN_CENTER, 10)
        hbox_ss.Add(self.ss_ctrl, 0, wx.ALIGN_CENTER, 10)

        hbox_mesh = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mesh.Add(mesh_label, 0, wx.ALIGN_CENTER, 10)
        hbox_mesh.Add(self.mesh1, 0, wx.ALIGN_CENTER, 5)
        hbox_mesh.Add(self.mesh2, 0, wx.ALIGN_CENTER, 5)
        hbox_mesh.Add(self.mesh3, 0, wx.ALIGN_CENTER, 5)

        self.vbox_tfm.Add(self.tfm_check, 0, wx.ALIGN_CENTER, 10)

        self.box_sizer.Add(hbox_metric)
        self.box_sizer.Add(hbox_sr)
        self.box_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        self.box_sizer.Add(hbox_lr)
        self.box_sizer.Add(hbox_it)
        self.box_sizer.Add(hbox_mv)
        self.box_sizer.Add(hbox_ws)
        self.box_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        self.box_sizer.Add(hbox_sf)
        self.box_sizer.Add(hbox_ss)
        if name == "Elastic":
            self.box_sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        self.box_sizer.Add(hbox_mesh)

        self.vbox_tfm.Add(self.box_sizer, 0, wx.ALIGN_CENTER, 10)

        self.metric_combo.Enable(False)
        self.sampling_sc.Enable(False)
        self.lr_ctrl.Enable(False)
        self.it_ctrl.Enable(False)
        self.mv_ctrl.Enable(False)
        self.ws_ctrl.Enable(False)
        self.sf_ctrl.Enable(False)
        self.ss_ctrl.Enable(False)
        self.mesh1.Enable(False)
        self.mesh2.Enable(False)
        self.mesh3.Enable(False)

        if name != "Elastic":
            hbox_mesh.Show(False)
            mesh_label.Show(False)
            self.mesh1.Show(False)
            self.mesh2.Show(False)
            self.mesh3.Show(False)
        else:
            hbox_mesh.Show(True)
            mesh_label.Show(True)
            self.mesh1.Show(True)
            self.mesh2.Show(True)
            self.mesh3.Show(True)

        self.SetSizer(self.vbox_tfm)

        self.tfm_check.Bind(wx.EVT_CHECKBOX, self.on_check_tfm)

    def on_check_tfm(self, event):
        if self.tfm_check.GetValue() is False:
            self.metric_combo.Enable(False)
            self.sampling_sc.Enable(False)
            self.lr_ctrl.Enable(False)
            self.it_ctrl.Enable(False)
            self.mv_ctrl.Enable(False)
            self.ws_ctrl.Enable(False)
            self.sf_ctrl.Enable(False)
            self.ss_ctrl.Enable(False)
            self.mesh1.Enable(False)
            self.mesh2.Enable(False)
            self.mesh3.Enable(False)
        else:
            self.metric_combo.Enable(True)
            self.sampling_sc.Enable(True)
            self.lr_ctrl.Enable(True)
            self.it_ctrl.Enable(True)
            self.mv_ctrl.Enable(True)
            self.ws_ctrl.Enable(True)
            self.sf_ctrl.Enable(True)
            self.ss_ctrl.Enable(True)
            self.mesh1.Enable(True)
            self.mesh2.Enable(True)
            self.mesh3.Enable(True)


class RegistrationFrame(wx.Frame):
    def __init__(self, parent, title, path_fix, path_mov):
        super(RegistrationFrame, self).__init__(parent, title=title, size=(1000, 600))

        panel_reg = wx.Panel(self)
        panel_reg.SetBackgroundColour('WHEAT')

        self.path_fix = str(path_fix)
        self.path_mov = str(path_mov)
        self.path_reg = None

        self.currentDirectory = os.getcwd()
        self.wildcard = "Image source (*.nii, *nii.gz)|*.nii; *nii.gz|" \
                        "All files (*.*)|*.*"

        controls_font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)

        # 3 trasformazioni con toggle per selezionare multistep
        # save per immagine, immagine iso e trasformazione

        # a funzione di registrazione va passato parametro su numero e quali trasformazioni, tutti i parametri di
        # sample, ottimizzatori (all'inizio un solo ottimizzatore), boolean se immagine va ISO o no

        # Labels for already chosen images
        fixed_img_label = wx.StaticText(panel_reg, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                        label="Fixed Image",
                                        size=wx.Size(80, 30))
        fixed_img_label.SetFont(controls_font)
        fixed_img_path = wx.StaticText(panel_reg, -1,
                                       style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                       label=str(os.path.basename(self.path_fix)),
                                       size=wx.Size(120, 30))

        moving_img_label = wx.StaticText(panel_reg, -1,
                                         style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                         label="Moving Image",
                                         size=wx.Size(80, 30))
        moving_img_label.SetFont(controls_font)

        moving_img_path = wx.StaticText(panel_reg, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                        label=str(os.path.basename(self.path_mov)),
                                        size=wx.Size(120, 30))

        # Buttons and textlines for masks - optional
        self.fixed_msk_button = wx.Button(panel_reg, -1, "Select Fixed Mask", size=wx.Size(130, 30))
        self.fixed_msk_path = wx.StaticText(panel_reg, -1,
                                            style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                            label="Fixed Mask...",
                                            size=wx.Size(600, 30))
        self.fixed_msk_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.moving_msk_button = wx.Button(panel_reg, -1, "Select Moving Mask", size=wx.Size(130, 30))
        self.moving_msk_path = wx.StaticText(panel_reg, -1,
                                             style=wx.TE_CENTRE | wx.TE_READONLY | wx.ALIGN_CENTER_VERTICAL,
                                             label="Moving Mask...",
                                             size=wx.Size(600, 30))
        self.moving_msk_path.SetBackgroundColour(wx.Colour(255, 255, 255))

        # Checkbox for making image isotropic
        self.iso_checkbox = wx.CheckBox(panel_reg, -1, style=wx.TE_CENTRE, label="Isotropic Image",
                                        size=wx.Size(200, 30))
        self.iso_checkbox.SetFont(controls_font)

        # Rigid registration box - default values found for muscles
        self.rigid_box = RegistrationControl(parent=panel_reg, name="Rigid")
        self.rigid_box.sampling_sc.SetValue(50)
        self.rigid_box.lr_ctrl.SetValue(15)
        self.rigid_box.it_ctrl.SetValue(5000)
        self.rigid_box.mv_ctrl.SetValue(7)
        self.rigid_box.ws_ctrl.SetValue(20)
        self.rigid_box.sf_ctrl.SetLabelText("4 2 1")
        self.rigid_box.ss_ctrl.SetLabelText("2 1 0")

        # Affine registration widgets - default values found for muscles
        self.affine_box = RegistrationControl(parent=panel_reg, name="Affine")
        self.affine_box.sampling_sc.SetValue(50)
        self.affine_box.lr_ctrl.SetValue(2)
        self.affine_box.it_ctrl.SetValue(5000)
        self.affine_box.mv_ctrl.SetValue(7)
        self.affine_box.ws_ctrl.SetValue(20)
        self.affine_box.sf_ctrl.SetLabelText("4 2 1")
        self.affine_box.ss_ctrl.SetLabelText("2 1 0")

        # Elastic registration widgets - default values found for muscles
        self.elastic_box = RegistrationControl(parent=panel_reg, name="Elastic")
        self.elastic_box.sampling_sc.SetValue(50)
        self.elastic_box.lr_ctrl.SetValue(2)
        self.elastic_box.it_ctrl.SetValue(2000)
        self.elastic_box.mv_ctrl.SetValue(7)
        self.elastic_box.ws_ctrl.SetValue(20)
        self.elastic_box.sf_ctrl.SetLabelText("2 1")
        self.elastic_box.ss_ctrl.SetLabelText("1 0")
        self.elastic_box.mesh1.SetValue(8)
        self.elastic_box.mesh2.SetValue(8)
        self.elastic_box.mesh3.SetValue(8)

        self.registration_btn = wx.Button(panel_reg, -1, "Registration and Save", size=wx.Size(160, 30))

        hbox_fix = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fix.Add(fixed_img_label, 0, wx.ALIGN_CENTER, 10)
        hbox_fix.Add(fixed_img_path, 0, wx.ALIGN_CENTER, 10)
        hbox_mov = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mov.Add(moving_img_label, 0, wx.ALIGN_CENTER, 10)
        hbox_mov.Add(moving_img_path, 0, wx.ALIGN_CENTER, 10)

        vbox_imgs = wx.BoxSizer(wx.VERTICAL)
        vbox_imgs.Add(hbox_fix, 0, wx.ALIGN_CENTER, 10)
        vbox_imgs.Add(hbox_mov, 0, wx.ALIGN_CENTER, 10)

        hbox_fix_msk = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fix_msk.Add(self.fixed_msk_button, 0, wx.ALIGN_CENTER, 10)
        hbox_fix_msk.Add(self.fixed_msk_path, 0, wx.ALIGN_CENTER, 10)
        hbox_mov_msk = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mov_msk.Add(self.moving_msk_button, 0, wx.ALIGN_CENTER, 10)
        hbox_mov_msk.Add(self.moving_msk_path, 0, wx.ALIGN_CENTER, 10)

        vbox_msks = wx.BoxSizer(wx.VERTICAL)
        vbox_msks.Add(hbox_fix_msk, 0, wx.ALIGN_CENTER, 10)
        vbox_msks.Add(hbox_mov_msk, 0, wx.ALIGN_CENTER, 10)

        hbox_paths = wx.BoxSizer(wx.HORIZONTAL)
        hbox_paths.Add(vbox_imgs, 0, wx.ALIGN_CENTER, 10)
        hbox_paths.Add(vbox_msks, 0, wx.ALIGN_CENTER, 10)

        hbox_transform = wx.BoxSizer(wx.HORIZONTAL)

        hbox_transform.Add(self.rigid_box)
        hbox_transform.AddSpacer(50)
        hbox_transform.Add(self.affine_box)
        hbox_transform.AddSpacer(50)
        hbox_transform.Add(self.elastic_box)

        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_hbox.Add(self.registration_btn, 0, wx.ALIGN_CENTER, 10)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.AddSpacer(10)
        panel_sizer.Add(hbox_paths, 0, wx.ALIGN_CENTER, 10)
        panel_sizer.Add(wx.StaticLine(panel_reg, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(self.iso_checkbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        panel_sizer.Add(wx.StaticLine(panel_reg, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        panel_sizer.Add(hbox_transform, 0, wx.ALIGN_CENTER, 10)
        panel_sizer.Add(btn_hbox, 0, wx.ALIGN_CENTER, 10)

        panel_reg.SetSizer(panel_sizer)

        self.Centre()
        self.Show(True)

        # Connecting signals
        self.fixed_msk_button.Bind(wx.EVT_BUTTON, lambda event: self.on_open_file(event, 1))
        self.moving_msk_button.Bind(wx.EVT_BUTTON, lambda event: self.on_open_file(event, 2))
        self.registration_btn.Bind(wx.EVT_BUTTON, self.on_registration)

    def on_open_file(self, event, which_file):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=self.wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if which_file == 1:
                self.fixed_msk_path.SetLabelText(str(paths[0]))
            elif which_file == 2:
                self.moving_msk_path.SetLabelText(str(paths[0]))
        dlg.Destroy()

    def on_registration(self, event):
        mask_fixed = None
        mask_moving = None
        if self.fixed_msk_path.GetLabelText() != 'Fixed Mask...':
            mask_fixed = self.fixed_msk_path.GetLabelText()
        if self.moving_msk_path.GetLabelText() != 'Moving Mask...':
            mask_moving = self.moving_msk_path.GetLabelText()
        iso_img = self.iso_checkbox.GetValue()
        # dict with transformation info. If tfm is checked, key is filled with values, otherwise is = None
        transformations = {'rigid': None, 'affine': None, 'elastic': None}
        if self.rigid_box.tfm_check.GetValue() is True:
            transformations['rigid'] = dict(metric=dict(name=self.rigid_box.metric_combo.GetValue(),
                                                        s_perc=float(self.rigid_box.sampling_sc.GetValue()) / 100.0),
                                            optimizers=dict(learning_rate=self.rigid_box.lr_ctrl.GetValue(),
                                                            iterations=self.rigid_box.it_ctrl.GetValue(),
                                                            minval=self.rigid_box.mv_ctrl.GetValue(),
                                                            window_size=self.rigid_box.ws_ctrl.GetValue()),
                                            multires=dict(shrinking_factors=[int(member) for member in
                                                                             self.rigid_box.sf_ctrl.GetValue().split(
                                                                                 ' ')],
                                                          smoothing_sigmas=[int(member) for member in
                                                                            self.rigid_box.ss_ctrl.GetValue().split(
                                                                                ' ')]))

        if self.affine_box.tfm_check.GetValue() is True:
            transformations['affine'] = dict(metric=dict(name=self.affine_box.metric_combo.GetValue(),
                                                         s_perc=float(self.affine_box.sampling_sc.GetValue()) / 100.0),
                                             optimizers=dict(learning_rate=self.affine_box.lr_ctrl.GetValue(),
                                                             iterations=self.affine_box.it_ctrl.GetValue(),
                                                             minval=self.affine_box.mv_ctrl.GetValue(),
                                                             window_size=self.affine_box.ws_ctrl.GetValue()),
                                             multires=dict(shrinking_factors=[int(member) for member in
                                                                              self.affine_box.sf_ctrl.GetValue().split(
                                                                                  ' ')],
                                                           smoothing_sigmas=[int(member) for member in
                                                                             self.affine_box.ss_ctrl.GetValue().split(
                                                                                 ' ')])
                                             )

        if self.elastic_box.tfm_check.GetValue() is True:
            transformations['elastic'] = dict(metric=dict(name=self.elastic_box.metric_combo.GetValue(),
                                                          s_perc=float(
                                                              self.elastic_box.sampling_sc.GetValue()) / 100.0),
                                              optimizers=dict(learning_rate=self.elastic_box.lr_ctrl.GetValue(),
                                                              iterations=self.elastic_box.it_ctrl.GetValue(),
                                                              minval=self.elastic_box.mv_ctrl.GetValue(),
                                                              window_size=self.elastic_box.ws_ctrl.GetValue()),
                                              multires=dict(shrinking_factors=[int(member) for member in
                                                                               self.elastic_box.sf_ctrl.GetValue().split(
                                                                                   ' ')],
                                                            smoothing_sigmas=[int(member) for member in
                                                                              self.elastic_box.ss_ctrl.GetValue().split(
                                                                                  ' ')]),
                                              mesh_size=[self.elastic_box.mesh1.GetValue(),
                                                         self.elastic_box.mesh2.GetValue(),
                                                         self.elastic_box.mesh3.GetValue()])

        # TODO per ora ok cosi, poi fare try e raise per intercettare eccezioni e metterle in warning win
        reg_prod, metric = registration_pipeline.make_registration(fixed_img_path=self.path_fix,
                                                                   moving_img_path=self.path_mov,
                                                                   fixed_msk_path=mask_fixed,
                                                                   moving_msk_path=mask_moving,
                                                                   iso_img=iso_img,
                                                                   tfm_dict=transformations)

        if reg_prod[0]['rigid'] is not None:
            with wx.FileDialog(self, "Save Rigid Nifti file", wildcard=self.wildcard,
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[0]['rigid'], str(pathname))
                        self.path_reg = str(pathname)
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if reg_prod[0]['affine'] is not None:
            with wx.FileDialog(self, "Save Affine Nifti file", wildcard=self.wildcard,
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[0]['affine'], str(pathname))
                        self.path_reg = str(pathname)
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if reg_prod[0]['elastic'] is not None:
            with wx.FileDialog(self, "Save Elastic Nifti file", wildcard=self.wildcard,
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[0]['elastic'], str(pathname))
                        self.path_reg = str(pathname)
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if reg_prod[1]['rigid'] is not None:
            with wx.FileDialog(self, "Save Rigid tfm file", wildcard="tfm files (*.tfm)|*.tfm",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[1]['rigid'], str(pathname))
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if reg_prod[1]['affine'] is not None:
            with wx.FileDialog(self, "Save Affine tfm file", wildcard="tfm files (*.tfm)|*.tfm",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[1]['affine'], str(pathname))
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if reg_prod[1]['elastic'] is not None:
            with wx.FileDialog(self, "Save Elastic tfm file", wildcard="tfm files (*.tfm)|*.tfm",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(str(pathname), 'w') as file:
                        utility_fx.save_file(reg_prod[1]['elastic'], str(pathname))
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        with wx.FileDialog(self, "Save Metric", wildcard="png files (*.png)|*.png",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(str(pathname), 'w') as file:
                    plt.plot(metric[0], 'r')
                    plt.plot(metric[1], [metric[0][index] for index in metric[1]], 'b*')
                    plt.xlabel('Iteration Number', fontsize=12)
                    plt.ylabel('Metric Value', fontsize=12)
                    plt.savefig(pathname)
            # plt.show()
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % str(pathname))

        if self.path_reg is not None:
            # img_fix = utility_fx.read_image(self.path)
            reg_img_win = RegistrationOutputViewer(parent=None, title="Registration Output Viewer",
                                                   path_fix=self.path_fix, path_reg=self.path_reg,
                                                   metric_val=metric[0], multires=metric[1])

            reg_img_win.Show()

        # Close the registration panel after completion of registration progress
        self.Destroy()


class CanvasPanel(wx.Panel):
    """
    Matplotlib Canvas class embedded in wx.Panel
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=wx.Size(400, 400))
        self.SetBackgroundColour("WHEAT")
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.CENTRE | wx.ALIGN_CENTRE_VERTICAL | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self, mv, mr):
        self.axes.plot(mv, 'r')
        self.axes.plot(mr, [mv[index] for index in mr], 'b*')
        self.axes.set_xlabel('Iteration Number', fontsize=12)
        self.axes.set_ylabel('Metric Value', fontsize=12)


class RegistrationOutputViewer(wx.Frame):
    def __init__(self, parent, title, path_fix, path_reg, metric_val, multires):
        super(RegistrationOutputViewer, self).__init__(parent, title=title, size=(1000, 600))

        self.SetBackgroundColour("WHEAT")
        panel_reg = sp.ScrolledPanel(self)
        panel_reg.SetupScrolling(scroll_y=True)

        reg_img_view = ImageViewer.ImageViewer(panel_reg, "Registered Image")
        fix_img_view = ImageViewer.ImageViewer(panel_reg, "Fixed Image")

        metric_canva = CanvasPanel(panel_reg)
        metric_canva.draw(metric_val, multires)

        reg_img_view.populate_view(path_reg)
        fix_img_view.populate_view(path_fix)

        vbox_imgs = wx.BoxSizer(wx.VERTICAL)
        vbox_imgs.Add(reg_img_view, 0, wx.ALIGN_CENTRE | wx.CENTRE, 5)
        vbox_imgs.Add(wx.StaticLine(panel_reg, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        vbox_imgs.Add(fix_img_view, 0, wx.ALIGN_CENTRE | wx.CENTRE, 5)
        vbox_imgs.Add(wx.StaticLine(panel_reg, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
        vbox_imgs.Add(metric_canva, 0, wx.ALIGN_CENTRE | wx.CENTRE, 5)

        panel_reg.SetSizer(vbox_imgs)
