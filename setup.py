import os
import sys

from setuptools import setup

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = [
    'httpx>=0.12.0',
    "future>=0.17.1",
    "marshmallow==2.16.3"
]


# Don't import openpay module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openpay'))
from version import VERSION


setup(name='openpay_async',
      python_requires='>=3.6',
      version=VERSION,
      description='Openpay python async bindings',
      author='Openpay',
      author_email='soporte@openpay.mx',
      url='https://www.openpay.mx/',
      packages=['openpay', 'openpay.data'],
      package_data={'openpay': ['data/ca-certificates.crt', '../VERSION']},
      install_requires=install_requires,
      )
