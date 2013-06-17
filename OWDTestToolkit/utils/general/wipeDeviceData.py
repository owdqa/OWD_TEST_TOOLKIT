from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def wipeDeviceData(self):
        #
        # Clean all data from the device (reboots the device).
        #
        self.logResult("info", "wipeDeviceData: This is a BAD idea at the moment - ignoring request!")
        return
        self.device.stop_b2g()
        self.device.manager.removeDir('/data/local/indexedDB')
        self.device.manager.removeDir('/data/b2g/mozilla')
        self.device.start_b2g()

