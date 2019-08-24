from setuptools import setup

setup(
    name="plotting",
    version="0.1.0",
    author="Andrei Berceanu",
    author_email="andrei.berceanu@eli-np.ro",
    packages=["plotting"],
    package_dir={"plotting": "plotting"},
    package_data={"plotting": ["data/*.mplstyle"]},
    license="LICENSE.txt",
    description="An awesome package that does something",
    long_description=open("README.txt").read(),
)
