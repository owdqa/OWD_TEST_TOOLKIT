
import sys
sys.path.insert(1, "./")
import os
import base64
from marionette import HTMLElement
# from pil_engine import Engine as pil_Engine
# from perceptualdiff_engine import Engine as diff_Engine


class visualtests(object):

    def __init__(self, parent):
        self.parent = parent
        if not self.parent.general.get_config_variable('enabled', 'visualtest'):
            return

        self.parent.reporting.info("[Visual tests] Using visualtest")
        self.marionette = parent.marionette
        engine_type = self.parent.general.get_config_variable('engine', 'visualtest')
        self.engine = diff_Engine() if engine_type == 'perceptualdiff' else pil_Engine()
        self.save_baseline = self.parent.general.get_config_variable('save_baseline', 'visualtest')
        # This directory should be permanent
        self.baseline_dir = self.parent.general.get_config_variable('baseline_dir', 'visualtest')
        # This directory could be temporary
        self.cmp_dir = self.parent.general.get_config_variable('cmp_dir', 'visualtest')

        if not os.path.exists(self.baseline_dir):
            os.makedirs(self.baseline_dir)
        if not self.save_baseline:
            if not os.path.exists(self.cmp_dir):
                os.makedirs(self.cmp_dir)

    def take_screenshot(self, element_or_locator):
        """
        Takes a screenshot of a certain HTMLElement, given the element itself or the locator.
        The screen capture is returned as a lossless PNG image encoded as a base 64 string by default.
        :param element_or_selector:
            Either a selector as a tuple (selector_type, selector) or a :py:class:`~marionette.HTMLElement` 
            object that represents the element to capture.

        """
        self.parent.reporting.info("[Visual tests] Taking screenshot")

        element = element_or_locator if isinstance(
            element_or_locator, HTMLElement) else self.marionette.find_element(*element_or_locator)

        return self.marionette.screenshot(element=element)

    def save_screenshot_as_png(self, raw_screenshot, output_file):
        """
        Saves the screenshot in the file system as a PNG file
        :param raw_screenshot:
            Lossless PNG image encoded as a base 64 string
        """
        self.parent.reporting.info("[Visual tests] Saving screenshot")
        with open(output_file, 'w') as f:
            f.write(base64.decodestring(raw_screenshot))

    def assertScreenshot(self, element_or_selector, filename, threshold=0):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk, within a given threshold.

        :param element_or_selector:
            Either a selector as a tuple (selector_type, selector) or a :py:class:`~marionette.HTMLElement` 
            object that represents the element to capture.
        :param filename:
            The filename for the screenshot, which will be appended with ``.png``.
        :param file_suffix:
            A string to be appended to the output filename.
        :param threshold:
            The threshold for triggering a test failure.
        """
        if not self.parent.general.get_config_variable('enabled', 'visualtest'):
            return

        # Determine whether we should save the baseline image
        baseline_file = os.path.join(self.baseline_dir, '{}.png'.format(filename))
        if self.save_baseline or not os.path.exists(baseline_file):
            # Save the baseline screenshot and bail out
            self.save_screenshot_as_png(self.take_screenshot(element_or_locator), baseline_file)
            self.parent.reporting.info(
                "[Visual tests] Visual screenshot '{}' saved in baseline folder '{}'".format(filename, self.baseline_dir))
        else:
            self.parent.reporting.info("[Visual tests] Ready to compare screenshots")
            prefix = datetime.now().strftime("%y-%m-%d_%H%M%S")
            unique_name = "{}_{}".format(prefix, filename)
            compare_file = os.path.join(self.cmp_dir, unique_name)

            # Save the new screenshot
            self.save_screenshot_as_png(self.take_screenshot(element_or_locator), compare_file)

            # Compare the screenshots
            self.engine.assertSameFiles(compare_file, baseline_file, threshold)
