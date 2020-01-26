from setuptools import setup

setup(
    name="dataash5",
    version="0.1.0",
    author="Andrei Berceanu",
    author_email="andrei.berceanu@eli-np.ro",
    packages=["dataash5"],
    package_dir={"dataash5": "dataash5"},
    package_data={"dataash5": ["data/*.h5"]},
    license="LICENSE.txt",
    description="An awesome package that does something",
    long_description=open("README.txt").read(),
)
