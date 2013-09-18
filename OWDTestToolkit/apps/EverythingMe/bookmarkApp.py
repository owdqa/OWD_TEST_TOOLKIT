from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

	def bookmarkApp(self, p_appName):
		#
		# 'Bookmarks' (installs) an app from EME (assumes everything.me is already running).
		#
		x = self.searchForApp(p_appName)
		if not x:
			#
			# No point going beyond this point.
			#
			return False
		
		x.tap()
		
		self.marionette.switch_to_frame()
		
		self.UTILS.waitForElements(DOM.EME.launched_button_bar, "Button bar", False)
		
		#
		# Wait for the bookmark option to be enabled (can take a few seconds).
		#
		boolOK = False
		for i in range(0,10):
			x = self.marionette.find_element(*DOM.EME.launched_button_bookmark)
			if not x.get_attribute("data-disabled"):
				boolOK = True
				break

			time.sleep(6)
		
		x = self.UTILS.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
		x.tap()
		
		self.UTILS.TEST(boolOK, "Bookmark button is enabled in the button bar.", True)
		
		time.sleep(1)
		
		x = self.UTILS.getElement(DOM.EME.launched_button_bookmark, "Button bar - bookmark button")
		self.UTILS.TEST(not x.get_attribute("data-disabled"), "Bookmark button is enabled.", True)
		x.tap()
		
		self.marionette.switch_to_frame()
		_boolOK = False
		x = self.UTILS.getElements(DOM.EME.launched_add_to_homescreen, "Apps to be added to homescreen")
		for i in x:
			if i.text == p_appName:
				i.tap()
				_boolOK = True
				break
			
		self.UTILS.TEST(_boolOK, "Adding '%s' to homescreen (app selected)." % p_appName)
		
		self.UTILS.switchToFrame(*DOM.EME.add_to_home_screen_frame)
		x = self.UTILS.screenShotOnErr()
		self.UTILS.logResult("info", "Screenshot at this point:", x)
		
		x = self.UTILS.getElement(DOM.EME.add_to_home_screen_btn, "Add to homescreen (button)")
		x.tap()
		
		self.marionette.switch_to_frame()
		x = self.UTILS.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
		x.tap()
		
		x = self.UTILS.getElement(DOM.EME.launched_button_bookmark , "Button bar - bookmark button")
		self.UTILS.TEST(x.get_attribute("data-disabled") == "true", "Bookmark button is now disabled.")
		
		self.UTILS.TEST(self.UTILS.findAppIcon(p_appName), "'%s' is now installed." % p_appName)
		
		x = self.UTILS.screenShotOnErr()
		self.UTILS.logResult("info", "Screenshot of the button bar:", x)
		
		return True
