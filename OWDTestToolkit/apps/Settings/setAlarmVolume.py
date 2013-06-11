from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setAlarmVolume(self, p_vol):
        #
        # Set the volume for alarms.
        #
        self.data_layer.set_setting('audio.volume.alarm', p_vol)
        
