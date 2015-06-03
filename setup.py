from distutils.core import setup

from distutils import cmd
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build

import msgfmt
import os
import site


class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'OWDTestToolkit/locale')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = path.split('/')[-1]
                    src = os.path.join(path, f)
                    dist_dir = site.getsitepackages()[0]
                    dest_path = os.path.join(dist_dir, 'OWDTestToolkit/locale', lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'default.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print '*** Compiling {}'.format(src)
                        msgfmt.make(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print '*** Compiling {}'.format(src)
                            msgfmt.make(src, dest)


class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]

    def run(self):
        _build.run(self)


class install_data(_install_data):

    def run(self):
        print "**** locale listing: {}".format(os.listdir('OWDTestToolkit/locale'))
        for lang in os.listdir('OWDTestToolkit/locale'):
            print "**** install_data run LANG {}".format(lang)
            lang_dir = os.path.join('', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('', 'locale', lang, 'LC_MESSAGES', 'default.mo')
            self.data_files.append((lang_dir, [lang_file]))
        _install_data.run(self)

cmdclass = {
    'build': build,
    'build_trans': build_trans
#    'install_data': install_data,
}

setup(name='OWD_TEST_TOOLKIT',
      version='1.0',
      url='https://github.com/owdqa/OWD_TEST_TOOLKIT.git',
      author='Telefonica PDI',
      author_email='fjcs@tid.es',
      packages=['OWDTestToolkit',
                'OWDTestToolkit/DOM',
                'OWDTestToolkit/apps',
                'OWDTestToolkit/utils',
                'OWDTestToolkit/utils/engines'],
      cmdclass=cmdclass
      )
