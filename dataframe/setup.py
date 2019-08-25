from setuptools import setup

setup(
    name="dataframe",
    version="0.1.0",
    author="Andrei Berceanu",
    author_email="andrei.berceanu@eli-np.ro",
    packages=["dataframe"],
    package_dir={"dataframe": "dataframe"},
    package_data={"dataframe": ["data/*.h5"]},
    license="LICENSE.txt",
    description="An awesome package that does something",
    long_description=open("README.txt").read(),
)
