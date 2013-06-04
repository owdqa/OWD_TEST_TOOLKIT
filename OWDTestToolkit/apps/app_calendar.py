import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppCalendar(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS


    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Calendar')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Calendar app - loading overlay");

    def addEvent(self):
        #
        # Press the 'add event' button.
        #
        x = self.UTILS.getElement(DOM.Calendar.add_event_btn, "Add event button")
        x.tap()
        
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

        self._select("hours", 5)
        self._select("minutes", 01)
        scroller = self.UTILS.getElement(DOM.Clock.time_picker_ampm, "AM/PM picker")
        currVal  = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
        
        if t_ampm != currVal:
            if currVal == "AM":
                self._scrollForward(scroller)
            else:
                self._scrollBackward(scroller)

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
        
    def setView(self, p_type):
        #
        # Set to view type (day / week / month).
        #
        x = self.UTILS.getElement((DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % p_type),
                                  "'" + p_type + "' view type selector")
        x.tap()
        
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
                    














    def _calcStep(self, p_scroller):
        #
        # Calculates how big the step should be
        # when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment
        # the scroller by 1 element.
        #
        x = float(len(p_scroller.find_elements("class name", "picker-unit")))
        
        #
        # This is a little formula I worked out - seems to work, but I've only 
        # tested it on the scrollers on my Ungai.
        #
        x = 1 - ((1/((x/100)*0.8))/100)
        
        return x
        
        
    def _scrollForward(self, p_scroller):
        #
        # Move the scroller forward one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start * x

        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)
#         actions = Actions(self.marionette)
#         actions.press(p_scroller, x_pos, y_start).move_by_offset(x_pos, y_end).release()
#         actions.perform()


        time.sleep(0.5)
        
    def _scrollBackward(self, p_scroller):
        #
        # Move the scroller back one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start / x
        
        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)

        time.sleep(0.5)
        
    def _select(self, p_component, p_number):
        #
        # Set the time using the scroller.
        #        
        scroller = self.UTILS.getElement(
            (DOM.Clock.time_picker_column[0],DOM.Clock.time_picker_column[1] % p_component),
            "Scroller '" + p_component + "'")
        
        #
        # Get the current setting for this scroller.
        #
        currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
        
        #
        # Now flick the scroller as many times as required 
        # (the current value might be padded with 0's so check for that match too).
        #
        while str(p_number) != currVal and str(p_number).zfill(2) != currVal:
            # Do we need to go forwards or backwards?
            if p_number > int(currVal):
                self._scrollForward(scroller)
            if p_number < int(currVal):
                self._scrollBackward(scroller)
                
            # Get the new 'currVal'.
            currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
                






