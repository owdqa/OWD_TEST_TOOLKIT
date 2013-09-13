from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

	def addMultipleGroups(self, p_groupArray=False):
		#
		# Adds multiple groups based on an array of numbers (defaults to all available groups).
		# <br><br>
		# For example: addMultipleGroups([0,1,2,3,8,11]).
		#
		x = self.UTILS.getElement(DOM.EME.add_group_button, "'More' icon")
		x.tap()
		self.UTILS.waitForNotElements(DOM.EME.loading_groups_message, "'Loading' message", True, 120)
		
		#
		# Switch to group selector (in top level iframe).
		#
		self.marionette.switch_to_frame()

		_list_names = [] #(for checking later)
		_list	   = self.UTILS.getElements(DOM.GLOBAL.modal_valueSel_list, "Groups list", False)
			
		for i in range(0,len(_list)):
			
			if i > 0:
				# Keep shuffling the groups into view so they can be tapped.
				self.actions.press(_list[i]).move(_list[i-1]).wait(0.5).release().perform()
				_list = self.marionette.find_elements(*DOM.GLOBAL.modal_valueSel_list)
			
			#
			# Only select it if it's the list, or there is no list.
			#
			_boolDoIt = False
			if p_groupArray:
				if len(p_groupArray) == len(_list_names):
					#
					# We've done all of them - stop looping!
					break
				
				if i in p_groupArray:
					_boolDoIt = True
			else:
				_boolDoIt = True
			
			if _boolDoIt:
				_tmpnam = _list[i].find_element("tag name", "span").text
				self.UTILS.logResult("info", "Selecting '%s' ..." % _tmpnam)
				_list_names.append(_tmpnam)
				_list[i].tap()
			
				#
				# Sometimes the first tap does nothing for some reason.
				#
				if not _list[i].get_attribute("aria-checked"):
					_list[i].tap()
		
		#
		# Click the OK button.
		#
		x = self.UTILS.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button")
		try:
			# Sometimes it's one, sometimes the other ...
			x.tap()
			x.click()
		except:
			pass
		
		time.sleep(1)

		#
		# Checkk all the items we expect are now loaded in evme.
		#
		self.UTILS.switchToFrame(*DOM.Home.frame_locator)
		time.sleep(5)
		for _list_name in _list_names:
			_boolOK = False
			
			# Reload the groups (silently or we'll have loads of these messages!).
			try:
				x = self.marionette.find_elements(*DOM.EME.groups)
			except:
				break
			
			for i in x:
				_group_name = i.get_attribute("data-query")
				if _group_name == _list_name:
					_boolOK = True
					break
				
			self.UTILS.TEST(_boolOK, "'%s' is now among the groups." % _list_name)
		

