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

# Define notification event for thread completion
EVT_SERIAL_RX = wx.NewId()
EVT_SERIAL_TX = wx.NewId()
EVT_NEW_DATAPOINT = wx.NewId()
EVT_INSTRUMENT_STATUS = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_SERIAL_RX, func)

class serialRxEvent(wx.PyEvent):
    """"Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SERIAL_RX)
        self.data = data

class newDataPointEvent(wx.PyEvent):
    """"Simple event to carry arbitrary result data."""
    def __init__(self, channel, time, pressure):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SERIAL_RX)
        self.channel = channel
        self.time = time
        self.pressure = pressure

class instrumentChangeEvent(wx.PyEvent):
    """"Simple event to carry arbitrary result data."""
    def __init__(self, channel, instrumentCode, instrumentName, errorCode, errorString):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SERIAL_RX)
        self.channel = channel
        self.instrumentCode = instrumentCode
        self.instrumentName = instrumentName
        self.errorCode = errorCode
        self.errorString = errorString

class mainPanel(wx.Frame):
    '''
    classdocs
    '''

    def __init__(self, parent, title):
        '''
        
        :param parent:
        :type parent:
        :param title:
        :type title:
        '''
        wx.Frame.__init__(self, None, -1, title)
        
        self.parent = parent
        
        self.create_menuBar()
        self.create_status_bar()
        self.create_main_panel()
        
        #Create serial port
        #self.port1, self.port2, self.port3, self.port4, self.port5, self.port6 = instruments
        
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)


#===============================================================================
# Menu Drawing Routines
#===============================================================================
    
    def create_menuBar(self):
        menuBar = wx.MenuBar()
        
        for eachMenuData in self.menuData(): 
            menuLabel = eachMenuData[0] 
            menuItems = eachMenuData[1] 
            menuBar.Append(self.createMenu(menuItems), menuLabel) 
        self.SetMenuBar(menuBar)
    
    def create_menu(self, menuItems):
        menu = wx.Menu() 
        for menuTuple in menuItems: 
            if len(menuTuple) == 2:
                menu.AppendMenu(self.create_menu(menuTuple[1]), menuTuple[0])
            if len(menuTuple) == 4:
                eachID, eachLabel, eachStatus, eachHandler = menuTuple
                if not eachLabel: 
                    menu.AppendSeparator() 
                    continue 
                if not eachID:
                    eachID = wx.ID_ANY
                if eachLabel:
                    menuItem = menu.Append(eachID, eachLabel, eachStatus) 
                else:
                    menuItem = menu.Append(eachID)
                self.Bind(wx.EVT_MENU, eachHandler, menuItem) 
        return menu
    
    def menuData(self):
        '''Returns menu structure as nested tuples. Length two tuples are menu levels, length 4 are menu items'''
        return (
            ("&File",
                ((wx.ID_SAVE, "&Save data\tCtrl+S", "Save data to CSV format", self.onSaveCSV),
                ("", "Save plot\tCtrl+Shift+S", "Save plot to file", self.onSavePlot),
                ("", "", "", ""),
                ("", "Exit\tCtrl+X", "Exit", self.onExit)
            )), ("&View",
                (("", "Axis Settings", "Opens Axis Settings Window", self.onAxisSettings))
            ))
    
    def create_menu1(self):
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

#===============================================================================
# Status Bar Drawing Routines
#===============================================================================

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

#===============================================================================
# Main Panel Drawing Routines
#===============================================================================

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

#===============================================================================
# Event Handlers - To be moved!
#===============================================================================
    
    def on_save_data(self):
        pass
    
    def on_save_plot(self):
        pass
    
    def on_exit(self):
        pass
       
    def on_redraw_timer(self):
        pass
    

                    
def formatMenuData(inputString, width, enforceWidth=False, seperator='\t'):
    '''
    Splits inputString on character defined by seperator and returns string padded to specified width.
    
    :param inputString: string to be formatted
    :type inputString: str
    :param width: Desired width of returned string
    :type width: int
    :param enforceWidth: Forces returned string length to be exactly width
    :type enforceWidth: bool
    :param seperator: string split around
    :type seperator: str
    '''

    if inputString.find(seperator) != -1:
        number = len(inputString.split(seperator))
        length = sum([len(x) for x in inputString.split(seperator)]) #Calculate total length of string sections
        if length > width:
            if enforceWidth:
                return ''.join(inputString.split(seperator))[:width] # Returns concatenated string, cut to specified width. Index width-1 used as first index 0.
            return ''.join(inputString.split(seperator)) # Return concatenated string, but at width greater than 
        if not (width - length) % (number - 1): # Parse string if fits with even spacing between words
            return (' '*((width - length)/(number - 1))).join(inputString.split(seperator))
        else:
            gapsToReduce = ((width - length) % (number - 1)) + 1
            spacing = ((width - length) // (number - 1)) + 1
            return (' ' * (spacing - 1)).join((inputString.split(seperator)[:length - gapsToReduce]+[(' ' * spacing).join(inputString.split(seperator)[-gapsToReduce:])]))
    return inputString.ljust(width)
