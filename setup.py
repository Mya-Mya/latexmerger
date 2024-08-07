from setuptools import setup
from pathlib import Path
from texpack import __version__
from texpack.utils import read_text

name = "texpack"

setup(
    name=name,
    packages=[name],
    version=__version__+read_text(Path("./pypi-trial-sub-version.txt")),
    license="MIT",
    install_requires="",
    tests_require="",
    author="Mya-Mya",
    url="https://github.com/Mya-Mya/texpack",
    description="Pack LaTeX Files into Single .tex File",
    keywords="LaTeX, tex, academic",
    long_description=read_text(Path("./README.md")),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Education",
    ],
)
