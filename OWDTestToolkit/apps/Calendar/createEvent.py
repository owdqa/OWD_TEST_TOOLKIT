from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createEvent(self):
        #
        # Create a new event - use 'False' in the following fields if you want to leave them at default:
        # 
        #   start date,
        #   end date,
        #   location,
        #   notes
        #
		x = self.UTILS.getElement(DOM.Calendar.add_event_btn, "Add event button")
		x.tap()
		
		title			= ("xpath"	, "//input[@name='title']")
		where			= ("xpath"	, "//input[@name='location']")
		allday			= ("xpath"	, "//li[@class='allday']")		#<-- checkbox, True False (use tap())
		start_date		= ("xpath"	, "//li[@class='start-date']")
		start_time		= ("id"		, "start-time-locale")
		end_date		= ("id"		, "end-date-locale")
		end_time		= ("id"		, "end-time-locale")
		reminders 		= ("xpath"	, "//select[@name='alarm[]']/option") # *
		notes			= ("xpath"	, "//textarea[@name='description']")

		x = self.UTILS.getElement(title		, "Title", True, 10)
		x.send_keys("hello title")
		
		x = self.UTILS.getElement(where		, "Where")
		x.send_keys("hello where")
		
  		x = self.UTILS.getElement(allday	, "All day")
  		x.tap()
  		
  		self.marionette.execute_script("document.getElementById('start-date-locale').click()")
#  		x = self.UTILS.getElement(start_date	, "sdate", False)
#  		x.tap()

# 		self.UTILS.typeThis(start_time	, "stime", "Hello stime", p_no_keyboard=False, p_validate=False)
# 		self.UTILS.typeThis(end_date	, "edate", "Hello edate", p_no_keyboard=False, p_validate=False)
# 		self.UTILS.typeThis(end_time	, "etime", "Hello etime", p_no_keyboard=False, p_validate=False)
# 		self.UTILS.getElements(reminders, "y", True, 1, False)
# 		self.UTILS.typeThis(notes		, "Notes", "Hello notes", p_no_keyboard=False, p_validate=False)
		
		
		# * - [ARRAY] available options are in the @value attribute. tap() the select, then tap() the option.
