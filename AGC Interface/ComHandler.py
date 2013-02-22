'''
Created on 22 Feb 2013

@author: Ali
'''
import threading
import time

import serial

class ComHandler(threading.thread):
    '''
    A thread for reading and validating data from the COM port. The opening of the COM port is handled on thread start.
    
    dataQueue:
        A tuple containing the individual gauge queues. gaugeData objcets will then be placed on these to be picked up by the gui.
    
    errorQueue:
        Passes serialerrors between ComHandler process and the main process.
    
    port:
        COM port for to listen on
        
    baudRate:
        Baud rate of incoming data.
    
    stopBits:
        Number of stop bits between each serial message.
    
    parityBits:
        Number of parity bits at the end of each serial message.
    '''


    def __init__(self, dataQueue, errorQueue, port, baudRate, stopBits, parityBits):
        '''
        Constructor
        '''
        if parityBits == 0:
            parityBits = serial.PARITY_NONE
        elif parityBits == 1:
            parityBits = serial.PARITY_EVEN
        else:
            parityBits = serial.PARITY_ODD
            
        if stopBits == 1:
            stopBits = serial.STOPBITS_ONE
        else:
            stopBits = serial.STOPBITS_TWO
        
        self.serial = None
        self.serialOptions = dict(
                                port=port,
                                baudrate=baudRate,
                                stopbits=stopBits,
                                parity=parityBits,
                                timeout=0)
        
        # Unpack Queues
        self.gauge1, self.gauge2, self.gauge3, self.gauge4, self.gauge5, self.gauge6 = dataQueue
        self.errorQueue = errorQueue
        
        self.alive = threading.Event()
        self.alive.set()
        
    def run(self):
        try:
            if self.serial: 
                self.serial.close()
            self.serial = serial.Serial(**self.serialOptions)
        except serial.SerialException, e:
            self.errorQueue.put(e.message)
            return
          
        # Restart the clock
        time.clock()
        
        while self.alive.isSet():
            #TODO: reading of serial data  
            pass
        
        # clean up
        if self.serial:
            self.serial.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)