import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name='stocktalk',
    version='v2.5',
    author='Anthony Federico',
    author_email='dephoona@gmail.com',
    description='Data collection toolkit for social media analytics',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/maxzzze/Stocktalk',
    zip_safe=False,
    packages=find_packages('stocktalk'),
    install_requires=[
        'pytz',
        'bokeh>=0.12.4',
        'nltk>=3.2.2',
        'tornado>=4.4.2',
        'tweepy>=3.5.0',
        'twython>=3.4.0',
        'configargparse',
        'elasticsearch'
    ]
)
