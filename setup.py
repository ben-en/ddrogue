from setuptools import setup

import ddrogue as mod

setup(
    name='ddrogue',
    version='0.1',
    author='Ben Ennis',
    author_email='pnw.ben.ennis@gmail.com',
    description='Another Python roguelike',
    packages=[mod.__name__],
    entry_points={
        'console_scripts': [
            'ddrogue = ddrogue.main:main',
        ],
    },
)
