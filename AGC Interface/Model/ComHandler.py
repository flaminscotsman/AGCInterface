'''
Created on 22 Feb 2013

@author: Ali
'''
import threading
import time

import serial

class ComHandler(threading.Thread):
    '''
    A thread for reading data from the COM port. The opening of the COM port is handled on thread start.
        
    port:
        COM port for to listen on
        
    baudRate:
        Baud rate of incoming data.
    
    stopBits:
        Number of stop bits between each serial message.
    
    parityBits:
        Number of parity bits at the end of each serial message.
    '''


    def __init__(self, port, baudRate, stopBits, parityBits):
        '''
        Constructor
        '''
        #Construction of serial port
        
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
        
        #Register Events
        self.read = EventHook()
        self.error = EventHook()
        
        self.writeQueue = []
        
        self.alive = threading.Event()
        self.alive.set()
        
    def run(self):
        try:
            # Dispose of old serial if exists
            if self.serial: 
                self.serial.close()
            # Open new serial interface
            self.serial = serial.Serial(**self.serialOptions)
        except serial.SerialException, e:
            self.errorQueue.put(e.message)
            return
          
        # Restart the clock
        time.clock()
        
        while self.alive.isSet():
            text = self.serial.read(1)          # Read Character from serial eort
            if text:                            # Check if character read
                n = self.serial.inWaiting()     # Check if more to read
                if n:
                    text = text + self.serial.read(n) # Consume any further characters from serial port
                while text.find("\r\n"):
                    data, text = text.split("\r\n", 1) # Extract first data string
                    self.read.fire()
            pass
        
        # clean up
        if self.serial:
            self.serial.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)