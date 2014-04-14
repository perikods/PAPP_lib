'''
Created on 14/04/2014

@author: Pedro
'''
from PAPP_lib import PAPP_frame, PAPP_frame_cmd, ReadPAPPFrame
from struct import pack, unpack
import serial
import sys

## Script usage:
## python Example_SET_PORTA.py <COM Port> <addr in hex> <PORTA>
## e.g. python Example_SET_PORTA.py com2 0x2 0xFF

## COM Port configuration
s = serial.Serial(sys.argv[1])
s.timeout=1

## PORTA value to send
data=int(sys.argv[3],16)
PORTA_data=pack('B',data)   ## pack to match object type

#===============================================================================
# Prints the raw frame in console
#===============================================================================
def print_raw_frame(data):
    print data.encode('hex')
        
#===============================================================================
# Main block
#===============================================================================
def main():    
    ## Generate Custom data frame
    my_frame=PAPP_frame()
    my_frame.addr=int(sys.argv[2],16)                ## Destination address
    my_frame.flen=2                                  ## CMD + PORTA
    my_frame.data_cmd=PAPP_frame_cmd.SET_PORTA       ## Type
    my_frame.data= PORTA_data                        ## PORTA value to set in remote node
    
    my_frame.WritePAPPFrame(s.write)                 ## Write to COM port
    print ('Raw frame sent:')
    my_frame.WritePAPPFrame(print_raw_frame)         ## Write to console raw frame
    print ('--------------------')
    print my_frame                                   ## Write to console object details
    print ('--------------------')
    
    my_read_frame=ReadPAPPFrame(s.read, timeout=10)
    if my_read_frame is not None and my_read_frame.data_cmd==PAPP_frame_cmd.ACK_RSP:
        print ('Raw frame received:')        
        my_read_frame.WritePAPPFrame(print_raw_frame) ## Write to console raw frame
        print ('--------------------')
        print my_read_frame                           ## Write to console object details
        RSSI_lr, RSSI_rl= unpack('BB',my_read_frame.data[-2:])  ## Unpack RSSI (last two bytes)
        ## Print RSSI, both directions   
        print ('\nRSSI (local -> remote): %d' %((RSSI_lr/1.9)-127))
        print ('RSSI (local <- remote): %d' %((RSSI_rl/1.9)-127))          
    
    else:
        print ('Timeout')
    s.close()

if __name__ == "__main__":
    main()