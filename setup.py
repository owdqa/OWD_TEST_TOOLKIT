from distutils.core import setup
setup(name='OWD_TEST_TOOLKIT',
      version='1.0',
      url='https://github.com/owdqa/OWD_TEST_TOOLKIT.git',
      author='Telefonica PDI',
      author_email='fjcs@tid.es',
      packages=['OWDTestToolkit',
                'OWDTestToolkit/DOM',
                'OWDTestToolkit/apps',
                'OWDTestToolkit/utils']
      )
