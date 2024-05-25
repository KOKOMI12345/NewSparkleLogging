from setuptools import setup, find_packages
from SparkleLogging import __version__

setup(
    name='SparkleLogging-new',
    version=__version__,
    packages=find_packages(),
    author='花火official',
    author_email='3072252442@qq.com',
    description='A logging library for Python',
    long_description=open('Readme.md','r',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KOKOMI12345/NewSparkleLogging',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
