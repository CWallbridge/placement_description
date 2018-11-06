 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
import os
from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='placement_description',
      version='0.1.0',
      license='ISC',
      description='Tool for generating natural language descriptions.',
      long_description=readme(),
      url='https://github.com/CWallbridge/placement_description',
      author='Christopher D. Wallbridge',
      author_email='chris.wallbridge@googlemail.com',
      maintainer='Christopher D. Wallbridge',
      maintainer_email='chris.wallbridge@googlemail.com',
      #package_dir = {'src'},
      packages=['placement_description'],
      install_requires=["numpy","underworlds","enchant"]
)
