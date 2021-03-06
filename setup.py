#!/usr/bin/env python3
import setuptools
import io
fh = io.open("README.md", mode="r", encoding="utf-8")
long_description = fh.read()

tool_name="pyddoz"
version_num = "0.0.1"
author_name = "benorcunozdemir"
email = "benorcunozdemir@gmail.com"
setuptools.setup(name=tool_name,
        version=version_num,
        author=author_name,
        author_email=email,
        description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/n1rv4n4",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
        ],
        scripts = [
                'core/pyddoz'
        ],
        install_requires=[
            "colorama==0.3.9",
            "proxify==1.0.2",
            "requests==2.19.1",
            "urllib3==1.22",
            "fake-useragent==0.1.10"
            ]
)
