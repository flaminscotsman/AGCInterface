'''
Created on 17 May 2013

@author: Ali
'''
import re
from datetime import datetime
from Views.mainPanel import newDataPointEvent, instrumentChangeEvent

DEBUG = 0

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coroutine
def dispatch(target):
    while True:
        pass

@coroutine
def printHandler(target):
    matcher = re.compile('(\d = \w{3})')
    while True:
        printString = (yield)
        if len(printString) == 41 and matcher.match(printString): #Only Handle Valid Packets
            port = printString[:1]
            instrument = printString[4:10].rstrip()
            data = printString[11:22].lstrip().rstrip()
            
            if printString[12:13].isdigit(): #Test to see if data or an error
                payload = ('data', port, instrument, data)
            else:
                payload = ('error', port, instrument, data)
            
            target.send(payload)
        elif DEBUG == 1:
            print 'Invalid Packet received'
        elif DEBUG > 1:
            print 'Invalid Packet received', printString 

@coroutine
def instrumentParser(target):
    instrumentLUT = {
        'WRG' : 'Wide Range Gauge', 
        'APG M' : 'Active Pirani APG-M', 
        'APG L' : 'Active Pirani APG-L', 
        'AIM S' : 'Active Inverted Magnetron AIM-S', 
        'AIM X' : 'Active Inverted Magnetron AIM-X', 
        'ATC 6M' : 'Active Thermocouple - 6M Tube', 
        'ATC 4D' : 'Active Thermocouple - 4D Tube', 
        'ION IR' : 'Ion Gauge Controller - IGC - Resistive degas', 
        'ION EB' : 'Ion Gauge Controller - IGC - E Beam degas', 
        'ASG' : 'Active Strain Gauge', 
        'APGX' : 'Linear Pirani Gauge', 
        'APGX-H' : 'Linear Convection Gauge', 
        'AIGX' : 'Active Ion Gauge - AIGX', 
        '590 CM' : 'Capacitance manometer Gauge - 500 Series', 
        '600 CM' : 'Capacitance manometer Gauge - 600 Series', 
        'TURBO' : 'Turbo Controller'}
    
    while True:
        dataPacket = (yield)
        if instrumentLUT.has_key(dataPacket[2]):
            payload = dataPacket[:3]+(instrumentLUT[dataPacket[2]],)+dataPacket[3:]
            target.send(payload)
        elif DEBUG == 1:
            print 'Invalid instrument string'
        elif DEBUG > 1:
            print 'Invalid instrument string', dataPacket[2] 

@coroutine
def errrorParser(target):
    errorLUT = {
        'OFF' : 'Gauge switched off or Auto gauge off',
        'SRKING' : 'AIM gauge striking',
        'AC ERR' : 'Auto gauge fault',
        '???' : 'Unknown gauge type',
        '‘ ‘' : 'Unclassified error',
        'ID ERR' : 'Gauge type error',
        '?VOLT' : 'Gauge voltage under range',
        'ADCERR' : 'Volts conversion error',
        'NOTSRK' : 'AIM gauge not struck',
        'EMERR' : 'Ion gauge emission error',
        'IGEMIS' : 'Ion gauge is warming up, not timed out.',
        'IG INH' : 'Ion gauge inhibited',
        'SW ERR' : 'Gauge switch error.',
        'FAULT' : 'Gauge Fault',
        'NEW ID' : 'New gauge type detected',
        'EXP BD' : 'New expansion board detected',
        'SYSERR' : 'System Error',
        'OVER R' : 'CAPMAN pressure over range'}
    
    while True:
        dataPacket = (yield)
        if dataPacket[0] == 'data': #Pass on non error packets uneffected
            target.send(dataPacket)
            continue
        elif dataPacket[0] == 'error':
            if errorLUT.has_key(dataPacket[4]):
                payload = dataPacket + (errorLUT[dataPacket[4]],)
                target.send(payload)
            elif DEBUG == 1:
                print 'Invalid error string'
            elif DEBUG > 1:
                print 'Invalid error string', dataPacket[4] 
        else: #Catch malformed payloads
            print 'Error. Malformed payload found in co-routine chain'
            
@coroutine
def eventHandler():
    def milliseconds():
        return ((datetime.now.day*24*3600) + datetime.now().microsecond / 1000)
    
    try:
        while True:
            dataPacket = (yield)
            if dataPacket[0] == 'data': #Pass on non error packets uneffected
                newDataPointEvent(dataPacket[1], milliseconds(), dataPacket[4])
            elif dataPacket[0] == 'error':
                instrumentChangeEvent(*dataPacket[1:])
            else: #Catch malformed payloads
                print 'Error. Malformed payload found in co-routine chain'
    except GeneratorExit:
        