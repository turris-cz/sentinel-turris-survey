#!/usr/bin/env python
from setuptools import setup

setup(
    name="turris-survey",
    version="0.4",
    description="Turris OS usage survey",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.nic.cz/turris/sentinel/turris-survey",
    author="CZ.NIC, z.s.p.o. (http://www.nic.cz/)",
    author_email="packaging@turris.cz",
    license="GPLv3+",
    install_requires=[
        "pyzmq",
        "msgpack",
        "svupdater @ git+https://gitlab.nic.cz/turris/updater/supervisor.git#egg=supervisor",
    ],
    packages=[
        "turris_survey",
    ],
    extras_require={"tests": ["pytest", "compress_pickle"]},
    entry_points={
        "console_scripts": [
            "turris-survey = turris_survey.__main__:main",
        ]
    },
    zip_safe=False,
)
