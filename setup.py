from distutils.core import setup
setup(name='OWD_TEST_TOOLKIT',
      version='1.0',
      url='https://github.com/roydude/owd_smoketests.git',
      author='roy',
      author_email='roy.collings@sogeti.com',
      packages=['OWDTestToolkit',
                'OWDTestToolkit/DOM',
                'OWDTestToolkit/apps',
                'OWDTestToolkit/utils']
      )
