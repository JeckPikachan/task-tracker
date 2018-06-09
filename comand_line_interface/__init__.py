"""
This is ready to use task tracker with command line interface.
It uses adastra_library module as main building block.
To use it print `adastra [any command you want]`.
To get help print `adastra [-h|--help]
"""
from .parser import Parser
from .handlers import *
from .app import app
