from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkAlarmPreview(self, p_hour, p_min, p_ampm, p_label, p_repeat):
        #
        # Verify the alarm details in the clock screen.
        #

        #
        # Put the time in a format we can compare easily with.
        #
        p_time = str(p_hour) + ":" + str(p_min).zfill(2)
        
        alarms = self.UTILS.getElements(DOM.Clock.alarm_preview_alarms, "Alarm preview list")
        
        foundBool = False
        for alarm in alarms:
            alarm_time   = alarm.find_element(*DOM.Clock.alarm_preview_time).text
            alarm_ampm   = alarm.find_element(*DOM.Clock.alarm_preview_ampm).text
            alarm_label  = alarm.find_element(*DOM.Clock.alarm_preview_label).text
            alarm_repeat = alarm.find_element(*DOM.Clock.alarm_preview_repeat).text
            
            if  p_time      == alarm_time   and \
                p_ampm      == alarm_ampm:
                    foundBool = True
                    self.UTILS.TEST(p_label == alarm_label, 
                                    "Alarm description is correct in Clock screen preview.")
                    break
                
        self.UTILS.TEST(foundBool, 
                        "Alarm preview is found in Clock screen for " + p_time + p_ampm + ".")
             
             
