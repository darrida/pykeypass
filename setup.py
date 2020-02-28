from setuptools import setup

setup(
    name='pykeypass',
    version='0.9',
    py_modules=['pykeypass'],
    install_requires=[
        'Click',
        'pykeepass',
    ],
    entry_points='''
        [console_scripts]
        pykeypass=pykeypass:cli
    ''',
)