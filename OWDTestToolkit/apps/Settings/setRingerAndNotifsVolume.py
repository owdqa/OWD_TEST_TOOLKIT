from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setRingerAndNotifsVolume(self, p_vol):
        #
        # Set the volume for ringer and notifications.
        #
        self.data_layer.set_setting('audio.volume.notification', p_vol)
        
