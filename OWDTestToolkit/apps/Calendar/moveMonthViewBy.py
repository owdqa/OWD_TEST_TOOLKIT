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
 			el = -1
 			x2 = -500
 		if numMoves < 0:
 			el = 0
 			x2 = 500
 			numMoves = numMoves * -1
 		
 		for i in range (0,numMoves):
 			# Flick the display to show the date we're aiming for.
 			_el = self.UTILS.getElements(DOM.Calendar.mview_first_row_for_flick, "First row of dates")[el]
 			self.actions.flick(_el,0,0,x2,0).perform()
 
 		time.sleep(0.3)
 
 		#
 		# Work out what the header should now be.
 		#
		x = self.UTILS.getDateTimeAdjusted(p_months=p_num)
		_expect = x.month_name.lower() + " " + str(x.year).lower()
		_actual = self.UTILS.getElement(DOM.Calendar.current_view_header, "Header").text.lower()
		
		self.UTILS.TEST(_expect in _actual, "Expecting header to contain '%s' (it was '%s')" % (_expect, _actual))
		
		
