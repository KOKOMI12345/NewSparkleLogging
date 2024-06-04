from setuptools import setup, find_packages
from NsparkleLog import __version__ , __author__ , __packageName__

def load_requirements(filepath: str = "requirements.txt") -> list[str]:
    try:
       with open(filepath, 'r') as f:
           return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        return []

setup(
    name=__packageName__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email='3072252442@qq.com',
    description='A useful logging library for Python',
    long_description=open('Readme.md','r',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KOKOMI12345/NewSparkleLogging',
    requires=load_requirements(),  # 依赖
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
