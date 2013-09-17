from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

	def launchFromGroup(self, p_appName):
		#
		# Function to launch an app directly from an EME group.
		#
		x = self.UTILS.getElement( ("xpath", "//li[@data-name='%s']" % p_appName), "Icon for app '%s'" % p_appName, False)
		try:
			x.tap()
		except:
			#
			# App is not visible, so I need to move it into view first.
			#
			_id = x.get_attribute("id")
			self.marionette.execute_script("document.getElementById('%s').scrollIntoView();" % _id)
			x.tap()
		
		time.sleep(1)
		self.UTILS.waitForNotElements(DOM.EME.launched_activity_bar, "Activity notifier", True, 30)

		x = self.UTILS.screenShotOnErr()
		self.UTILS.logResult("info", "Screenshot of app running:", x)