import wx
import utility_fx
import numpy as np
import nibabel as nib
import math


class ImageViewer(wx.Panel):
    """
    Class ImageViewer implements the visualization of the three panel view for image 3d arrays
    """

    def __init__(self, parent, name):
        super(ImageViewer, self).__init__(parent, style=wx.RAISED_BORDER, name="Image")

        self.back_colour = 'LIGHT STEEL BLUE'
        self.SetBackgroundColour(self.back_colour)

        self.img_max_size = 200
        self.title = name

        # draw vertical title near first view
        self.title_bmp = wx.Bitmap(50, 220)
        dc = wx.MemoryDC(self.title_bmp)
        gc = wx.GraphicsContext.Create(dc)
        title_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, False)
        gc.SetFont(title_font, "Black")
        # dc.Clear()
        w, h = dc.GetSize()
        tw, th = gc.GetTextExtent(self.title)
        # angle in radiants
        gc.DrawText(self.title.lower(), x=15, y=(h + tw) / 2, angle=math.pi / 2)  # display text in center
        del dc
        del gc
        self.title_view = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.title_bmp))

        image_view1 = wx.Image(200, 200)
        image_view2 = wx.Image(200, 200)
        image_view3 = wx.Image(200, 200)

        self.imageCtrl_view1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image_view1))
        self.imageCtrl_view2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image_view2))
        self.imageCtrl_view3 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image_view3))

        self.imageCtrl_view1.Enable(False)
        self.imageCtrl_view2.Enable(False)
        self.imageCtrl_view3.Enable(False)

        self.img_view = None

        self.img_index_view1 = 0
        self.img_dim_view1 = 0
        self.img_spin_view1 = wx.SpinCtrl(self, size=wx.Size(60, 20))
        self.img_spin_view1.SetValue(self.img_index_view1)
        self.img_spin_view1.Enable(False)

        self.img_index_view2 = 0
        self.img_dim_view2 = 0
        self.img_spin_view2 = wx.SpinCtrl(self, size=wx.Size(60, 20))
        self.img_spin_view2.SetValue(self.img_index_view2)
        self.img_spin_view2.Enable(False)

        self.img_index_view3 = 0
        self.img_dim_view3 = 0
        self.img_spin_view3 = wx.SpinCtrl(self, size=wx.Size(60, 20))
        self.img_spin_view3.SetValue(self.img_index_view3)
        self.img_spin_view3.Enable(False)

        title_font = wx.Font(7.5, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        img_view1_label = wx.StaticText(self, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        label="Axial",
                                        size=wx.Size(80, -1))
        img_view1_label.SetFont(title_font)
        img_view2_label = wx.StaticText(self, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        label="Coronal",
                                        size=wx.Size(80, -1))
        img_view2_label.SetFont(title_font)
        img_view3_label = wx.StaticText(self, -1,
                                        style=wx.TE_CENTRE | wx.TE_READONLY,
                                        label="Sagittal",
                                        size=wx.Size(80, -1))
        img_view3_label.SetFont(title_font)

        min_label = wx.StaticText(self, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Minimum",
                                  size=wx.Size(80, -1))
        min_label.SetFont(title_font)
        max_label = wx.StaticText(self, -1,
                                  style=wx.TE_CENTRE | wx.TE_READONLY,
                                  label="Maximum",
                                  size=wx.Size(80, -1))
        max_label.SetFont(title_font)
        gamma_label = wx.StaticText(self, -1,
                                    style=wx.TE_CENTRE | wx.TE_READONLY,
                                    label="Gamma",
                                    size=wx.Size(80, -1))
        gamma_label.SetFont(title_font)

        self.img_min_slide = wx.Slider(self, size=wx.Size(200, -1), name="Minimum")
        self.img_min_slide.SetRange(0, 255)
        self.img_min_slide.SetValue(0)
        self.img_min_slide.SetLineSize(1)
        self.img_min_slide.Enable(False)

        self.img_max_slide = wx.Slider(self, size=wx.Size(200, -1), name="Maximum")
        self.img_max_slide.SetRange(0, 255)
        self.img_max_slide.SetValue(255)
        self.img_max_slide.SetLineSize(1)
        self.img_max_slide.Enable(False)

        self.img_gamma_slide = wx.Slider(self, size=wx.Size(200, -1), name="Gamma")
        self.img_gamma_slide.SetRange(1, 500)
        self.img_gamma_slide.SetValue(100)
        self.img_gamma_slide.SetLineSize(1)
        self.img_gamma_slide.Enable(False)

        self.img_hbox = wx.BoxSizer(wx.HORIZONTAL)

        img_view1_labelled = wx.BoxSizer(wx.VERTICAL)
        img_view1_labelled.Add(img_view1_label, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view1_labelled.Add(self.imageCtrl_view1, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL | wx.CENTRE, 1)

        img_view1_hbox = wx.BoxSizer(wx.HORIZONTAL)
        img_view1_hbox.Add(img_view1_labelled, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view1_hbox.Add(self.img_spin_view1, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        img_view2_labelled = wx.BoxSizer(wx.VERTICAL)
        img_view2_labelled.Add(img_view2_label, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view2_labelled.Add(self.imageCtrl_view2, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL | wx.CENTRE, 1)

        img_view2_hbox = wx.BoxSizer(wx.HORIZONTAL)
        img_view2_hbox.Add(img_view2_labelled, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view2_hbox.Add(self.img_spin_view2, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        img_view3_labelled = wx.BoxSizer(wx.VERTICAL)
        img_view3_labelled.Add(img_view3_label, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view3_labelled.Add(self.imageCtrl_view3, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL | wx.CENTRE, 1)

        img_view3_hbox = wx.BoxSizer(wx.HORIZONTAL)
        img_view3_hbox.Add(img_view3_labelled, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 1)
        img_view3_hbox.Add(self.img_spin_view3, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        img_ctrl_vbox = wx.BoxSizer(wx.VERTICAL)
        img_ctrl_vbox.Add(min_label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        img_ctrl_vbox.Add(self.img_min_slide, 0, wx.ALL, 5)
        img_ctrl_vbox.Add(max_label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        img_ctrl_vbox.Add(self.img_max_slide, 0, wx.ALL, 5)
        img_ctrl_vbox.Add(gamma_label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        img_ctrl_vbox.Add(self.img_gamma_slide, 0, wx.ALL, 5)

        # if title_img:
        self.img_hbox.Add(self.title_view, 0, wx.ALIGN_CENTRE | wx.ALIGN_CENTRE_VERTICAL, 5)
        self.img_hbox.Add(img_view1_hbox, 0, wx.ALL, 5)
        self.img_hbox.Add(img_view2_hbox, 0, wx.ALL, 5)
        self.img_hbox.Add(img_view3_hbox, 0, wx.ALL, 5)
        self.img_hbox.Add(img_ctrl_vbox, 0, wx.ALL, 5)

        self.SetSizer(self.img_hbox)

        self.imageCtrl_view1.Bind(wx.EVT_MOUSEWHEEL, lambda event: self.on_wheel_image(event, 1))
        self.imageCtrl_view2.Bind(wx.EVT_MOUSEWHEEL, lambda event: self.on_wheel_image(event, 2))
        self.imageCtrl_view3.Bind(wx.EVT_MOUSEWHEEL, lambda event: self.on_wheel_image(event, 3))

        self.img_spin_view1.Bind(wx.EVT_SPINCTRL, lambda event: self.on_spin_image(event, 1))
        self.img_spin_view1.Bind(wx.EVT_SPINCTRL, self.on_ctr_scroll)
        self.img_spin_view2.Bind(wx.EVT_SPINCTRL, lambda event: self.on_spin_image(event, 2))
        self.img_spin_view2.Bind(wx.EVT_SPINCTRL, self.on_ctr_scroll)
        self.img_spin_view3.Bind(wx.EVT_SPINCTRL, lambda event: self.on_spin_image(event, 3))
        self.img_spin_view3.Bind(wx.EVT_SPINCTRL, self.on_ctr_scroll)
        self.img_min_slide.Bind(wx.EVT_SCROLL, self.on_ctr_scroll)
        self.img_max_slide.Bind(wx.EVT_SCROLL, self.on_ctr_scroll)
        self.img_gamma_slide.Bind(wx.EVT_SCROLL, self.on_ctr_scroll)

    # TODO riorganizzare e raggruppare funzioni su signals immagini
    def convert_nparray_for_bitmap(self, path_img, img=None):
        if img is None:
            img_data, img_head, img = utility_fx.read_image(path_img)
        else:
            img_data_ref, img_head, img_ref = utility_fx.read_image(path_img)
            img = nib.Nifti1Image(img, img_ref.affine, img_head)

        pix_dim = img_head['pixdim'][1:4]
        resolution = min(pix_dim)
        # Make isotropic for visualization
        img_arr = utility_fx.make_isotropic_nilearn(image=img, res=resolution).get_data()
        img_arr = img_arr.astype(np.float64)
        # Normalize array first to positive values, then in the interval 0-255
        img_arr = (img_arr - img_arr.min()) / (img_arr.max() - img_arr.min())
        img_arr = np.multiply(img_arr, 255.0, casting="unsafe") / img_arr.max()
        # img_data = img_data * 255.0 / img_data.max()
        self.img_view = np.flipud(img_arr.T)

        return np.flipud(img_arr.T)

    def get_bitmap(self, data, index, dim):
        if dim == 2:
            img_data = data[:, :, index]
            self.img_index_view3 = index
            self.img_dim_view3 = data.shape[dim]

        elif dim == 1:
            img_data = data[:, index, :]
            self.img_index_view2 = index
            self.img_dim_view2 = data.shape[dim]

        elif dim == 0:
            img_data = data[index, :, :]
            self.img_index_view1 = index
            self.img_dim_view1 = data.shape[dim]

        # From grayscale array to RGB and uint8 for wxImage
        # TODO controllare parte su colour img
        if len(img_data.shape) == 2:
            array = np.array([[[s, s, s] for s in r] for r in img_data], dtype="u1")
        elif len(img_data.shape) == 3:
            array = img_data
        else:
            raise ValueError("Data format not yet supported")
        image = wx.Image(array.shape[1], array.shape[0])
        image.SetData(array.tostring())
        image.ConvertToGreyscale()
        width = image.GetWidth()
        height = image.GetHeight()
        if width > height:
            new_w = self.img_max_size
            new_h = self.img_max_size * height / width
        else:
            new_h = self.img_max_size
            new_w = self.img_max_size * width / height
        image = image.Scale(new_w, new_h)
        wx_bit = image.ConvertToBitmap()  # OR:  wx.BitmapFromImage(image)
        return wx_bit

    def populate_view(self, path_img, img=None):
        self.imageCtrl_view1.Enable(True)
        self.imageCtrl_view2.Enable(True)
        self.imageCtrl_view3.Enable(True)
        self.img_max_slide.SetValue(255)
        self.img_min_slide.SetValue(0)
        self.img_gamma_slide.SetValue(100)
        img1 = self.convert_nparray_for_bitmap(path_img, img)
        bitmap3 = self.get_bitmap(data=img1, index=int(img1.shape[2] / 2), dim=2)
        self.imageCtrl_view3.SetBitmap(wx.Bitmap(bitmap3))
        bitmap2 = self.get_bitmap(data=img1, index=int(img1.shape[1] / 2), dim=1)
        self.imageCtrl_view2.SetBitmap(wx.Bitmap(bitmap2))
        bitmap1 = self.get_bitmap(data=img1, index=int(img1.shape[0] / 2), dim=0)
        self.imageCtrl_view1.SetBitmap(wx.Bitmap(bitmap1))

        self.img_spin_view1.SetRange(0, self.img_dim_view1 - 1)
        self.img_spin_view1.SetValue(self.img_index_view1)
        self.img_spin_view1.Enable(True)
        self.img_spin_view2.SetRange(0, self.img_dim_view2 - 1)
        self.img_spin_view2.SetValue(self.img_index_view2)
        self.img_spin_view2.Enable(True)
        self.img_spin_view3.SetRange(0, self.img_dim_view3 - 1)
        self.img_spin_view3.SetValue(self.img_index_view3)
        self.img_spin_view3.Enable(True)
        self.img_min_slide.Enable(True)
        self.img_max_slide.Enable(True)
        self.img_gamma_slide.Enable(True)

    def on_spin_image(self, event, which_image):
        if which_image == 3:
            new_bit = self.get_bitmap(self.img_view, self.img_spin_view3.GetValue(), 2)
            self.imageCtrl_view3.SetBitmap(wx.Bitmap(new_bit))
        elif which_image == 2:
            new_bit = self.get_bitmap(self.img_view, self.img_spin_view2.GetValue(), 1)
            self.imageCtrl_view2.SetBitmap(wx.Bitmap(new_bit))
        elif which_image == 1:
            new_bit = self.get_bitmap(self.img_view, self.img_spin_view1.GetValue(), 0)
            self.imageCtrl_view1.SetBitmap(wx.Bitmap(new_bit))
        self.Refresh()

    def on_wheel_image(self, event, which_image):
        if which_image == 3:
            if event.GetWheelRotation() < 0:
                self.img_spin_view3.SetValue(self.img_spin_view3.GetValue() - 1)
            else:
                self.img_spin_view3.SetValue(self.img_spin_view3.GetValue() + 1)
            minimum = self.img_min_slide.GetValue()
            maximum = self.img_max_slide.GetValue()
            gamma = float(self.img_gamma_slide.GetValue()) / 100.0
            img = self.img_view
            img = np.clip(img, minimum, maximum)
            img = 255 * (img / 255) ** (1 / gamma)
            new_bit = self.get_bitmap(img, self.img_spin_view3.GetValue(), 2)
            self.imageCtrl_view3.SetBitmap(wx.Bitmap(new_bit))
        elif which_image == 2:
            if event.GetWheelRotation() < 0:
                self.img_spin_view2.SetValue(self.img_spin_view2.GetValue() - 1)
            else:
                self.img_spin_view2.SetValue(self.img_spin_view2.GetValue() + 1)
            minimum = self.img_min_slide.GetValue()
            maximum = self.img_max_slide.GetValue()
            gamma = float(self.img_gamma_slide.GetValue()) / 100.0
            img = self.img_view
            img = np.clip(img, minimum, maximum)
            img = 255 * (img / 255) ** (1 / gamma)
            new_bit = self.get_bitmap(img, self.img_spin_view2.GetValue(), 1)
            self.imageCtrl_view2.SetBitmap(wx.Bitmap(new_bit))
        elif which_image == 1:
            if event.GetWheelRotation() < 0:
                self.img_spin_view1.SetValue(self.img_spin_view1.GetValue() - 1)
            else:
                self.img_spin_view1.SetValue(self.img_spin_view1.GetValue() + 1)
            minimum = self.img_min_slide.GetValue()
            maximum = self.img_max_slide.GetValue()
            gamma = float(self.img_gamma_slide.GetValue()) / 100.0
            img = self.img_view
            img = np.clip(img, minimum, maximum)
            img = 255 * (img / 255) ** (1 / gamma)
            new_bit = self.get_bitmap(img, self.img_spin_view1.GetValue(), 0)
            self.imageCtrl_view1.SetBitmap(wx.Bitmap(new_bit))
        self.Refresh()

    def on_ctr_scroll(self, event):
        minimum = self.img_min_slide.GetValue()
        maximum = self.img_max_slide.GetValue()
        gamma = float(self.img_gamma_slide.GetValue()) / 100.0
        img = self.img_view
        img = np.clip(img, minimum, maximum)
        img = 255 * (img / 255) ** (1 / gamma)
        new_bit3 = self.get_bitmap(img, self.img_spin_view3.GetValue(), 2)
        self.imageCtrl_view3.SetBitmap(wx.Bitmap(new_bit3))
        new_bit2 = self.get_bitmap(img, self.img_spin_view2.GetValue(), 1)
        self.imageCtrl_view2.SetBitmap(wx.Bitmap(new_bit2))
        new_bit1 = self.get_bitmap(img, self.img_spin_view1.GetValue(), 0)
        self.imageCtrl_view1.SetBitmap(wx.Bitmap(new_bit1))

        self.Refresh()
