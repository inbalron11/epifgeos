from setuptools import setup

setup(name='epifgeos',
      version='0.1',
      description='epifgeos package',
      url='http://github.com/storborg/funniest',
      author='Inbal Ronay',
      author_email='inbalron11@gmail.com',
      packages=['epifgeos'],
      install_requires=[
          'osgeo','csv','numpy','sklearn','multiprocessing','itertools','matplotlib','functools',],
      zip_safe=False)
