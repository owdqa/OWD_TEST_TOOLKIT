from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

	def changeDay(self, p_numDays, p_viewType):
		#
		# Changes the calendar day to a different day relative to 'today' - <b>uses the
		# month view to do this, then switches back to whichever
		# view you want (month, week, day)</b>.<br>
		# <b>p_numDays</b> is a number (can be negative to go back, i.e. -5,-2,1,3,5 etc...).<br>
		# <b>p_viewType</b> is the calendar view to return to (today / day / week / month)<br> 
		# Returns a modified DateTime object from <i>UTILS.getDateTimeFromEpochSecs()</i>.
		#
		self.actions	= Actions(self.marionette)
		
# 		_days	  = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# 		_month_end = [31,28,31,30,31,30,31,31,30,31,30,31]
		_now_secs  = time.time()
		_now_diff  = int(_now_secs) + (86400*p_numDays)
#		 _today	 = self.UTILS.getDateTimeFromEpochSecs(_now_secs)
		_new_today = self.UTILS.getDateTimeFromEpochSecs(_now_diff)
					
		#
		# Switch to month view and tap this day, then switch back to our view.
		#
		self.moveMonthViewBy(p_numDays)
			
		el_id_str = "d-%s-%s-%s" % (_new_today.year, _new_today.mon-1, _new_today.mday)
		x = self.UTILS.getElement( ("xpath", 
									"//li[@data-date='%s']" % el_id_str),
								  "Cell for day %s/%s/%s" % (_new_today.mday, _new_today.mon, _new_today.year))
		x.tap()
		self.setView(p_viewType.lower())

		
		return _new_today
