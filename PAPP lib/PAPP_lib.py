'''
Peri-App library.
Created on 11 Apr 2014

@author: PedroDiaz
'''
from struct import pack, unpack
import time

#===============================================================================
# Peri-App frame types
#===============================================================================
class PAPP_frame_cmd (object):
    
    CUSTOM_DATA=     0x00
    SET_PORTA=       0x01
    GET_PORTA=       0x02
    GET_ADC=         0x03
    DISCOVER=        0x04
    SET_CONFIG=      0x06
    GET_CONFIG=      0x07
    GET_PORTA_RSP=   0x12
    GET_ADC_RSP=     0x13
    DISCOVER_RSP=    0x14
    ACK_RSP=         0x15
    SET_CONFIG_OK=   0x16
    GET_CONFIG_RSP=  0x17
    
    #-----Errors--------#
    BAD_FRAME_ERROR= 0xE0
    CCA_ERROR=       0xE1
    BUSY_ERROR=      0xE2
    
    frame_names = ["<unknown>"] * 256
    frame_names [0:0x05] = ["CUSTOM_DATA", "SET_PORTA", "GET_PORTA", "GET_ADC", "DISCOVER" ]
    frame_names [0x06:0x08] = ["SET_CONFIG", "GET_CONFIG" ]
    frame_names [0x12:0x18] = ["GET_PORTA_RSP", "GET_ADC_RSP", "DISCOVER_RSP", "ACK_RSP", "SET_CONFIG_OK", "GET_CONFIG_RSP" ]
    frame_names [0xE0:0xE3] = ["BAD_FRAME_ERROR", "CCA_ERROR", "BUSY_ERROR"]
    
#===============================================================================
# Peri-App frame class
#===============================================================================    
class PAPP_frame (object):
    START_FRAME =    0xF4
    BROADCAST_ADDR = 0xFFFF   
    SELF_ADDR =      0x0000
    HEADER_SIZE=     4          ## Start frame(1) + address(2) + len(1)     
    
    def __init__(self, st_frame=START_FRAME, addr=0, flen=0, data_cmd=0, data=""):
        self._st_frame = st_frame
        self._addr = addr
        self._flen = flen
        self._data_cmd= data_cmd
        self._data = data

    def __str__(self):
        ret = "Start Frame (0x%02X)\n" % self.st_frame
        ret += "Address: 0x%04X\n" % self.addr
        ret += "Data len: %i\n" % self.flen        
        ret += "Data Type: (%s)\n" %  PAPP_frame_cmd.frame_names[self.data_cmd] 
        if (len(self.data) > 0):
            ret += "data: 0x"
            ret += self.data.encode('hex')
            ret += '\n'
               
        ret += "Checksum: 0x%02X" % self.checksum
        return ret

    @property
    def st_frame(self):
        return self._st_frame
    
    @st_frame.setter
    def st_frame(self, value):
        self._st_frame = value

    @property
    def size(self):
        return self._flen + self.HEADER_SIZE
    
    @size.setter
    def size(self, value):
        pass
    
    @property
    def flen(self):
        return self._flen
    
    @flen.setter
    def flen(self, value):
        self._flen = value
        
    @property
    def addr(self):
        return self._addr
    
    @addr.setter
    def addr(self, value):
        self._addr = value
    
    @property
    def data_cmd(self):
        return self._data_cmd
    
    @data_cmd.setter
    def data_cmd(self, value):
        self._data_cmd= value    
        
    @property
    def checksum(self):
        return self.generateChecksum()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        
    #===========================================================================
    # Method to generate the frame checksum 
    #===========================================================================
    def generateChecksum(self):
        checksum = 0;
        frame = pack("<BHBB",
                     self.st_frame,
                     self.addr,
                     self.flen,
                     self.data_cmd)
        frame+= self.data

        for byte in frame:
            checksum += ord(byte)
            
        checksum&=0xFF
        checksum^=0xFF
        checksum+=1
        return checksum 

        return (checksum & 0x000000FF)
    #===========================================================================
    # Method to write the frame 
    #===========================================================================
    def WritePAPPFrame(self, write):
        
        frame = pack("<BHBB",
                     self.st_frame,
                     self.addr,
                     self.flen,
                     self.data_cmd)
        frame+= self.data
        frame += pack("B", self.checksum)
        
        write(frame)
        
#===========================================================================
# Method to read a PAPP frame 
#===========================================================================
def ReadPAPPFrame(read, timeout=5):
    start_time=time.time()                  ## Initial time
    start_frame_found =False
    
    ## Looking for the start frame   
    while not start_frame_found and ((time.time()-start_time)<timeout):
        byte=read()               
        if (byte and (ord(byte)==PAPP_frame.START_FRAME)):
            start_frame_found= True
                
    if start_frame_found:
        addr=read(2)
        flen=read()
        data_cmd=read()
        data=read(ord(flen)-1)        
        chsum=read()        
        frame=addr+flen+data_cmd+data
        
        ## Create object
        my_PAPP_frame=PAPP_frame()
        my_PAPP_frame.addr,  my_PAPP_frame.flen, my_PAPP_frame.data_cmd, my_PAPP_frame.data= unpack('<HBB%ds' % (ord(flen)-1) , frame)
        
        ## Validate checksum
        if ord(chsum)==my_PAPP_frame.checksum:
            return my_PAPP_frame
        
    return None

            
            
            
        
        
        
        
     
