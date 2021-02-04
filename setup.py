from io import open
from os import environ, path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, "requirements.in"), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(name='pod-whois',
      version=0.2,
      description='Babashka pod query whois info.',
      author='ntestoc3',
      author_email='ntoooooon@outlook.com',
      url='https://github.com/ntestoc3/pod-whois',
      keywords='babashka pod whois',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",

      include_package_data=True,
      packages=["pod_whois"],
      package_data={
          'pod_whois': ['*'],
      },
      exclude_package_data={
          'pod_whois': ['*.log'],
      },

      entry_points={  # Optional
          'console_scripts': [
              'pod.py-whois=pod_whois.core:main',
         ],
      },

      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      python_requires='>=3.6, <4',
      install_requires=requirements,
)
