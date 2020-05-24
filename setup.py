import os
import re

from pip.req import parse_requirements
from setuptools import setup, find_packages

install_requirements = parse_requirements('./requirements.txt', session=False)
install_requirements = [str(ir.req) for ir in install_requirements]


def load_version():
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cmake_tidy", "version.py"))
    with open(filename, "rt") as version_file:
        return re.search(r"VERSION = '([0-9a-z.-]+)'", version_file.read()).group(1)


setup(
    name='cmake-tidy',
    version=load_version(),
    python_requires='>=3.6.0',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    url='https://github.com/MaciejPatro/cmake-tidy',
    license='LICENSE',
    author='Maciej Patro',
    author_email='maciejpatro@gmail.com',
    install_requires=install_requirements,
    description='cmake-tidy is a tool to format/analyze cmake source files.',
    long_description='For More information visit https://github.com/MaciejPatro/cmake-tidy',
    long_description_content_type='text/plain',
    package_data={
        '': ['*.json', '*.adoc', '*.txt']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords=['cmake', 'format', 'static-analysis', 'developer', 'tool'],
    entry_points={
        'console_scripts': [
            'cmake-tidy=cmake_tidy.run:run',
        ],
    },
)
