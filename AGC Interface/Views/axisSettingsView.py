'''
Created on 25 Feb 2013

@author: Ali
'''
import wx

class axisSettingsView(wx.Frame):
    def __init__(self, controller, parent, ID): #TODO: Rename
        '''
        Constructor
        '''
        wx.Frame.__init__(self, parent, ID, 'Axis Settings')
        self.panel = wx.Panel(self, -1)
        self.controller = controller
        
        self.Bind(wx.EVT_SHOW, self.controller.onShow, self)
        self.Bind(wx.EVT_CLOSE, self.controller.onCancel, self)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer.Add(self.createX(), 1, wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.createY(), 1, wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.createButtons(), 0, wx.ALIGN_RIGHT)
        
        self.panel.SetSizerAndFit(self.sizer)
    
    def createX(self):
        return self.createAxisBox('x')
    
    def createY(self):
        return self.createAxisBox('y')
                     
    def createAxisBox(self, letter):
        letter = letter.lower()
        
        Box                = wx.BoxSizer(wx.HORIZONTAL)
        settingsBox         = wx.BoxSizer(wx.VERTICAL)
        
        text                = wx.StaticText(self.panel, id=wx.ID_ANY, label= letter.upper() + ":", name=letter.upper())
        textcontrol         = self.createSpinCtrlPair(self.panel, letter + 'Min', letter + 'Max')
        scaleradiobuttons   = self.createRadioButtons(self.panel, wx.HORIZONTAL, ((letter + 'Linear', 'Linear'), (letter + 'Log', 'Logarithmic')))
        controlradiobuttons = self.createRadioButtons(self.panel, wx.VERTICAL, ((letter + 'Auto', 'Auto'), (letter + 'Manual', 'Manual')))
        
        settingsBox.Add(textcontrol,        0, wx.ALIGN_LEFT | wx.EXPAND | wx.FIXED_MINSIZE)
        settingsBox.Add(scaleradiobuttons,  0, wx.ALIGN_LEFT)
        
        Box.Add(text,                      0, wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.RIGHT | wx.TOP,   5)
        Box.Add(settingsBox,               1, wx.ALIGN_RIGHT | wx.RIGHT| wx.TOP | wx.EXPAND,       5)
        Box.Add(controlradiobuttons,       0, wx.ALIGN_RIGHT | wx.Right| wx.TOP,                   5)
        
        return Box
        
      
    def createButtons(self):
        buttonBox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self.panel, wx.ID_OK)
        cancelButton = wx.Button(self.panel, wx.ID_CANCEL)
        
        self.Bind(wx.EVT_BUTTON, self.controller.onOK, okButton)
        self.Bind(wx.EVT_BUTTON, self.controller.onCancel, cancelButton)
        
        buttonBox.Add(okButton, 0, wx.ALIGN_RIGHT | wx.Right, 20)
        buttonBox.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
        
        return buttonBox
    
    def createRadioButtons(self, parent, orientation, labels):
        box = wx.BoxSizer( orientation )
        
        if orientation == wx.VERTICAL:            
            button_name, button_label = labels[0]
            button = wx.RadioButton(parent, -1, name=button_name, label=button_label, style=wx.RB_GROUP)
            box.Add(button, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.controller.onRadiobutton, button )
            
            for button_name, button_label in labels[1:]:
                button = wx.RadioButton(parent, -1, name=button_name, label=button_label)
                box.Add(button, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT | wx.TOP, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.controller.onRadiobutton, button )
        else:
            button_name, button_label = labels[0]
            button = wx.RadioButton(parent, -1, name=button_name, label=button_label, style=wx.RB_GROUP)
            box.Add(button, 0, wx.ALIGN_LEFT | wx.RIGHT, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.controller.onRadiobutton, button )
                        
            for button_name, button_label in labels[1:]:
                button = wx.RadioButton(parent, -1, name=button_name, label=button_label)
                box.Add(button, 0, wx.ALIGN_LEFT | wx.RIGHT , 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.controller.onRadiobutton, button )
        
        return box
        
    
    def createSpinCtrlPair(self, parent,  name1, name2):
        box = wx.BoxSizer( wx.HORIZONTAL )
        
        textCtrl1   = wx.SpinCtrlDouble(parent, id=wx.ID_ANY, value="0", style=wx.SP_ARROW_KEYS, initial=0, inc=1, name=name1)
        textCtrl2   = wx.SpinCtrlDouble(parent, id=wx.ID_ANY, value="0", style=wx.SP_ARROW_KEYS, initial=0, inc=1, name=name2)
        panel       = wx.Panel(parent, id=wx.ID_ANY, name='Spacer')
        panel.SetBackgroundColour('DIM GREY')
        panel.SetMinSize(wx.Size(5, 1))
        
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.controller.onSpinCtrl, textCtrl1)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.controller.onSpinCtrl, textCtrl2)
        
        spacerBox = wx.BoxSizer(wx.HORIZONTAL)
        spacerBox.AddSpacer(2, 0)
        spacerBox.Add(panel, 0)
        spacerBox.AddSpacer(2, 0)
        
        box.Add(textCtrl1,  1, wx.ALIGN_LEFT | wx.EXPAND | wx.FIXED_MINSIZE,                    5)
        box.Add(spacerBox,  0, wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.LEFT | wx.Right,   5)
        box.Add(textCtrl2,  1, wx.ALIGN_LEFT | wx.RIGHT | wx.EXPAND | wx.FIXED_MINSIZE,         5)
        
        return box
    