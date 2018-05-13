from setuptools import setup

setup(
    name='adastra',
    version='0.0.1',
    py_modules=['app', 'user_interface'],
    entry_points='''
    [console_scripts]
    adastra=index:main
    '''
)
