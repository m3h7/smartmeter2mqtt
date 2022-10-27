# -*- coding: utf-8 -*-
import setuptools
import os
import re
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='smartmeter2mqtt',
    version=find_version('sm2mqtt', '__init__.py'),
    description='Smartmeter data  to MQTT',
    author='mahiso',
    author_email='karel.blavka@hardwario.com',
    url='https://github.com/m3h7/smartmeter2mqtt',
    include_package_data=True,
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read('requirements.txt'),
    license='MIT',
    keywords=['mqtt', 'smartmeter', 'obis'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Environment :: Console'
    ],
    platforms='any',
    entry_points='''
        [console_scripts]
        smartmeter2mqtt=sm2mqtt.cli:main
    '''
)
