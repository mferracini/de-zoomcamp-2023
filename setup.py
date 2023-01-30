#!/usr/bin/env python

from distutils.core import setup

setup(name='src',
      version='0.0.1',
      description='Package utilities',
      author='Mateus Ferracini',
      author_email='mat.ferracini@gmail.com',
      packages=['src'],
      package_dir={'src': 'src'},
      package_data={'src': ['elt/queries/*.sql']},
     )
