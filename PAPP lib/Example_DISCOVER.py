'''
Created on 16 Apr 2014

@author: PedroDiaz
'''

from PAPP_lib import PAPP_frame, PAPP_frame_cmd, ReadPAPPFrame
from struct import pack, unpack
import serial
import sys

## Script usage:
## python Example_DISCOVER.py <COM Port>
## e.g. python Example_DISCOVER.py com2

## COM Port configuration
s = serial.Serial(sys.argv[1])
s.timeout=1

#===============================================================================
# Prints the raw frame in console
#===============================================================================
def print_raw_frame(data):
    print data.encode('hex')
        
#===============================================================================
# Main block
#===============================================================================
def main():    
    ## Generate DISCOVER frame
    my_frame=PAPP_frame()
    my_frame.addr= PAPP_frame.BROADCAST_ADDR         ## Destination address (0xFFFF if BROADCAST)
    my_frame.flen=1                                  ## CMD 
    my_frame.data_cmd=PAPP_frame_cmd.DISCOVER        ## Type
    
    my_frame.WritePAPPFrame(s.write)                 ## Write to COM port
    print ('Raw frame sent:')
    my_frame.WritePAPPFrame(print_raw_frame)         ## Write to console raw frame
    print ('--------------------')
    print my_frame                                   ## Write to console object details
    print ('--------------------')
    
    discover_again = True
    
    while discover_again:
        my_read_frame = ReadPAPPFrame(s.read, timeout=10)
        
        discover_again = False
        
        if my_read_frame is not None and my_read_frame.data_cmd==PAPP_frame_cmd.GET_PORTA_RSP:
            print ('Raw frame received:')        
            my_read_frame.WritePAPPFrame(print_raw_frame) ## Write to console raw frame
            print ('--------------------')
            print my_read_frame                           ## Write to console object details
            ## Unpack DISCOVER NAME and RSSI (last two bytes)
            NAME, RSSI_lr, RSSI_rl= unpack('10sBB',my_read_frame.data)
            print ('\nNAME: %s' % NAME) 
            ## Print RSSI, both directions   
            print ('RSSI (local -> remote): %d' %((RSSI_lr/1.9)-127))
            print ('RSSI (local <- remote): %d' %((RSSI_rl/1.9)-127))
            
            discover_again = True          
        
        else:
            print ('Timeout')
    s.close()

if __name__ == "__main__":
    main()