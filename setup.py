from setuptools import setup

setup(
    name='glokov',
    version='0.1.0',
    description='A text generation library',
    url='http://github.com/MatthewScholefield/glokov',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    license='MIT',
    py_modules=[
        'glokov'
    ],
    entry_points={
        'console_scripts': [
            'glokov-chain=glokov.chain:main'
        ]
    },
    zip_safe=True
)
