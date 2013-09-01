"""

blink1_pyusb.py -- blink(1) Python library using PyUSB

Uses "PyUSB 1.0" to do direct USB HID commands

See: https://github.com/walac/pyusb

Linux (Ubuntu/Debian):
 % sudo apt-get install pip
 % sudo pip install pyusb
 Note: will give "not claimed" error or similar.  Try blink1.py instead

Mac OS X:
 do "brew install libusb" on osx 
 or "port install py26-pyusb-devel" on osx

Windows:
 libusb-win32 (inf method) on windows?

Based on blink1hid-demo.py by Aaron Blondeau

2013, Tod E. Kurt, http://thingm.com/

"""

import usb 
import time
import string


report_id = 0x01
debug_rw = False

class Blink1:

    def __init__(self):
        return self.find()
    
    def find(self):
        self.dev = usb.core.find(idVendor=0x27b8, idProduct=0x01ed)
        if( self.dev == None ): 
            return None

        #print "kernel_driver_active: %i" % (self.dev.is_kernel_driver_active(0))
        if( self.dev.is_kernel_driver_active(0) ):
            try:
                self.dev.detach_kernel_driver(0)
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver: %s" % str(e))
        #self.dev.set_configuration()
            
    def notfound(self):
        return None  # fixme what to do here

    """
    Write command to blink(1)
    Send USB Feature Report 0x01 to blink(1) with 8-byte payload
    Note: arg 'buf' must be 8 bytes or bad things happen
    """
    def write(self,buf):
        if debug_rw : print "blink1write: " + ",".join( '0x%02x' % v for v in buf )
        if( self.dev == None ): return self.notfound()
        bmRequestTypeOut = usb.util.build_request_type(usb.util.CTRL_OUT, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)
        self.dev.ctrl_transfer( bmRequestTypeOut, 
                                0x09,    # == HID set_report
                                (3 << 8) | report_id,  # (3==HID feat.report)
                                0, 
                                buf) 
        
    """
    Read command result from blink(1)
    Receive USB Feature Report 0x01 from blink(1) with 8-byte payload
    Note: buf must be 8 bytes or bad things happen
    """
    def read(self):
        bmRequestTypeIn = usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)
        buf = self.dev.ctrl_transfer( bmRequestTypeIn, 
                                      0x01,  # == HID get_report
                                      (3 << 8) | report_id, 
                                      0, 
                                      8 )    # == number of bytes to read
        if debug_rw : print "blink1read:  " + ",".join( '0x%02x' % v for v in buf )
        return buf

    """
    Command blink(1) to fade to RGB color

    """
    def fade_to_rgbn(self, fadeMillis, red,green,blue, ledn):
        action = ord('c')
        fadeMillis = fadeMillis/10
        th = (fadeMillis & 0xff00) >> 8
        tl = fadeMillis & 0x00ff
        buf = [report_id, action, red,green,blue, th,tl, ledn]
        return self.write(buf)

    """
    Command blink(1) to fade to RGB color

    """
    def fade_to_rgb(self, fadeMillis, red,green,blue):
        return self.fade_to_rgbn(fadeMillis, red,green,blue,0)

    """
    """
    def playloop(self, play,startpos,endpos,count):
        buf = [0x01, ord('p'), play, startpos, endpos, count, 0,0 ]
        return self.write(buf)

    """
    """
    def play(self, play,startpos):
        return self.playloop( play, startpos, 0,0)

    """
    Get blink(1) firmware version

    """
    def get_version(self):
        if( self.dev == None ): return ''
        action = ord('v') # 0x76 # ='v' (version)
        buf = [0x01, action, 0,0, 0,0,0,0]
        self.write(buf)
        time.sleep(.05)
        #bmRequestTypeIn = usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)
        #version_raw = self.dev.ctrl_transfer(bmRequestTypeIn, 0x01, (3 << 8) | 0x01, 0, 8)
        version_raw = self.read()
        version = (version_raw[3]-ord('0'))*100 + (version_raw[4]-ord('0'))
        return str(version)






