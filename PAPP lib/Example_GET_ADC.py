'''
Created on 15 Apr 2014

@author: PedroDiaz
'''
'''
Created on 14/04/2014

@author: Pedro
'''
from PAPP_lib import PAPP_frame, PAPP_frame_cmd, ReadPAPPFrame
from struct import pack, unpack
import serial
import sys

## Script usage:
## python Example_GET_ADC.py <COM Port> <addr in hex> <channel>
## e.g. python Example_GET_ADC.py com2 0x2 0

## COM Port configuration
s = serial.Serial(sys.argv[1])
s.timeout=1

## ADC Channel to read
data=int(sys.argv[3])
channel=pack('B',data)                          ## pack to match object type

#===============================================================================
# Prints the raw frame in console
#===============================================================================
def print_raw_frame(data):
    print data.encode('hex')
        
#===============================================================================
# Main block
#===============================================================================
def main():    
    ## Generate Get ADC frame
    my_frame=PAPP_frame()
    my_frame.addr=int(sys.argv[2],16)                ## Destination address
    my_frame.flen=2                                  ## CMD + channel 
    my_frame.data_cmd=PAPP_frame_cmd.GET_ADC         ## Type
    my_frame.data= channel                       ## PORTA value to set in remote node
    
    my_frame.WritePAPPFrame(s.write)                 ## Write to COM port
    print ('Raw frame sent:')
    my_frame.WritePAPPFrame(print_raw_frame)         ## Write to console raw frame
    print ('--------------------')
    print my_frame                                   ## Write to console object details
    print ('--------------------')
    
    my_read_frame=ReadPAPPFrame(s.read, timeout=10)
    if my_read_frame is not None and my_read_frame.data_cmd==PAPP_frame_cmd.GET_ADC_RSP:
        print ('Raw frame received:')        
        my_read_frame.WritePAPPFrame(print_raw_frame) ## Write to console raw frame
        print ('--------------------')
        print my_read_frame                           ## Write to console object details
        ## Unpack ADC channel, data and RSSI (last two bytes)
        ADC_channel, ADC_data, RSSI_lr, RSSI_rl= unpack('<BHBB',my_read_frame.data)
        print ('\nADC data of channel (%d): %d' % (ADC_channel, ADC_data)) 
        ## Print RSSI, both directions   
        print ('RSSI (local -> remote): %d' %((RSSI_lr/1.9)-127))
        print ('RSSI (local <- remote): %d' %((RSSI_rl/1.9)-127))          
    
    else:
        print ('Timeout')
    s.close()

if __name__ == "__main__":
    main()