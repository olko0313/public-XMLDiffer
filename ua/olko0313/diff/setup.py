
from distutils.core import setup
#import py2exe
import os

setup(
    windows=[{"script":"Main.py"}],
    options={"py2exe": {"includes":["sip"]}}
)