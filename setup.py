from setuptools import setup

setup(
    name='pipi',  # Name can be anything
    packages=['pipi'],
    include_package_data=True,
    install_requires=[
        'flask','cloudinary'
    ],
)
