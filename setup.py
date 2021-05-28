# -*- coding: utf-8 -*-

import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pcbnewTransition",
    python_requires='>3.7',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Jan Mrázek",
    author_email="email@honzamrazek.cz",
    description="Library that allows you to support both, KiCAD 5 and KiCAD 6 in your plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaqwsx/pcbnewTransition",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=[
        "versioneer"
    ],
    zip_safe=False,
    include_package_data=True
)