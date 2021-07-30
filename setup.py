import re
from setuptools import setup


def get_version():
    VERSION_FPATH = "src/anchorpy/_version.py"
    ver_line = open(VERSION_FPATH, "rt").read()

    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    return re.search(VSRE, ver_line, re.M).group(1)


test_deps = [
    "black",
    "pylint",
    "pytest",
]
extras = {
    "test": test_deps,
}

setup(
    name="anchorpy",
    version=get_version(),
    author="Matthew-Jennings",
    author_email="Centrus.007@gmail.com",
    packages=["anchorpy"],
    package_dir={"": "src"},
    scripts=["scripts/print_anchor.py"],
    url="",
    license="LICENSE.txt",
    description="",
    long_description=open("README.md").read(),
    install_requires=["terra_sdk", "requests"],
    tests_require=test_deps,
    extras_require=extras,
)
