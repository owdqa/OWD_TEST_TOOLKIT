from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def getEventPreview(self, p_view, p_hour24, p_title, p_location=False):
        #
        # Return object for an event in month / week or day view.
        #
        
        #
        # The tag identifiers aren't consistent, so set them here.
        #
        # <type>: (<event preview identifier>, <event title identifier>)
        #
        event_view = {
            "month": (DOM.Calendar.view_events_block_m % p_hour24, DOM.Calendar.view_events_title_month),
            "week" : (DOM.Calendar.view_events_block_w % p_hour24, DOM.Calendar.view_events_title_week),
            "day"  : (DOM.Calendar.view_events_block_d % p_hour24, DOM.Calendar.view_events_title_day)
        }
        
        viewStr = event_view[p_view]
        
        #
        # Switch to the desired view.
        #
        # For the life of me I can't get 'wait_for_element' ... to work in day view, so I'm
        # just waiting a few seconds then checking with .is_displayed() instead.
        #
        self.setView(p_view)
        time.sleep(2)
        
        #
        # Start by getting the parent element objects, which could contain event details.
        #
        event_objects = self.UTILS.getElements(('xpath', viewStr[0]), "'" + p_view + "' event details list", False, 20, False)
        if not event_objects:
            return False
        
        if len(event_objects) <= 0:
            return False

        for event_object in event_objects:
            if p_title in event_object.text:
                return event_object
            
        #
        # If we get to here we failed to return the element we're after.
        #
        return False
                    














