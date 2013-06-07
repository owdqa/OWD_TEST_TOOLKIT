from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def addFileToDevice(self, p_file, count=1, destination=''):
        #
        # Put a file onto the device (path is relative to the dir
        # you are physically in when running the tests).
        #
        self.parent.device.push_file(p_file, count, '/'.join(['sdcard', destination]))

    
