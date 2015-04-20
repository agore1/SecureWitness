from setuptools import setup

setup(
    name='SWDesktop',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
        'simple-crypt'
    ],
    entry_points='''
        [console_scripts]
        secwit=main:main
        '''
)
