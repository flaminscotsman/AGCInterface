'''
Created on 26 Feb 2013

@author: Ali
'''
from Views.axisSettingsView import axisSettingsView

class axisSettingsController():
    def __init__(self, parent, ID):
        '''
        Constructor
        '''
        self.parent  = parent
#        assert isinstance(parent, mainController)
        self.view = axisSettingsView(self, parent.get_frame() , ID)
        self.xChange = False
        self.yChange = False
        self.log     = False
    
    def Show(self, show):
        self.view.Show(show)
    
    def onRadiobutton(self, event):
        name = event.GetEventObject().GetName()
        
        if 'x' in name:
            self.xChange = True
            if name == 'xAuto':
                self.autoscale('x', True)
            elif name == 'xManual':
                self.autoscale('x', False)
        if 'y' in name:
            self.yChange = True
            if name == 'yAuto':
                self.autoscale('y', True)
            elif name == 'yManual':
                self.autoscale('y', False)
        if 'Linear' in name:
            self.log = False
        if 'Log' in name:
            if name == 'xLog':
                if self.view.FindWindowByName('yLog').GetValue():
                    self.yChange = True
                    self.log = True
            if name == 'yLog':
                if self.view.FindWindowByName('xLog').GetValue():
                    self.xChange = True
                    self.log = True
    
    def onSpinCtrl(self, event):
        name = event.GetEventObject().GetName()
        
        if 'x' in name:
            self.xChange = True
            if name == 'xMin':
                self.spinCtrlVerify(True)
            else:
                self.spinCtrlVerify(False)
        if 'y' in name:
            self.yChange = True
            if name == 'yMin':
                self.spinCtrlVerify(True)
            else:
                self.spinCtrlVerify(False)
    
    def onOK(self, event):
        if self.xChange:
            if self.log:
                self.parent.set_scaleX('log', base=10)
            if self.view.FindWindowByName('xLog').GetValue():
                self.parent.set_scaleX('symlog', base=10)
            else:
                self.parent.set_scaleX('linear')
            if self.view.FindWindowByName('xAuto').GetValue():
                self.parent.set_autoscaleX(True)
            else:
                self.parent.set_autoscaleX(False)
                self.parent.set_limX(
                    lower=self.view.FindWindowByName('xMin').GetValue(), 
                    upper=self.view.FindWindowByName('xMax').GetValue())
        if self.yChange:
            if self.log:
                self.parent.set_scaleY('log', base=10)
            if self.view.FindWindowByName('yLog').GetValue():
                self.parent.set_scaleY('symlog', base=10)
            else:
                self.parent.set_scaleY('linear')
            if self.view.FindWindowByName('yAuto').GetValue():
                self.parent.set_autoscaleY(True)
            else:
                self.parent.set_autoscaleY(False)
                self.parent.set_limY(
                    lower=self.view.FindWindowByName('yMin').GetValue(), 
                    upper=self.view.FindWindowByName('yMax').GetValue())
        self.view.Destroy()
    
    def onCancel(self, event):
        self.view.Destroy()
        
    def onShow(self, event):
        self.autoscale('x', self.parent.get_autoscaleX())
        self.autoscale('y', self.parent.get_autoscaleY())
        self.view.FindWindowByName('xMin').SetValue(self.parent.get_limX()[0])
        self.view.FindWindowByName('xMax').SetValue(self.parent.get_limX()[1])
        self.view.FindWindowByName('yMin').SetValue(self.parent.get_limY()[0])
        self.view.FindWindowByName('yMax').SetValue(self.parent.get_limY()[1])
        if self.parent.get_scaleX() == 'linear':
            self.view.FindWindowByName('xLinear').SetValue(True)
        else:
            self.view.FindWindowByName('xLog').SetValue(True)
        if self.parent.get_scaleY() == 'linear':
            self.view.FindWindowByName('yLinear').SetValue(True)
        else:
            self.view.FindWindowByName('yLog').SetValue(True)
        if not (self.parent.get_scaleX() == 'linear' and
                self.parent.get_scaleY() == 'linear'):
            self.log = True
    
    def autoscale(self, axis, autoscale):
        axis = axis.lower()
        if autoscale:
            self.view.FindWindowByName(axis + 'Auto').SetValue(True)
            self.view.FindWindowByName(axis + 'Min').Disable()
            self.view.FindWindowByName(axis + 'Max').Disable()
        else:
            self.view.FindWindowByName(axis + 'Manual').SetValue(True)
            self.view.FindWindowByName(axis + 'Min').Enable()
            self.view.FindWindowByName(axis + 'Max').Enable()
            
    def spinCtrlVerify(self, Min):
        xMin = self.view.FindWindowByName('xMin').GetValue()
        xMax = self.view.FindWindowByName('xMax').GetValue()
        yMin = self.view.FindWindowByName('yMin').GetValue()
        yMax = self.view.FindWindowByName('yMax').GetValue()
        
        if Min:
            if xMin > xMax:
                self.view.FindWindowByName('xMax').SetValue(xMin)
            if yMin > yMax:
                self.view.FindWindowByName('yMax').SetValue(yMin)
        else:
            if xMin > xMax:
                self.view.FindWindowByName('xMin').SetValue(xMax)
            if yMin > yMax:
                self.view.FindWindowByName('yMin').SetValue(yMax)