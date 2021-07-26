from setuptools import setup

setup(
    name="anchorpy",
    version="0.0.1",
    author="Matthew-Jennings",
    author_email="Centrus.007@gmail.com",
    packages=["anchorpy"],
    package_dir={"": "src"},
    scripts=["scripts/print_anchor.py"],
    url="",
    license="LICENSE.txt",
    description="",
    long_description=open("README.md").read(),
    install_requires=[
        "terra_sdk",
    ],
)
