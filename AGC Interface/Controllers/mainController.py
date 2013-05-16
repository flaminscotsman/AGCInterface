'''
Created on 13 Mar 2013

@author: Ali
'''
from Views.mainPanel import mainPanel
from Controllers.axisSettingsController import axisSettingsController
import wx

class mainController():

    def __init__(self, app):
        self.view = mainPanel(self, 'title')

#   View API
    def get_frame(self):
        return self.view
    
    def Show(self):
        self.view.Show()

#   Axes API

    def get_scaleX(self):
        return self.__get_scale('x')
    
    def get_scaleY(self):
        return self.__get_scale('y')
    
    def set_scaleX(self, scale, **kwargs):
        self.__set_scale('x', scale, **kwargs)
    
    def set_scaleY(self, scale, **kwargs):
        self.__set_scale('y', scale, **kwargs)
    
    def get_limX(self):
        return self.__get_lim('x')
    
    def get_limY(self):
        return self.__get_lim('y')
    
    def set_limX(self, lower=None, upper=None):
        self.__set_lim('x', lower, upper)
    
    def set_limY(self, lower=None, upper=None):
        self.__set_lim('y', lower, upper)
    
    def get_autoscaleX(self):
        return self.__get_autoscale('x')
    
    def get_autoscaleY(self):
        return self.__get_autoscale('y')
    
    def set_autoscaleX(self, autoscale):
        self.__set_autoscale('x', autoscale)
    
    def set_autoscaleY(self, autoscale):
        self.__set_autoscale('y', autoscale)

    def on_axis_settings(self, event):
        axisSettings = axisSettingsController(self, wx.ID_ANY)
        axisSettings.Show(True)
        
#Internal Functions for Interfacing to view begin here
    
    def __get_scale(self, axis):
        if axis.lower() == 'x':
            return self.view.axes.get_xscale()
        elif axis.lower() == 'y':
            return self.view.axes.get_yscale()
    
    def __set_scale(self, axis, scale, **kwargs):
        args = {}
        if scale == 'log':
            if 'base' in kwargs:
                args['base'] = kwargs['base']
            else:
                args['base'] = 10
            if 'nonpos' in kwargs and (kwargs['nonpos'] == 'clip' or kwargs['nonpos'] == 'mask'):
                args['nonpos'] = kwargs['nonpos']
            if 'subs' in kwargs:
                args['subs'] = kwargs['subs']
        elif scale == 'symlog':
            if 'base' in kwargs:
                args['base'] = kwargs['base']
            else:
                args['base'] = 10
            if 'linthresh' in kwargs:
                args['linthresh'] = kwargs['linthresh']
            if 'subs' in kwargs:
                args['subs'] = kwargs['subs']
            if 'linscale' in kwargs:
                args['linscale'] = kwargs['linscale']
        else:
            pass
        if axis.lower() == 'x':
            self.view.axes.set_xscale(scale, **args)
        elif axis.lower() == 'y':
            self.view.axes.set_yscale(scale, **args)
      
    def __get_autoscale(self, axis):
        if axis.lower() == 'x':
            return self.view.axes.get_autoscalex_on()
        elif axis.lower() == 'y':
            return self.view.axes.get_autoscaley_on()
    
    def __set_autoscale(self, axis, autoscale):
        if axis.lower() == 'x':
            self.view.axes.set_autoscalex_on(autoscale)
        elif axis.lower() == 'y':
            self.view.axes.set_autoscaley_on(autoscale)
      
    def __get_lim(self, axis):
        if axis.lower() == 'x':
            return self.view.axes.get_xbound()
        elif axis.lower() == 'y':
            return self.view.axes.get_ybound()
        
    def __set_lim(self, axis, lower, upper):
        if axis.lower() == 'x':
            self.view.axes.set_xbound(lower=lower, upper=upper)
        elif axis.lower() == 'y':
            self.view.axes.set_ybound(lower=lower, upper=upper)
    