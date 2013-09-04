from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def moveMonthViewBy(self, p_num):
		#
		# Switches to month view, then moves 'p_num' months in the future or past (if the p_num is 
		# positive or negative) relative to today.
		#
		self.UTILS.logResult("info","<b>Adjusting month view by %s months ...</b>" % p_num)
 		self.setView("month")
 		self.setView("today")
 		
 		if p_num == 0:
 			return
 		
 		#
 		# Set the y-coordinate offset, depending on which
 		# direction we need to flick the display.
 		#
 		numMoves = p_num
 		x2 = 0
 		if numMoves > 0:
 			el_num 	= -1
 			x2 		= -500
 		if numMoves < 0:
 			el_num 	= 0
 			x2 		= 500
 			numMoves = numMoves * -1

 		_now   = time.localtime(int(time.time()))
 		_month = _now.tm_mon
 		_year  = _now.tm_year
 			
 		for i in range (0,numMoves):
 			#
 			# Flick the display to show the date we're aiming for.
 			#
 			_el = self.marionette.find_elements(*DOM.Calendar.mview_first_row_for_flick)[el_num]
 			self.actions.flick(_el,0,0,x2,0).perform()
 			
 			#
 			# Increment the month and year so we keep track of what's expected.
 			#
 			if p_num < 0:
 				_month = _month -1
			else:
				_month = _month + 1
				
			if _month <= 0:
				_month = 12
				_year  = _year - 1
			elif _month >= 13:
				_month = 1
				_year  = _year + 1
 
 		time.sleep(0.3)
 
 		#
 		# Work out what the header should now be.
 		#
 		_month_names = ["January", "February", "March"    , "April"  , "May"     , "June",
						"July"   , "August"  , "September", "October", "November", "December"]
 		
 		_expect = "%s %s" % (_month_names[_month-1], _year)
 		_actual = self.UTILS.getElement(DOM.Calendar.current_view_header, "Header").text
 		
 		self.UTILS.TEST(_expect.lower() in _actual.lower(), "Expecting header to contain '%s' (it was '%s')" % (_expect, _actual))
		
		
