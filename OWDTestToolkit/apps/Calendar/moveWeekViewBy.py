from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def moveWeekViewBy(self, p_num):
		#
		# Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is 
		# positive or negative) relative to today.
		#
		self.UTILS.logResult("info","<b>Adjusting month view by %s months ...</b>" % p_num)
 		self.setView("week")
 		self.setView("today")
 		
 		if p_num == 0:
 			return
 		
 		#
 		# Set the y-coordinate offset, depending on which
 		# direction we need to flick the display.
 		#
 		numMoves = p_num
 		y2 = 0
 		if numMoves > 0:
 			el = -1
 			y2 = -500
 		if numMoves < 0:
 			el = 0
 			y2 = 500
 			numMoves = numMoves * -1
 		
 		#
 		# Keep track of how many days we're adjusting the display by (so we can check
 		# we're looking at the correct display at the end).
 		#
 		_days_offset = 0
 		_now         = self.UTILS.getDateTimeFromEpochSecs(int(time.time()))
 		_now_str	 = "%s %s %02d %s" % (_now.day_name[:3], _now.month_name[:3], _now.mday, _now.year)

		x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
		for i in range(0,len(x)):
			if _now_str in x[i].get_attribute("data-date"):
				_startpos = i+1
				break
		if numMoves < 0:
			_days_offset = _startpos
		else:
			_days_offset = len(x) - _startpos

 		self.UTILS.logResult("info", "(%s vs %s) X: '%s'" % (_startpos, len(x), _days_offset))
 		return
		
 		
 		for i in range (0,numMoves):
			x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
			
			#
			# Get the count of days we're adjusting (so we can check later).
			#
			_days_offset = _days_offset + len(x)
				
			#
			# Flick the screen to move it.
			#
 			self.actions.flick(x[el],0,0,y2,0).perform()
 			
 		time.sleep(0.3)
 
 		#
 		# Work out what the display should now be.
 		# header shoudl be month + year, now + _days_offset shoudl be in active days.
 		x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
 
