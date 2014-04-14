'''
Created on 13/04/2014

@author: Pedro
'''
from PAPP_lib import PAPP_frame, PAPP_frame_cmd, ReadPAPPFrame
from struct import pack, unpack
import serial
import sys

## Script usage:
## python Example_CUSTOM_DATA.py <COM Port> <addr in hex>
## e.g. python Example.py com2 0x2

## COM Port configuration
s = serial.Serial(sys.argv[1])
s.timeout=1

## Data to send in hex
data_to_send="0A1B2C3D".decode('hex')                ## 4 bytes
data=pack('4s', data_to_send)                        ## Pack data

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
    my_frame.addr=int(sys.argv[2],16)               ## Destination address
    my_frame.flen=len(data)+1                       ## CMD + DATA
    my_frame.data_cmd=PAPP_frame_cmd.CUSTOM_DATA    ## Type
    my_frame.data= data                              ## Data
    
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
        RSSI_lr, RSSI_rl= unpack('BB',my_read_frame.data[-2:])   
        print ('\nRSSI (local -> remote): %d' %((RSSI_lr/1.9)-127))
        print ('RSSI (local <- remote): %d' %((RSSI_rl/1.9)-127))
          
    
    else:
        print ('Timeout')
    s.close()

if __name__ == "__main__":
    main()