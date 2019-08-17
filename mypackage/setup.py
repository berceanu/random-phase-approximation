from setuptools import setup

setup(
   name='MyPackage',
   version='0.1.0',
   author='Andrei Berceanu',
   author_email='andrei.berceanu@eli-np.ro',
   packages=['mypackage'],
   package_dir={'mypackage': 'mypackage'},
   package_data={'mypackage': ['talys/database/structure/gamma/hfb/*.psf']},
   license='LICENSE.txt',
   description='An awesome package that does something',
   long_description=open('README.txt').read(),
)
