from distutils.core import setup

setup(name='rpmversion',
      version='0.1.0',
      scripts=['rpmversion.py'],
      description='Package versions from YAML.',
      install_requires=['PyYAML'],
)
