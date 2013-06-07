from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createEvent(self, p_title, p_location, p_allDay, p_startDate, p_startTime, p_endDate, p_endTime, p_notes):
        #
        # Create a new event - use 'False' in the following fields if you want to leave them at default:
        # 
        #   start date,
        #   end date,
        #   location,
        #   notes
        #
        self.addEvent()
        
        #
        # Set the title.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_title, "'Title' field")
        x.send_keys(p_title)

        #
        # Set the location.
        #
        if p_location:
            x = self.UTILS.getElement(DOM.Calendar.event_location, "'Location' field")
            x.send_keys(p_location)

        #
        # Set the 'all day' marker.
        #
        if p_allDay:
            x = self.UTILS.getElement(DOM.Calendar.event_allDay, "All day marker")
            x.tap()

        #
        # Set start date.
        #
        if p_startDate: 
            x = self.UTILS.getElement(DOM.Calendar.event_start_date, "'Start date' field")
            x.send_keys(p_startDate)
        
        #
        # Start start time.
        #
        self.UTILS.logResult("info", "ROY: Time settings have changed to a scroller - make Clock scroller functionality available to this!!")
        return
        x = self.UTILS.getElement( ("id", "start-time-locale"), "Start time field")
        x.tap()

        self.UTILS.setScrollerVal("hours", 5)
        self.UTILS.setScrollerVal("minutes", 01)
        scroller = self.UTILS.getElement(DOM.Clock.time_picker_ampm, "AM/PM picker")
        currVal  = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
        
        if t_ampm != currVal:
            if currVal == "AM":
                self.UTILS.moveScroller(scroller, True)
            else:
                self.UTILS.moveScroller(scroller, False)

        self.UTILS.screenShotOnErr()
        
        return
        x.send_keys(p_startTime)
        
        #
        # Set end date.
        #
        if p_endDate: 
            x = self.UTILS.getElement(DOM.Calendar.event_end_date, "'End date' field")
            x.send_keys(p_endDate)
        
        #
        # Set end time.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_end_time, "'End time' field")
        x.send_keys(p_endTime)
        
        #
        # Set notes.
        #
        if p_notes: 
            x = self.UTILS.getElement(DOM.Calendar.event_notes, "'Notes' field")
            x.send_keys(p_notes)
        
        #
        # Save it.
        #
        x = self.UTILS.getElement(DOM.Calendar.event_save_btn, "Save button")
        x.tap()
        
