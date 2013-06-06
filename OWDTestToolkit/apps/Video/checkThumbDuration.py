from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkThumbDuration(self, p_thumb_num, p_length_str_MMSS, p_errorMargin_SS):
        #
        # Check the duration of a video thumbnail.
        #
        durations = self.UTILS.getElements(DOM.Video.thumb_durations,
                                           "Thumbnail durations", True, 20, False)
        
        if not durations:
        	return False
        
        myDur = durations[p_thumb_num].text
        
        #
        # Video length didn't match exactly, but is it within the acceptable error margin?
        #
        from datetime import datetime, timedelta
        
        actual_time = datetime.strptime(myDur, '%M:%S')
        expect_time = datetime.strptime(p_length_str_MMSS, '%M:%S')
        margin_time = timedelta(seconds=p_errorMargin_SS)
        
        diff_time   = actual_time - expect_time
        
        in_errorMargin = False
            
        # Less than expected, but within the error margin?
        if margin_time >= diff_time:
            in_errorMargin = True
            
        self.UTILS.TEST(in_errorMargin, 
            "Expected video length on thumbnail to be %s, +- %s seconds (it was %s seconds)." % 
                (p_length_str_MMSS, p_errorMargin_SS, myDur))

