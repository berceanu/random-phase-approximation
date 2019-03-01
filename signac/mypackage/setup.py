from setuptools import setup

setup(
   name='MyPackage',
   version='0.1.0',
   author='Andrei Berceanu',
   author_email='andrei.berceanu@eli-np.ro',
   packages=['mypackage'],
#    scripts=['bin/script1','bin/script2'],
#    url='http://pypi.python.org/pypi/PackageName/',
   license='LICENSE.txt',
   description='An awesome package that does something',
   long_description=open('README.txt').read(),
   install_requires=[
       "signac >= 0.9.4",
       "signac-flow >= 0.6.4",
       "signac-dashboard >= 0.1.6",
   ],
)
