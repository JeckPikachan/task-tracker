from setuptools import setup

setup(
    name='adastra',
    version='0.0.1',
    py_modules=['app', 'comand_line_interface'],
    entry_points='''
    [console_scripts]
    adastra=comand_line_interface.main:main
    ''',
    install_requires=[
        "python-dateutil"
    ]
)
