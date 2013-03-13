'''
Created on 24 Feb 2013

@author: Ali
'''
# Matplotlib with wxPython example from matplotlib.org
import wx
import wx.aui
import matplotlib
import pylab
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from Controllers.axisSettingsController import axisSettingsController

class mainPanel(wx.Frame):
    '''
    classdocs
    '''


    def __init__(self, parent, title):
        '''
        TODO: Fill function definition
        '''
        wx.Frame.__init__(self, None, -1, title)
        
        self.parent = parent
        
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        
        #Unpack individual instruments from instruments tuple
        #self.port1, self.port2, self.port3, self.port4, self.port5, self.port6 = instruments
        
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        
    def create_menu(self):
        self.MenuBar = wx.MenuBar()
        
        menu_file = wx.Menu()
        menu_file_saveData = menu_file.Append(-1, "Save data\tCtrl-S", "Save data to CSV format")
        menu_file_savePlot = menu_file.Append(-1, "Save plot\tCtrl-Shift-S", "Save plot to file")
        menu_file.AppendSeparator()
        menu_file_exit     = menu_file.Append(-1, "Exit\tCtrl-X", "Exit")
        
        menu_view = wx.Menu()
        menu_view_axis_settings = menu_view.Append(-1, "Axis Settings", "Opens Axis Settings Window")
        
        
        self.Bind(wx.EVT_MENU, self.on_save_data, menu_file_saveData)
        self.Bind(wx.EVT_MENU, self.on_save_plot, menu_file_savePlot)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_file_exit)
        
        self.Bind(wx.EVT_MENU, self.parent.on_axis_settings, menu_view_axis_settings)
        
        self.MenuBar.Append(menu_file, "File")
        self.MenuBar.Append(menu_view, "View")
    
    def create_main_panel(self):
        self.panel = wx.Panel(self)
                
        self.create_instrument_readout()
        self.create_plot()
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border = 10)  
        self.vbox.Add((-1, 10))   
        self.vbox.Add(self.instrument_grid, 1, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)
        
        self.panel.SetSizer(self.vbox)
        
    def create_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_title('Pressure vs Time', size=12)
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data = self.axes.plot((0,1), linewidth=1, color=(1, 1, 0), )[0]
        self.canvas = Canvas(self.panel, -1, self.fig)
    
    def create_instrument_readout(self):
        self.instrument_grid = wx.GridBagSizer(vgap=10, hgap=5)
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Instrument"), (0,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Pressure"), (0,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 1"), (1,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (1,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (1,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 2"), (2,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (2,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (2,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 3"), (3,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (3,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (3,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 4"), (4,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (4,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (4,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 5"), (5,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (5,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (5,2))
        
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, "Port 6"), (6,0))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (6,1))
        self.instrument_grid.Add(wx.StaticText(self.panel, -1, ""), (6,2))
        
        self.instrument_grid.AddGrowableCol(1)
        self.instrument_grid.AddGrowableCol(2)
    
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()
    
    def on_save_data(self):
        pass
    
    def on_save_plot(self):
        pass
    
    def on_exit(self):
        pass
       
    def on_redraw_timer(self):
        pass