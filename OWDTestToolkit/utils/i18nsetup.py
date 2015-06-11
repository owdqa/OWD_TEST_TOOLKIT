import os
import gettext
import site
from marionette_driver.marionette import Marionette


class SingletonType(type):

    def __call__(self, cls):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__()
            return cls.__instance


class I18nSetup(object):
    """Configure gettext function to locate translations.
    """
    __metaclass__ = SingletonType
    configured = False
    _ = None

    def setup(self):
        I18nSetup.locale_path = os.path.join(site.getsitepackages()[0], 'OWDTestToolkit/locale')
        if not I18nSetup.configured:
            marionette = Marionette()
            marionette.start_session()
            # Configure the translation to be used based on the previously retrieved language. Should
            # the translation is not found, the fallback will prevent a failure
            lang = marionette.execute_script("""return window.navigator.language;""")
            translation = gettext.translation('default', I18nSetup.locale_path, languages=[lang], fallback=True)
            I18nSetup._ = translation.ugettext
            I18nSetup.configured = True
        return I18nSetup._
