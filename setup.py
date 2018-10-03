from setuptools import setup

setup(
    name='robotframework-pykafka',
    packages=['robotframework-pykafka'],  # this must be the same as the name above
    version='0.0.2',
    install_requires=[

    ],
    description='This is a robot framework wrapper around pykafka, the best python kafka library out there as of this writing, and the only one that supports kafka 1.0 and 1.1.',
    author='Michael Sesterhenn',
    author_email='invadergir@users.noreply.github.com',
    url='https://github.com/invadergir/robotframework-pykafka',
    download_url='https://github.com/spothero/py-responsys/tarball/0.0.2',
    keywords=['robotframework', 'kafka','testing'],
    classifiers=["Programming Language :: Python :: 2.7",
                 "Topic :: Software Development :: Libraries :: Python Modules"]
)
