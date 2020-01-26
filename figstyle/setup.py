from setuptools import setup

setup(
    name="figstyle",
    version="0.1.0",
    author="Andrei Berceanu",
    author_email="andrei.berceanu@eli-np.ro",
    packages=["figstyle"],
    package_dir={"figstyle": "figstyle"},
    package_data={"figstyle": ["data/*.mplstyle"]},
    license="LICENSE.txt",
    description="An awesome package that does something",
    long_description=open("README.txt").read(),
)
