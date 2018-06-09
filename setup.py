from setuptools import setup, find_packages

setup(
    name='adastra',
    version='0.0.1',
    py_modules=['app', 'comand_line_interface'],
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    adastra=comand_line_interface.main:main
    ''',
    install_requires=[
        "python-dateutil"
    ]
)
