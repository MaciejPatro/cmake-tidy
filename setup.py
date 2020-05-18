from pip.req import parse_requirements
from setuptools import setup, find_packages

from cmake_tidy.version import VERSION

install_requirements = parse_requirements('./requirements.txt', session=False)
install_requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='cmake-tidy',
    version=VERSION,
    python_requires='>=3.6.0',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    url='https://github.com/MaciejPatro/cmake-tidy',
    license=open('LICENSE').read(),
    author='Maciej Patro',
    author_email='maciejpatro@gmail.com',
    description='cmake-tidy is a tool to format/ analyze cmake source files.',
    long_description=open('README.adoc').read(),
    long_description_content_type='text/markdown',
    package_data={
        '': ['*.json', '*.adoc', '*.txt']
    },
)
