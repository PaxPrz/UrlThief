import setuptools
import sys

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="UrlThief",
    version="0.1.0",
    author="PaxPrz",
    author_email="paxprajapati@gmail.com",
    description="Captures URL and window name from famous browsers",
    long_description=long_description,
    long_description_content="text/markdown",
    url="https://github.com/PaxPrz/UrlThief",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Dependent",
    ],
    python_requires=">=3.8",
    install_requires=[
        'pylru>=1.2.0,<2',
        'typing>=3.7.4.3,<4',
    ] + [
        'python-xlib>=0.28,<1',
        'clipboard>=0.0.4,<1',
        'pynput>=1.7.1,<2',
    ] if sys.platform == "linux" else [
    ] + [
        'uiautomation>=2.0.6,<3',
        'pywin32==228',
        'psutil>=5.7.2,<6',
    ] if sys.platform == "win" else [
    ] 
)