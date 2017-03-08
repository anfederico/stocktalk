from distutils.core import setup

setup(name='stocktalk',
      version='v2.5',
      description='Data collection toolkit for social media analytics',
      author='Anthony Federico',
      author_email='dephoona@gmail.com',
      url='https://github.com/anfederico/Stocktalk',
      packages=['stocktalk'],
      scripts=['bin/stocktalk-corpus']
     )