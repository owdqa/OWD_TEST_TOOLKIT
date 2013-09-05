from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def moveWeekViewBy(self, p_num):
		#
		# Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is 
		# positive or negative) relative to today.
		#
		self.UTILS.logResult("info","<b>Adjusting week view by %s screens ...</b>" % p_num)
 		self.setView("week")
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
 		
 		#
 		# Keep track of how many days we're adjusting the display by (so we can check
 		# we're looking at the correct display at the end).
 		#
 		_days_offset = 0
 		_now_epoch	 = int(time.time())
 		_now         = self.UTILS.getDateTimeFromEpochSecs(_now_epoch)
 		_now_str	 = "%s %s" % (_now.day_name[:3].upper(),_now.mday)

		_displayed_days = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
		_startpos = 0
		for i in range(0,len(_displayed_days)):
			x = _displayed_days[i].text
			if x:
				if _now_str in x:
					_startpos = i - 1
					break
		
		if p_num < 0:
			_days_offset = _startpos
		else:
			_days_offset = len(_displayed_days) - _startpos - 2

 		#
 		# Now move to the desired screen.
 		#
 		for i in range (0,numMoves):
			#
			# Flick the screen to move it.
			#
 			self.actions.flick(_displayed_days[el],0,0,x2,0).perform()
			
			#
			# Get the count of days we're adjusting (so we can check later).
			#
			_displayed_days = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
			_days_offset = _days_offset + len(_displayed_days)
				
 			
 		time.sleep(0.3)
 
 		#
 		# Work out what the display should now be:
 		#
 		# 1. Today + _days_offset should be displayed.
 		# 2. Header should be month + year, now + _days_offset should be in active days.
 		#
 		if p_num < 0:
 			_new_epoch = _now_epoch - (_days_offset * 24 * 60 * 60)
		else:
 			_new_epoch = _now_epoch + (_days_offset * 24 * 60 * 60)
			  
 		_new_now       = self.UTILS.getDateTimeFromEpochSecs(_new_epoch)
 		
 		_new_now_str   = "%s %s" % (_new_now.day_name[:3].upper(), _new_now.mday)

		x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
		boolOK = False
		for i in range(0,len(x)):
			x = _displayed_days[i].text
			if x:
				if _new_now_str in x:
					boolOK = True
					break
 
 		self.UTILS.TEST(boolOK, "The column for date '<b>%s</b>' displayed." % _new_now_str)

		x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Current view header")
		self.UTILS.TEST(_new_now.month_name in x.text, "'<b>%s</b>' is in header ('%s')." % (_new_now.month_name, x.text))
		self.UTILS.TEST(str(_new_now.year) in x.text, "'<b>%s</b>' is in header ('%s')." % (_new_now.year, x.text))

 		x = self.UTILS.screenShotOnErr()
 		self.UTILS.logResult("info", "Week view screen after moving %s pages: " % p_num, x)
