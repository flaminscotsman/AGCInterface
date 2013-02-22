#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:     user_name
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from ComHandler import ComHandler

__all__ = []
__version__ = 0.1
__date__ = '2013-02-22'
__updated__ = '2013-02-22'

DEBUG = 1

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-r', "--baud-rate", dest='baudRate', type=int, choices=[110, 300, 600, 1200, 2400, 4800, 9600, 19200], default=9600, help='Sets baud rate for incoming signal')
        parser.add_argument('-p', '--parity', dest='parity', type=int, choices=[0, 1, 2], default=0, help='Sets number of parity bits for incoming signal [0-2]')
        parser.add_argument('-s', '--stop-bits', dest='stop', type=int, choices=[1,2], default=1, help='Sets number of stop bits for incoming signal [1-2]')
        parser.add_argument(dest="port", dest='port', help="COM for for incoming serial data")
        
        # Process arguments
        args = parser.parse_args()
        
        verbose = args.verbose
        port    = args.port
        baudRate= args.baudRate
        parity  = args.parity
        stopbits= args.stop
        
        if verbose > 0:
            print("Verbose mode on")
        
        
        dataQueue = None
        errorQueue = None #TODO: Implement queues
        comHandler = ComHandler(dataQueue, errorQueue, port, baudRate, stopbits, parity)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    sys.exit(main())