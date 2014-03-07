from distutils.core import setup
setup(name='OWD_TEST_TOOLKIT',
      version='1.0',
      url='https://github.com/owdqa/OWD_TEST_TOOLKIT.git',
      author='Telefonica PDI',
      author_email='fjcs@tid.es',
      packages=['OWDTestToolkit',
                'OWDTestToolkit/DOM',
                'OWDTestToolkit/apps',
                'OWDTestToolkit/apps/Clock',
                'OWDTestToolkit/apps/Settings',
                'OWDTestToolkit/apps/Messages',
                'OWDTestToolkit/apps/Contacts',
                'OWDTestToolkit/utils',
                'OWDTestToolkit/utils/app',
                'OWDTestToolkit/utils/debug',
                'OWDTestToolkit/utils/date_and_time',
                'OWDTestToolkit/utils/element',
                'OWDTestToolkit/utils/general',
                'OWDTestToolkit/utils/home',
                'OWDTestToolkit/utils/iframe',
                'OWDTestToolkit/utils/network',
                'OWDTestToolkit/utils/reporting',
                'OWDTestToolkit/utils/statusbar',
                'OWDTestToolkit/utils/test']
      )
